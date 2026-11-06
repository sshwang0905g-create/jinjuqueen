import os
import re
import hashlib
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, 'images', 'complex_cards')
os.makedirs(CARDS_DIR, exist_ok=True)

# Font configurations
FONT_BOLD_PATH = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REGULAR_PATH = "C:/Windows/Fonts/malgun.ttf"

def get_theme(category: str, title: str):
    cat = (category or "").strip()
    tit = (title or "").strip()

    if cat == "택지" or "택지" in tit or "토지" in tit or "주택용지" in tit:
        return {
            "tag_text": "진주혁신도시 토지·택지 실매물",
            "bg_top": (255, 243, 234),       # Warm Peach Apricot
            "bg_bottom": (253, 226, 206),
            "border": (235, 188, 160),
            "text_title": (65, 32, 16),
            "text_accent": (217, 119, 6),
            "tag_color": (194, 65, 12),
            "pill_bg": (255, 255, 255)
        }
    elif cat == "오피스텔" or "오피스텔" in tit or "허브시티" in tit or "프라이빗시티" in tit:
        return {
            "tag_text": "진주혁신도시 오피스텔 실매물",
            "bg_top": (224, 247, 238),       # Fresh Mint Sage
            "bg_bottom": (198, 238, 220),
            "border": (145, 210, 185),
            "text_title": (16, 48, 38),
            "text_accent": (5, 150, 105),
            "tag_color": (5, 150, 105),
            "pill_bg": (255, 255, 255)
        }
    elif cat == "상가" or "상가" in tit or "사무실" in tit or "점포" in tit:
        return {
            "tag_text": "진주혁신도시 상가·사무실 실매물",
            "bg_top": (252, 248, 238),       # Warm Sand Cream / Champagne
            "bg_bottom": (245, 236, 218),
            "border": (218, 200, 172),
            "text_title": (50, 38, 22),
            "text_accent": (180, 83, 9),
            "tag_color": (180, 83, 9),
            "pill_bg": (255, 255, 255)
        }
    else:  # 아파트 or default
        # Vary pastel tone based on apartment name for variety
        if "더퍼스트" in tit or "로즈" in tit:
            return {
                "tag_text": "진주혁신도시 아파트 실매물",
                "bg_top": (254, 239, 244),       # Soft Pastel Rose Cream
                "bg_bottom": (250, 220, 228),
                "border": (236, 178, 192),
                "text_title": (72, 24, 38),
                "text_accent": (190, 24, 93),
                "tag_color": (190, 24, 93),
                "pill_bg": (255, 255, 255)
            }
        elif "대방" in tit or "라벤더" in tit:
            return {
                "tag_text": "진주혁신도시 아파트 실매물",
                "bg_top": (236, 238, 254),       # Soft Pastel Lavender Periwinkle
                "bg_bottom": (218, 222, 250),
                "border": (178, 186, 236),
                "text_title": (28, 36, 76),
                "text_accent": (79, 70, 229),
                "tag_color": (79, 70, 229),
                "pill_bg": (255, 255, 255)
            }
        elif "중흥" in tit or "센트럴" in tit:
            return {
                "tag_text": "진주혁신도시 아파트 실매물",
                "bg_top": (225, 247, 247),       # Soft Pastel Ice Teal
                "bg_bottom": (199, 236, 237),
                "border": (148, 208, 212),
                "text_title": (16, 52, 58),
                "text_accent": (13, 148, 136),
                "tag_color": (13, 148, 136),
                "pill_bg": (255, 255, 255)
            }
        else:
            return {
                "tag_text": "진주혁신도시 아파트 실매물",
                "bg_top": (226, 240, 253),       # Soft Pastel Sky Blue
                "bg_bottom": (202, 225, 248),
                "border": (155, 195, 232),
                "text_title": (18, 38, 68),
                "text_accent": (2, 132, 199),
                "tag_color": (2, 132, 199),
                "pill_bg": (255, 255, 255)
            }

def clean_title_for_card(title: str) -> str:
    tit = title or "진주혁신도시 추천 실매물"
    # Remove redundant prefixes or brackets if messy
    tit = re.sub(r'\[.*?\]', '', tit)
    tit = tit.strip()
    return tit

