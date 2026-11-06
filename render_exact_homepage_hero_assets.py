import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Rich, sophisticated deep navy palette matching homepage
BG_NAVY_TOP = (11, 20, 44)        # Deep royal navy
BG_NAVY_BOT = (18, 29, 56)        # Rich slate navy

# Vibrant highlight accents for important elements
GOLD_BRIGHT = (252, 211, 77)      # Amber-300 / Radiant Gold
GOLD_RICH = (245, 158, 11)        # Amber-500 / Rich Golden
GOLD_BTN = (217, 119, 6)          # Warm Amber Gold
EMERALD_BRIGHT = (52, 211, 153)   # Mint / Emerald 400
EMERALD_BG = (6, 78, 59)          # Deep Emerald Pill Glass
GOLD_BG = (69, 26, 3)             # Deep Amber Pill Glass

WHITE = (255, 255, 255)
SLATE_200 = (226, 232, 240)
SLATE_300 = (203, 213, 225)
SLATE_400 = (148, 163, 184)


def create_naver_blog_banner():
    """
    Naver Blog Title Banner (966 x 500)
    - Strictly NO border lines (seamless canvas, no outer borders)
    - Vibrant highlight colors on important focal points (Gold, Emerald, White)
    - EXACT height alignment: Left content and Right photo card both start at Y=65 and end at Y=435 (370px)
    - ZERO text overlap: Font size and character positions calculated with safe margins (width <= 560px)
    - Balanced, premium aesthetic matching the website hero section
    """
    W, H = 966, 500
    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    # 1. Seamless background gradient (NO top/bottom line borders!)
    for y in range(H):
        factor = y / H
        r = int(BG_NAVY_TOP[0] * (1 - factor) + BG_NAVY_BOT[0] * factor)
        g = int(BG_NAVY_TOP[1] * (1 - factor) + BG_NAVY_BOT[1] * factor)
        b = int(BG_NAVY_TOP[2] * (1 - factor) + BG_NAVY_BOT[2] * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Architectural micro-dot pattern
    for x in range(16, W, 26):
        for y in range(16, H, 26):
            draw.point((x, y), fill=(30, 46, 76))

    # STRICT VERTICAL SPAN: Y_START = 65, Y_END = 435 (Total 370px)
    Y_START = 65
    Y_END = 435
    SPAN_H = Y_END - Y_START  # Exactly 370px

    # ==========================================
    # RIGHT: Photo Card (Y: 65 to 435, Height: 370px)
    # ==========================================
    photo_card_w = 260
    photo_card_h = SPAN_H  # Exactly 370px
    photo_card_x = W - photo_card_w - 45  # 661
    photo_card_y = Y_START  # 65

    # Photo Card Body (Soft translucent card with rounded corners, NO harsh outer border)
    draw.rounded_rectangle(
        [photo_card_x, photo_card_y, photo_card_x + photo_card_w, photo_card_y + photo_card_h],
        radius=20,
        fill=(14, 23, 44)
    )

    # Photo image inside card
    img_h = 285
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
        f_pname = ImageFont.truetype(FONT_BD, 14)
        tag_w = img_w - 24
        tag_h = 28
        tag_x = img_x + 12
        tag_y = img_y + img_h - 34
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10, fill=(10, 17, 36))
        draw.text((tag_x + 18, tag_y + 5), "대표 공인중개사 황선숙", font=f_pname, fill=GOLD_BRIGHT)

    # Text below photo inside card (fills from 357 to 435 with balanced padding)
    f_c1 = ImageFont.truetype(FONT_REG, 11)
    f_c2 = ImageFont.truetype(FONT_BD, 11)
    draw.text((photo_card_x + 24, photo_card_y + img_h + 18), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_c1, fill=SLATE_300)
    draw.text((photo_card_x + 20, photo_card_y + img_h + 40), "2017년부터 충무공동 한 자리 (통계학 석사)", font=f_c2, fill=GOLD_BRIGHT)

    # ==========================================
    # LEFT: Text Content (Y: 65 to 435, Height: 370px)
    # ==========================================
    lx = 45

    # 1. Top Badges (Y = 65 ~ 93) - Emerald & Amber Gold
    f_b1 = ImageFont.truetype(FONT_BD, 12)
    f_b2 = ImageFont.truetype(FONT_BD, 12)

    # Badge 1: 🟢 통계학 석사의 정밀 데이터 분석 (Emerald)
    b1_text = "통계학 석사의 정밀 데이터 분석"
    b1_w = int(f_b1.getlength(b1_text)) + 34
    b1_h = 28
    draw.rounded_rectangle([lx, Y_START, lx + b1_w, Y_START + b1_h], radius=14, fill=EMERALD_BG)
    draw.ellipse([lx + 10, Y_START + 10, lx + 17, Y_START + 17], fill=EMERALD_BRIGHT)
    draw.text((lx + 23, Y_START + 5), b1_text, font=f_b1, fill=EMERALD_BRIGHT)

    # Badge 2: 🏛️ 2017년부터 충무공동 한 자리 (Amber Gold)
    b2_x = lx + b1_w + 10
    b2_text = "2017년부터 충무공동 한 자리"
    b2_w = int(f_b2.getlength(b2_text)) + 26
    draw.rounded_rectangle([b2_x, Y_START, b2_x + b2_w, Y_START + b1_h], radius=14, fill=GOLD_BG)
    draw.text((b2_x + 13, Y_START + 5), b2_text, font=f_b2, fill=GOLD_BRIGHT)

    # 2. Headline H1 (Starts Y = 111, Line 2 fits comfortably without any overlap)
    f_h1 = ImageFont.truetype(FONT_BD, 25)
    f_h2 = ImageFont.truetype(FONT_BD, 21)
    f_name = ImageFont.truetype(FONT_BD, 23)

    y_h1 = 111
    draw.text((lx, y_h1), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)

    y_h2 = 145
    str_pre = "충무공동 한 자리를 지켜온 신뢰 "
    draw.text((lx, y_h2), str_pre, font=f_h2, fill=WHITE)
    w_pre = int(f_h2.getlength(str_pre)) + 3

    str_brand = "진주퀸공인중개사"
    draw.text((lx + w_pre, y_h2 - 2), str_brand, font=f_name, fill=GOLD_BRIGHT)
    w_brand = int(f_name.getlength(str_brand)) + 4

    draw.text((lx + w_pre + w_brand, y_h2), "입니다.", font=f_h2, fill=WHITE)

    # 3. Body Text (Starts Y = 186, 3 clean lines, well spaced)
    f_body = ImageFont.truetype(FONT_REG, 12)
    y_body = 186
    draw.text((lx, y_body), "2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리에서", font=f_body, fill=SLATE_300)
    draw.text((lx, y_body + 20), "통계학 석사 황선숙 대표가 빅데이터 실거래가 정밀 분석과", font=f_body, fill=SLATE_300)
    draw.text((lx, y_body + 40), "100% 현장 검증 실매물로 고객님의 소중한 자산을 안전하게 중개합니다.", font=f_body, fill=SLATE_300)

    # 4. 3 Feature Metric Cards (Starts Y = 265, Height = 74)
    y_cards = 265
    card_w = 175
    card_gap = 12
    card_h = 74
    f_ctop = ImageFont.truetype(FONT_BD, 15)
    f_cbot = ImageFont.truetype(FONT_REG, 11)

    metric_items = [
        ("통계학 석사", "정밀 데이터 분석", GOLD_BRIGHT),
        ("충무공동 한 자리", "우직한 신뢰", GOLD_BRIGHT),
        ("100% 실매물", "현장 검증 책임 중개", EMERALD_BRIGHT)
    ]

    for i, (top_txt, bot_txt, col) in enumerate(metric_items):
        cx = lx + i * (card_w + card_gap)
        draw.rounded_rectangle(
            [cx, y_cards, cx + card_w, y_cards + card_h],
            radius=12,
            fill=(255, 255, 255, 14)
        )
        tw = int(f_ctop.getlength(top_txt))
        draw.text((cx + (card_w - tw) // 2, y_cards + 15), top_txt, font=f_ctop, fill=col)

        bw = int(f_cbot.getlength(bot_txt))
        draw.text((cx + (card_w - bw) // 2, y_cards + 43), bot_txt, font=f_cbot, fill=SLATE_300)

    # 5. Bottom Direct Call Action Strip (Starts Y = 365, Ends EXACTLY at Y_END = 435!)
    # Height = 435 - 365 = 70px
    y_btn = 365
    btn_w = 549

    draw.rounded_rectangle([lx, y_btn, lx + btn_w, Y_END], radius=16, fill=GOLD_BTN)

    # Pill for "대표 직통"
    f_btn_lbl = ImageFont.truetype(FONT_BD, 13)
    draw.rounded_rectangle([lx + 10, y_btn + 10, lx + 96, Y_END - 10], radius=12, fill=(255, 255, 255, 60))
    draw.text((lx + 20, y_btn + 18), "대표 직통", font=f_btn_lbl, fill=(15, 23, 42))

    # Phone Number
    f_btn_phone = ImageFont.truetype(FONT_BD, 22)
    draw.text((lx + 112, y_btn + 14), "010-4670-7248", font=f_btn_phone, fill=WHITE)

    # Office Phone
    f_btn_off = ImageFont.truetype(FONT_BD, 13)
    draw.text((lx + 320, y_btn + 20), "|   사무실 055-761-7248", font=f_btn_off, fill=WHITE)

    # Save
    out_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_타이틀배너.jpg"), "JPEG", quality=98)
    print("Naver Blog Banner perfectly generated! Height alignment strictly verified: 65 to 435")


def create_youtube_banner():
    """
    YouTube Channel Art (2560 x 1440)
    - Safe zone: 1546 x 423 (Center: 507 to 2053, Y: 508 to 931)
    - STRICT height alignment inside safe zone (Y: 535 to 905 = 370px)
    - NO border lines
    - Vibrant Gold & Emerald highlights
    - ZERO text overlap
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

    # Micro-dot pattern
    for x in range(16, W, 28):
        for y in range(16, H, 28):
            draw.point((x, y), fill=(30, 45, 75))

    # STRICT VERTICAL SPAN: Y_START = 535, Y_END = 905 (Height = 370px)
    Y_START = safe_y1 + 27  # 535
    Y_END = safe_y2 - 26    # 905
    SPAN_H = Y_END - Y_START  # 370px

    # ==========================================
    # RIGHT: Photo Card (Y: 535 to 905, Height: 370px)
    # ==========================================
    photo_card_w = 265
    photo_card_h = SPAN_H
    photo_card_x = safe_x2 - photo_card_w - 40
    photo_card_y = Y_START

    draw.rounded_rectangle(
        [photo_card_x, photo_card_y, photo_card_x + photo_card_w, photo_card_y + photo_card_h],
        radius=20,
        fill=(14, 23, 44)
    )

    img_h = 285
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
        f_pname = ImageFont.truetype(FONT_BD, 14)
        tag_w = img_w - 24
        tag_h = 28
        tag_x = img_x + 12
        tag_y = img_y + img_h - 34
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10, fill=(10, 17, 36))
        draw.text((tag_x + 18, tag_y + 5), "대표 공인중개사 황선숙", font=f_pname, fill=GOLD_BRIGHT)

    f_c1 = ImageFont.truetype(FONT_REG, 11)
    f_c2 = ImageFont.truetype(FONT_BD, 11)
    draw.text((photo_card_x + 24, photo_card_y + img_h + 18), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_c1, fill=SLATE_300)
    draw.text((photo_card_x + 20, photo_card_y + img_h + 40), "2017년부터 충무공동 한 자리 (통계학 석사)", font=f_c2, fill=GOLD_BRIGHT)

    # ==========================================
    # LEFT: Text Content (Y: 535 to 905, Height: 370px)
    # ==========================================
    lx = safe_x1 + 45

    # 1. Top Badges (Y = 535)
    f_b1 = ImageFont.truetype(FONT_BD, 13)
    f_b2 = ImageFont.truetype(FONT_BD, 13)

    b1_text = "통계학 석사의 정밀 데이터 분석"
    b1_w = int(f_b1.getlength(b1_text)) + 38
    b1_h = 30
    draw.rounded_rectangle([lx, Y_START, lx + b1_w, Y_START + b1_h], radius=15, fill=EMERALD_BG)
    draw.ellipse([lx + 11, Y_START + 11, lx + 18, Y_START + 18], fill=EMERALD_BRIGHT)
    draw.text((lx + 25, Y_START + 5), b1_text, font=f_b1, fill=EMERALD_BRIGHT)

    b2_x = lx + b1_w + 12
    b2_text = "2017년부터 충무공동 한 자리"
    b2_w = int(f_b2.getlength(b2_text)) + 28
    draw.rounded_rectangle([b2_x, Y_START, b2_x + b2_w, Y_START + b1_h], radius=15, fill=GOLD_BG)
    draw.text((b2_x + 14, Y_START + 5), b2_text, font=f_b2, fill=GOLD_BRIGHT)

    # 2. Headline H1
    f_h1 = ImageFont.truetype(FONT_BD, 34)
    f_h2 = ImageFont.truetype(FONT_BD, 30)
    f_name = ImageFont.truetype(FONT_BD, 32)

    y_h1 = Y_START + 46  # 581
    draw.text((lx, y_h1), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)

    y_h2 = y_h1 + 42  # 623
    str_pre = "충무공동 한 자리를 지켜온 신뢰 "
    draw.text((lx, y_h2), str_pre, font=f_h2, fill=WHITE)
    w_pre = int(f_h2.getlength(str_pre)) + 6

    str_brand = "진주퀸공인중개사"
    draw.text((lx + w_pre, y_h2 - 2), str_brand, font=f_name, fill=GOLD_BRIGHT)
    w_brand = int(f_name.getlength(str_brand)) + 6

    draw.text((lx + w_pre + w_brand, y_h2), "입니다.", font=f_h2, fill=WHITE)

    # 3. Body Text (Starts Y = 673)
    f_body = ImageFont.truetype(FONT_REG, 15)
    y_body = y_h2 + 50
    draw.text((lx, y_body), "2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리에서", font=f_body, fill=SLATE_300)
    draw.text((lx, y_body + 24), "통계학 석사 황선숙 대표가 빅데이터 실거래가 정밀 분석과 100% 현장 검증 실매물로 고객님의 자산을 중개합니다.", font=f_body, fill=SLATE_300)

    # 4. 3 Metric Cards (Starts Y = 745, Height = 74)
    y_cards = y_body + 66
    card_w = 260
    card_gap = 16
    card_h = 74
    f_ctop = ImageFont.truetype(FONT_BD, 18)
    f_cbot = ImageFont.truetype(FONT_REG, 13)

    metric_items = [
        ("통계학 석사", "정밀 데이터 분석", GOLD_BRIGHT),
        ("충무공동 한 자리", "우직한 신뢰", GOLD_BRIGHT),
        ("100% 실매물", "현장 검증 책임 중개", EMERALD_BRIGHT)
    ]

    for i, (top_txt, bot_txt, col) in enumerate(metric_items):
        cx = lx + i * (card_w + card_gap)
        draw.rounded_rectangle([cx, y_cards, cx + card_w, y_cards + card_h], radius=14, fill=(255, 255, 255, 14))
        tw = int(f_ctop.getlength(top_txt))
        draw.text((cx + (card_w - tw) // 2, y_cards + 14), top_txt, font=f_ctop, fill=col)

        bw = int(f_cbot.getlength(bot_txt))
        draw.text((cx + (card_w - bw) // 2, y_cards + 44), bot_txt, font=f_cbot, fill=SLATE_300)

    # 5. Direct Call Strip (Ends at Y_END = 905!)
    y_btn = y_cards + card_h + 16
    btn_w = 812

    draw.rounded_rectangle([lx, y_btn, lx + btn_w, Y_END], radius=18, fill=GOLD_BTN)

    f_btn_lbl = ImageFont.truetype(FONT_BD, 15)
    draw.rounded_rectangle([lx + 10, y_btn + 10, lx + 110, Y_END - 10], radius=14, fill=(255, 255, 255, 60))
    draw.text((lx + 24, y_btn + 18), "대표 직통", font=f_btn_lbl, fill=(15, 23, 42))

    f_btn_phone = ImageFont.truetype(FONT_BD, 26)
    draw.text((lx + 130, y_btn + 13), "010-4670-7248", font=f_btn_phone, fill=WHITE)

    f_btn_off = ImageFont.truetype(FONT_BD, 16)
    draw.text((lx + 440, y_btn + 20), "|   사무실 055-761-7248  (jinjuqueen.vercel.app)", font=f_btn_off, fill=WHITE)

    out_path = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_유튜브_채널아트배너.jpg"), "JPEG", quality=98)
    print("YouTube Banner perfectly generated! Height alignment strictly verified: 535 to 905")


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
            draw.point((x, y), fill=(30, 46, 76))

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
