import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Fresh, rich color palette (Royal Navy + Gold + Emerald + Sapphire + Coral)
NAVY_BG = (10, 18, 38)          # Deep rich navy
NAVY_CARD = (17, 28, 54)
NAVY_ACCENT = (24, 40, 74)

GOLD_MAIN = (212, 168, 62)       # Royal Gold
GOLD_LIGHT = (252, 228, 148)
GOLD_BG = (42, 32, 14)

EMERALD_MAIN = (16, 185, 129)    # Emerald Green
EMERALD_LIGHT = (209, 250, 229)
EMERALD_BG = (12, 44, 34)

BLUE_MAIN = (56, 189, 248)       # Sky / Sapphire
BLUE_LIGHT = (224, 242, 254)
BLUE_BG = (14, 38, 62)

WHITE = (255, 255, 255)
SLATE_LIGHT = (210, 220, 235)
SLATE_MUTED = (145, 160, 185)


def generate_modern_naver_blog_title():
    """
    Naver Blog Title Banner (966 x 500)
    - Clean & spacious (NOT text-heavy)
    - NO '9년차' (uses timeless '2017년부터 충무공동 한 자리')
    - Moderate photo size (NOT too big)
    - Vibrant fresh colors (Gold, Emerald, Sky Blue)
    """
    bw, bh = 966, 500
    banner = Image.new('RGB', (bw, bh), NAVY_BG)
    draw = ImageDraw.Draw(banner)

    # Ambient luxury gradient background
    for y in range(bh):
        factor = y / bh
        r = int(10 * (1 - factor * 0.3) + 16 * (factor * 0.3))
        g = int(18 * (1 - factor * 0.3) + 26 * (factor * 0.3))
        b = int(38 * (1 - factor * 0.3) + 60 * (factor * 0.3))
        draw.line([(0, y), (bw, y)], fill=(r, g, b))

    # Top & bottom gold hairline borders
    draw.line([(0, 2), (bw, 2)], fill=GOLD_MAIN, width=3)
    draw.line([(0, bh - 3), (bw, bh - 3)], fill=GOLD_MAIN, width=3)

    # 1. Representative Photo on the right - MODERATE SIZE (width 230, height 310)
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    photo_w, photo_h = 230, 310
    photo_x = bw - photo_w - 45
    photo_y = 65

    # Decorative colored glow card behind photo
    draw.rounded_rectangle(
        [photo_x - 6, photo_y - 6, photo_x + photo_w + 6, photo_y + photo_h + 6],
        radius=24,
        fill=NAVY_ACCENT,
        outline=GOLD_MAIN,
        width=2
    )

    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        
        # Rounded mask for photo
        pmask = Image.new('L', (photo_w, photo_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_w - 1, photo_h - 1], radius=18, fill=255)
        banner.paste(ceo_r, (photo_x, photo_y), pmask)

        # Name plate below photo
        f_card_name = ImageFont.truetype(FONT_BD, 15)
        f_card_sub = ImageFont.truetype(FONT_REG, 12)
        
        tag_y = photo_y + photo_h + 16
        draw.rounded_rectangle(
            [photo_x - 6, tag_y, photo_x + photo_w + 6, tag_y + 56],
            radius=14,
            fill=NAVY_CARD,
            outline=(50, 70, 105),
            width=1
        )
        draw.text((photo_x + 22, tag_y + 8), "대표 공인중개사 황선숙", font=f_card_name, fill=GOLD_LIGHT)
        draw.text((photo_x + 36, tag_y + 30), "통계학 석사 · 정밀 데이터 분석", font=f_card_sub, fill=EMERALD_MAIN)

    # 2. Left side: Logo & Typography
    lx = 45
    ly = 50

    # Top Brand Logo
    logo_path = os.path.join(IMAGES_DIR, "logo.png")
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert('RGBA')
        logo_s = 70
        logo_r = logo_im.resize((logo_s, logo_s), Image.Resampling.LANCZOS)
        banner.paste(logo_r, (lx, ly), logo_r)

    # 2 Vibrant Pill Badges (Emerald + Gold)
    f_badge = ImageFont.truetype(FONT_BD, 13)
    bx = lx + 85
    by = ly + 4

    # Badge 1: 📊 통계학 석사 데이터 분석 (Emerald)
    draw.rounded_rectangle([bx, by, bx + 225, by + 28], radius=14, fill=EMERALD_BG, outline=EMERALD_MAIN, width=1)
    draw.text((bx + 14, by + 4), "📊 통계학 석사의 정밀 데이터 분석", font=f_badge, fill=EMERALD_LIGHT)

    # Badge 2: 🏛️ 2017년부터 충무공동 한 자리 (Gold)
    bx2 = bx + 235
    draw.rounded_rectangle([bx2, by, bx2 + 205, by + 28], radius=14, fill=GOLD_BG, outline=GOLD_MAIN, width=1)
    draw.text((bx2 + 14, by + 4), "🏛️ 2017년부터 충무공동 한 자리", font=f_badge, fill=GOLD_LIGHT)

    # Main Brand Title (Big, Crisp, Confident)
    f_title = ImageFont.truetype(FONT_BD, 42)
    ly += 55
    draw.text((lx, ly), "진주퀸공인중개사사무소", font=f_title, fill=WHITE)

    # Elegant Slogan / Tagline (1 line, spacious)
    f_slogan = ImageFont.truetype(FONT_BD, 18)
    ly += 58
    draw.text((lx, ly), "충무공동 한 자리를 지켜온 정직한 신뢰와 전문성", font=f_slogan, fill=GOLD_LIGHT)

    # Category Chips (Colored Pills: 아파트 / 오피스텔 / 토지·택지 / 상가)
    ly += 36
    chips = [
        ("🏢 아파트", BLUE_BG, BLUE_MAIN, BLUE_LIGHT),
        ("🏬 오피스텔", EMERALD_BG, EMERALD_MAIN, EMERALD_LIGHT),
        ("🌱 토지·택지", GOLD_BG, GOLD_MAIN, GOLD_LIGHT),
        ("🏪 상가·점포", (40, 20, 45), (236, 72, 153), (253, 232, 244))
    ]
    f_chip = ImageFont.truetype(FONT_BD, 13)
    cx = lx
    for label, bg_col, border_col, txt_col in chips:
        bbox = f_chip.getbbox(label)
        cw = (bbox[2] - bbox[0]) + 26
        draw.rounded_rectangle([cx, ly, cx + cw, ly + 30], radius=15, fill=bg_col, outline=border_col, width=1)
        draw.text((cx + 13, ly + 5), label, font=f_chip, fill=txt_col)
        cx += cw + 10

    # Contact Box with 2 Colored Action Buttons (Gold Direct Call + Blue Office)
    ly += 46
    f_call_label = ImageFont.truetype(FONT_BD, 14)
    f_call_num = ImageFont.truetype(FONT_BD, 22)

    # Button 1: 황선숙 대표 직통 (Gold)
    btn1_w = 300
    btn_h = 56
    draw.rounded_rectangle([lx, ly, lx + btn1_w, ly + btn_h], radius=16, fill=(38, 28, 12), outline=GOLD_MAIN, width=2)
    draw.rounded_rectangle([lx + 6, ly + 6, lx + 90, ly + btn_h - 6], radius=12, fill=GOLD_MAIN)
    draw.text((lx + 15, ly + 14), "대표 직통", font=f_call_label, fill=(15, 23, 42))
    draw.text((lx + 105, ly + 11), "010-4670-7248", font=f_call_num, fill=WHITE)

    # Button 2: 사무실 유선 (Blue / Sapphire)
    btn2_x = lx + btn1_w + 14
    btn2_w = 260
    draw.rounded_rectangle([btn2_x, ly, btn2_x + btn2_w, ly + btn_h], radius=16, fill=(14, 28, 48), outline=BLUE_MAIN, width=2)
    draw.rounded_rectangle([btn2_x + 6, ly + 6, btn2_x + 75, ly + btn_h - 6], radius=12, fill=BLUE_MAIN)
    draw.text((btn2_x + 15, ly + 14), "사무실", font=f_call_label, fill=(15, 23, 42))
    draw.text((btn2_x + 90, ly + 11), "055-761-7248", font=f_call_num, fill=WHITE)

    # Single-line Clean Footer (No text clutter!)
    f_footer = ImageFont.truetype(FONT_REG, 13)
    ly += 70
    draw.text((lx, ly), "진주시 에나로 146, 105호 라온프라이빗시티  |  등록번호 : 48170-2017-00038  |  jinjuqueen.vercel.app", font=f_footer, fill=SLATE_MUTED)

    # Save
    out_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_타이틀배너.jpg"), "JPEG", quality=98)
    print("Naver Blog Title generated successfully!")


