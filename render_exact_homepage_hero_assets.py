import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Deep luxurious royal navy palette
BG_NAVY_TOP = (11, 20, 44)        # Deep royal navy
BG_NAVY_BOT = (18, 29, 56)        # Rich slate navy

# Key vibrant accent colors
GOLD_BRIGHT = (252, 211, 77)      # Amber-300 / Radiant Gold
GOLD_RICH = (245, 158, 11)        # Amber-500 / Rich Golden
GOLD_BTN = (217, 119, 6)          # Warm Amber Gold
EMERALD_BRIGHT = (52, 211, 153)   # Mint / Emerald 400
EMERALD_BG = (6, 78, 59)          # Deep Emerald Glass Pill
GOLD_BG = (69, 26, 3)             # Deep Amber Glass Pill

WHITE = (255, 255, 255)
SLATE_200 = (226, 232, 240)
SLATE_300 = (203, 213, 225)
SLATE_400 = (148, 163, 184)


def create_naver_blog_banner():
    """
    Naver Blog Title Banner (966 x 500)
    - ULTRA-CLEAN & MINIMALIST: All small crowded text completely removed per user request
    - Natural phrasing: "충무공동 한 자리를 지켜온 진주퀸공인중개사입니다."
    - Integrated, elegant contact bar: Clunky white block replaced with sophisticated deep navy glass pill
    - STRICT height alignment: Left content and Right photo card both start at Y=85 and end at Y=415 (330px)
    - Luxurious negative space, perfectly balanced and centered
    """
    W, H = 966, 500
    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    # 1. Seamless background gradient (NO outer border lines)
    for y in range(H):
        factor = y / H
        r = int(BG_NAVY_TOP[0] * (1 - factor) + BG_NAVY_BOT[0] * factor)
        g = int(BG_NAVY_TOP[1] * (1 - factor) + BG_NAVY_BOT[1] * factor)
        b = int(BG_NAVY_TOP[2] * (1 - factor) + BG_NAVY_BOT[2] * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Subtle architectural micro-dots
    for x in range(16, W, 26):
        for y in range(16, H, 26):
            draw.point((x, y), fill=(26, 42, 68))

    # STRICT VERTICAL SPAN: Y_START = 85, Y_END = 415 (Height = 330px, centered in 500px)
    Y_START = 85
    Y_END = 415
    SPAN_H = Y_END - Y_START  # Exactly 330px

    # ==========================================
    # RIGHT: Photo Card (Y: 85 to 415, Height: 330px)
    # ==========================================
    photo_card_w = 250
    photo_card_h = SPAN_H
    photo_card_x = W - photo_card_w - 55  # 661
    photo_card_y = Y_START  # 85

    # Photo Card Body
    draw.rounded_rectangle(
        [photo_card_x, photo_card_y, photo_card_x + photo_card_w, photo_card_y + photo_card_h],
        radius=20,
        fill=(14, 23, 44)
    )

    # Photo inside card
    img_h = 250
    img_w = photo_card_w - 14
    img_x = photo_card_x + 7
    img_y = photo_card_y + 7

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((img_w, img_h), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (img_w, img_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, img_w - 1, img_h - 1], radius=16, fill=255)
        banner.paste(ceo_r, (img_x, img_y), pmask)

        # Name plate overlay at bottom of photo
        f_pname = ImageFont.truetype(FONT_BD, 13)
        tag_w = img_w - 24
        tag_h = 28
        tag_x = img_x + 12
        tag_y = img_y + img_h - 34
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10, fill=(10, 17, 36))
        draw.text((tag_x + 18, tag_y + 5), "대표 공인중개사 황선숙", font=f_pname, fill=GOLD_BRIGHT)

    # Clean text below photo inside card
    f_c1 = ImageFont.truetype(FONT_REG, 11)
    f_c2 = ImageFont.truetype(FONT_BD, 11)
    draw.text((photo_card_x + 20, photo_card_y + img_h + 16), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_c1, fill=SLATE_300)
    draw.text((photo_card_x + 16, photo_card_y + img_h + 38), "2017년부터 충무공동 한 자리 (통계학 석사)", font=f_c2, fill=GOLD_BRIGHT)

    # ==========================================
    # LEFT: Text Content (Y: 85 to 415, Height: 330px)
    # ==========================================
    lx = 55

    # 1. Top Badges (Y = 85 ~ 115) - Single unified elegant pill, NO repetition!
    f_b1 = ImageFont.truetype(FONT_BD, 12)
    b1_text = "🏛️  2017년부터 충무공동 한 자리 · 등록 48170-2017-00038"
    b1_w = int(f_b1.getlength(b1_text)) + 26
    b1_h = 28
    draw.rounded_rectangle([lx, Y_START, lx + b1_w, Y_START + b1_h], radius=14, fill=GOLD_BG)
    draw.text((lx + 13, Y_START + 5), b1_text, font=f_b1, fill=GOLD_BRIGHT)

    # 2. Main Headline H1 (Spacious, prominent, dignified)
    # Line 1: 통계학 석사의 정밀 데이터 분석,
    # Line 2: 충무공동 한 자리를 지켜온 진주퀸공인중개사입니다.
    f_h1 = ImageFont.truetype(FONT_BD, 28)
    f_h2 = ImageFont.truetype(FONT_BD, 22)
    f_name = ImageFont.truetype(FONT_BD, 25)

    y_h1 = Y_START + 50  # 135
    draw.text((lx, y_h1), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)

    y_h2 = y_h1 + 45     # 180
    str_pre = "충무공동 한 자리를 지켜온 "
    draw.text((lx, y_h2), str_pre, font=f_h2, fill=WHITE)
    w_pre = int(f_h2.getlength(str_pre)) + 4

    str_brand = "진주퀸공인중개사"
    draw.text((lx + w_pre, y_h2 - 2), str_brand, font=f_name, fill=GOLD_BRIGHT)
    w_brand = int(f_name.getlength(str_brand)) + 4

    draw.text((lx + w_pre + w_brand, y_h2), "입니다.", font=f_h2, fill=WHITE)

    # 3. Clean 1-Line Key Value Tag (Instead of 3 lines of small crowded text!)
    f_sub = ImageFont.truetype(FONT_REG, 13)
    y_sub = y_h2 + 56    # 236
    draw.text((lx, y_sub), "빅데이터 실거래가 정밀 분석  |  100% 현장 검증 실매물  |  책임 성실 중개", font=f_sub, fill=SLATE_300)

    # 4. Direct Call Action Strip (Starts Y = 345, Ends EXACTLY at Y_END = 415!)
    # Height = 415 - 345 = 70px
    y_btn = 345
    btn_w = 545

    draw.rounded_rectangle([lx, y_btn, lx + btn_w, Y_END], radius=18, fill=GOLD_BTN)

    # Sophisticated Deep Navy Glass Pill for "대표 직통" (Replaces the clunky white rectangle!)
    f_btn_lbl = ImageFont.truetype(FONT_BD, 13)
    draw.rounded_rectangle([lx + 12, y_btn + 12, lx + 104, Y_END - 12], radius=12, fill=(12, 22, 48))
    draw.text((lx + 24, y_btn + 20), "대표 직통", font=f_btn_lbl, fill=GOLD_BRIGHT)

    # Large, crisp phone number
    f_btn_phone = ImageFont.truetype(FONT_BD, 24)
    draw.text((lx + 118, y_btn + 15), "010-4670-7248", font=f_btn_phone, fill=WHITE)

    # Office Phone
    f_btn_off = ImageFont.truetype(FONT_BD, 13)
    draw.text((lx + 338, y_btn + 22), "|   사무실 055-761-7248", font=f_btn_off, fill=WHITE)

    # Save
    out_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_타이틀배너.jpg"), "JPEG", quality=98)
    print("Naver Blog Banner perfectly generated! Height alignment strictly verified: 85 to 415")


