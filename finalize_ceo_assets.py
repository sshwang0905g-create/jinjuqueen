import os
from PIL import Image, ImageDraw, ImageFont

def finalize_all_ceo_assets():
    src_path = 'C:/Users/User/.gemini/antigravity/brain/22ad999b-b105-4739-9ac9-9c3b7b7fc818/hwang_sun_sook_ceo_portrait_true_identity_1793856434813.jpg'
    artifact_dir = 'C:/Users/User/.gemini/antigravity/brain/22ad999b-b105-4739-9ac9-9c3b7b7fc818'
    
    im = Image.open(src_path).convert('RGB')
    w, h = im.size # 896 x 1200

    # 1. Homepage Portrait (images/ceo-profile.jpg)
    im.save('images/ceo-profile.jpg', 'JPEG', quality=96)

    # 2. Square Profile for YouTube & Naver Blog (images/ceo-square.jpg)
    # In 896x1200, her head top is around y=100, chin around y=560, shoulders down to y=930.
    # For a circle/square avatar, centering around y=40 to y=936 (896x896) gives generous headroom and balanced shoulders!
    sq_crop = im.crop((0, 35, w, 35 + w))
    sq_800 = sq_crop.resize((800, 800), Image.Resampling.LANCZOS)
    sq_800.save('images/ceo-square.jpg', 'JPEG', quality=96)
    sq_800.save(os.path.join(artifact_dir, 'ceo-square-final.jpg'), 'JPEG', quality=96)

    # 3. Also create a preview showing how it looks inside a circular frame with a subtle gold ring (ceo-circle-profile.png)
    circle_size = 800
    circle_img = sq_800.convert('RGBA')
    mask = Image.new('L', (circle_size, circle_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, circle_size - 1, circle_size - 1), fill=255)
    
    out_circle = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
    out_circle.paste(circle_img, (0, 0), mask)
    
    # Subtle royal gold outer ring
    ring_draw = ImageDraw.Draw(out_circle)
    ring_draw.ellipse((4, 4, circle_size - 5, circle_size - 5), outline=(212, 175, 55, 255), width=8)
    out_circle.save('images/ceo-circle-profile.png', 'PNG')
    out_circle.save(os.path.join(artifact_dir, 'ceo-circle-profile.png'), 'PNG')

    # 4. Update Naver Blog Title Banner (966 x 500) with the new confirmed CEO portrait & non-clipped layout
    bw, bh = 966, 500
    blog_banner = Image.new('RGB', (bw, bh), (10, 18, 34))
    bdraw = ImageDraw.Draw(blog_banner)

    # Top and bottom gold accent lines
    bdraw.line([(0, 2), (bw, 2)], fill=(212, 175, 55), width=3)
    bdraw.line([(0, bh - 3), (bw, bh - 3)], fill=(212, 175, 55), width=3)

    # Paste new CEO portrait on the right side of Naver Blog Banner
    ceo_target_h = 460
    ceo_target_w = int(ceo_target_h * (w / h))
    ceo_resized = im.resize((ceo_target_w, ceo_target_h), Image.Resampling.LANCZOS).convert('RGBA')

    # Soft fade on left, right, top, bottom edges
    cmask = Image.new('L', (ceo_target_w, ceo_target_h), 255)
    for x in range(ceo_target_w):
        for y in range(ceo_target_h):
            val = 255
            if x < 90:
                val = min(val, int(255 * (x / 90)))
            if x > ceo_target_w - 30:
                val = min(val, int(255 * ((ceo_target_w - x) / 30)))
            if y < 25:
                val = min(val, int(255 * (y / 25)))
            if y > ceo_target_h - 25:
                val = min(val, int(255 * ((ceo_target_h - y) / 25)))
            cmask.putpixel((x, y), val)

    blog_banner.paste(ceo_resized, (bw - ceo_target_w - 15, 20), cmask)

    # Paste Golden Logo on the left
    try:
        logo = Image.open('images/logo.png').convert('RGBA')
        logo_s = 115
        logo_r = logo.resize((logo_s, logo_s), Image.Resampling.LANCZOS)
        blog_banner.paste(logo_r, (35, 55), logo_r)
    except Exception as e:
        print("Logo error:", e)

    # Fonts for Naver Blog Title
    font_bd = "C:/Windows/Fonts/malgunbd.ttf"
    font_reg = "C:/Windows/Fonts/malgun.ttf"
    f_badge = ImageFont.truetype(font_bd, 15)
    f_title = ImageFont.truetype(font_bd, 40)
    f_sub = ImageFont.truetype(font_bd, 19)
    f_info = ImageFont.truetype(font_reg, 15)
    f_phone_lbl = ImageFont.truetype(font_bd, 19)
    f_phone = ImageFont.truetype(font_bd, 28)

    tx = 170
    ty = 50
    gold = (212, 175, 55)

    # Badge
    bdraw.rounded_rectangle([tx, ty, tx + 155, ty + 28], radius=14, fill=(18, 30, 54), outline=gold, width=1)
    bdraw.text((tx + 16, ty + 4), "진주 혁신도시 전문", font=f_badge, fill=(245, 215, 110))

    ty += 38
    bdraw.text((tx, ty), "진주퀸공인중개사사무소", font=f_title, fill=(255, 255, 255))

    ty += 54
    bdraw.text((tx, ty), "혁신도시 아파트 · 오피스텔 · 상가 · 택지 100% 확인 실매물", font=f_sub, fill=gold)

    ty += 38
    bdraw.text((tx, ty), "개업공인중개사 대표 황선숙  |  등록번호 : 48170-2017-00038", font=f_info, fill=(195, 210, 230))
    ty += 24
    bdraw.text((tx, ty), "소재지 : 경남 진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_info, fill=(175, 190, 215))
    ty += 24
    bdraw.text((tx, ty), "LH 한국토지주택공사 본사 공원 맞은편 탑마트 주변 중심상가", font=f_info, fill=(155, 175, 200))

    ty += 36
    # Phone Box
    bdraw.rounded_rectangle([tx, ty, tx + 410, ty + 76], radius=12, fill=(14, 24, 44), outline=gold, width=2)
    bdraw.text((tx + 20, ty + 10), "직통 상담", font=f_phone_lbl, fill=(245, 215, 110))
    bdraw.text((tx + 115, ty + 5), "010-4670-7248", font=f_phone, fill=(255, 255, 255))
    bdraw.text((tx + 20, ty + 45), "사무실 : 055-761-7248   |   월~토 09:30 ~ 19:30", font=f_info, fill=(185, 200, 220))

    blog_banner.save('images/naver-blog-title-966.jpg', 'JPEG', quality=96)
    blog_banner.save(os.path.join(artifact_dir, 'naver-blog-title-966.jpg'), 'JPEG', quality=96)
    print("All assets finalized successfully!")

if __name__ == '__main__':
    finalize_all_ceo_assets()

