import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Colors matching the Website Hero Section
NAVY_DEEP = (11, 19, 43)        # #0B132B
NAVY_CARD = (18, 28, 54)
GOLD_RICH = (194, 155, 56)       # #C29B38
GOLD_LIGHT = (245, 218, 128)
WHITE = (255, 255, 255)
SLATE_LIGHT = (203, 213, 225)
SLATE_MUTED = (148, 163, 184)
EMERALD = (16, 185, 129)

def generate_naver_blog_title():
    """
    Naver Blog Title Banner (966 x 500)
    100% identically matching the website hero section:
    - 통계학 석사의 정밀 데이터 분석 · 충무공동 9년차
    - 통계학 석사의 정밀 데이터 분석, 충무공동 9년의 신뢰 진주퀸공인중개사입니다.
    - 2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리...
    - 3 Trust Cards: 통계학 석사 / 충무공동 9년차 / 100% 실매물
    """
    bw, bh = 966, 500
    banner = Image.new('RGB', (bw, bh), NAVY_DEEP)
    draw = ImageDraw.Draw(banner)

    # Ambient subtle background gradient
    for y in range(bh):
        blend = y / bh
        r = int(11 * (1 - blend * 0.25) + 18 * (blend * 0.25))
        g = int(19 * (1 - blend * 0.25) + 28 * (blend * 0.25))
        b = int(43 * (1 - blend * 0.25) + 60 * (blend * 0.25))
        draw.line([(0, y), (bw, y)], fill=(r, g, b))

    # Gold top & bottom accent borders
    draw.line([(0, 2), (bw, 2)], fill=GOLD_RICH, width=4)
    draw.line([(0, bh - 3), (bw, bh - 3)], fill=GOLD_RICH, width=4)

    # Right Card: CEO Photo Card (like the website hero right card!)
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    card_w, card_h = 280, 430
    card_x = bw - card_w - 28
    card_y = 35

    # Card background with border
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=20,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=2
    )

    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        # Photo size inside card
        pw, ph = card_w - 24, 255
        ceo_resized = ceo_im.resize((pw, ph), Image.Resampling.LANCZOS)
        
        # Rounded mask for photo
        pmask = Image.new('L', (pw, ph), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=14, fill=255)
        
        banner.paste(ceo_resized, (card_x + 12, card_y + 12), pmask)

        # Name banner below photo
        f_name = ImageFont.truetype(FONT_BD, 15)
        draw.rounded_rectangle(
            [card_x + 25, card_y + ph - 2, card_x + card_w - 25, card_y + ph + 28],
            radius=14,
            fill=(11, 19, 43),
            outline=GOLD_RICH,
            width=1
        )
        draw.text((card_x + 58, card_y + ph + 4), "대표 공인중개사 황선숙", font=f_name, fill=GOLD_LIGHT)

    # Info below photo inside card
    f_card_sub1 = ImageFont.truetype(FONT_REG, 12)
    f_card_sub2 = ImageFont.truetype(FONT_BD, 12)
    f_card_btn = ImageFont.truetype(FONT_BD, 14)

    draw.text((card_x + 26, card_y + 302), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_card_sub1, fill=SLATE_MUTED)
    draw.text((card_x + 20, card_y + 324), "2017년 2월 개업 · 충무공동 9년차 (통계학 석사)", font=f_card_sub2, fill=GOLD_LIGHT)

    # Yellow CTA Button inside card
    btn_y = card_y + 355
    draw.rounded_rectangle(
        [card_x + 20, btn_y, card_x + card_w - 20, btn_y + 44],
        radius=22,
        fill=GOLD_RICH
    )
    draw.text((card_x + 44, btn_y + 11), "📞 010-4670-7248 직접 상담", font=f_card_btn, fill=(15, 23, 42))

    # Left Section Content (Exact text from screenshot)
    lx = 36
    ly = 32

    # Top Badges
    f_badge = ImageFont.truetype(FONT_BD, 13)
    f_reg = ImageFont.truetype(FONT_BD, 12)

    # Badge 1: 통계학 석사의 정밀 데이터 분석 · 충무공동 9년차
    draw.rounded_rectangle([lx, ly, lx + 270, ly + 28], radius=14, fill=(255, 255, 255, 25), outline=(255, 255, 255, 50), width=1)
    draw.text((lx + 12, ly + 4), "통계학 석사의 정밀 데이터 분석 · 충무공동 9년차", font=f_badge, fill=GOLD_LIGHT)

    # Badge 2: 등록 48170-2017-00038
    bx2 = lx + 282
    draw.rounded_rectangle([bx2, ly, bx2 + 155, ly + 28], radius=14, fill=(35, 20, 10), outline=GOLD_RICH, width=1)
    draw.text((bx2 + 12, ly + 5), "🛡️ 등록 48170-2017-00038", font=f_reg, fill=GOLD_LIGHT)

    # Main Headline (Exact 2 lines from screenshot)
    f_h1 = ImageFont.truetype(FONT_BD, 31)
    f_h2 = ImageFont.truetype(FONT_BD, 28)

    ly += 42
    draw.text((lx, ly), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)
    ly += 42
    draw.text((lx, ly), "충무공동 9년의 신뢰 ", font=f_h2, fill=WHITE)
    bbox_pre = f_h2.getbbox("충무공동 9년의 신뢰 ")
    draw.text((lx + bbox_pre[2], ly), "진주퀸공인중개사", font=f_h2, fill=GOLD_LIGHT)
    bbox_mid = f_h2.getbbox("충무공동 9년의 신뢰 진주퀸공인중개사")
    draw.text((lx + bbox_mid[2], ly), "입니다.", font=f_h2, fill=WHITE)

    # Body Paragraph
    f_body = ImageFont.truetype(FONT_REG, 13)
    ly += 48
    draw.text((lx, ly), "2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리를 지켜온", font=f_body, fill=SLATE_LIGHT)
    ly += 22
    draw.text((lx, ly), "통계학 석사 황선숙 대표가 실거래가 빅데이터 분석과 정밀 권리분석,", font=f_body, fill=SLATE_LIGHT)
    ly += 22
    draw.text((lx, ly), "100% 현장 검증 실매물로 소중한 자산을 안전하게 중개합니다.", font=f_body, fill=SLATE_LIGHT)

    # 3 Trust Cards (Exact matching bottom 3 cards from screenshot!)
    # 1: 통계학 석사 / 정밀 데이터 분석
    # 2: 충무공동 9년차 / 한 자리 우직한 신뢰
    # 3: 100% 실매물 / 현장 검증 책임 중개
    ly += 44
    card_block_w = 180
    card_gap = 14
    f_card_top = ImageFont.truetype(FONT_BD, 16)
    f_card_bot = ImageFont.truetype(FONT_REG, 12)

    cards_data = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 9년차", "한 자리 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (ctop, cbot) in enumerate(cards_data):
        cx = lx + i * (card_block_w + card_gap)
        draw.rounded_rectangle(
            [cx, ly, cx + card_block_w, ly + 68],
            radius=14,
            fill=(18, 28, 54),
            outline=(51, 65, 85),
            width=1
        )
        draw.text((cx + 38, ly + 12), ctop, font=f_card_top, fill=GOLD_LIGHT)
        draw.text((cx + 38, ly + 38), cbot, font=f_card_bot, fill=SLATE_LIGHT)

    # Website link footer line
    draw.text((lx, ly + 82), "공식 홈페이지 : jinjuqueen.vercel.app  |  사무실 : 055-761-7248", font=f_card_bot, fill=SLATE_MUTED)

    out_file = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_file, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    print("Naver Blog Title Banner updated:", out_file)