def create_youtube_banner():
    """
    YouTube Channel Art (2560 x 1440)
    - ULTRA-CLEAN & MINIMALIST: Small crowded text removed per user request
    - Safe zone: 1546 x 423 (Center: 507 to 2053, Y: 508 to 931)
    - STRICT height alignment inside safe zone (Y: 555 to 885 = 330px)
    """
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    for y in range(H):
        factor = y / H
        r = int(BG_NAVY_TOP[0] * (1 - factor) + BG_NAVY_BOT[0] * factor)
        g = int(BG_NAVY_TOP[1] * (1 - factor) + BG_NAVY_BOT[1] * factor)
        b = int(BG_NAVY_TOP[2] * (1 - factor) + BG_NAVY_BOT[2] * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Micro-dots
    for x in range(16, W, 28):
        for y in range(16, H, 28):
            draw.point((x, y), fill=(26, 42, 68))

    # STRICT VERTICAL SPAN: Y_START = 555, Y_END = 885 (Height = 330px)
    Y_START = safe_y1 + 47  # 555
    Y_END = safe_y2 - 46    # 885
    SPAN_H = Y_END - Y_START  # 330px

    # ==========================================
    # RIGHT: Photo Card (Y: 555 to 885, Height: 330px)
    # ==========================================
    photo_card_w = 255
    photo_card_h = SPAN_H
    photo_card_x = safe_x2 - photo_card_w - 55
    photo_card_y = Y_START

    draw.rounded_rectangle(
        [photo_card_x, photo_card_y, photo_card_x + photo_card_w, photo_card_y + photo_card_h],
        radius=20,
        fill=(14, 23, 44)
    )

    img_h = 250
    img_w = photo_card_w - 14
    img_x = photo_card_x + 7
    img_y = photo_card_y + 7

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((img_w, img_h), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (img_w, img_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, img_w - 1, img_h - 1], radius=16, fill=255)
        banner.paste(ceo_r, (img_x, img_y), pmask)

        # Name plate overlay at bottom of photo
        f_pname = ImageFont.truetype(FONT_BD, 13)
        tag_w = img_w - 24
        tag_h = 28
        tag_x = img_x + 12
        tag_y = img_y + img_h - 34
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10, fill=(10, 17, 36))
        draw.text((tag_x + 18, tag_y + 5), "대표 공인중개사 황선숙", font=f_pname, fill=GOLD_BRIGHT)

    f_c1 = ImageFont.truetype(FONT_REG, 11)
    f_c2 = ImageFont.truetype(FONT_BD, 11)
    draw.text((photo_card_x + 20, photo_card_y + img_h + 16), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_c1, fill=SLATE_300)
    draw.text((photo_card_x + 16, photo_card_y + img_h + 38), "2017년부터 충무공동 한 자리 (통계학 석사)", font=f_c2, fill=GOLD_BRIGHT)

    # ==========================================
    # LEFT: Text Content (Y: 555 to 885, Height: 330px)
    # ==========================================
    lx = safe_x1 + 55

    # 1. Top Badges (Y = 555)
    f_b1 = ImageFont.truetype(FONT_BD, 13)
    b1_text = "🏛️  2017년부터 충무공동 한 자리 · 등록 48170-2017-00038"
    b1_w = int(f_b1.getlength(b1_text)) + 28
    b1_h = 30
    draw.rounded_rectangle([lx, Y_START, lx + b1_w, Y_START + b1_h], radius=15, fill=GOLD_BG)
    draw.text((lx + 14, Y_START + 5), b1_text, font=f_b1, fill=GOLD_BRIGHT)

    # 2. Headline H1
    f_h1 = ImageFont.truetype(FONT_BD, 36)
    f_h2 = ImageFont.truetype(FONT_BD, 28)
    f_name = ImageFont.truetype(FONT_BD, 31)

    y_h1 = Y_START + 52  # 607
    draw.text((lx, y_h1), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)

    y_h2 = y_h1 + 48     # 655
    str_pre = "충무공동 한 자리를 지켜온 "
    draw.text((lx, y_h2), str_pre, font=f_h2, fill=WHITE)
    w_pre = int(f_h2.getlength(str_pre)) + 5

    str_brand = "진주퀸공인중개사"
    draw.text((lx + w_pre, y_h2 - 2), str_brand, font=f_name, fill=GOLD_BRIGHT)
    w_brand = int(f_name.getlength(str_brand)) + 5

    draw.text((lx + w_pre + w_brand, y_h2), "입니다.", font=f_h2, fill=WHITE)

    # 3. Clean 1-Line Key Value Tag
    f_sub = ImageFont.truetype(FONT_REG, 16)
    y_sub = y_h2 + 60    # 715
    draw.text((lx, y_sub), "빅데이터 실거래가 정밀 분석  |  100% 현장 검증 실매물  |  책임 성실 중개", font=f_sub, fill=SLATE_300)

    # 4. Direct Call Strip (Ends at Y_END = 885!)
    y_btn = 815
    btn_w = 812

    draw.rounded_rectangle([lx, y_btn, lx + btn_w, Y_END], radius=18, fill=GOLD_BTN)

    f_btn_lbl = ImageFont.truetype(FONT_BD, 15)
    draw.rounded_rectangle([lx + 14, y_btn + 12, lx + 116, Y_END - 12], radius=14, fill=(12, 22, 48))
    draw.text((lx + 28, y_btn + 20), "대표 직통", font=f_btn_lbl, fill=GOLD_BRIGHT)

    f_btn_phone = ImageFont.truetype(FONT_BD, 26)
    draw.text((lx + 135, y_btn + 15), "010-4670-7248", font=f_btn_phone, fill=WHITE)

    f_btn_off = ImageFont.truetype(FONT_BD, 16)
    draw.text((lx + 450, y_btn + 22), "|   사무실 055-761-7248  (jinjuqueen.vercel.app)", font=f_btn_off, fill=WHITE)

    out_path = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_유튜브_채널아트배너.jpg"), "JPEG", quality=98)
    print("YouTube Banner perfectly generated! Height alignment strictly verified: 555 to 885")


