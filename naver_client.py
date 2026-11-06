import httpx
import re
import json
import logging
import time
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("NaverRealEstate")

class NaverRealEstateClient:
    """
    네이버 부동산 매물 데이터 및 고해상도 실사진,
    중개사 매물특징 및 상세설명 자동 수집 클라이언트
    (httpx 브라우저 헤더 에뮬레이션 & 보안 쿠키 자동 발급/갱신 지원)
    """
    def __init__(self):
        self.prop_test_key: Optional[str] = None
        self.prop_test_id: Optional[str] = None
        self.realestate_cookie: Optional[str] = None
        self.session_cookies: Dict[str, str] = {}
        self.last_cookie_refresh_time: float = 0.0

        # 실제 크롬 브라우저와 100% 동일한 헤더 설정
        self.browser_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        self.client = httpx.Client(
            headers=self.browser_headers,
            timeout=12.0,
            follow_redirects=True,
            verify=False
        )

        # 모바일 갤러리 전체 사진 수집용 헤더
        self.mobile_headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9",
        }

        self.refresh_cookies()

    def refresh_cookies(self) -> bool:
        """
        네이버 부동산 시드 페이지(https://new.land.naver.com/)에 접속하여
        응답 헤더(Set-Cookie)에서 PROP_TEST_KEY, PROP_TEST_ID, REALESTATE 등의
        보안 쿠키를 파싱하고 메모리 변수에 안전하게 저장합니다.
        """
        logger.info("[Cookie Refresh] 네이버 부동산 보안 쿠키(PROP_TEST_KEY, PROP_TEST_ID) 갱신 요청 시작...")
        seed_url = "https://new.land.naver.com/"
        
        try:
            resp = self.client.get(seed_url, headers=self.browser_headers)
            cookies_dict = dict(self.client.cookies)
            
            # 응답 헤더 Set-Cookie 원문에서 보안 키값 정밀 추출
            set_cookie_raw = resp.headers.get("set-cookie", "")
            if "PROP_TEST_KEY=" in set_cookie_raw:
                match_k = re.search(r"PROP_TEST_KEY=([^;,\s]+)", set_cookie_raw)
                if match_k:
                    cookies_dict["PROP_TEST_KEY"] = match_k.group(1)
            if "PROP_TEST_ID=" in set_cookie_raw:
                match_i = re.search(r"PROP_TEST_ID=([^;,\s]+)", set_cookie_raw)
                if match_i:
                    cookies_dict["PROP_TEST_ID"] = match_i.group(1)
            if "REALESTATE=" in set_cookie_raw:
                match_r = re.search(r"REALESTATE=([^;,\s]+)", set_cookie_raw)
                if match_r:
                    cookies_dict["REALESTATE"] = match_r.group(1)

            self.prop_test_key = cookies_dict.get("PROP_TEST_KEY")
            self.prop_test_id = cookies_dict.get("PROP_TEST_ID")
            self.realestate_cookie = cookies_dict.get("REALESTATE")
            self.session_cookies = cookies_dict
            self.last_cookie_refresh_time = time.time()

            logger.info(f"[Cookie Refresh 완료] 활성 보안 쿠키 {len(self.session_cookies)}개 메모리 로드 완료")
            return True

        except Exception as e:
            logger.error(f"[Cookie Refresh 오류] {e}")
            return False

    def fetch_article_detail(self, article_id: str, retry_count: int = 2) -> Dict[str, Any]:
        """
        네이버 매물번호를 받아 메모리에 저장된 쿠키와 브라우저 헤더를 동봉하여 호출.
        차단(401, 403, 429, 503) 또는 세션 만료 시 자동으로 쿠키를 갱신하고 재시도합니다.
        """
        clean_id_match = re.search(r'\d{8,12}', str(article_id))
        if not clean_id_match:
            return {"success": False, "message": "유효한 8~10자리 매물번호가 아닙니다."}
        
        atcl_no = clean_id_match.group(0)

        # 쿠키가 없거나 10분 이상 경과 시 선제적 갱신
        if not self.prop_test_key or not self.prop_test_id or (time.time() - self.last_cookie_refresh_time > 600):
            self.refresh_cookies()

        target_url = f"https://fin.land.naver.com/articles/{atcl_no}"
        api_headers = {
            **self.browser_headers,
            "Referer": "https://new.land.naver.com/",
            "Sec-Fetch-Site": "same-site"
        }

        try:
            logger.info(f"[매물 데이터 요청] 매물번호: {atcl_no}")
            resp = self.client.get(
                target_url,
                headers=api_headers,
                cookies=self.session_cookies
            )

            # 차단 또는 쿠키 만료 감지 시 자동 갱신 후 재시도
            if resp.status_code in [401, 403, 429, 503] or len(resp.text) < 1000:
                if retry_count > 0:
                    logger.warning(f"[차단 감지 ({resp.status_code})] 쿠키 재갱신 후 즉시 재요청 (남은 재시도: {retry_count})...")
                    self.refresh_cookies()
                    time.sleep(0.5)
                    return self.fetch_article_detail(atcl_no, retry_count=retry_count - 1)
                else:
                    return {"success": False, "message": f"네이버 응답 코드 {resp.status_code}"}

            html = resp.text

            # 1. 전체 사진 갤러리 파싱 (네이버 등록 실사진 전수 수집 및 고해상도 변환)
            photos = []
            room_photos = []
            complex_photos = []
            seen_urls = set()

            try:
                gallery_url = f"https://m.land.naver.com/article/image/{atcl_no}"
                g_resp = self.client.get(gallery_url, headers=self.mobile_headers, cookies=self.session_cookies)
                if g_resp.status_code == 200:
                    g_matches = re.findall(r'https://landthumb-phinf\.pstatic\.net/[^"\'\s,\\]+', g_resp.text)
                    for m in g_matches:
                        clean_url = m.split('?')[0]
                        if clean_url in seen_urls or any(ex in clean_url.lower() for ex in ['icon', 'logo', 'blank', 'favicon']):
                            continue
                        seen_urls.add(clean_url)
                        hd_url = clean_url + '?type=m1024'
                        if f"{atcl_no}_" in clean_url:
                            room_photos.append(hd_url)
                        else:
                            complex_photos.append(hd_url)
            except Exception as ge:
                logger.warning(f"사진 수집 보조 알림: {ge}")

            # 본문 메인 사진 보강
            cdn_matches = re.findall(r'https://landthumb-phinf\.pstatic\.net/[^"\'\s,\\]+', html)
            for m in cdn_matches:
                clean_url = m.split('?')[0]
                if clean_url not in seen_urls and not any(ex in clean_url.lower() for ex in ['icon', 'logo', 'blank']):
                    seen_urls.add(clean_url)
                    hd_url = clean_url + '?type=m1024'
                    if f"{atcl_no}_" in clean_url:
                        room_photos.append(hd_url)
                    else:
                        complex_photos.append(hd_url)

            photos = room_photos + complex_photos

            # 2. 제목
            title = ""
            title_match = re.search(r'<title>(.*?)</title>', html)
            if title_match:
                raw_title = title_match.group(1).replace(' - 네이버페이 부동산', '').replace('네이버 부동산', '').strip()
                if raw_title and '네이버' not in raw_title:
                    title = raw_title

            if not title:
                title = f"충무공동 매물 ({atcl_no})"

            # 3. 가격 및 거래유형 (억 단위 완벽 정밀 파싱)
            price_formatted = "매매 협의"
            trans_type = "매매"
            deposit = 50000
            monthly = 0

            desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
            if desc_match:
                desc_text = desc_match.group(1).strip()
                if "월세" in desc_text:
                    trans_type = "월세"
                    p_m = re.search(r'월세\s*([0-9억,\s]+)\s*/\s*([0-9,]+)', desc_text)
                    if p_m:
                        dep_str = p_m.group(1).strip()
                        mon_str = p_m.group(2).strip()
                        dep_unit = "" if dep_str.endswith("만원") or "억" in dep_str else "만원"
                        price_formatted = f"보증금 {dep_str}{dep_unit} / 월세 {mon_str}만원"
                        try:
                            m_uk = re.search(r'(\d+)\s*억', dep_str)
                            uk_val = int(m_uk.group(1)) * 10000 if m_uk else 0
                            rem = re.sub(r'\d+\s*억', '', dep_str)
                            m_rem = re.search(r'([0-9,]+)', rem)
                            rem_val = int(m_rem.group(1).replace(',', '')) if m_rem else 0
                            deposit = uk_val + rem_val
                            monthly = int(mon_str.replace(',', ''))
                        except Exception:
                            pass
                elif "전세" in desc_text:
                    trans_type = "전세"
                    p_m = re.search(r'전세\s*([0-9억,\s]+)', desc_text)
                    if p_m:
                        val = p_m.group(1).strip()
                        val_unit = "" if val.endswith("만원") else "만원"
                        price_formatted = f"전세 {val}{val_unit}"
                        m_uk = re.search(r'(\d+)\s*억', val)
                        uk_val = int(m_uk.group(1)) * 10000 if m_uk else 0
                        rem = re.sub(r'\d+\s*억', '', val)
                        m_rem = re.search(r'([0-9,]+)', rem)
                        rem_val = int(m_rem.group(1).replace(',', '')) if m_rem else 0
                        deposit = uk_val + rem_val
                elif "매매" in desc_text:
                    trans_type = "매매"
                    p_m = re.search(r'매매\s*([0-9억,\s]+)', desc_text)
                    if p_m:
                        val = p_m.group(1).strip()
                        val_unit = "" if val.endswith("만원") else "만원"
                        price_formatted = f"매매 {val}{val_unit}"
                        m_uk = re.search(r'(\d+)\s*억', val)
                        uk_val = int(m_uk.group(1)) * 10000 if m_uk else 0
                        rem = re.sub(r'\d+\s*억', '', val)
                        m_rem = re.search(r'([0-9,]+)', rem)
                        rem_val = int(m_rem.group(1).replace(',', '')) if m_rem else 0
                        deposit = uk_val + rem_val

