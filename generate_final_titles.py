import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Color Palette precisely matched to user's uploaded screenshot (media_1793957375436_5aa17c94.jpg)
BG_NAVY_TOP = (11, 20, 42)        # Deep royal navy
BG_NAVY_BOT = (8, 14, 30)         # Midnight slate navy
BG_CARD = (15, 25, 46)            # Dark card background
BORDER_CARD = (32, 48, 80)        # Card border

GOLD_MAIN = (251, 191, 36)        # Amber-400 / Radiant Gold
GOLD_LINE = (245, 158, 11)        # Underline gold

WHITE = (255, 255, 255)
SLATE_300 = (203, 213, 225)
SLATE_400 = (148, 163, 184)
SLATE_500 = (100, 116, 139)

MINT_TEXT = (52, 211, 153)        # Emerald-400
MINT_BG = (6, 78, 59)             # Deep emerald
MINT_BORDER = (16, 185, 129)

AMBER_PILL_TEXT = (251, 191, 36)
AMBER_PILL_BG = (69, 26, 3)
AMBER_PILL_BORDER = (217, 119, 6)

# Phone Button: Royal Blue per user's explicit request
BLUE_BTN_TOP = (37, 99, 235)      # Royal Blue
BLUE_BTN_BOT = (29, 78, 216)      # Indigo Blue
BLUE_BTN_BORDER = (96, 165, 250)


def draw_dot_grid(draw, width, height, step=22):
    for x in range(12, width, step):
        for y in range(12, height, step):
            draw.point((x, y), fill=(24, 38, 65))


def draw_green_dot(draw, cx, cy, r=3.5, color=MINT_TEXT):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def draw_shield_icon(draw, x, y, size=13, color=AMBER_PILL_TEXT):
    # Precise shield outline
    pts = [
        (x + size * 0.5, y),
        (x + size, y + size * 0.22),
        (x + size * 0.85, y + size * 0.72),
        (x + size * 0.5, y + size),
        (x + size * 0.15, y + size * 0.72),
        (x, y + size * 0.22)
    ]
    draw.polygon(pts, fill=None, outline=color)
    # Checkmark inside
    draw.line([(x + size * 0.3, y + size * 0.5), (x + size * 0.48, y + size * 0.68)], fill=color, width=2)
    draw.line([(x + size * 0.48, y + size * 0.68), (x + size * 0.75, y + size * 0.32)], fill=color, width=2)


def draw_phone_icon(draw, x, y, size=13, color=GOLD_MAIN):
    # Clean phone receiver handset
    pts = [
        (x + 2, y + 2), (x + 5, y + 1), (x + 7, y + 4), (x + 5, y + 6),
        (x + 7, y + 9), (x + 9, y + 8), (x + 11, y + 10), (x + 11, y + 13),
        (x + 8, y + 14), (x + 1, y + 7)
    ]
    draw.polygon(pts, fill=color)