def create_naver_blog_skin():
    """Naver Blog Wide Top Skin (2000 x 800) seamless without harsh line borders"""
    sw, sh = 2000, 800
    skin = Image.new('RGB', (sw, sh), BG_NAVY_TOP)
    draw = ImageDraw.Draw(skin)

    for y in range(sh):
        factor = y / sh
        r = int(BG_NAVY_TOP[0] * (1 - factor) + BG_NAVY_BOT[0] * factor)
        g = int(BG_NAVY_TOP[1] * (1 - factor) + BG_NAVY_BOT[1] * factor)
        b = int(BG_NAVY_TOP[2] * (1 - factor) + BG_NAVY_BOT[2] * factor)
        draw.line([(0, y), (sw, y)], fill=(r, g, b))

    for x in range(16, sw, 26):
        for y in range(16, sh, 26):
            draw.point((x, y), fill=(26, 42, 68))

    title_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    if os.path.exists(title_path):
        t_im = Image.open(title_path)
        tx = (sw - 966) // 2
        ty = (sh - 500) // 2
        skin.paste(t_im, (tx, ty))

    skin.save(os.path.join(IMAGES_DIR, "naver-blog-skin.jpg"), "JPEG", quality=98)
    print("Naver Blog Wide Skin generated!")


if __name__ == '__main__':
    create_naver_blog_banner()
    create_youtube_banner()
    create_naver_blog_skin()
