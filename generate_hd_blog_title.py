import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\63e20e20-51d7-4926-afc4-8ed1c231408e"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Ultra-sharp contrast color scheme
BG_NAVY_TOP = (10, 18, 38)
BG_NAVY_BOT = (6, 12, 26)
BG_CARD = (14, 24, 46)
BORDER_CARD = (36, 54, 92)

GOLD_MAIN = (255, 196, 38)        # Crisp radiant amber gold
GOLD_LINE = (245, 158, 11)
GOLD_LIGHT = (254, 240, 199)

WHITE = (255, 255, 255)
SLATE_BRIGHT = (230, 238, 248)    # Highly legible light slate
SLATE_MUTED = (160, 178, 204)     # Crisp readable secondary

MINT_TEXT = (52, 211, 153)
MINT_BG = (6, 78, 59)
MINT_BORDER = (16, 185, 129)

AMBER_PILL_TEXT = (255, 196, 38)
AMBER_PILL_BG = (69, 26, 3)
AMBER_PILL_BORDER = (217, 119, 6)

BLUE_BTN_TOP = (37, 99, 235)
BLUE_BTN_BOT = (29, 78, 216)
BLUE_BTN_BORDER = (96, 165, 250)


def draw_dot_grid(draw, width, height, step=22):
    for x in range(12, width, step):
        for y in range(12, height, step):
            draw.point((x, y), fill=(26, 42, 72))


def draw_green_dot(draw, cx, cy, r=3.5, color=MINT_TEXT):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def draw_shield_icon(draw, x, y, size=13, color=AMBER_PILL_TEXT):
    pts = [
        (x + size * 0.5, y),
        (x + size, y + size * 0.22),
        (x + size * 0.85, y + size * 0.72),
        (x + size * 0.5, y + size),
        (x + size * 0.15, y + size * 0.72),
        (x, y + size * 0.22)
    ]
    draw.polygon(pts, fill=None, outline=color)
    draw.line([(x + size * 0.3, y + size * 0.5), (x + size * 0.48, y + size * 0.68)], fill=color, width=2)
    draw.line([(x + size * 0.48, y + size * 0.68), (x + size * 0.75, y + size * 0.32)], fill=color, width=2)


def draw_phone_icon(draw, x, y, size=14, color=GOLD_MAIN):
    pts = [
        (x + 2, y + 2), (x + 5, y + 1), (x + 7, y + 4), (x + 5, y + 6),
        (x + 7, y + 9), (x + 9, y + 8), (x + 11, y + 10), (x + 11, y + 13),
        (x + 8, y + 14), (x + 1, y + 7)
    ]
    draw.polygon(pts, fill=color)


