import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Clean, disciplined 2-color palette: Deep Classic Navy + Refined Royal Gold + Pure White
NAVY_BG = (10, 18, 38)            # Deep Classic Navy
NAVY_SURFACE = (16, 26, 50)       # Elevated surface
NAVY_BORDER = (35, 50, 80)

GOLD_ACCENT = (212, 168, 62)      # Refined Royal Gold
GOLD_LIGHT = (248, 224, 150)      # Soft warm gold for text
GOLD_PILL_BG = (35, 30, 16)       # Subtle gold-tinted dark pill

WHITE = (255, 255, 255)
SLATE_LIGHT = (205, 218, 235)
SLATE_MUTED = (140, 155, 180)


def generate_clean_naver_blog_title():
    """
    Naver Blog Title Banner (966 x 500)
    - Disciplined colors (Classic Navy + Gold + White)
    - Perfectly height-aligned (Left content height == Right photo height)
    - Photo size strictly balanced (width 260, height 360)
    - Zero text cutoff, minimal, spacious, trustworthy
    """
    bw, bh = 966, 500
    banner = Image.new('RGB', (bw, bh), NAVY_BG)
    draw = ImageDraw.Draw(banner)

    # Ambient subtle navy lighting
    for y in range(bh):
        factor = y / bh
        r = int(10 * (1 - factor * 0.25) + 14 * (factor * 0.25))
        g = int(18 * (1 - factor * 0.25) + 24 * (factor * 0.25))
        b = int(38 * (1 - factor * 0.25) + 54 * (factor * 0.25))
        draw.line([(0, y), (bw, y)], fill=(r, g, b))

    # Top & bottom refined gold hairline borders
    draw.line([(0, 2), (bw, 2)], fill=GOLD_ACCENT, width=3)
    draw.line([(0, bh - 3), (bw, bh - 3)], fill=GOLD_ACCENT, width=3)

    # Coordinated vertical bounds for BOTH left content and right photo
    # Top Y = 68, Bottom Y = 432 (Total height = 364px)
    CONTENT_TOP_Y = 68
    CONTENT_BOT_Y = 432
    BOX_HEIGHT = CONTENT_BOT_Y - CONTENT_TOP_Y # 364px

    # Right: Photo Box (width 260, height 364)
    photo_w = 260
    photo_h = BOX_HEIGHT
    photo_x = bw - photo_w - 45
    photo_y = CONTENT_TOP_Y

    # Photo container with gold accent border
    draw.rounded_rectangle(
        [photo_x, photo_y, photo_x + photo_w, photo_y + photo_h],
        radius=20,
        fill=NAVY_SURFACE,
        outline=GOLD_ACCENT,
        width=2
    )

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        # Photo image height: 300px, leaving 64px at bottom for name plate
        img_h = photo_h - 60
        img_w = photo_w - 8
        ceo_r = ceo_im.resize((img_w, img_h), Image.Resampling.LANCZOS)
        
        # Rounded top mask for photo
        pmask = Image.new('L', (img_w, img_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, img_w - 1, img_h - 1], radius=16, fill=255)
        banner.paste(ceo_r, (photo_x + 4, photo_y + 4), pmask)

        # Name plate below photo inside the card
        f_pname = ImageFont.truetype(FONT_BD, 15)
        f_psub = ImageFont.truetype(FONT_REG, 12)
        tag_y = photo_y + img_h + 8
        draw.text((photo_x + 36, tag_y), "대표 공인중개사 황선숙", font=f_pname, fill=WHITE)
        draw.text((photo_x + 46, tag_y + 22), "통계학 석사 · 정밀 데이터 분석", font=f_psub, fill=GOLD_LIGHT)

    # Left: Clean Content Box matching the exact height (top 68 to bottom 432)
    lx = 50
    ly = CONTENT_TOP_Y

    # 1. Top Single-Tone Pill Badge: 통계학 석사의 정밀 데이터 분석 · 2017년부터 충무공동 한 자리
    f_badge = ImageFont.truetype(FONT_BD, 13)
    badge_text = "통계학 석사의 정밀 데이터 분석  ·  2017년부터 충무공동 한 자리"
    bbox_b = f_badge.getbbox(badge_text)
    bw_badge = (bbox_b[2] - bbox_b[0]) + 26
    draw.rounded_rectangle([lx, ly, lx + bw_badge, ly + 28], radius=14, fill=GOLD_PILL_BG, outline=GOLD_ACCENT, width=1)
    draw.text((lx + 13, ly + 4), badge_text, font=f_badge, fill=GOLD_LIGHT)

    # 2. Logo + Main Title
    ly += 42
    logo_path = os.path.join(IMAGES_DIR, "logo.png")
    logo_size = 62
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert('RGBA')
        logo_r = logo_im.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        banner.paste(logo_r, (lx, ly), logo_r)

    f_title = ImageFont.truetype(FONT_BD, 42)
    draw.text((lx + logo_size + 16, ly + 4), "진주퀸공인중개사사무소", font=f_title, fill=WHITE)

    # 3. Clean Subtitle
    ly += 74
    f_sub = ImageFont.truetype(FONT_BD, 19)
    draw.text((lx, ly), "충무공동 아파트 · 오피스텔 · 토지 · 상가 전문", font=f_sub, fill=GOLD_LIGHT)

    # 4. Short Tagline (No text wall!)
    ly += 34
    f_desc = ImageFont.truetype(FONT_REG, 14)
    draw.text((lx, ly), "실거래가 빅데이터 분석과 정직한 신뢰로 안전하게 중개합니다.", font=f_desc, fill=SLATE_LIGHT)

    # 5. Direct Call Action Card (Gold accent box)
    ly += 40
    btn_w = 480
    btn_h = 58
    draw.rounded_rectangle([lx, ly, lx + btn_w, ly + btn_h], radius=16, fill=NAVY_SURFACE, outline=GOLD_ACCENT, width=2)
    
    # Gold badge for direct phone
    draw.rounded_rectangle([lx + 6, ly + 6, lx + 90, ly + btn_h - 6], radius=12, fill=GOLD_ACCENT)
    f_call_lbl = ImageFont.truetype(FONT_BD, 14)
    draw.text((lx + 16, ly + 15), "대표 직통", font=f_call_lbl, fill=(15, 23, 42))
    
    # Direct Phone Number
    f_call_num = ImageFont.truetype(FONT_BD, 23)
    draw.text((lx + 104, ly + 11), "010-4670-7248", font=f_call_num, fill=WHITE)

    # Office Phone
    f_office = ImageFont.truetype(FONT_REG, 13)
    draw.text((lx + 295, ly + 18), "|   사무실 055-761-7248", font=f_office, fill=SLATE_LIGHT)

    # 6. Minimal Address Line (Perfect alignment with photo bottom)
    ly += 78
    f_footer = ImageFont.truetype(FONT_REG, 12)
    draw.text((lx, ly), "경남 진주시 에나로 146, 105호 (라온프라이빗시티)  |  등록 48170-2017-00038", font=f_footer, fill=SLATE_MUTED)

    # Save
    out_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_타이틀배너.jpg"), "JPEG", quality=98)
    print("Clean Naver Blog Title generated successfully!")


