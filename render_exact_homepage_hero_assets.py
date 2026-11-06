import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Colors matching the Website Hero Section (#hero in index.html)
BG_TOP = (11, 19, 43)            # #0B132B
BG_BOT = (22, 33, 58)            # Slate 900 gradient
GOLD_ACCENT = (194, 155, 56)      # #C29B38 (brand gold)
GOLD_TEXT = (251, 191, 36)        # Amber 400
GOLD_LIGHT = (253, 230, 138)      # Amber 200
WHITE = (255, 255, 255)
SLATE_300 = (203, 213, 225)
SLATE_400 = (148, 163, 184)
SLATE_500 = (100, 116, 139)
EMERALD_DOT = (52, 211, 153)

def draw_dot_grid(draw, w, h, spacing=24):
    """Subtle architectural dot texture matching index.html #hero"""
    for x in range(12, w, spacing):
        for y in range(12, h, spacing):
            draw.point((x, y), fill=(35, 50, 80))

def generate_exact_hero_naver_blog_title():
    """
    Naver Blog Title Banner (966 x 500)
    100% FAITHFUL recreation of index.html #hero screenshot (media_1793948263823_7adfd87e.jpg):
    - Left:
        * Badge 1: 통계학 석사의 정밀 데이터 분석 · 충무공동 한 자리
        * Badge 2: 등록 48170-2017-00038
        * H1: 통계학 석사의 정밀 데이터 분석, / 충무공동 한 자리를 지켜온 신뢰 진주퀸공인중개사입니다.
        * Body paragraph: 2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리를 지켜온...
        * 3 Metric Cards: [통계학 석사 / 정밀 데이터 분석] [충무공동 한 자리 / 한 자리 우직한 신뢰] [100% 실매물 / 현장 검증 책임 중개]
    - Right:
        * Showcase Card (dark rounded card with gold border)
        * Photo of Hwang Sun-sook in gold-bordered rounded frame
        * Name tag: 대표 공인중개사 황선숙
        * Sub: 진주시 에나로 146, 105호 (라온프라이빗시티)
        * Sub: 2017년 2월 개업 이래 충무공동 한 자리 (통계학 석사)
        * Yellow button: 📞 010-4670-7248 직접 상담
    """
    bw, bh = 966, 500
    banner = Image.new('RGB', (bw, bh), BG_TOP)
    draw = ImageDraw.Draw(banner)

    # Gradient background
    for y in range(bh):
        factor = y / bh
        r = int(BG_TOP[0] * (1 - factor) + BG_BOT[0] * factor)
        g = int(BG_TOP[1] * (1 - factor) + BG_BOT[1] * factor)
        b = int(BG_TOP[2] * (1 - factor) + BG_BOT[2] * factor)
        draw.line([(0, y), (bw, y)], fill=(r, g, b))

    # Dot grid
    draw_dot_grid(draw, bw, bh)

    # Gold borders top and bottom
    draw.line([(0, 2), (bw, 2)], fill=GOLD_ACCENT, width=3)
    draw.line([(0, bh - 3), (bw, bh - 3)], fill=GOLD_ACCENT, width=3)

    # Right Showcase Card (width 265, height 420)
    card_w, card_h = 265, 420
    card_x = bw - card_w - 40
    card_y = 40

    # Draw card shadow & card body
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=24,
        fill=(15, 23, 42),
        outline=(194, 155, 56),
        width=1
    )

    # Inner Photo inside Showcase Card
    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    photo_s = card_w - 36 # 229px square
    photo_x = card_x + 18
    photo_y = card_y + 18

    draw.rounded_rectangle(
        [photo_x - 2, photo_y - 2, photo_x + photo_s + 2, photo_y + photo_s + 2],
        radius=18,
        fill=None,
        outline=(194, 155, 56),
        width=2
    )

    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((photo_s, photo_s), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (photo_s, photo_s), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_s - 1, photo_s - 1], radius=16, fill=255)
        banner.paste(ceo_r, (photo_x, photo_y), pmask)

        # Name tag overlay at bottom of photo
        f_tag = ImageFont.truetype(FONT_BD, 13)
        tag_w = photo_s - 24
        tag_h = 28
        tag_x = photo_x + 12
        tag_y = photo_y + photo_s - 34
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10, fill=(11, 19, 43))
        draw.text((tag_x + 18, tag_y + 5), "대표 공인중개사 황선숙", font=f_tag, fill=GOLD_LIGHT)

    # Info below photo inside card
    f_csub1 = ImageFont.truetype(FONT_REG, 11)
    f_csub2 = ImageFont.truetype(FONT_BD, 11)
    f_cbtn = ImageFont.truetype(FONT_BD, 13)

    draw.text((card_x + 22, card_y + photo_s + 32), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_csub1, fill=SLATE_300)
    draw.text((card_x + 16, card_y + photo_s + 50), "2017년 2월 개업 · 충무공동 한 자리 (통계학 석사)", font=f_csub2, fill=GOLD_TEXT)

    # Yellow Gold Pill Button inside card
    btn_y = card_y + photo_s + 74
    draw.rounded_rectangle([card_x + 18, btn_y, card_x + card_w - 18, btn_y + 38], radius=19, fill=GOLD_ACCENT)
    draw.text((card_x + 40, btn_y + 10), "📞 010-4670-7248 직접 상담", font=f_cbtn, fill=(15, 23, 42))

    # Left Content Section
    lx = 42
    ly = 40

    # 1. Top Badges
    f_badge1 = ImageFont.truetype(FONT_BD, 12)
    f_badge2 = ImageFont.truetype(FONT_BD, 12)

    # Badge 1: 통계학 석사의 정밀 데이터 분석 · 충무공동 한 자리 (with green dot)
    b1_w = 320
    draw.rounded_rectangle([lx, ly, lx + b1_w, ly + 28], radius=14, fill=(255, 255, 255, 25), outline=(255, 255, 255, 40), width=1)
    draw.ellipse([lx + 12, ly + 10, lx + 18, ly + 16], fill=EMERALD_DOT)
    draw.text((lx + 26, ly + 5), "통계학 석사의 정밀 데이터 분석 · 충무공동 한 자리", font=f_badge1, fill=GOLD_LIGHT)

    # Badge 2: 등록 48170-2017-00038
    bx2 = lx + b1_w + 10
    b2_w = 165
    draw.rounded_rectangle([bx2, ly, bx2 + b2_w, ly + 28], radius=14, fill=(50, 25, 10), outline=GOLD_ACCENT, width=1)
    draw.text((bx2 + 14, ly + 5), "🛡️ 등록 48170-2017-00038", font=f_badge2, fill=GOLD_LIGHT)

    # 2. Main H1 Headline (Exact 2 lines)
    f_h1 = ImageFont.truetype(FONT_BD, 28)
    f_h2_pre = ImageFont.truetype(FONT_BD, 26)
    f_h2_name = ImageFont.truetype(FONT_BD, 28)

    ly += 42
    draw.text((lx, ly), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)
    ly += 38
    draw.text((lx, ly), "충무공동 한 자리를 지켜온 신뢰 ", font=f_h2_pre, fill=WHITE)
    w_pre = f_h2_pre.getbbox("충무공동 한 자리를 지켜온 신뢰 ")[2]
    draw.text((lx + w_pre, ly - 2), "진주퀸공인중개사", font=f_h2_name, fill=GOLD_TEXT)
    w_name = f_h2_name.getbbox("진주퀸공인중개사")[2]
    draw.text((lx + w_pre + w_name + 4, ly), "입니다.", font=f_h2_pre, fill=WHITE)

    # 3. Body Paragraph (3 lines, exact text)
    f_body = ImageFont.truetype(FONT_REG, 13)
    ly += 44
    draw.text((lx, ly), "2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리를 지켜온", font=f_body, fill=SLATE_300)
    ly += 20
    draw.text((lx, ly), "통계학 석사 황선숙 대표가 실거래가 빅데이터 분석과 정밀 권리분석,", font=f_body, fill=SLATE_300)
    ly += 20
    draw.text((lx, ly), "100% 현장 검증 실매물로 고객님의 소중한 자산을 안전하게 중개합니다.", font=f_body, fill=SLATE_300)

    # 4. 3 Metric Cards Grid (Bottom)
    ly += 36
    card_block_w = 180
    card_gap = 12
    card_block_h = 72
    f_mtop = ImageFont.truetype(FONT_BD, 16)
    f_mbot = ImageFont.truetype(FONT_REG, 11)

    cards = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "한 자리 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (mtop, mbot) in enumerate(cards):
        cx = lx + i * (card_block_w + card_gap)
        draw.rounded_rectangle(
            [cx, ly, cx + card_block_w, ly + card_block_h],
            radius=14,
            fill=(255, 255, 255, 14),
            outline=(255, 255, 255, 28),
            width=1
        )
        # Center text horizontally in each card
        bbox_top = f_mtop.getbbox(mtop)
        tw = bbox_top[2] - bbox_top[0]
        draw.text((cx + (card_block_w - tw) // 2, ly + 14), mtop, font=f_mtop, fill=GOLD_TEXT)

        bbox_bot = f_mbot.getbbox(mbot)
        bw_t = bbox_bot[2] - bbox_bot[0]
        draw.text((cx + (card_block_w - bw_t) // 2, ly + 40), mbot, font=f_mbot, fill=SLATE_300)

    # 5. Office info footer line
    ly += card_block_h + 14
    f_subline = ImageFont.truetype(FONT_REG, 12)
    draw.text((lx, ly), "사무실 : 055-761-7248  |  jinjuqueen.vercel.app  (모바일 & PC)", font=f_subline, fill=SLATE_400)

    # Save outputs
    out_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_타이틀배너.jpg"), "JPEG", quality=98)
    print("Exact Hero Naver Blog Title generated!")


def generate_exact_hero_youtube_banner():
    """
    YouTube Channel Art (2560 x 1440)
    100% FAITHFUL recreation of index.html #hero screenshot across YouTube canvas & safe area
    """
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    # Entire canvas has seamless rich navy ambient tone with subtle dot grid
    banner = Image.new('RGB', (W, H), BG_TOP)
    draw = ImageDraw.Draw(banner)

    for y in range(H):
        factor = y / H
        r = int(BG_TOP[0] * (1 - factor * 0.4) + BG_BOT[0] * (factor * 0.4))
        g = int(BG_TOP[1] * (1 - factor * 0.4) + BG_BOT[1] * (factor * 0.4))
        b = int(BG_TOP[2] * (1 - factor * 0.4) + BG_BOT[2] * (factor * 0.4))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_dot_grid(draw, W, H, spacing=28)

    # Gold hairline accents for YouTube safe zone
    draw.line([(safe_x1 + 20, safe_y1 + 8), (safe_x2 - 20, safe_y1 + 8)], fill=GOLD_ACCENT, width=2)
    draw.line([(safe_x1 + 20, safe_y2 - 8), (safe_x2 - 20, safe_y2 - 8)], fill=GOLD_ACCENT, width=2)

    # Right Showcase Card inside safe zone
    card_w, card_h = 280, 395
    card_x = safe_x2 - card_w - 40
    card_y = safe_y1 + (safe_h - card_h) // 2

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=24,
        fill=(15, 23, 42),
        outline=GOLD_ACCENT,
        width=1
    )

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    photo_s = card_w - 36 # 244px
    photo_x = card_x + 18
    photo_y = card_y + 16

    draw.rounded_rectangle(
        [photo_x - 2, photo_y - 2, photo_x + photo_s + 2, photo_y + photo_s + 2],
        radius=18,
        fill=None,
        outline=GOLD_ACCENT,
        width=2
    )

    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        ceo_r = ceo_im.resize((photo_s, photo_s), Image.Resampling.LANCZOS)
        pmask = Image.new('L', (photo_s, photo_s), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_s - 1, photo_s - 1], radius=16, fill=255)
        banner.paste(ceo_r, (photo_x, photo_y), pmask)

        # Name tag overlay at bottom of photo
        f_tag = ImageFont.truetype(FONT_BD, 14)
        tag_w = photo_s - 24
        tag_h = 30
        tag_x = photo_x + 12
        tag_y = photo_y + photo_s - 36
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=11, fill=(11, 19, 43))
        draw.text((tag_x + 22, tag_y + 5), "대표 공인중개사 황선숙", font=f_tag, fill=GOLD_LIGHT)

    # Info below photo inside card
    f_csub1 = ImageFont.truetype(FONT_REG, 11)
    f_csub2 = ImageFont.truetype(FONT_BD, 11)
    f_cbtn = ImageFont.truetype(FONT_BD, 14)

    draw.text((card_x + 26, card_y + photo_s + 26), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=f_csub1, fill=SLATE_300)
    draw.text((card_x + 20, card_y + photo_s + 44), "2017년 2월 개업 · 충무공동 한 자리 (통계학 석사)", font=f_csub2, fill=GOLD_TEXT)

    # Yellow Gold Pill Button inside card
    btn_y = card_y + photo_s + 66
    draw.rounded_rectangle([card_x + 18, btn_y, card_x + card_w - 18, btn_y + 40], radius=20, fill=GOLD_ACCENT)
    draw.text((card_x + 44, btn_y + 10), "📞 010-4670-7248 직접 상담", font=f_cbtn, fill=(15, 23, 42))

    # Left Section Content inside Safe Area
    lx = safe_x1 + 45
    ly = safe_y1 + 22

    # 1. Top Badges
    f_badge1 = ImageFont.truetype(FONT_BD, 15)
    f_badge2 = ImageFont.truetype(FONT_BD, 14)

    b1_w = 380
    draw.rounded_rectangle([lx, ly, lx + b1_w, ly + 32], radius=16, fill=(255, 255, 255, 25), outline=(255, 255, 255, 40), width=1)
    draw.ellipse([lx + 14, ly + 12, lx + 22, ly + 20], fill=EMERALD_DOT)
    draw.text((lx + 30, ly + 6), "통계학 석사의 정밀 데이터 분석 · 충무공동 한 자리", font=f_badge1, fill=GOLD_LIGHT)

    bx2 = lx + b1_w + 14
    b2_w = 195
    draw.rounded_rectangle([bx2, ly, bx2 + b2_w, ly + 32], radius=16, fill=(50, 25, 10), outline=GOLD_ACCENT, width=1)
    draw.text((bx2 + 16, ly + 6), "🛡️ 등록 48170-2017-00038", font=f_badge2, fill=GOLD_LIGHT)

    # 2. Main H1 Headline
    f_h1 = ImageFont.truetype(FONT_BD, 38)
    f_h2_pre = ImageFont.truetype(FONT_BD, 34)
    f_h2_name = ImageFont.truetype(FONT_BD, 36)

    ly += 46
    draw.text((lx, ly), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=WHITE)
    ly += 48
    draw.text((lx, ly), "충무공동 한 자리를 지켜온 신뢰 ", font=f_h2_pre, fill=WHITE)
    w_pre = f_h2_pre.getbbox("충무공동 한 자리를 지켜온 신뢰 ")[2]
    draw.text((lx + w_pre, ly - 2), "진주퀸공인중개사", font=f_h2_name, fill=GOLD_TEXT)
    w_name = f_h2_name.getbbox("진주퀸공인중개사")[2]
    draw.text((lx + w_pre + w_name + 4, ly), "입니다.", font=f_h2_pre, fill=WHITE)

    # 3. Body Paragraph
    f_body = ImageFont.truetype(FONT_REG, 17)
    ly += 54
    draw.text((lx, ly), "2017년 2월 개업 이래 충무공동 라온프라이빗시티 한 자리를 지켜온 통계학 석사 황선숙 대표가", font=f_body, fill=SLATE_300)
    ly += 26
    draw.text((lx, ly), "실거래가 빅데이터 분석과 정밀 권리분석, 100% 현장 검증 실매물로 고객님의 소중한 자산을 안전하게 중개합니다.", font=f_body, fill=SLATE_300)

    # 4. 3 Metric Cards Grid
    ly += 40
    card_block_w = 260
    card_gap = 16
    card_block_h = 80
    f_mtop = ImageFont.truetype(FONT_BD, 20)
    f_mbot = ImageFont.truetype(FONT_REG, 14)

    cards = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "한 자리 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (mtop, mbot) in enumerate(cards):
        cx = lx + i * (card_block_w + card_gap)
        draw.rounded_rectangle(
            [cx, ly, cx + card_block_w, ly + card_block_h],
            radius=16,
            fill=(255, 255, 255, 14),
            outline=(255, 255, 255, 28),
            width=1
        )
        bbox_top = f_mtop.getbbox(mtop)
        tw = bbox_top[2] - bbox_top[0]
        draw.text((cx + (card_block_w - tw) // 2, ly + 14), mtop, font=f_mtop, fill=GOLD_TEXT)

        bbox_bot = f_mbot.getbbox(mbot)
        bw_t = bbox_bot[2] - bbox_bot[0]
        draw.text((cx + (card_block_w - bw_t) // 2, ly + 44), mbot, font=f_mbot, fill=SLATE_300)

    # Save outputs
    out_path = os.path.join(IMAGES_DIR, "youtube-channel-banner-2560.jpg")
    banner.save(out_path, "JPEG", quality=98)
    banner.save(os.path.join(ARTIFACT_DIR, "youtube-channel-banner-2560.jpg"), "JPEG", quality=98)
    banner.save(os.path.join(DESKTOP_DIR, "진주퀸_유튜브_채널아트배너.jpg"), "JPEG", quality=98)
    print("Exact Hero YouTube Channel Banner generated!")


def generate_exact_hero_naver_blog_skin():
    """Naver Blog Wide Top Skin (2000 x 800) with title centered"""
    sw, sh = 2000, 800
    skin = Image.new('RGB', (sw, sh), BG_TOP)
    draw = ImageDraw.Draw(skin)

    for y in range(sh):
        factor = y / sh
        r = int(BG_TOP[0] * (1 - factor * 0.35) + BG_BOT[0] * (factor * 0.35))
        g = int(BG_TOP[1] * (1 - factor * 0.35) + BG_BOT[1] * (factor * 0.35))
        b = int(BG_TOP[2] * (1 - factor * 0.35) + BG_BOT[2] * (factor * 0.35))
        draw.line([(0, y), (sw, y)], fill=(r, g, b))

    draw_dot_grid(draw, sw, sh, spacing=24)
    draw.line([(0, 2), (sw, 2)], fill=GOLD_ACCENT, width=4)

    title_path = os.path.join(IMAGES_DIR, "naver-blog-title-966.jpg")
    if os.path.exists(title_path):
        t_im = Image.open(title_path)
        tx = (sw - t_im.width) // 2
        ty = 80
        skin.paste(t_im, (tx, ty))

    skin.save(os.path.join(IMAGES_DIR, "naver-blog-skin.jpg"), "JPEG", quality=98)
    print("Exact Hero Naver Blog Wide Skin generated!")


if __name__ == '__main__':
    generate_exact_hero_naver_blog_title()
    generate_exact_hero_youtube_banner()
    generate_exact_hero_naver_blog_skin()