def generate_youtube_banner():
    """
    YouTube Channel Art (2560 x 1440)
    100% identically matching the website hero section in the safe zone (1546 x 423)
    """
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    YT_BG = (15, 15, 15)
    img = Image.new('RGB', (W, H), YT_BG)
    draw = ImageDraw.Draw(img)

    # Ambient glow inside safe zone
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for x in range(safe_x1 - 150, safe_x2 + 150):
        rel = (x - safe_x1) / safe_w
        factor = 1.0 - abs(rel - 0.5) * 1.8
        factor = max(0.0, min(1.0, factor))
        alpha = int(70 * factor)
        odraw.line([(x, safe_y1 - 60), (x, safe_y2 + 60)], fill=(11, 23, 50, alpha))

    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Gold hairline top & bottom
    draw.line([(safe_x1 + 40, safe_y1 + 10), (safe_x2 - 40, safe_y1 + 10)], fill=GOLD_RICH, width=2)
    draw.line([(safe_x1 + 40, safe_y2 - 10), (safe_x2 - 40, safe_y2 - 10)], fill=GOLD_RICH, width=2)

    # Right Card: CEO Profile Box inside YouTube Safe Area
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    card_w = 320
    card_h = 380
    card_x = safe_x2 - card_w - 40
    card_y = safe_y1 + (safe_h - card_h) // 2

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=20,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=2
    )

    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        pw, ph = card_w - 24, 220
        ceo_resized = ceo_im.resize((pw, ph), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (pw, ph), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=14, fill=255)
        img.paste(ceo_resized, (card_x + 12, card_y + 12), pmask)

        # Name banner
        f_name = ImageFont.truetype(FONT_BD, 15)
        draw.rounded_rectangle(
            [card_x + 30, card_y + ph - 2, card_x + card_w - 30, card_y + ph + 28],
            radius=14,
            fill=(11, 19, 43),
            outline=GOLD_RICH,
            width=1
        )
        draw.text((card_x + 65, card_y + ph + 4), "대표 공인중개사 황선숙", font=f_name, fill=GOLD_LIGHT)

    # Text & Call Button inside Right Card
    f_sub1 = ImageFont.truetype(FONT_REG, 13)
    f_sub2 = ImageFont.truetype(FONT_BD, 13)
    f_btn = ImageFont.truetype(FONT_BD, 16)

    draw.text((card_x + 32, card_y + 265), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_sub1, fill=SLATE_MUTED)
    draw.text((card_x + 28, card_y + 288), "2017년 2월 개업 · 충무공동 9년차 (통계학 석사)", font=f_sub2, fill=GOLD_LIGHT)

    btn_y = card_y + 318
    draw.rounded_rectangle([card_x + 20, btn_y, card_x + card_w - 20, btn_y + 46], radius=23, fill=GOLD_RICH)
    draw.text((card_x + 50, btn_y + 12), "📞 010-4670-7248 직접 상담", font=f_btn, fill=(15, 23, 42))

    # Left Section Content inside YouTube Safe Area
    lx = safe_x1 + 50
    ly = safe_y1 + 35

    # Top Badges
    f_badge = ImageFont.truetype(FONT_BD, 16)
    f_reg = ImageFont.truetype(FONT_BD, 15)

    draw.rounded_rectangle([lx, ly, lx + 330, ly + 34], radius=17, fill=(255, 255, 255, 25), outline=(255, 255, 255, 50), width=1)
    draw.text((lx + 16, ly + 5), "통계학 석사의 정밀 데이터 분석 · 충무공동 9년차", font=f_badge, fill=GOLD_LIGHT)

    bx2 = lx + 345
    draw.rounded_rectangle([bx2, ly, bx2 + 185, ly + 34], radius=17, fill=(35, 20, 10), outline=GOLD_RICH, width=1)
    draw.text((bx2 + 16, ly + 6), "🛡️ 등록 48170-2017-00038", font=f_reg, fill=GOLD_LIGHT)

    # Main Headline
    f_h1 = ImageFont.truetype(FONT_BD, 44)
    f_h2 = ImageFont.truetype(FONT_BD, 38)

    ly += 50
    draw.text((lx, ly), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)
    ly += 58
    draw.text((lx, ly), "충무공동 9년의 신뢰 ", font=f_h2, fill=WHITE)
    bbox_pre = f_h2.getbbox("충무공동 9년의 신뢰 ")
    draw.text((lx + bbox_pre[2], ly), "진주퀸공인중개사", font=f_h2, fill=GOLD_LIGHT)
    bbox_mid = f_h2.getbbox("충무공동 9년의 신뢰 진주퀸공인중개사")
    draw.text((lx + bbox_mid[2], ly), "입니다.", font=f_h2, fill=WHITE)

    # Body Paragraph
    f_body = ImageFont.truetype(FONT_REG, 17)
    ly += 60
    draw.text((lx, ly), "2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리를 지켜온 통계학 석사 황선숙 대표가", font=f_body, fill=SLATE_LIGHT)
    ly += 28
    draw.text((lx, ly), "실거래가 빅데이터 분석과 정밀 권리분석, 100% 현장 검증 실매물로 안전하게 중개합니다.", font=f_body, fill=SLATE_LIGHT)

    # 3 Trust Cards
    ly += 45
    card_w_block = 230
    card_gap = 18
    f_ctop = ImageFont.truetype(FONT_BD, 20)
    f_cbot = ImageFont.truetype(FONT_REG, 15)

    cards_data = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 9년차", "한 자리 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (ctop, cbot) in enumerate(cards_data):
        cx = lx + i * (card_w_block + card_gap)
        draw.rounded_rectangle([cx, ly, cx + card_w_block, ly + 76], radius=16, fill=(18, 28, 54), outline=(51, 65, 85), width=1)
        draw.text((cx + 50, ly + 14), ctop, font=f_ctop, fill=GOLD_LIGHT)
        draw.text((cx + 50, ly + 44), cbot, font=f_cbot, fill=SLATE_LIGHT)

    out_file = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    img.save(out_file, "JPEG", quality=98)
    img.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    print("YouTube Channel Banner updated:", out_file)