def create_naver_blog_banner_exact():
    """
    Naver Blog Title Banner (966 x 450)
    1:1 Translation of media_1793957375436_5aa17c94.jpg
    """
    W, H = 966, 450
    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    # 1. Background gradient & dot grid
    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_dot_grid(draw, W, H, step=22)

    # Coordinated vertical bounds: Y_TOP = 42, Y_BOT = 408 (Span = 366px)
    Y_TOP = 42
    Y_BOT = 408

    # ==========================================
    # RIGHT SHOWCASE CARD (X: 674, Y: 42, W: 250, H: 366)
    # ==========================================
    card_w = 250
    card_h = Y_BOT - Y_TOP  # 366
    card_x = W - card_w - 42 # 674
    card_y = Y_TOP

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=20,
        fill=BG_CARD,
        outline=BORDER_CARD,
        width=1
    )

    photo_w = card_w - 20 # 230
    photo_h = 220
    photo_x = card_x + 10
    photo_y = card_y + 10

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (photo_w, photo_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_w - 1, photo_h - 1], radius=16, fill=255)
        banner.paste(ceo_r, (photo_x, photo_y), pmask)

        # Name tag overlay at photo bottom
        f_name = ImageFont.truetype(FONT_BD, 12)
        tag_w = photo_w - 32
        tag_h = 25
        tag_x = photo_x + 16
        tag_y = photo_y + photo_h - 31
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10, fill=(11, 18, 35))
        draw.text((tag_x + 24, tag_y + 4), "대표 공인중개사 황선숙", font=f_name, fill=WHITE)

    # Address & Info Text below photo
    f_addr = ImageFont.truetype(FONT_REG, 11)
    f_stat = ImageFont.truetype(FONT_REG, 10)
    draw.text((card_x + 25, photo_y + photo_h + 10), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_addr, fill=SLATE_300)
    draw.text((card_x + 20, photo_y + photo_h + 26), "2017년 2월 개업 이래 충무공동 한 자리 (통계학 석사)", font=f_stat, fill=GOLD_MAIN)

    # Royal Blue Call Button
    btn_w = card_w - 24
    btn_h = 36
    btn_x = card_x + 12
    btn_y = card_y + card_h - btn_h - 12
    for by in range(btn_h):
        bf = by / btn_h
        br = int(BLUE_BTN_TOP[0] * (1 - bf) + BLUE_BTN_BOT[0] * bf)
        bg = int(BLUE_BTN_TOP[1] * (1 - bf) + BLUE_BTN_BOT[1] * bf)
        bb = int(BLUE_BTN_TOP[2] * (1 - bf) + BLUE_BTN_BOT[2] * bf)
        draw.line([(btn_x, btn_y + by), (btn_x + btn_w, btn_y + by)], fill=(br, bg, bb))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=12, outline=BLUE_BTN_BORDER, width=1)
    
    # Phone Icon + Text
    draw_phone_icon(draw, btn_x + 30, btn_y + 11, size=14, color=GOLD_MAIN)
    f_btn = ImageFont.truetype(FONT_BD, 12)
    draw.text((btn_x + 50, btn_y + 9), "010-4670-7248 직접 상담", font=f_btn, fill=WHITE)

    # ==========================================
    # LEFT CONTENT (X: 42, Y: 42 to 408)
    # ==========================================
    lx = 42

    # 1. Top Badges
    f_pill = ImageFont.truetype(FONT_BD, 11)
    pill1_text = "통계학 석사의 정밀 데이터 분석 · 2017년부터 충무공동 한 자리"
    pill2_text = "등록 48170-2017-00038"

    bbox1 = f_pill.getbbox(pill1_text)
    pw1 = (bbox1[2] - bbox1[0]) + 30
    draw.rounded_rectangle([lx, Y_TOP, lx + pw1, Y_TOP + 24], radius=12, fill=MINT_BG, outline=MINT_BORDER, width=1)
    draw_green_dot(draw, lx + 12, Y_TOP + 12, r=3.5, color=MINT_TEXT)
    draw.text((lx + 22, Y_TOP + 4), pill1_text, font=f_pill, fill=MINT_TEXT)

    lx2 = lx + pw1 + 8
    bbox2 = f_pill.getbbox(pill2_text)
    pw2 = (bbox2[2] - bbox2[0]) + 30
    draw.rounded_rectangle([lx2, Y_TOP, lx2 + pw2, Y_TOP + 24], radius=12, fill=AMBER_PILL_BG, outline=AMBER_PILL_BORDER, width=1)
    draw_shield_icon(draw, lx2 + 10, Y_TOP + 5, size=13, color=AMBER_PILL_TEXT)
    draw.text((lx2 + 27, Y_TOP + 4), pill2_text, font=f_pill, fill=AMBER_PILL_TEXT)

    # 2. Main Headline (3 Lines)
    f_h1 = ImageFont.truetype(FONT_BD, 28)
    h_y = Y_TOP + 42
    draw.text((lx, h_y), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=GOLD_MAIN)
    draw.text((lx, h_y + 38), "2017년부터 충무공동 한 자리를 지켜온", font=f_h1, fill=WHITE)

    # Line 3: 진주퀸공인중개사 (Gold + Underline) + 입니다. (White)
    draw.text((lx, h_y + 76), "진주퀸공인중개사", font=f_h1, fill=GOLD_MAIN)
    bbox_brand = f_h1.getbbox("진주퀸공인중개사")
    bw_brand = bbox_brand[2] - bbox_brand[0]
    draw.line([(lx, h_y + 112), (lx + bw_brand, h_y + 112)], fill=GOLD_LINE, width=3)
    draw.text((lx + bw_brand + 2, h_y + 76), "입니다.", font=f_h1, fill=WHITE)

    # 3. Summary (2 lines)
    f_sub = ImageFont.truetype(FONT_REG, 13)
    s_y = h_y + 128
    draw.text((lx, s_y), "실거래가 빅데이터와 정밀 권리분석을 바탕으로,", font=f_sub, fill=SLATE_300)
    draw.text((lx, s_y + 20), "100% 현장 검증 실매물로 고객님의 소중한 자산을 안전하게 중개합니다.", font=f_sub, fill=SLATE_300)

    # 4. Three Highlight Cards (Bottom Y = 408, Height = 60px)
    c_y = Y_BOT - 60
    c_w = 190
    c_gap = 14
    f_ctitle = ImageFont.truetype(FONT_BD, 13)
    f_csub = ImageFont.truetype(FONT_REG, 11)

    cards = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "2017년부터 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (ct, cs) in enumerate(cards):
        cx = lx + i * (c_w + c_gap)
        draw.rounded_rectangle([cx, c_y, cx + c_w, c_y + 60], radius=14, fill=BG_CARD, outline=BORDER_CARD, width=1)
        bt = f_ctitle.getbbox(ct)
        tw = bt[2] - bt[0]
        draw.text((cx + (c_w - tw) // 2, c_y + 11), ct, font=f_ctitle, fill=GOLD_MAIN)

        bs = f_csub.getbbox(cs)
        sw = bs[2] - bs[0]
        draw.text((cx + (c_w - sw) // 2, c_y + 32), cs, font=f_csub, fill=SLATE_400)

    out_art = os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg")
    out_img = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    out_desk = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_966x450.jpg")

    banner.save(out_art, quality=95)
    banner.save(out_img, quality=95)
    banner.save(out_desk, quality=95)
    print("Saved Naver Blog Banner:", out_art)
    return out_art


def create_youtube_channel_banner_exact():
    """
    YouTube Channel Banner (2560 x 1440)
    Safe Area: Center 1546 x 423 (Y: 508 to 931, X: 507 to 2053)
    Content fits seamlessly in safe area, matching the website hero 1:1.
    """
    W, H = 2560, 1440
    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    # 1. Seamless background gradient across full 2560x1440
    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_dot_grid(draw, W, H, step=30)

    # Safe Area Bounds: Y: 520 to 920 (Height = 400px), X: 540 to 2020 (Width = 1480px)
    SAFE_TOP = 520
    SAFE_BOT = 920
    SAFE_LEFT = 540
    SAFE_RIGHT = 2020

    # Right Card inside Safe Area
    card_w = 340
    card_h = SAFE_BOT - SAFE_TOP # 400
    card_x = SAFE_RIGHT - card_w # 1680
    card_y = SAFE_TOP

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=24,
        fill=BG_CARD,
        outline=BORDER_CARD,
        width=1
    )

    photo_w = card_w - 24 # 316
    photo_h = 236
    photo_x = card_x + 12
    photo_y = card_y + 12

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (photo_w, photo_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_w - 1, photo_h - 1], radius=18, fill=255)
        banner.paste(ceo_r, (photo_x, photo_y), pmask)

        # Name tag overlay
        f_name = ImageFont.truetype(FONT_BD, 14)
        tag_w = photo_w - 40
        tag_h = 28
        tag_x = photo_x + 20
        tag_y = photo_y + photo_h - 34
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=12, fill=(11, 18, 35))
        draw.text((tag_x + 36, tag_y + 5), "대표 공인중개사 황선숙", font=f_name, fill=WHITE)

    # Text under photo
    f_addr = ImageFont.truetype(FONT_REG, 13)
    f_stat = ImageFont.truetype(FONT_REG, 12)
    draw.text((card_x + 36, photo_y + photo_h + 12), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_addr, fill=SLATE_300)
    draw.text((card_x + 28, photo_y + photo_h + 32), "2017년 2월 개업 이래 충무공동 한 자리 (통계학 석사)", font=f_stat, fill=GOLD_MAIN)

    # Royal Blue Call Button
    btn_w = card_w - 28
    btn_h = 44
    btn_x = card_x + 14
    btn_y = card_y + card_h - btn_h - 14
    for by in range(btn_h):
        bf = by / btn_h
        br = int(BLUE_BTN_TOP[0] * (1 - bf) + BLUE_BTN_BOT[0] * bf)
        bg = int(BLUE_BTN_TOP[1] * (1 - bf) + BLUE_BTN_BOT[1] * bf)
        bb = int(BLUE_BTN_TOP[2] * (1 - bf) + BLUE_BTN_BOT[2] * bf)
        draw.line([(btn_x, btn_y + by), (btn_x + btn_w, btn_y + by)], fill=(br, bg, bb))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=14, outline=BLUE_BTN_BORDER, width=1)
    
    draw_phone_icon(draw, btn_x + 44, btn_y + 14, size=15, color=GOLD_MAIN)
    f_btn = ImageFont.truetype(FONT_BD, 14)
    draw.text((btn_x + 68, btn_y + 12), "010-4670-7248 직접 상담", font=f_btn, fill=WHITE)

    # Left side inside Safe Area
    lx = SAFE_LEFT

    # 1. Badges
    f_pill = ImageFont.truetype(FONT_BD, 13)
    pill1_text = "통계학 석사의 정밀 데이터 분석 · 2017년부터 충무공동 한 자리"
    pill2_text = "등록 48170-2017-00038"

    bbox1 = f_pill.getbbox(pill1_text)
    pw1 = (bbox1[2] - bbox1[0]) + 32
    draw.rounded_rectangle([lx, SAFE_TOP, lx + pw1, SAFE_TOP + 28], radius=14, fill=MINT_BG, outline=MINT_BORDER, width=1)
    draw_green_dot(draw, lx + 14, SAFE_TOP + 14, r=4, color=MINT_TEXT)
    draw.text((lx + 26, SAFE_TOP + 5), pill1_text, font=f_pill, fill=MINT_TEXT)

    lx2 = lx + pw1 + 10
    bbox2 = f_pill.getbbox(pill2_text)
    pw2 = (bbox2[2] - bbox2[0]) + 32
    draw.rounded_rectangle([lx2, SAFE_TOP, lx2 + pw2, SAFE_TOP + 28], radius=14, fill=AMBER_PILL_BG, outline=AMBER_PILL_BORDER, width=1)
    draw_shield_icon(draw, lx2 + 12, SAFE_TOP + 6, size=15, color=AMBER_PILL_TEXT)
    draw.text((lx2 + 32, SAFE_TOP + 5), pill2_text, font=f_pill, fill=AMBER_PILL_TEXT)

    # 2. Main Headline
    f_h1 = ImageFont.truetype(FONT_BD, 36)
    h_y = SAFE_TOP + 46
    draw.text((lx, h_y), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=GOLD_MAIN)
    draw.text((lx, h_y + 48), "2017년부터 충무공동 한 자리를 지켜온", font=f_h1, fill=WHITE)

    draw.text((lx, h_y + 96), "진주퀸공인중개사", font=f_h1, fill=GOLD_MAIN)
    bbox_brand = f_h1.getbbox("진주퀸공인중개사")
    bw_brand = bbox_brand[2] - bbox_brand[0]
    draw.line([(lx, h_y + 142), (lx + bw_brand, h_y + 142)], fill=GOLD_LINE, width=4)
    draw.text((lx + bw_brand + 4, h_y + 96), "입니다.", font=f_h1, fill=WHITE)

    # 3. Summary
    f_sub = ImageFont.truetype(FONT_REG, 16)
    s_y = h_y + 158
    draw.text((lx, s_y), "실거래가 빅데이터와 정밀 권리분석을 바탕으로,", font=f_sub, fill=SLATE_300)
    draw.text((lx, s_y + 26), "100% 현장 검증 실매물로 고객님의 소중한 자산을 안전하게 중개합니다.", font=f_sub, fill=SLATE_300)

    # 4. Highlight Cards (c_w = 330, gap = 20 -> total 1030px)
    c_y = SAFE_BOT - 74
    c_w = 330
    c_gap = 20
    f_ctitle = ImageFont.truetype(FONT_BD, 16)
    f_csub = ImageFont.truetype(FONT_REG, 13)

    cards = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "2017년부터 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (ct, cs) in enumerate(cards):
        cx = lx + i * (c_w + c_gap)
        draw.rounded_rectangle([cx, c_y, cx + c_w, c_y + 74], radius=16, fill=BG_CARD, outline=BORDER_CARD, width=1)
        bt = f_ctitle.getbbox(ct)
        tw = bt[2] - bt[0]
        draw.text((cx + (c_w - tw) // 2, c_y + 14), ct, font=f_ctitle, fill=GOLD_MAIN)

        bs = f_csub.getbbox(cs)
        sw = bs[2] - bs[0]
        draw.text((cx + (c_w - sw) // 2, c_y + 42), cs, font=f_csub, fill=SLATE_400)

    out_art = os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg")
    out_img = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    out_desk = os.path.join(DESKTOP_DIR, "진주퀸_유튜브채널아트_2560x1440.jpg")

    banner.save(out_art, quality=95)
    banner.save(out_img, quality=95)
    banner.save(out_desk, quality=95)
    print("Saved YouTube Channel Banner:", out_art)
    return out_art


def create_naver_blog_banner_500():
    """
    Naver Blog Title Banner (966 x 500) - Slightly taller option for spacious blog header
    """
    W, H = 966, 500
    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_dot_grid(draw, W, H, step=22)

    Y_TOP = 55
    Y_BOT = 445

    card_w = 260
    card_h = Y_BOT - Y_TOP  # 390
    card_x = W - card_w - 42
    card_y = Y_TOP

    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=22, fill=BG_CARD, outline=BORDER_CARD, width=1)

    photo_w = card_w - 20
    photo_h = 236
    photo_x = card_x + 10
    photo_y = card_y + 10

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (photo_w, photo_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_w - 1, photo_h - 1], radius=18, fill=255)
        banner.paste(ceo_r, (photo_x, photo_y), pmask)

        f_name = ImageFont.truetype(FONT_BD, 13)
        tag_w = photo_w - 36
        tag_h = 26
        tag_x = photo_x + 18
        tag_y = photo_y + photo_h - 32
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=11, fill=(11, 18, 35))
        draw.text((tag_x + 28, tag_y + 5), "대표 공인중개사 황선숙", font=f_name, fill=WHITE)

    f_addr = ImageFont.truetype(FONT_REG, 11)
    f_stat = ImageFont.truetype(FONT_REG, 10.5)
    draw.text((card_x + 30, photo_y + photo_h + 12), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_addr, fill=SLATE_300)
    draw.text((card_x + 22, photo_y + photo_h + 28), "2017년 2월 개업 이래 충무공동 한 자리 (통계학 석사)", font=f_stat, fill=GOLD_MAIN)

    btn_w = card_w - 24
    btn_h = 38
    btn_x = card_x + 12
    btn_y = card_y + card_h - btn_h - 14
    for by in range(btn_h):
        bf = by / btn_h
        br = int(BLUE_BTN_TOP[0] * (1 - bf) + BLUE_BTN_BOT[0] * bf)
        bg = int(BLUE_BTN_TOP[1] * (1 - bf) + BLUE_BTN_BOT[1] * bf)
        bb = int(BLUE_BTN_TOP[2] * (1 - bf) + BLUE_BTN_BOT[2] * bf)
        draw.line([(btn_x, btn_y + by), (btn_x + btn_w, btn_y + by)], fill=(br, bg, bb))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=12, outline=BLUE_BTN_BORDER, width=1)
    
    draw_phone_icon(draw, btn_x + 34, btn_y + 12, size=14, color=GOLD_MAIN)
    f_btn = ImageFont.truetype(FONT_BD, 12.5)
    draw.text((btn_x + 56, btn_y + 10), "010-4670-7248 직접 상담", font=f_btn, fill=WHITE)

    # Left content
    lx = 42

    f_pill = ImageFont.truetype(FONT_BD, 11.5)
    pill1_text = "통계학 석사의 정밀 데이터 분석 · 2017년부터 충무공동 한 자리"
    pill2_text = "등록 48170-2017-00038"

    bbox1 = f_pill.getbbox(pill1_text)
    pw1 = (bbox1[2] - bbox1[0]) + 30
    draw.rounded_rectangle([lx, Y_TOP, lx + pw1, Y_TOP + 26], radius=13, fill=MINT_BG, outline=MINT_BORDER, width=1)
    draw_green_dot(draw, lx + 12, Y_TOP + 13, r=3.5, color=MINT_TEXT)
    draw.text((lx + 22, Y_TOP + 5), pill1_text, font=f_pill, fill=MINT_TEXT)

    lx2 = lx + pw1 + 8
    bbox2 = f_pill.getbbox(pill2_text)
    pw2 = (bbox2[2] - bbox2[0]) + 30
    draw.rounded_rectangle([lx2, Y_TOP, lx2 + pw2, Y_TOP + 26], radius=13, fill=AMBER_PILL_BG, outline=AMBER_PILL_BORDER, width=1)
    draw_shield_icon(draw, lx2 + 10, Y_TOP + 6, size=13, color=AMBER_PILL_TEXT)
    draw.text((lx2 + 27, Y_TOP + 5), pill2_text, font=f_pill, fill=AMBER_PILL_TEXT)

    f_h1 = ImageFont.truetype(FONT_BD, 29)
    h_y = Y_TOP + 46
    draw.text((lx, h_y), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=GOLD_MAIN)
    draw.text((lx, h_y + 40), "2017년부터 충무공동 한 자리를 지켜온", font=f_h1, fill=WHITE)

    draw.text((lx, h_y + 80), "진주퀸공인중개사", font=f_h1, fill=GOLD_MAIN)
    bbox_brand = f_h1.getbbox("진주퀸공인중개사")
    bw_brand = bbox_brand[2] - bbox_brand[0]
    draw.line([(lx, h_y + 118), (lx + bw_brand, h_y + 118)], fill=GOLD_LINE, width=3)
    draw.text((lx + bw_brand + 2, h_y + 80), "입니다.", font=f_h1, fill=WHITE)

    f_sub = ImageFont.truetype(FONT_REG, 13.5)
    s_y = h_y + 134
    draw.text((lx, s_y), "실거래가 빅데이터와 정밀 권리분석을 바탕으로,", font=f_sub, fill=SLATE_300)
    draw.text((lx, s_y + 22), "100% 현장 검증 실매물로 고객님의 소중한 자산을 안전하게 중개합니다.", font=f_sub, fill=SLATE_300)

    c_y = Y_BOT - 64
    c_w = 188
    c_gap = 14
    f_ctitle = ImageFont.truetype(FONT_BD, 13.5)
    f_csub = ImageFont.truetype(FONT_REG, 11)

    cards = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "2017년부터 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (ct, cs) in enumerate(cards):
        cx = lx + i * (c_w + c_gap)
        draw.rounded_rectangle([cx, c_y, cx + c_w, c_y + 64], radius=14, fill=BG_CARD, outline=BORDER_CARD, width=1)
        bt = f_ctitle.getbbox(ct)
        tw = bt[2] - bt[0]
        draw.text((cx + (c_w - tw) // 2, c_y + 12), ct, font=f_ctitle, fill=GOLD_MAIN)

        bs = f_csub.getbbox(cs)
        sw = bs[2] - bs[0]
        draw.text((cx + (c_w - sw) // 2, c_y + 35), cs, font=f_csub, fill=SLATE_400)

    out_art = os.path.join(ARTIFACT_DIR, "naver-blog-title-966x500.jpg")
    out_img = os.path.join(IMAGES_DIR, "naver-blog-title-966x500.jpg")
    out_desk = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_966x500.jpg")

    banner.save(out_art, quality=95)
    banner.save(out_img, quality=95)
    banner.save(out_desk, quality=95)
    print("Saved Naver Blog Banner 500px:", out_art)
    return out_art


def create_naver_blog_wide_skin():
    """
    Naver Blog Wide Skin Banner (1920 x 500)
    Full HD Skin background for modern wide blogs, centered 966px area.
    """
    W, H = 1920, 500
    banner = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(banner)

    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_dot_grid(draw, W, H, step=26)

    # Center 966x500 area
    center_banner = Image.open(os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg"))
    # Resize or paste in center
    cx = (W - 966) // 2
    cy = (H - 450) // 2
    banner.paste(center_banner, (cx, cy))

    out_art = os.path.join(ARTIFACT_DIR, "naver-blog-skin.jpg")
    out_img = os.path.join(IMAGES_DIR, "naver-blog-skin.jpg")
    out_desk = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그와이드스킨_1920x500.jpg")

    banner.save(out_art, quality=95)
    banner.save(out_img, quality=95)
    banner.save(out_desk, quality=95)
    print("Saved Naver Blog Wide Skin:", out_art)
    return out_art


if __name__ == '__main__':
    create_naver_blog_banner_exact()
    create_naver_blog_banner_500()
    create_youtube_channel_banner_exact()
    create_naver_blog_wide_skin()
