import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Colors
NAVY_DEEP = (11, 19, 43)       # #0B132B
NAVY_CARD = (18, 28, 54)
GOLD_RICH = (194, 155, 56)      # #C29B38
GOLD_LIGHT = (245, 218, 128)
EMERALD = (13, 148, 136)        # #0D9488
EMERALD_LIGHT = (209, 250, 229)
WHITE = (255, 255, 255)
SLATE_MUTED = (160, 175, 200)

def generate_naver_blog_title():
    """Naver Blog Title Banner (966 x 500) with updated branding & no forbidden phrases"""
    bw, bh = 966, 500
    banner = Image.new('RGB', (bw, bh), NAVY_DEEP)
    draw = ImageDraw.Draw(banner)

    # Ambient subtle gradient background
    for y in range(bh):
        blend = y / bh
        r = int(NAVY_DEEP[0] * (1 - blend * 0.3) + 16 * (blend * 0.3))
        g = int(NAVY_DEEP[1] * (1 - blend * 0.3) + 24 * (blend * 0.3))
        b = int(NAVY_DEEP[2] * (1 - blend * 0.3) + 48 * (blend * 0.3))
        draw.line([(0, y), (bw, y)], fill=(r, g, b))

    # Top & bottom gold accent lines
    draw.line([(0, 2), (bw, 2)], fill=GOLD_RICH, width=4)
    draw.line([(0, bh - 3), (bw, bh - 3)], fill=GOLD_RICH, width=4)

    # 1. Representative Portrait on the right
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        # Circular framed portrait with gold border
        c_size = 400
        ceo_resized = ceo_im.resize((c_size, c_size), Image.Resampling.LANCZOS)
        
        # Circle mask
        mask = Image.new('L', (c_size, c_size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse((0, 0, c_size - 1, c_size - 1), fill=255)
        
        # Gold ring around avatar
        ring_im = Image.new('RGBA', (c_size, c_size), (0, 0, 0, 0))
        rdraw = ImageDraw.Draw(ring_im)
        rdraw.ellipse((3, 3, c_size - 4, c_size - 4), outline=GOLD_RICH, width=6)
        
        cx = bw - c_size - 40
        cy = (bh - c_size) // 2
        banner.paste(ceo_resized, (cx, cy), mask)
        banner.paste(ring_im, (cx, cy), ring_im)

        # Name tag below portrait
        f_name_tag = ImageFont.truetype(FONT_BD, 16)
        tag_w = 170
        tag_h = 32
        tag_x = cx + (c_size - tag_w) // 2
        tag_y = cy + c_size - 25
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=16, fill=GOLD_RICH)
        draw.text((tag_x + 18, tag_y + 4), "황선숙 대표공인중개사", font=f_name_tag, fill=(15, 23, 42))

    # 2. Golden Logo on the left
    logo_path = os.path.join(IMAGES_DIR, "logo.png")
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert('RGBA')
        logo_s = 105
        logo_resized = logo_im.resize((logo_s, logo_s), Image.Resampling.LANCZOS)
        banner.paste(logo_resized, (35, 45), logo_resized)

    # 3. Typography & Information
    f_badge = ImageFont.truetype(FONT_BD, 15)
    f_title = ImageFont.truetype(FONT_BD, 38)
    f_sub = ImageFont.truetype(FONT_BD, 18)
    f_info = ImageFont.truetype(FONT_REG, 15)
    f_phone_lbl = ImageFont.truetype(FONT_BD, 17)
    f_phone_main = ImageFont.truetype(FONT_BD, 28)
    f_phone_sub = ImageFont.truetype(FONT_REG, 14)

    tx = 160
    ty = 42

    # Top Pill Badge
    draw.rounded_rectangle([tx, ty, tx + 175, ty + 28], radius=14, fill=NAVY_CARD, outline=GOLD_RICH, width=1)
    draw.text((tx + 14, ty + 4), "진주 혁신도시 부동산 전문", font=f_badge, fill=GOLD_LIGHT)

    # Title
    ty += 38
    draw.text((tx, ty), "진주퀸공인중개사사무소", font=f_title, fill=WHITE)

    # Subtitle (strictly compliant, NO '확인 실매물')
    ty += 52
    draw.text((tx, ty), "아파트 · 오피스텔 · 토지·택지 · 상가 전문 중개", font=f_sub, fill=GOLD_LIGHT)

    # Office Info
    ty += 36
    draw.text((tx, ty), "개업공인중개사 대표 황선숙  |  등록번호 : 48170-2017-00038", font=f_info, fill=SLATE_MUTED)
    ty += 24
    draw.text((tx, ty), "소재지 : 경남 진주시 에나로 146, 105호 라온프라이빗시티", font=f_info, fill=SLATE_MUTED)
    ty += 24
    draw.text((tx, ty), "홈페이지 : jinjuqueen.vercel.app  (모바일 & PC)", font=f_info, fill=(147, 197, 253))

    # Contact Cards Box
    ty += 34
    draw.rounded_rectangle([tx, ty, tx + 330, ty + 72], radius=14, fill=(15, 25, 48), outline=GOLD_RICH, width=2)
    draw.text((tx + 16, ty + 10), "대표 직통", font=f_phone_lbl, fill=GOLD_LIGHT)
    draw.text((tx + 100, ty + 6), "010-4670-7248", font=f_phone_main, fill=WHITE)
    draw.text((tx + 16, ty + 44), "사무실 : 055-761-7248  ·  월~토 09:30~19:30", font=f_phone_sub, fill=SLATE_MUTED)

    out_file = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_file, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    print("Naver Blog Title Banner generated:", out_file)


def generate_youtube_banner():
    """YouTube Channel Art (2560 x 1440) matching website baseline & YouTube dark theme"""
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    YT_BG = (15, 15, 15)
    img = Image.new('RGB', (W, H), YT_BG)
    draw = ImageDraw.Draw(img)

    # Ambient deep navy / gold glow in the center safe zone
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for x in range(safe_x1 - 150, safe_x2 + 150):
        rel = (x - safe_x1) / safe_w
        factor = 1.0 - abs(rel - 0.5) * 1.8
        factor = max(0.0, min(1.0, factor))
        alpha = int(75 * factor)
        odraw.line([(x, safe_y1 - 60), (x, safe_y2 + 60)], fill=(11, 23, 50, alpha))

    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Top & bottom gold hairline borders inside safe zone
    draw.line([(safe_x1 + 40, safe_y1 + 10), (safe_x2 - 40, safe_y1 + 10)], fill=GOLD_RICH, width=2)
    draw.line([(safe_x1 + 40, safe_y2 - 10), (safe_x2 - 40, safe_y2 - 10)], fill=GOLD_RICH, width=2)

    # 1. Left side: Golden Logo
    logo_path = os.path.join(IMAGES_DIR, "logo.png")
    logo_size = 220
    logo_x = safe_x1 + 80
    logo_y = safe_y1 + (safe_h - logo_size) // 2
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert('RGBA')
        logo_r = logo_im.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        img.paste(logo_r, (logo_x, logo_y), logo_r)

    # 2. Right side: Representative Portrait inside stylish circle
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    c_size = 280
    cx = safe_x2 - c_size - 80
    cy = safe_y1 + (safe_h - c_size) // 2
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((c_size, c_size), Image.Resampling.LANCZOS)
        mask = Image.new('L', (c_size, c_size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse((0, 0, c_size - 1, c_size - 1), fill=255)
        
        ring = Image.new('RGBA', (c_size, c_size), (0, 0, 0, 0))
        rdraw = ImageDraw.Draw(ring)
        rdraw.ellipse((3, 3, c_size - 4, c_size - 4), outline=GOLD_RICH, width=5)
        
        img.paste(ceo_r, (cx, cy), mask)
        img.paste(ring, (cx, cy), ring)

        # Name tag below
        f_tag = ImageFont.truetype(FONT_BD, 18)
        tag_w = 170
        tag_h = 32
        tag_x = cx + (c_size - tag_w) // 2
        tag_y = cy + c_size - 16
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=16, fill=GOLD_RICH)
        draw.text((tag_x + 18, tag_y + 4), "황선숙 대표공인중개사", font=f_tag, fill=(15, 23, 42))

    # 3. Center Content
    content_x = logo_x + logo_size + 60
    f_title = ImageFont.truetype(FONT_BD, 68)
    f_sub = ImageFont.truetype(FONT_BD, 28)
    f_info = ImageFont.truetype(FONT_REG, 20)
    f_btn_lbl = ImageFont.truetype(FONT_BD, 22)
    f_btn_num = ImageFont.truetype(FONT_BD, 34)

    # Main Channel Title
    title_y = safe_y1 + 45
    draw.text((content_x, title_y), "진주퀸공인중개사", font=f_title, fill=WHITE)
    
    # Subtitle
    sub_y = title_y + 88
    draw.text((content_x, sub_y), "진주 혁신도시 아파트 · 상가 · 오피스텔 · 토지 전문", font=f_sub, fill=GOLD_LIGHT)

    # Info Line
    info_y = sub_y + 45
    draw.text((content_x, info_y), "충무공동 라온프라이빗시티 105호  |  홈페이지 : jinjuqueen.vercel.app", font=f_info, fill=SLATE_MUTED)

    # Two Call-To-Action Pills
    btn_y = info_y + 42
    
    # Pill 1: Mobile Direct (010-4670-7248) - Gold Gradient Look
    p1_w = 360
    p1_h = 68
    draw.rounded_rectangle([content_x, btn_y, content_x + p1_w, btn_y + p1_h], radius=34, fill=(35, 45, 68), outline=GOLD_RICH, width=2)
    draw.rounded_rectangle([content_x + 6, btn_y + 6, content_x + 105, btn_y + p1_h - 6], radius=28, fill=GOLD_RICH)
    draw.text((content_x + 18, btn_y + 18), "대표 직통", font=f_btn_lbl, fill=(15, 23, 42))
    draw.text((content_x + 120, btn_y + 12), "010-4670-7248", font=f_btn_num, fill=WHITE)

    # Pill 2: Landline (055-761-7248) - Blue/Slate
    p2_x = content_x + p1_w + 20
    p2_w = 320
    draw.rounded_rectangle([p2_x, btn_y, p2_x + p2_w, btn_y + p1_h], radius=34, fill=(22, 32, 50), outline=(70, 90, 130), width=2)
    draw.rounded_rectangle([p2_x + 6, btn_y + 6, p2_x + 95, btn_y + p1_h - 6], radius=28, fill=(45, 60, 90))
    draw.text((p2_x + 20, btn_y + 18), "사무실", font=f_btn_lbl, fill=(210, 225, 245))
    draw.text((p2_x + 110, btn_y + 12), "055-761-7248", font=f_btn_num, fill=WHITE)

    out_file = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    img.save(out_file, "JPEG", quality=98)
    img.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    print("YouTube Channel Banner generated:", out_file)


def generate_naver_blog_skin():
    """Naver Blog Wide Top Skin (2000 x 800)"""
    sw, sh = 2000, 800
    skin = Image.new('RGB', (sw, sh), NAVY_DEEP)
    draw = ImageDraw.Draw(skin)

    # Luxury subtle gradient & ambient lighting
    for y in range(sh):
        blend = y / sh
        r = int(NAVY_DEEP[0] * (1 - blend * 0.4) + 8 * (blend * 0.4))
        g = int(NAVY_DEEP[1] * (1 - blend * 0.4) + 14 * (blend * 0.4))
        b = int(NAVY_DEEP[2] * (1 - blend * 0.4) + 32 * (blend * 0.4))
        draw.line([(0, y), (sw, y)], fill=(r, g, b))

    # Top gold accent
    draw.line([(0, 2), (sw, 2)], fill=GOLD_RICH, width=4)

    # Center placement of blog title banner
    title_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    if os.path.exists(title_path):
        t_im = Image.open(title_path)
        tx = (sw - t_im.width) // 2
        ty = 80
        skin.paste(t_im, (tx, ty))

    out_file = os.path.join(IMAGES_DIR, "naver-blog-skin.jpg")
    skin.save(out_file, "JPEG", quality=98)
    skin.save(os.path.join(ARTIFACT_DIR, "naver-blog-skin.jpg"), "JPEG", quality=98)
    print("Naver Blog Wide Skin generated:", out_file)

if __name__ == '__main__':
    generate_naver_blog_title()
    generate_youtube_banner()
    generate_naver_blog_skin()