# [Category determination moved after full_decoded]

            # 4. 네이버 구조화 Next.js 청크 파싱
            feature_desc = ""
            detail_desc = ""

            chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html)
            full_decoded = ""
            for c in chunks:
                try:
                    decoded_chunk = c.encode("utf-8").decode("unicode_escape").encode("latin1").decode("utf-8", errors="ignore")
                except Exception:
                    decoded_chunk = c
                full_decoded += decoded_chunk + "\n"

                if "articleFeatureDescription" in decoded_chunk or "articleDescription" in decoded_chunk:
                    m_feat = re.search(r'"articleFeatureDescription":"([^"]+)"', decoded_chunk)
                    if m_feat and not feature_desc:
                        feature_desc = m_feat.group(1).strip()

                    m_desc = re.search(r'"articleDescription":"(.*?)"(?:,"|\})', decoded_chunk)
                    if m_desc and not detail_desc:
                        raw_desc = m_desc.group(1)
                        detail_desc = raw_desc.replace("\\n", "\n").replace("\\r", "").replace('\\"', '"').strip()

            # (0) 카테고리 (Category) & 매물명 정밀 판별
            art_match = re.search(r'"articleName":"([^"]+)"', full_decoded)
            art_name_val = art_match.group(1).strip() if art_match else ""
            rlet_match = re.search(r'"realEstateType":"([^"]+)"', full_decoded)
            rlet_code = rlet_match.group(1).strip() if rlet_match else ""

            category = "아파트"
            if rlet_code in ["F01", "F02", "E03"] or any(k in art_name_val or k in title for k in ["토지", "택지", "대지", "전원주택지", "주택용지", "필지", "주택지", "단독주택지", "대"]):
                category = "택지"
            elif rlet_code in ["D01", "D02", "D03", "E01", "E02"] or any(k in art_name_val or k in title for k in ["상가", "점포", "사무실", "근린"]):
                category = "상가"
            elif rlet_code in ["B01", "B02"] or "오피스텔" in art_name_val or "오피스텔" in title or "라온프라이빗시티" in title or "허브시티" in title:
                category = "오피스텔"
            elif rlet_code in ["C01", "C02", "C03"] or any(k in art_name_val or k in title for k in ["원룸", "투룸"]):
                category = "원룸/투룸"
            elif rlet_code in ["A01", "A02"] or any(k in art_name_val or k in title for k in ["아파트", "단지"]):
                category = "아파트"
            elif any(k in art_name_val for k in ["상가", "점포"]):
                category = "상가"

            # (1) 방향 (direction & directionStandard)
            direction_map = {
                "EN": "북동향", "ES": "남동향", "WN": "북서향", "WS": "남서향",
                "EE": "동향", "WW": "서향", "SS": "남향", "NN": "북향",
                "E": "동향", "W": "서향", "S": "남향", "N": "북향"
            }
            dir_match = re.search(r'"direction":"([A-Z]+)"', full_decoded)
            dir_code = dir_match.group(1) if dir_match else ""
            dir_name = direction_map.get(dir_code, dir_code)

            std_match = re.search(r'"directionStandard":"([^"]+)"', full_decoded)
            std_name = std_match.group(1).replace(" ", "") if std_match else "거실기준"
            direction_parsed = f"{dir_name}({std_name})" if dir_name else "남향(거실기준)"

            # 토지 전용 필드 추출 (지목, 용도지역, 토지면적, 도로접면, 추천용도, 허가구역)
            land_m = re.search(r'"(?:landSpace|platArea|landArea|area1)":([0-9.]+)', full_decoded)
            jimok_m = re.search(r'"(?:landCategoryName|landCategory|jimokName)":"([^"]+)"', full_decoded)
            use_m = re.search(r'"(?:usageDistrictName|useDistrictName|usageDistrict|areaUsage)":"([^"]+)"', full_decoded)
            road_m = re.search(r'"(?:roadConditionName|roadRelationName|roadAccessName)":"([^"]+)"', full_decoded)
            rec_m = re.search(r'"(?:recommendedUsageName|recommendedUsage|recommendedPurpose)":"([^"]+)"', full_decoded)
            curr_purp_m = re.search(r'"currentPurpose":"([^"]+)"', full_decoded)
            perm_m = re.search(r'"landTradePermission":(true|false|"[^"]*")', full_decoded)

            land_area = float(land_m.group(1)) if land_m else 0.0
            land_pyeong = round(land_area / 3.305785, 1) if land_area else 0.0
            
            # 지목 최우선 판별
            if art_name_val in ["대", "전", "답", "임야", "잡종지", "과수원", "목장용지"]:
                land_category_name = art_name_val
            else:
                land_category_name = jimok_m.group(1).strip() if jimok_m else ("대" if "대" in title else "대")

            usage_district = use_m.group(1).strip() if use_m else "제1종일반주거지역"
            road_condition = road_m.group(1).strip() if road_m else "소로한면접함 (8m 아스팔트 도로)"
            
            if rec_m:
                recommended_usage = rec_m.group(1).strip()
            elif curr_purp_m:
                recommended_usage = f"{curr_purp_m.group(1).strip()} (단독주택)"
            else:
                recommended_usage = "단독주택지 (상가주택 협의)"

            is_perm = perm_m and perm_m.group(1) == "true"
            permission_zone = "지정구역 (토지거래허가 필요)" if is_perm else "해당없음 (비지정구역)"

            # (2) 면적 (전용면적, 공급면적 및 평수 환산)
            ex_match = re.search(r'"exclusiveSpace":([0-9.]+)', full_decoded)
            sp_match = re.search(r'"supplySpace":([0-9.]+)', full_decoded)

            if category == "택지":
                exclusive_area = land_area if land_area > 0 else (float(ex_match.group(1)) if ex_match else 280.9)
                supply_area = exclusive_area
                exclusive_pyeong = round(exclusive_area / 3.305785, 1)
                supply_pyeong = exclusive_pyeong
                floor_parsed = f"토지 (지목: {land_category_name} / {usage_district})"
                room_count = 0
                bath_count = 0
                approval_date = "토지분양 완료 (즉시 착공/건축 가능)"
                parking_parsed = "건축 시 부지 내 확보 가능"
                direction_parsed = "남향(추천 건축방향)"
            else:
                exclusive_area = float(ex_match.group(1)) if ex_match else (land_area if land_area > 0 else 84.89)
                supply_area = float(sp_match.group(1)) if sp_match else (exclusive_area * 1.35)
                exclusive_pyeong = round(exclusive_area / 3.305785, 1)
                supply_pyeong = round(supply_area / 3.305785, 1)

                # (3) 층수 (해당층 / 총층)
                tf_match = re.search(r'"targetFloor":"([^"]+)"', full_decoded)
                tot_match = re.search(r'"totalFloor":"?([0-9]+)"?', full_decoded)
                target_floor = tf_match.group(1) if tf_match else ""
                total_floor = tot_match.group(1) if tot_match else ""
                if target_floor and total_floor:
                    target_clean = target_floor if "층" in target_floor else f"{target_floor}층"
                    floor_parsed = f"{target_clean} / 총 {total_floor}층"
                elif target_floor:
                    floor_parsed = target_floor if "층" in target_floor else f"{target_floor}층"
                else:
                    floor_parsed = "1층" if category == "상가" else "중층"

                # (4) 방수 / 욕실수
                rc_match = re.search(r'"roomCount":([0-9]+)', full_decoded)
                bc_match = re.search(r'"bathRoomCount":([0-9]+)', full_decoded)
                if category == "상가":
                    room_count = 1
                    bath_count = 1
                else:
                    room_count = int(rc_match.group(1)) if rc_match else 3
                    bath_count = int(bc_match.group(1)) if bc_match else 2

                # (5) 사용승인일
                app_match = re.search(r'"useApprovalDate":"([0-9]{4})([0-9]{2})([0-9]{2})"', full_decoded)
                if app_match:
                    approval_date = f"{app_match.group(1)}년 {int(app_match.group(2))}월 {int(app_match.group(3))}일"
                else:
                    app_year = re.search(r'"useApprovalDate":"([0-9]{4})"', full_decoded)
                    approval_date = f"{app_year.group(1)}년" if app_year else "2018년"

                # (6) 주차대수
                p_per = re.search(r'"parkingCountPerHousehold":([0-9.]+)', full_decoded)
                p_tot = re.search(r'"totalParkingCount":([0-9]+)', full_decoded)
                if p_per and p_tot:
                    parking_parsed = f"세대당 {p_per.group(1)}대 (총 {p_tot.group(1)}대)"
                elif p_tot:
                    parking_parsed = f"총 {p_tot.group(1)}대 주차가능"
                else:
                    parking_parsed = "지하 주차장 완비" if category in ["아파트", "오피스텔"] else "주차가능"

            # (7) 동명 포함 정밀 매물명
            c_name = re.search(r'"complexName":"([^"]+)"', full_decoded)
            dong_name = re.search(r'"dongName":"([^"]+)"', full_decoded)
            if c_name and dong_name:
                title = f"{c_name.group(1)} {dong_name.group(1)}동"
            elif c_name:
                title = c_name.group(1)
            elif art_name_val:
                if category == "상가":
                    feat_short = feature_desc.split(',')[0].strip() if feature_desc else ""
                    if feat_short and len(feat_short) > 3:
                        title = f"충무공동 {art_name_val} ({feat_short})"
                    else:
                        title = f"충무공동 {art_name_val}"
                elif category == "택지":
                    feat_short = feature_desc.split(',')[0].strip() if feature_desc else ""
                    if feat_short and len(feat_short) > 3:
                        title = f"충무공동 단독주택용지 ({feat_short})"
                    elif land_pyeong > 0:
                        title = f"충무공동 단독주택용지 ({land_pyeong}평, 지목:{land_category_name})"
                    else:
                        title = "충무공동 단독주택용지 (택지)"
                else:
                    title = art_name_val

            # 중개사 매물설명 구성 (상대 중개업소 홍보문구는 배제하고 실매물 특징만 정제)
            final_description = ""
            if detail_desc:
                cleaned = re.split(r'📌\s*(?:진주퀸)?공인중개사사무소\s*소개|(?:진주퀸)?공인중개사사무소\s*소개|📌\s*중개업소\s*소개', detail_desc)[0].strip()
                final_description = cleaned if cleaned else detail_desc
            elif feature_desc:
                final_description = f"📌 매물특징\n\n✔ {feature_desc}"
            else:
                final_description = f"네이버부동산 등록 검증 실매물(매물번호: {atcl_no})입니다."

            # 사진이 전혀 없는 경우 화사하고 밝은 파스텔(Pastel) 컬러 타이틀 카드 동적 자동생성
            if len(photos) == 0:
                detail_str = ""
                if category == "택지":
                    detail_str = f"{land_pyeong}평 · {usage_district or '제1종일반주거'}"
                elif floor_parsed:
                    detail_str = f"{floor_parsed} · 전용 {exclusive_pyeong}평"
                elif exclusive_pyeong:
                    detail_str = f"전용 {exclusive_pyeong}평"

                try:
                    from generate_pastel_card import generate_pastel_card
                    card_path = generate_pastel_card(title, category, detail_str, atcl_no)
                    photos = [card_path]
                    logger.info(f"[화사한 파스텔 타이틀 카드 동적 생성 완료] {card_path}")
                except Exception as card_err:
                    logger.error(f"[파스텔 카드 생성 예외 Fallback] {card_err}")
                    if category == "택지":
                        photos = ["images/complex_cards/토지_클린카드.jpg"]
                    elif category == "상가":
                        photos = ["images/complex_cards/일반상가_클린카드.jpg"]
                    elif category == "오피스텔":
                        photos = ["images/complex_cards/pastel_ea18771ace.jpg"]
                    else:
                        photos = ["images/complex_cards/기본_아파트_클린카드.jpg"]

            logger.info(f"[매물 파싱 완료] {atcl_no} | {title} | {price_formatted} | 사진 {len(photos)}장")

            return {
                "success": True,
                "articleNo": atcl_no,
                "title": title,
                "priceFormatted": price_formatted,
                "deposit": deposit,
                "monthlyRent": monthly,
                "category": category,
                "landArea": land_area if category == "택지" else None,
                "landAreaPyeong": land_pyeong if category == "택지" else None,
                "landCategory": land_category_name if category == "택지" else None,
                "usageDistrict": usage_district if category == "택지" else None,
                "roadCondition": road_condition if category == "택지" else None,
                "recommendedUsage": recommended_usage if category == "택지" else None,
                "permissionZone": permission_zone if category == "택지" else None,
                "transactionType": trans_type,
                "location": "진주시 충무공동 (혁신도시)",
                "direction": direction_parsed,
                "exclusiveArea": exclusive_area,
                "exclusiveAreaPyeong": exclusive_pyeong,
                "supplyArea": supply_area,
                "supplyAreaPyeong": supply_pyeong,
                "floor": floor_parsed,
                "rooms": room_count,
                "bathrooms": bath_count,
                "approvalDate": approval_date,
                "parking": parking_parsed,
                "photos": photos,
                "feature": feature_desc,
                "description": final_description,
                "tags": ["네이버등록", "실매물인증", trans_type]
            }

        except Exception as e:
            logger.error(f"[요청 오류] {e}")
            if retry_count > 0:
                self.refresh_cookies()
                time.sleep(0.5)
                return self.fetch_article_detail(atcl_no, retry_count=retry_count - 1)
            return {"success": False, "message": str(e)}

client = NaverRealEstateClient()

if __name__ == "__main__":
    test_id = "2659230421"
    res = client.fetch_article_detail(test_id)
    print("\n--- 결과 테스트 ---")
    print("Success:", res.get("success"))
    print("Title:", res.get("title"))
    print("Price:", res.get("priceFormatted"))
    print("Photos:", len(res.get("photos", [])))
