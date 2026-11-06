from naver_client import client
# Local Development Server supporting /api/board and /api/auth
# Run with: python server.py

import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_FILE = os.path.join(BASE_DIR, "data", "board.json")
PROPERTIES_FILE = os.path.join(BASE_DIR, "data", "properties.json")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "queen1234!")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/board':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            if os.path.exists(BOARD_FILE):
                with open(BOARD_FILE, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
            else:
                posts = []

            resp = {
                "success": True,
                "source": "local",
                "posts": posts
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        if parsed.path == '/api/inquiry':
            inquiry_file = os.path.join(DATA_DIR, 'inquiries.json')
            inquiries = []
            if os.path.exists(inquiry_file):
                try:
                    with open(inquiry_file, 'r', encoding='utf-8') as f:
                        inquiries = json.load(f)
                except Exception:
                    inquiries = []
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "inquiries": inquiries}, ensure_ascii=False).encode('utf-8'))
            return

        if parsed.path == '/api/inquiry':
            inquiry_file = os.path.join(DATA_DIR, 'inquiries.json')
            inquiries = []
            if os.path.exists(inquiry_file):
                try:
                    with open(inquiry_file, 'r', encoding='utf-8') as f:
                        inquiries = json.load(f)
                except Exception:
                    inquiries = []
            import datetime
            payload['id'] = f"inq-{int(time.time()*1000)}"
            payload['createdAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inquiries.insert(0, payload)
            with open(inquiry_file, 'w', encoding='utf-8') as f:
                json.dump(inquiries, f, ensure_ascii=False, indent=2)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "의뢰가 접수되었습니다."}).encode('utf-8'))
            return

        if parsed.path == '/api/properties':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            if os.path.exists(PROPERTIES_FILE):
                with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
                    props = json.load(f)
            else:
                props = []

            resp = {
                "success": True,
                "source": "local",
                "properties": props
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        # Block any direct static download of .xlsx files without admin token
        if parsed.path.lower().endswith('.xlsx'):
            params = urllib.parse.parse_qs(parsed.query)
            token = params.get('token', [''])[0]
            auth_header = self.headers.get('Authorization', '').replace('Bearer ', '').strip()
            if token != ADMIN_PASSWORD and auth_header != ADMIN_PASSWORD:
                self.send_response(403)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("<h3 style='color:red; font-family:sans-serif;'>[접근 거부] 엑셀 매물대장은 관리자만 다운로드할 수 있습니다.</h3>".encode('utf-8'))
                return

        if parsed.path == '/api/download_properties_excel':
            # Check Admin Authentication (관리자 전용 다운로드 검증)
            params = urllib.parse.parse_qs(parsed.query)
            token = params.get('token', [''])[0]
            auth_header = self.headers.get('Authorization', '').replace('Bearer ', '').strip()

            if token != ADMIN_PASSWORD and auth_header != ADMIN_PASSWORD:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "관리자만 다운로드할 수 있습니다. 관리자 로그인이 필요합니다."}).encode('utf-8'))
                return

            excel_path = os.path.join(BASE_DIR, '진주퀸공인중개사_매물관리대장.xlsx')
            try:
                import subprocess
                subprocess.run(['python', os.path.join(BASE_DIR, 'generate_excel.py')], check=True)
            except Exception as e:
                print('Error generating excel:', e)

            if os.path.exists(excel_path):
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                quoted_name = urllib.parse.quote('진주퀸공인중개사_매물관리대장.xlsx')
                self.send_header('Content-Disposition', f"attachment; filename*=UTF-8''{quoted_name}")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(excel_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return


        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        
        if parsed.path == '/api/fetch_naver':
            article_input = payload.get('articleInput', '')
            try:
                res = client.fetch_article_detail(article_input)
            except Exception as e:
                res = {"success": False, "message": str(e)}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            return

        if parsed.path == '/api/generate_card':
            title = payload.get('title', '진주혁신도시 추천매물')
            category = payload.get('category', '아파트')
            detail = payload.get('detail', '')
            atcl_no = payload.get('articleNo', '')
            try:
                from generate_pastel_card import generate_pastel_card
                card_path = generate_pastel_card(title, category, detail, atcl_no)
                res = {"success": True, "path": card_path}
            except Exception as e:
                res = {"success": False, "message": str(e), "path": "images/complex_cards/기본_아파트_클린카드.jpg"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            return

        if parsed.path == '/api/check_naver_status':
            atcl_no = payload.get('articleNo', '')
            sync_all = payload.get('syncAll', False)

            if atcl_no:
                try:
                    res = client.check_article_live_status(str(atcl_no))
                except Exception as e:
                    res = {"success": False, "is_live": True, "message": str(e)}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return

            elif sync_all:
                results = []
                auto_privated = []
                if os.path.exists(PROPERTIES_FILE):
                    with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
                        props = json.load(f)
                else:
                    props = []

                updated = False
                for p in props:
                    no = p.get('naverArticleNo')
                    if no:
                        try:
                            st = client.check_article_live_status(str(no))
                            is_live = st.get('is_live', True)
                            results.append({
                                "id": p.get('id'),
                                "title": p.get('title'),
                                "articleNo": no,
                                "is_live": is_live,
                                "status_code": st.get('status_code')
                            })
                            if not is_live:
                                # 네이버에서 내려간 경우 홈페이지 자동 비공개 전환
                                if not (p.get('isPrivate') or p.get('status') == 'PRIVATE' or p.get('hidden')):
                                    p['isPrivate'] = True
                                    p['hidden'] = True
                                    p['naverStatus'] = 'EXPIRED'
                                    auto_privated.append({
                                        "id": p.get('id'),
                                        "title": p.get('title'),
                                        "articleNo": no
                                    })
                                    updated = True
                        except Exception as err:
                            results.append({"id": p.get('id'), "articleNo": no, "is_live": True, "error": str(err)})

                if updated:
                    with open(PROPERTIES_FILE, 'w', encoding='utf-8') as f:
                        json.dump(props, f, ensure_ascii=False, indent=2)
                    js_data_path = os.path.join(BASE_DIR, 'js', 'data.js')
                    if os.path.exists(js_data_path):
                        try:
                            with open(js_data_path, 'r', encoding='utf-8') as jf:
                                js_content = jf.read()
                            start_i = js_content.find('let PROPERTIES_DATA = [')
                            if start_i != -1:
                                end_i = js_content.find('];', start_i)
                                if end_i != -1:
                                    formatted_json = json.dumps(props, ensure_ascii=False, indent=2)
                                    new_js = js_content[:start_i] + 'let PROPERTIES_DATA = ' + formatted_json + js_content[end_i+1:]
                                    with open(js_data_path, 'w', encoding='utf-8') as jf:
                                        jf.write(new_js)
                        except Exception as e:
                            print('Error updating js/data.js in check_naver_status:', e)

                resp_data = {
                    "success": True,
                    "results": results,
                    "auto_privated": auto_privated,
                    "auto_privated_count": len(auto_privated),
                    "properties": props,
                    "message": f"네이버 매물 동기화 완료: 총 {len(results)}건 점검, 내려간 매물 {len(auto_privated)}건 자동 비공개 전환"
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(resp_data, ensure_ascii=False).encode('utf-8'))
                return

        if parsed.path == '/api/upload_image':
            data_urls = payload.get('images', [])
            saved_paths = []
            import base64, time
            upload_dir = os.path.join(BASE_DIR, 'images', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            for idx, item in enumerate(data_urls):
                if isinstance(item, str) and item.startswith('data:image'):
                    try:
                        header, encoded = item.split(',', 1)
                        img_bytes = base64.b64decode(encoded)
                        fname = f"upload_{int(time.time())}_{idx+1}.jpg"
                        fpath = os.path.join(upload_dir, fname)
                        with open(fpath, 'wb') as img_f:
                            img_f.write(img_bytes)
                        saved_paths.append(f"images/uploads/{fname}")
                    except Exception as err:
                        print("Error saving image:", err)
                        saved_paths.append(item)
                else:
                    saved_paths.append(item)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "paths": saved_paths}, ensure_ascii=False).encode('utf-8'))
            return

        if parsed.path == '/api/auth':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            password = payload.get('password', '')
            if password == ADMIN_PASSWORD:
                resp = {
                    "success": True,
                    "token": ADMIN_PASSWORD,
                    "message": "인증 성공"
                }
            else:
                self.send_response(401)
                resp = {"success": False, "message": "비밀번호 불일치"}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        if parsed.path == '/api/board':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '').strip()

            if token != ADMIN_PASSWORD:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "인증 실패"}).encode('utf-8'))
                return

            action = payload.get('action', '')
            post = payload.get('post', {})

            if os.path.exists(BOARD_FILE):
                with open(BOARD_FILE, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
            else:
                posts = []

            if action == 'create' and post:
                import time
                post['id'] = f"board-{int(time.time()*1000)}"
                post['views'] = 0
                posts.insert(0, post)
            elif action == 'update' and post:
                for idx, p in enumerate(posts):
                    if p.get('id') == post.get('id'):
                        posts[idx].update(post)
                        break
            elif action == 'delete' and post:
                posts = [p for p in posts if p.get('id') != post.get('id')]

            with open(BOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            resp = {
                "success": True,
                "source": "local",
                "message": "data/board.json 파일에 성공적으로 저장되었습니다. (Vercel 배포 시 GitHub 자동 커밋)",
                "posts": posts
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        
        if parsed.path == '/api/properties':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '').strip()

            if token != ADMIN_PASSWORD:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "인증 실패"}).encode('utf-8'))
                return

            action = payload.get('action', '')
            prop = payload.get('property', {})

            if os.path.exists(PROPERTIES_FILE):
                with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
                    props = json.load(f)
            else:
                props = []

            if action == 'toggle_status' and prop:
                # Toggle ACTIVE <-> SOLD
                target_id = prop.get('id')
                for p in props:
                    if p.get('id') == target_id:
                        p['status'] = 'SOLD' if p.get('status') == 'ACTIVE' else 'ACTIVE'
                        if p['status'] == 'SOLD':
                            p['badge'] = '거래완료'
                        else:
                            p['badge'] = '추천매물'
                        break
            elif action == 'update' and prop:
                for idx, p in enumerate(props):
                    if p.get('id') == prop.get('id'):
                        props[idx].update(prop)
                        break
            elif action == 'create' and prop:
                if not prop.get('id'):
                    import time
                    prop['id'] = f"prop-{int(time.time()*1000)}"
                prop['status'] = prop.get('status', 'ACTIVE')
                existing_idx = next((i for i, p in enumerate(props) if p.get('id') == prop.get('id') or (prop.get('naverArticleNo') and p.get('naverArticleNo') == prop.get('naverArticleNo'))), -1)
                if existing_idx != -1:
                    props[existing_idx].update(prop)
                else:
                    props.insert(0, prop)
            elif action == 'delete' and prop:
                props = [p for p in props if p.get('id') != prop.get('id')]
            elif action == 'toggle_private' and prop:
                target_id = prop.get('id')
                for p in props:
                    if p.get('id') == target_id:
                        new_priv = prop.get('isPrivate', not bool(p.get('isPrivate') or p.get('status') == 'PRIVATE' or p.get('hidden')))
                        p['isPrivate'] = new_priv
                        p['hidden'] = new_priv
                        break

            with open(PROPERTIES_FILE, 'w', encoding='utf-8') as f:
                json.dump(props, f, ensure_ascii=False, indent=2)

            # Also sync into js/data.js for local static loading
            js_data_path = os.path.join(BASE_DIR, 'js', 'data.js')
            if os.path.exists(js_data_path):
                try:
                    with open(js_data_path, 'r', encoding='utf-8') as jf:
                        js_content = jf.read()
                    start_i = js_content.find('let PROPERTIES_DATA = [')
                    if start_i == -1:
                        start_i = js_content.find('const PROPERTIES_DATA = [')
                    end_i = js_content.find('const NEWS_DATA = [')
                    if start_i != -1 and end_i != -1:
                        new_js_part = 'let PROPERTIES_DATA = ' + json.dumps(props, ensure_ascii=False, indent=2) + ';\n\n'
                        updated_js = js_content[:start_i] + new_js_part + js_content[end_i:]
                        with open(js_data_path, 'w', encoding='utf-8') as jf:
                            jf.write(updated_js)
                except Exception as ex:
                    print("Error syncing js/data.js:", ex)

            # Auto-regenerate Excel workbook so adminMemo is always up to date
            try:
                import subprocess
                subprocess.run(['python', os.path.join(BASE_DIR, 'generate_excel.py')], check=False)
            except Exception as ex:
                print("Error updating excel workbook:", ex)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            resp = {
                "success": True,
                "source": "local",
                "message": "매물 상태가 성공적으로 변경되었습니다.",
                "properties": props
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()