def generate_pastel_card(title: str, category: str = "아파트", detail: str = "", atcl_no: str = "") -> str:
    """
    Generates a bright, radiant pastel title card (1200x800) for a property without attached photos.
    Returns relative web path: 'images/complex_cards/pastel_xxx.jpg'
    """
    clean_tit = clean_title_for_card(title)
    theme = get_theme(category, clean_tit)

    # Unique file identifier
    id_source = f"{atcl_no}_{clean_tit}_{category}"
    safe_hash = hashlib.md5(id_source.encode('utf-8')).hexdigest()[:10]
    filename = f"pastel_{safe_hash}.jpg"
    filepath = os.path.join(CARDS_DIR, filename)

    W, H = 1200, 800
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # 1. Smooth Vertical Gradient
    r1, g1, b1 = theme["bg_top"]
    r2, g2, b2 = theme["bg_bottom"]
    for y in range(H):
        t = y / (H - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Dual Rounded Borders
    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=theme["border"], width=2)
    draw.rounded_rectangle([42, 42, W - 42, H - 42], radius=18, outline=(255, 255, 255), width=2)

    # Load Fonts
    try:
        font_tag = ImageFont.truetype(FONT_BOLD_PATH, 24)
        font_title_large = ImageFont.truetype(FONT_BOLD_PATH, 62)
        font_title_med = ImageFont.truetype(FONT_BOLD_PATH, 50)
        font_detail = ImageFont.truetype(FONT_BOLD_PATH, 30)
        font_broker_bold = ImageFont.truetype(FONT_BOLD_PATH, 23)
        font_broker_sub = ImageFont.truetype(FONT_REGULAR_PATH, 18)
    except Exception:
        font_tag = font_title_large = font_title_med = font_detail = font_broker_bold = font_broker_sub = ImageFont.load_default()

    # 3. Top Tag Pill Badge
    tag_str = f"●  {theme['tag_text']}"
    tb = draw.textbbox((0, 0), tag_str, font=font_tag)
    tag_w = tb[2] - tb[0]
    pill_w = max(tag_w + 50, 360)
    pill_h = 52
    pill_x1 = (W - pill_w) // 2
    pill_y1 = 120
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x1 + pill_w, pill_y1 + pill_h], radius=26, fill=theme["pill_bg"], outline=(255, 255, 255), width=2)
    draw.text((pill_x1 + (pill_w - tag_w) // 2, pill_y1 + 12), tag_str, fill=theme["tag_color"], font=font_tag)

    # 4. Central Title (wrap if long)
    if len(clean_tit) <= 15:
        title_lines = [clean_tit]
        curr_font = font_title_large
    elif len(clean_tit) <= 24:
        # Split into 2 lines
        mid = len(clean_tit) // 2
        split_idx = clean_tit.find(' ', mid - 4)
        if split_idx == -1 or split_idx > mid + 5:
            split_idx = mid
        title_lines = [clean_tit[:split_idx].strip(), clean_tit[split_idx:].strip()]
        curr_font = font_title_med
    else:
        # 2 lines with medium font
        mid = len(clean_tit) // 2
        split_idx = clean_tit.find(' ', mid - 5)
        if split_idx == -1:
            split_idx = mid
        title_lines = [clean_tit[:split_idx].strip(), clean_tit[split_idx:split_idx+22].strip()]
        curr_font = font_title_med

    # Draw Title Lines
    title_start_y = 260 if len(title_lines) == 1 else 235
    for i, line in enumerate(title_lines):
        lb = draw.textbbox((0, 0), line, font=curr_font)
        lw = lb[2] - lb[0]
        lh = lb[3] - lb[1]
        line_y = title_start_y + i * (lh + 22)
        draw.text(((W - lw) // 2, line_y), line, fill=theme["text_title"], font=curr_font)

    # 5. Detail Sub-Pill
    det_str = (detail or "").strip()
    if not det_str:
        if category == "택지":
            det_str = "즉시 건축가능 토지 · 현장 실매물"
        elif category == "오피스텔":
            det_str = "진주혁신도시 중심 상권 프리미엄 오피스텔"
        elif category == "상가":
            det_str = "공공기관 11개 배후수요 · 핵심 메인상가"
        else:
            det_str = "진주혁신도시 선호 단지 · 정직 실매물"

    det_bb = draw.textbbox((0, 0), det_str, font=font_detail)
    det_w = det_bb[2] - det_bb[0]
    det_pill_w = det_w + 44
    det_pill_h = 48
    det_x = (W - det_pill_w) // 2
    det_y = title_start_y + len(title_lines) * 65 + 40
    # Soft translucent white pill
    draw.rounded_rectangle([det_x, det_y, det_x + det_pill_w, det_y + det_pill_h], radius=24, fill=(255, 255, 255), outline=theme["border"], width=1)
    draw.text((det_x + 22, det_y + 8), det_str, fill=theme["text_accent"], font=font_detail)

    # 6. Bottom Broker Branding Card
    card_w = 980
    card_h = 118
    card_x = (W - card_w) // 2
    card_y = 600

    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

    # Line 1: Office, Broker Name, Phone
    b1_str = "진주퀸공인중개사사무소   |   대표 황선숙   |   055-761-7248  ·  010-4670-7248"
    b1_bb = draw.textbbox((0, 0), b1_str, font=font_broker_bold)
    b1_w = b1_bb[2] - b1_bb[0]
    draw.text(((W - b1_w) // 2, card_y + 24), b1_str, fill=(30, 41, 59), font=font_broker_bold)

    # Line 2: AddressMasked & Experience
    b2_str = "경남 진주시 에나로 146, 105호 (라온프라이빗시티)   |   충무공동 9년차 정직과 데이터의 책임중개"
    b2_bb = draw.textbbox((0, 0), b2_str, font=font_broker_sub)
    b2_w = b2_bb[2] - b2_bb[0]
    draw.text(((W - b2_w) // 2, card_y + 68), b2_str, fill=(100, 116, 139), font=font_broker_sub)

    # Save image
    img.save(filepath, "JPEG", quality=92)
    return f"images/complex_cards/{filename}"

if __name__ == "__main__":
    # Test generation for each category
    p1 = generate_pastel_card("혁신LH허브시티 809호", "오피스텔", "809호 · 전용 25.5㎡ 주거용", "test1")
    p2 = generate_pastel_card("충무공동 단독주택용지 (10단지 앞)", "택지", "85평 · 제1종일반주거지역", "test2")
    p3 = generate_pastel_card("라온프라이빗시티S 1208호", "오피스텔", "1208호 · 풀옵션 로열층", "test3")
    p4 = generate_pastel_card("진주혁신 대방노블랜드 더센트럴", "아파트", "34평 판상형 로열동", "test4")
    print("Generated cards:")
    print("1:", p1)
    print("2:", p2)
    print("3:", p3)
    print("4:", p4)