def render_crisp_title_canvas(target_w=966, target_h=400, scale=3):
    """
    Renders with 3X Super-sampling (e.g. 2898 x 1200) for pristine text clarity.
    Layout:
    - Left:
      1. Top Badges (Mint: 통계학 석사 / Amber: 등록번호)
      2. Main Headline (3 lines with gold underline)
      3. Bottom 3 Highlight Cards (통계학 석사, 충무공동 한 자리, 100% 실매물)
      * Middle 2-line explanation is removed!
    - Right:
      1. CEO Photo Card
      2. CEO Name Tag
      3. Direct Call Button (📞 010-4670-7248 직접 상담)
      * Middle address text is removed!
    """
    W = target_w * scale
    H = target_h * scale

    canvas = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(canvas)

    # 1. Background gradient
    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Dot grid
    draw_dot_grid(draw, W, H, step=22 * scale)

    # Layout bounds
    PAD_X = 42 * scale
    PAD_Y = int(34 * scale)

    CONTENT_TOP_Y = PAD_Y
    CONTENT_BOT_Y = H - PAD_Y

    # ==========================================
    # RIGHT SHOWCASE CARD
    # ==========================================
    card_w = 252 * scale
    card_h = CONTENT_BOT_Y - CONTENT_TOP_Y
    card_x = W - card_w - PAD_X
    card_y = CONTENT_TOP_Y

    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=20 * scale,
        fill=BG_CARD,
        outline=BORDER_CARD,
        width=int(1.5 * scale)
    )

    # Call Button Dimensions at Bottom of Right Card
    btn_w = card_w - (24 * scale)
    btn_h = int(46 * scale)
    btn_x = card_x + (12 * scale)
    btn_y = card_y + card_h - btn_h - int(12 * scale)

    # CEO Photo fits comfortably above button
    photo_w = card_w - (20 * scale)
    photo_x = card_x + (10 * scale)
    photo_y = card_y + (10 * scale)
    photo_h = btn_y - photo_y - int(12 * scale)

    ceo_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_path):
        ceo_im = Image.open(ceo_path).convert('RGB')
        # Center-crop to exact aspect ratio
        im_w, im_h = ceo_im.size
        target_ratio = photo_w / photo_h
        cur_ratio = im_w / im_h

        if cur_ratio > target_ratio:
            new_w = int(im_h * target_ratio)
            left = (im_w - new_w) // 2
            ceo_cropped = ceo_im.crop((left, 0, left + new_w, im_h))
        else:
            new_h = int(im_w / target_ratio)
            top = 0  # keep top focus on head/face
            ceo_cropped = ceo_im.crop((0, top, im_w, top + new_h))

        ceo_r = ceo_cropped.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
        
        # Round mask
        pmask = Image.new('L', (photo_w, photo_h), 0)
        pdraw = ImageDraw.Draw(pmask)
        pdraw.rounded_rectangle([0, 0, photo_w - 1, photo_h - 1], radius=16 * scale, fill=255)
        canvas.paste(ceo_r, (photo_x, photo_y), pmask)

        # Name Tag Plate at bottom of photo
        f_name = ImageFont.truetype(FONT_BD, int(13.5 * scale))
        tag_w = photo_w - (28 * scale)
        tag_h = int(30 * scale)
        tag_x = photo_x + (14 * scale)
        tag_y = photo_y + photo_h - tag_h - int(8 * scale)
        
        # Dark pill with gold border for name tag
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=10 * scale, fill=(11, 18, 35), outline=BORDER_CARD, width=int(1 * scale))
        name_text = "대표 공인중개사 황선숙"
        bbox_n = f_name.getbbox(name_text)
        nw = bbox_n[2] - bbox_n[0]
        draw.text((tag_x + (tag_w - nw) // 2, tag_y + int(4.5 * scale)), name_text, font=f_name, fill=WHITE)

    # Royal Blue Call Button directly under CEO photo (Clean & Immediate)
    for by in range(btn_h):
        bf = by / btn_h
        br = int(BLUE_BTN_TOP[0] * (1 - bf) + BLUE_BTN_BOT[0] * bf)
        bg = int(BLUE_BTN_TOP[1] * (1 - bf) + BLUE_BTN_BOT[1] * bf)
        bb = int(BLUE_BTN_TOP[2] * (1 - bf) + BLUE_BTN_BOT[2] * bf)
        draw.line([(btn_x, btn_y + by), (btn_x + btn_w, btn_y + by)], fill=(br, bg, bb))
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=12 * scale, outline=BLUE_BTN_BORDER, width=int(1.5 * scale))

    draw_phone_icon(draw, btn_x + int(24 * scale), btn_y + int(14 * scale), size=int(15 * scale), color=GOLD_MAIN)
    f_btn = ImageFont.truetype(FONT_BD, int(13.5 * scale))
    draw.text((btn_x + int(48 * scale), btn_y + int(11 * scale)), "010-4670-7248 직접 상담", font=f_btn, fill=WHITE)

    # ==========================================
    # LEFT CONTENT
    # ==========================================
    lx = PAD_X

    # 1. Top Badges
    f_pill = ImageFont.truetype(FONT_BD, int(12 * scale))
    pill1_text = "통계학 석사의 정밀 데이터 분석 · 2017년부터 충무공동 한 자리"
    pill2_text = "등록 48170-2017-00038"

    bbox1 = f_pill.getbbox(pill1_text)
    pw1 = (bbox1[2] - bbox1[0]) + int(32 * scale)
    pill_h = int(28 * scale)
    draw.rounded_rectangle([lx, CONTENT_TOP_Y, lx + pw1, CONTENT_TOP_Y + pill_h], radius=14 * scale, fill=MINT_BG, outline=MINT_BORDER, width=int(1.2 * scale))
    draw_green_dot(draw, lx + int(14 * scale), CONTENT_TOP_Y + int(14 * scale), r=int(4 * scale), color=MINT_TEXT)
    draw.text((lx + int(25 * scale), CONTENT_TOP_Y + int(5 * scale)), pill1_text, font=f_pill, fill=MINT_TEXT)

    lx2 = lx + pw1 + int(10 * scale)
    bbox2 = f_pill.getbbox(pill2_text)
    pw2 = (bbox2[2] - bbox2[0]) + int(32 * scale)
    draw.rounded_rectangle([lx2, CONTENT_TOP_Y, lx2 + pw2, CONTENT_TOP_Y + pill_h], radius=14 * scale, fill=AMBER_PILL_BG, outline=AMBER_PILL_BORDER, width=int(1.2 * scale))
    draw_shield_icon(draw, lx2 + int(11 * scale), CONTENT_TOP_Y + int(6.5 * scale), size=int(14 * scale), color=AMBER_PILL_TEXT)
    draw.text((lx2 + int(30 * scale), CONTENT_TOP_Y + int(5 * scale)), pill2_text, font=f_pill, fill=AMBER_PILL_TEXT)

    # 2. Main Headline (3 Lines) - Bold, crystal clear typography
    f_h1 = ImageFont.truetype(FONT_BD, int(31 * scale))
    line_step = int(45 * scale)
    h_y = CONTENT_TOP_Y + int(48 * scale)
    draw.text((lx, h_y), "통계학 석사의 정밀 데이터 분석,", font=f_h1, fill=GOLD_MAIN)
    draw.text((lx, h_y + line_step), "2017년부터 충무공동 한 자리를 지켜온", font=f_h1, fill=WHITE)

    # Line 3: 진주퀸공인중개사 (Gold + Underline) + 입니다. (White)
    brand_text = "진주퀸공인중개사"
    draw.text((lx, h_y + line_step * 2), brand_text, font=f_h1, fill=GOLD_MAIN)
    bbox_brand = f_h1.getbbox(brand_text)
    bw_brand = bbox_brand[2] - bbox_brand[0]
    draw.line([(lx, h_y + line_step * 2 + int(40 * scale)), (lx + bw_brand, h_y + line_step * 2 + int(40 * scale))], fill=GOLD_LINE, width=int(4 * scale))
    draw.text((lx + bw_brand + int(6 * scale), h_y + line_step * 2), "입니다.", font=f_h1, fill=WHITE)

    # (Middle 2-line explanation is removed!)

    # 3. Highlight Cards (Directly below headline with comfortable spacing)
    c_h = int(72 * scale)
    c_y = CONTENT_BOT_Y - c_h
    c_w = int(190 * scale)
    c_gap = int(14 * scale)
    f_ctitle = ImageFont.truetype(FONT_BD, int(14.5 * scale))
    f_csub = ImageFont.truetype(FONT_REG, int(12 * scale))

    cards = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "2017년부터 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]

    for i, (ct, cs) in enumerate(cards):
        cx = lx + i * (c_w + c_gap)
        draw.rounded_rectangle([cx, c_y, cx + c_w, c_y + c_h], radius=14 * scale, fill=BG_CARD, outline=BORDER_CARD, width=int(1.2 * scale))
        
        bt = f_ctitle.getbbox(ct)
        tw = bt[2] - bt[0]
        draw.text((cx + (c_w - tw) // 2, c_y + int(14 * scale)), ct, font=f_ctitle, fill=GOLD_MAIN)

        bs = f_csub.getbbox(cs)
        sw = bs[2] - bs[0]
        draw.text((cx + (c_w - sw) // 2, c_y + int(39 * scale)), cs, font=f_csub, fill=SLATE_BRIGHT)

    return canvas


def make_sharp_image(canvas_large, target_w, target_h):
    """
    Downsamples from 3X supersampled canvas to target dimensions using Lanczos,
    then applies a mild unsharp mask to guarantee razor-sharp text on any screen.
    """
    im_resized = canvas_large.resize((target_w, target_h), Image.Resampling.LANCZOS)
    # Mild unsharp mask for enhanced font contrast
    im_sharp = im_resized.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=3))
    return im_sharp


def generate_all_blog_title_packages():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    # -------------------------------------------------------------
    # Package 1: [추천 1위] 966 x 400px 황금비율 표준형 (중간 삭제 최적 비율)
    # -------------------------------------------------------------
    c400_3x = render_crisp_title_canvas(target_w=966, target_h=400, scale=3)
    img_400_sharp = make_sharp_image(c400_3x, 966, 400)

    # Save 966x400 (PNG & JPG 100)
    p_400_jpg = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_황금비율_966x400.jpg")
    p_400_png = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_황금비율_966x400.png")
    img_400_sharp.save(p_400_jpg, "JPEG", quality=100)
    img_400_sharp.save(p_400_png, "PNG")
    img_400_sharp.save(os.path.join(IMAGES_DIR, "naver-blog-title-966x400.jpg"), "JPEG", quality=100)
    img_400_sharp.save(os.path.join(IMAGES_DIR, "naver-blog-title-966x400.png"), "PNG")
    img_400_sharp.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966x400.jpg"), "JPEG", quality=100)

    # Save 1932x800 Retina 2X (초고해상도 2배 원본)
    img_400_2x = make_sharp_image(c400_3x, 1932, 800)
    p_400_2x_jpg = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_레티나2배_1932x800.jpg")
    p_400_2x_png = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_레티나2배_1932x800.png")
    img_400_2x.save(p_400_2x_jpg, "JPEG", quality=100)
    img_400_2x.save(p_400_2x_png, "PNG")
    img_400_2x.save(os.path.join(IMAGES_DIR, "naver-blog-title-retina-1932x800.jpg"), "JPEG", quality=100)
    img_400_2x.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-retina-1932x800.jpg"), "JPEG", quality=100)

    # -------------------------------------------------------------
    # Package 2: 966 x 360px 컴팩트 슬림형
    # -------------------------------------------------------------
    c360_3x = render_crisp_title_canvas(target_w=966, target_h=360, scale=3)
    img_360_sharp = make_sharp_image(c360_3x, 966, 360)

    p_360_jpg = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_컴팩트슬림_966x360.jpg")
    p_360_png = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_컴팩트슬림_966x360.png")
    img_360_sharp.save(p_360_jpg, "JPEG", quality=100)
    img_360_sharp.save(p_360_png, "PNG")
    img_360_sharp.save(os.path.join(IMAGES_DIR, "naver-blog-title-compact-966x360.jpg"), "JPEG", quality=100)
    img_360_sharp.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-compact-966x360.jpg"), "JPEG", quality=100)

    # -------------------------------------------------------------
    # Package 3: 966 x 500px 기존 높이 유지형 (선명도 대폭 향상)
    # -------------------------------------------------------------
    c500_3x = render_crisp_title_canvas(target_w=966, target_h=500, scale=3)
    img_500_sharp = make_sharp_image(c500_3x, 966, 500)

    p_500_jpg = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_선명500_966x500.jpg")
    p_500_png = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그타이틀_선명500_966x500.png")
    img_500_sharp.save(p_500_jpg, "JPEG", quality=100)
    img_500_sharp.save(p_500_png, "PNG")
    img_500_sharp.save(os.path.join(IMAGES_DIR, "naver-blog-title-966x500.jpg"), "JPEG", quality=100)
    img_500_sharp.save(os.path.join(ARTIFACT_DIR, "naver-blog-title-966x500.jpg"), "JPEG", quality=100)

    # -------------------------------------------------------------
    # Package 4: 1920 x 450px 와이드 스킨 배경 (블로그 리모콘 > 스킨배경용)
    # -------------------------------------------------------------
    W_skin, H_skin = 1920, 450
    skin = Image.new('RGB', (W_skin, H_skin), BG_NAVY_TOP)
    sdraw = ImageDraw.Draw(skin)
    for y in range(H_skin):
        f = y / H_skin
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        sdraw.line([(0, y), (W_skin, y)], fill=(r, g, b))
    draw_dot_grid(sdraw, W_skin, H_skin, step=26)

    # Center-paste 966x400 sharp image
    skin.paste(img_400_sharp, ((W_skin - 966) // 2, (H_skin - 400) // 2))
    p_skin_jpg = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_와이드스킨배경_1920x450.jpg")
    p_skin_png = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_와이드스킨배경_1920x450.png")
    skin.save(p_skin_jpg, "JPEG", quality=100)
    skin.save(p_skin_png, "PNG")
    skin.save(os.path.join(IMAGES_DIR, "naver-blog-skin-1920x450.jpg"), "JPEG", quality=100)
    skin.save(os.path.join(ARTIFACT_DIR, "naver-blog-skin-1920x450.jpg"), "JPEG", quality=100)

    print("All High-Definition Title Packages generated successfully!")


if __name__ == '__main__':
    generate_all_blog_title_packages()