def generate_clean_youtube_banner():
    """
    YouTube Channel Art (2560 x 1440)
    - Full ambient navy canvas (seamless across 2560x1440)
    - Safe Zone (1546 x 423) is perfectly height-aligned
    - Photo height strictly matches text height
    - Disciplined Navy + Gold + White palette
    - Zero text cutoff on mobile, tablet, desktop
    """
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    banner = Image.new('RGB', (W, H), NAVY_BG)
    draw = ImageDraw.Draw(banner)

    # Subtle seamless horizontal wash
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for x in range(safe_x1 - 300, safe_x2 + 300):
        rel = (x - safe_x1) / safe_w
        factor = 1.0 - abs(rel - 0.5) * 1.7
        factor = max(0.0, min(1.0, factor))
        alpha = int(75 * factor)
        odraw.line([(x, safe_y1 - 150), (x, safe_y2 + 150)], fill=(20, 38, 75, alpha))

    banner = Image.alpha_composite(banner.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(banner)

    # Gold hairline accents for YouTube safe zone
    draw.line([(safe_x1 + 30, safe_y1 + 10), (safe_x2 - 30, safe_y1 + 10)], fill=GOLD_ACCENT, width=2)
    draw.line([(safe_x1 + 30, safe_y2 - 10), (safe_x2 - 30, safe_y2 - 10)], fill=GOLD_ACCENT, width=2)

    # Coordinated vertical bounds inside YouTube Safe Area
    # Safe area height: 423. Let's use top Y = 508 + 36 = 544, bottom Y = 931 - 36 = 895 (Height = 351px)
    CONTENT_TOP_Y = safe_y1 + 36
    CONTENT_BOT_Y = safe_y2 - 36
    BOX_HEIGHT = CONTENT_BOT_Y - CONTENT_TOP_Y # 351px

    # Right: Photo Box (width 250, height 351)
    photo_w = 250
    photo_h = BOX_HEIGHT
    photo_x = safe_x2 - photo_w - 60
    photo_y = CONTENT_TOP_Y

    draw.rounded_rectangle(
        [photo_x, photo_y, photo_x + photo_w, photo_y + photo_h],
        radius=20,
        fill=NAVY_SURFACE,
        outline=GOLD_ACCENT,
        width=2
    )

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        img_h = photo_h - 58
        img_w = photo_w - 8
        ceo_r = ceo_im.resize((img_w, img_h), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (img_w, img_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, img_w - 1, img_h - 1], radius=16, fill=255)
        banner.paste(ceo_r, (photo_x + 4, photo_y + 4), pmask)

        # Name plate
        f_pname = ImageFont.truetype(FONT_BD, 15)
        f_psub = ImageFont.truetype(FONT_REG, 12)
        tag_y = photo_y + img_h + 8
        draw.text((photo_x + 32, tag_y), "대표 공인중개사 황선숙", font=f_pname, fill=WHITE)
        draw.text((photo_x + 42, tag_y + 22), "통계학 석사 · 데이터 분석", font=f_psub, fill=GOLD_LIGHT)

    # Left: Coordinated Content
    lx = safe_x1 + 60
    ly = CONTENT_TOP_Y

    # 1. Top Pill Badge (Gold)
    f_badge = ImageFont.truetype(FONT_BD, 15)
    badge_text = "통계학 석사의 정밀 데이터 분석  ·  2017년부터 충무공동 한 자리"
    bbox_b = f_badge.getbbox(badge_text)
    bw_badge = (bbox_b[2] - bbox_b[0]) + 30
    draw.rounded_rectangle([lx, ly, lx + bw_badge, ly + 32], radius=16, fill=GOLD_PILL_BG, outline=GOLD_ACCENT, width=1)
    draw.text((lx + 15, ly + 5), badge_text, font=f_badge, fill=GOLD_LIGHT)

    # 2. Golden Logo + Brand Title
    ly += 48
    logo_path = os.path.join(IMAGES_DIR, "logo.png")
    logo_size = 76
    if os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert('RGBA')
        logo_r = logo_im.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        banner.paste(logo_r, (lx, ly), logo_r)

    f_title = ImageFont.truetype(FONT_BD, 54)
    draw.text((lx + logo_size + 20, ly + 6), "진주퀸공인중개사", font=f_title, fill=WHITE)

    # 3. Subtitle
    ly += 86
    f_sub = ImageFont.truetype(FONT_BD, 22)
    draw.text((lx, ly), "진주 혁신도시 아파트 · 오피스텔 · 토지 · 상가 전문", font=f_sub, fill=GOLD_LIGHT)

    # 4. Action Call Card
    ly += 45
    btn_w = 640
    btn_h = 62
    draw.rounded_rectangle([lx, ly, lx + btn_w, ly + btn_h], radius=18, fill=NAVY_SURFACE, outline=GOLD_ACCENT, width=2)
    draw.rounded_rectangle([lx + 6, ly + 6, lx + 105, ly + btn_h - 6], radius=14, fill=GOLD_ACCENT)
    
    f_call_lbl = ImageFont.truetype(FONT_BD, 16)
    f_call_num = ImageFont.truetype(FONT_BD, 26)
    f_office = ImageFont.truetype(FONT_REG, 16)
    
    draw.text((lx + 18, ly + 15), "대표 직통", font=f_call_lbl, fill=(15, 23, 42))
    draw.text((lx + 120, ly + 12), "010-4670-7248", font=f_call_num, fill=WHITE)
    draw.text((lx + 370, ly + 18), "|   사무실 055-761-7248", font=f_office, fill=SLATE_LIGHT)

    # 5. Clean Single-line Footer (aligned with photo bottom)
    ly += 80
    f_footer = ImageFont.truetype(FONT_REG, 14)
    draw.text((lx, ly), "충무공동 라온프라이빗시티 105호  |  등록 48170-2017-00038  |  jinjuqueen.vercel.app", font=f_footer, fill=SLATE_MUTED)

    # Save
    out_path = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_유튜브_채널아트배너.jpg"), "JPEG", quality=98)
    print("Clean YouTube Channel Banner generated successfully!")


def generate_clean_naver_blog_skin():
    """Naver Blog Wide Top Skin (2000 x 800) with title centered"""
    sw, sh = 2000, 800
    skin = Image.new('RGB', (sw, sh), NAVY_BG)
    draw = ImageDraw.Draw(skin)

    for y in range(sh):
        factor = y / sh
        r = int(10 * (1 - factor * 0.35) + 14 * (factor * 0.35))
        g = int(18 * (1 - factor * 0.35) + 24 * (factor * 0.35))
        b = int(38 * (1 - factor * 0.35) + 54 * (factor * 0.35))
        draw.line([(0, y), (sw, y)], fill=(r, g, b))

    draw.line([(0, 2), (sw, 2)], fill=GOLD_ACCENT, width=4)

    title_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    if os.path.exists(title_path):
        t_im = Image.open(title_path)
        tx = (sw - t_im.width) // 2
        ty = 80
        skin.paste(t_im, (tx, ty))

    skin.save(os.path.join(IMAGES_DIR, "naver-blog-skin.jpg"), "JPEG", quality=98)
    print("Clean Naver Blog Wide Skin generated successfully!")


if __name__ == '__main__':
    generate_clean_naver_blog_title()
    generate_clean_youtube_banner()
    generate_clean_naver_blog_skin()
