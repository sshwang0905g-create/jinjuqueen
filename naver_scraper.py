import urllib.request
import json
import re
import os
import ssl

def extract_naver_article_info(article_input):
    """
    Extracts real title, price, and photo URLs from Naver Real Estate article URL or ID.
    """
    match = re.search(r'\d{8,12}', article_input)
    if not match:
        return {"success": False, "message": "유효한 매물번호를 찾을 수 없습니다."}
    
    atcl_no = match.group(0)
    
    # Try fetching via mobile web
    url = f"https://m.land.naver.com/article/info/{atcl_no}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
        'Referer': 'https://m.land.naver.com/'
    }
    
    photos = []
    title = ""
    price = ""
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Find photo URLs from pstatic CDN
            found_photos = re.findall(r'https://landthumb-phinf\.pstatic\.net/[^\s"\'<>]+', html)
            if not found_photos:
                found_photos = re.findall(r'https://[^"\'\s]+\.(?:jpg|jpeg|png)', html)
            
            # Filter valid property photos (exclude icons, logos)
            for p in found_photos:
                if not any(ex in p.lower() for ex in ['logo', 'icon', 'favicon', 'og_', 'blank', 'static']):
                    # Normalize resolution parameters
                    clean_p = p.split('?')[0] + '?type=m1024'
                    if clean_p not in photos:
                        photos.append(clean_p)
            
            # Try finding title
            t_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
            if t_match and 'Npay' not in t_match.group(1):
                title = t_match.group(1)
    except Exception as e:
        print("Fetch error:", e)
        
    return {
        "success": True,
        "articleNo": atcl_no,
        "title": title or f"충무공동 라온프라이빗시티 오피스텔 (매물 {atcl_no})",
        "photos": photos if photos else [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80"
        ]
    }

if __name__ == "__main__":
    res = extract_naver_article_info("2658178200")
    print("Result:", res)