def generate_modern_youtube_banner():
    """
    YouTube Channel Art (2560 x 1440)
    - Whole 2560x1440 canvas filled with luxury ambient navy gradient (NO stark black bars!)
    - Safe Zone (1546 x 423) is perfectly balanced, colorful, spacious, and easy to read
    - Moderate photo size (~240px tall, elegant circle/frame)
    - NO '9년차' (uses timeless '2017년부터 충무공동 한 자리')
    - Vibrant colors (Gold, Emerald, Sky Blue)
    """
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    # Entire canvas has seamless rich navy ambient tone
    banner = Image.new('RGB', (W, H), NAVY_BG)
    draw = ImageDraw.Draw(banner)

    # Ambient radial / horizontal lighting across the safe area
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for x in range(safe_x1 - 250, safe_x2 + 250):
        rel = (x - safe_x1) / safe_w
        factor = 1.0 - abs(rel - 0.5) * 1.7
        factor = max(0.0, min(1.0, factor))
        alpha = int(85 * factor)
        odraw.line([(x, safe_y1 - 100), (x, safe_y2 + 100)], fill=(20, 42, 85, alpha))

    banner = Image.alpha_composite(banner.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(banner)

    # Subtle gold hairline accents top and bottom of safe area
    draw.line([(safe_x1 + 30, safe_y1 + 10), (safe_x2 - 30, safe_y1 + 10)], fill=GOLD_MAIN, width=2)
    draw.line([(safe_x1 + 30, safe_y2 - 10), (safe_x2 - 30, safe_y2 - 10)], fill=GOLD_MAIN, width=2)

    # 1. Left side: Golden Logo (size 170px)
    logo_path = os.path.join(IMAGES_DIR, "logo.png")
    logo_size = 170
    logo_x = safe_x1 + 60
    logo_y = safe_y1 + (safe_h - logo_size) // 2 - 5
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert('RGBA')
        logo_r = logo_im.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        banner.paste(logo_r, (logo_x, logo_y), logo_r)

    # 2. Right side: Moderate sized CEO Portrait inside gold ring card
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    card_w = 260
    card_h = 350
    card_x = safe_x2 - card_w - 60
    card_y = safe_y1 + (safe_h - card_h) // 2

    # Background card
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=20,
        fill=NAVY_CARD,
        outline=GOLD_MAIN,
        width=2
    )

    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        pw, ph = card_w - 20, 240
        ceo_r = ceo_im.resize((pw, ph), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (pw, ph), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=14, fill=255)
        banner.paste(ceo_r, (card_x + 10, card_y + 10), pmask)

        # Name & Title plate inside card
        f_cname = ImageFont.truetype(FONT_BD, 15)
        f_csub = ImageFont.truetype(FONT_REG, 12)
        draw.text((card_x + 36, card_y + ph + 18), "대표 공인중개사 황선숙", font=f_cname, fill=GOLD_LIGHT)
        draw.text((card_x + 48, card_y + ph + 42), "통계학 석사 · 데이터 분석", font=f_csub, fill=EMERALD_MAIN)

    # 3. Center Content (Bold, Colorful, Spacious)
    cx = logo_x + logo_size + 50
    cy = safe_y1 + 45

    # Top Badges (Emerald + Gold)
    f_badge = ImageFont.truetype(FONT_BD, 16)
    
    # Badge 1: 📊 통계학 석사의 정밀 데이터 분석 (Emerald)
    draw.rounded_rectangle([cx, cy, cx + 270, cy + 34], radius=17, fill=EMERALD_BG, outline=EMERALD_MAIN, width=1)
    draw.text((cx + 16, cy + 5), "📊 통계학 석사 데이터 분석", font=f_badge, fill=EMERALD_LIGHT)

    # Badge 2: 🏛️ 2017년부터 충무공동 한 자리 (Gold)
    bx2 = cx + 282
    draw.rounded_rectangle([bx2, cy, bx2 + 250, cy + 34], radius=17, fill=GOLD_BG, outline=GOLD_MAIN, width=1)
    draw.text((bx2 + 16, cy + 5), "🏛️ 2017년부터 충무공동 한 자리", font=f_badge, fill=GOLD_LIGHT)

    # Main Channel Title
    f_title = ImageFont.truetype(FONT_BD, 54)
    cy += 50
    draw.text((cx, cy), "진주퀸공인중개사", font=f_title, fill=WHITE)

    # Slogan
    f_sub = ImageFont.truetype(FONT_BD, 22)
    cy += 68
    draw.text((cx, cy), "진주 혁신도시 아파트 · 오피스텔 · 토지 · 상가 전문", font=f_sub, fill=GOLD_LIGHT)

    # Category Chips
    cy += 40
    f_chip = ImageFont.truetype(FONT_BD, 15)
    chips = [
        ("🏢 아파트", BLUE_BG, BLUE_MAIN, BLUE_LIGHT),
        ("🏬 오피스텔", EMERALD_BG, EMERALD_MAIN, EMERALD_LIGHT),
        ("🌱 토지·택지", GOLD_BG, GOLD_MAIN, GOLD_LIGHT),
        ("🏪 상가·점포", (40, 20, 45), (236, 72, 153), (253, 232, 244))
    ]
    cur_x = cx
    for label, bg_col, border_col, txt_col in chips:
        bbox = f_chip.getbbox(label)
        cw = (bbox[2] - bbox[0]) + 28
        draw.rounded_rectangle([cur_x, cy, cur_x + cw, cy + 34], radius=17, fill=bg_col, outline=border_col, width=1)
        draw.text((cur_x + 14, cy + 6), label, font=f_chip, fill=txt_col)
        cur_x += cw + 12

    # Two Call Buttons
    cy += 50
    f_btn_lbl = ImageFont.truetype(FONT_BD, 16)
    f_btn_num = ImageFont.truetype(FONT_BD, 26)

    # Button 1: 대표 직통 (Gold)
    btn1_w = 340
    btn_h = 60
    draw.rounded_rectangle([cx, cy, cx + btn1_w, cy + btn_h], radius=18, fill=(38, 28, 12), outline=GOLD_MAIN, width=2)
    draw.rounded_rectangle([cx + 6, cy + 6, cx + 105, cy + btn_h - 6], radius=14, fill=GOLD_MAIN)
    draw.text((cx + 18, cy + 15), "대표 직통", font=f_btn_lbl, fill=(15, 23, 42))
    draw.text((cx + 120, cy + 12), "010-4670-7248", font=f_btn_num, fill=WHITE)

    # Button 2: 사무실 (Blue)
    btn2_x = cx + btn1_w + 16
    btn2_w = 300
    draw.rounded_rectangle([btn2_x, cy, btn2_x + btn2_w, cy + btn_h], radius=18, fill=(14, 28, 48), outline=BLUE_MAIN, width=2)
    draw.rounded_rectangle([btn2_x + 6, cy + 6, btn2_x + 88, cy + btn_h - 6], radius=14, fill=BLUE_MAIN)
    draw.text((btn2_x + 18, cy + 15), "사무실", font=f_btn_lbl, fill=(15, 23, 42))
    draw.text((btn2_x + 102, cy + 12), "055-761-7248", font=f_btn_num, fill=WHITE)

    # Save
    out_path = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_유튜브_채널아트배너.jpg"), "JPEG", quality=98)
    print("YouTube Channel Banner generated successfully!")


def generate_modern_naver_blog_skin():
    """Naver Blog Wide Top Skin (2000 x 800) with new title centered"""
    sw, sh = 2000, 800
    skin = Image.new('RGB', (sw, sh), NAVY_BG)
    draw = ImageDraw.Draw(skin)

    for y in range(sh):
        factor = y / sh
        r = int(10 * (1 - factor * 0.35) + 16 * (factor * 0.35))
        g = int(18 * (1 - factor * 0.35) + 24 * (factor * 0.35))
        b = int(38 * (1 - factor * 0.35) + 56 * (factor * 0.35))
        draw.line([(0, y), (sw, y)], fill=(r, g, b))

    draw.line([(0, 2), (sw, 2)], fill=GOLD_MAIN, width=4)

    title_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    if os.path.exists(title_path):
        t_im = Image.open(title_path)
        tx = (sw - t_im.width) // 2
        ty = 80
        skin.paste(t_im, (tx, ty))

    skin.save(os.path.join(IMAGES_DIR, "naver-blog-skin.jpg"), "JPEG", quality=98)
    print("Naver Blog Wide Skin generated successfully!")


if __name__ == '__main__':
    generate_modern_naver_blog_title()
    generate_modern_youtube_banner()
    generate_modern_naver_blog_skin()