def generate_naver_blog_skin():
    """Naver Blog Wide Top Skin (2000 x 800) with the updated title banner centered"""
    sw, sh = 2000, 800
    skin = Image.new('RGB', (sw, sh), NAVY_DEEP)
    draw = ImageDraw.Draw(skin)

    for y in range(sh):
        blend = y / sh
        r = int(11 * (1 - blend * 0.35) + 16 * (blend * 0.35))
        g = int(19 * (1 - blend * 0.35) + 24 * (blend * 0.35))
        b = int(43 * (1 - blend * 0.35) + 52 * (blend * 0.35))
        draw.line([(0, y), (sw, y)], fill=(r, g, b))

    draw.line([(0, 2), (sw, 2)], fill=GOLD_RICH, width=4)

    title_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    if os.path.exists(title_path):
        t_im = Image.open(title_path)
        tx = (sw - t_im.width) // 2
        ty = 80
        skin.paste(t_im, (tx, ty))

    out_file = os.path.join(IMAGES_DIR, "naver-blog-skin.jpg")
    skin.save(out_file, "JPEG", quality=98)
    skin.save(os.path.join(ARTIFACT_DIR, "naver-blog-skin.jpg"), "JPEG", quality=98)
    print("Naver Blog Wide Skin updated:", out_file)


if __name__ == '__main__':
    generate_naver_blog_title()
    generate_youtube_banner()
    generate_naver_blog_skin()
