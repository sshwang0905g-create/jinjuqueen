import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://new.land.naver.com/',
    'Accept': 'application/json, text/plain, */*'
}

endpoints = [
    'https://new.land.naver.com/api/articles/2658178200',
    'https://fin.land.naver.com/front-api/v1/article/basic/2658178200',
    'https://m.land.naver.com/article/getArticleDetailInfo?atclNo=2658178200',
    'https://new.land.naver.com/api/articles/photos/2658178200',
    'https://fin.land.naver.com/front-api/v1/article/photos/2658178200'
]

for ep in endpoints:
    print(f"\nTrying endpoint: {ep}")
    try:
        req = urllib.request.Request(ep, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            data = resp.read().decode('utf-8')
            print(f"Status: {resp.status}, Length: {len(data)}")
            # Try parsing as JSON
            try:
                js = json.loads(data)
                print("JSON keys:", list(js.keys()) if isinstance(js, dict) else len(js))
                # Search for photos or image keys
                data_str = json.dumps(js, ensure_ascii=False)
                with open('api_response.json', 'w', encoding='utf-8') as out:
                    out.write(data_str)
                print("Saved api_response.json")
                break
            except Exception as je:
                print("Not JSON:", data[:200])
    except Exception as e:
        print(f"Failed {ep}: {e}")

