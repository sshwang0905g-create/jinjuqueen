import os
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\22ad999b-b105-4739-9ac9-9c3b7b7fc818"
IMAGES_DIR = "images"
DESKTOP_DIR = r"c:\Users\User\OneDrive\문서\바탕 화면"

FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_REG = "C:/Windows/Fonts/malgun.ttf"

# Colors synchronized with website
BG_NAVY_TOP = (11, 20, 42)
BG_NAVY_MID = (9, 16, 35)
BG_NAVY_BOT = (6, 10, 22)

GOLD_MAIN = (251, 191, 36)      # Amber-400
GOLD_LINE = (245, 158, 11)
WHITE = (255, 255, 255)
SLATE_200 = (226, 232, 240)
SLATE_300 = (203, 213, 225)
SLATE_400 = (148, 163, 184)
SLATE_500 = (100, 116, 139)

MINT_TEXT = (52, 211, 153)      # Emerald-400
MINT_BG = (6, 78, 59)
MINT_BORDER = (16, 185, 129)

AMBER_PILL_TEXT = (251, 191, 36)
AMBER_PILL_BG = (69, 26, 3)
AMBER_PILL_BORDER = (217, 119, 6)

BLUE_BTN_TOP = (37, 99, 235)    # Royal Blue
BLUE_BTN_BORDER = (96, 165, 250)


def draw_dot_grid(draw, width, height, step=24):
    for x in range(12, width, step):
        for y in range(12, height, step):
            draw.point((x, y), fill=(24, 38, 65))


def draw_shield_icon(draw, x, y, size=15, color=AMBER_PILL_TEXT):
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


def create_mobile_cover_option_a():
    """
    Option A: High-impact upper safe-zone branding (1000 x 1200)
    Optimal for Naver Blog app: upper half features full brand & CEO portrait,
    lower half provides a dark, elegant backdrop for Naver's native UI elements.
    """
    W, H = 1000, 1200
    canvas = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(canvas)

    # 1. Subtle smooth gradient
    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Dot grid
    draw_dot_grid(draw, W, H, step=26)

    # Subtle ambient glow in center-top
    glow_box = [150, 80, 850, 700]
    draw.ellipse(glow_box, fill=None, outline=(18, 30, 58), width=3)

    # Fonts
    f_badge = ImageFont.truetype(FONT_BD, 22)
    f_subbadge = ImageFont.truetype(FONT_BD, 20)
    f_h1_gold = ImageFont.truetype(FONT_BD, 42)
    f_h1_white = ImageFont.truetype(FONT_BD, 44)
    f_h1_brand = ImageFont.truetype(FONT_BD, 48)
    f_desc = ImageFont.truetype(FONT_REG, 23)
    f_card_t = ImageFont.truetype(FONT_BD, 21)
    f_card_s = ImageFont.truetype(FONT_REG, 17)
    f_ceo_name = ImageFont.truetype(FONT_BD, 26)
    f_ceo_title = ImageFont.truetype(FONT_BD, 18)
    f_ceo_phone = ImageFont.truetype(FONT_BD, 24)

    # ----------------------------------------------------
    # TOP BADGES (Y: 130 ~ 210)
    # ----------------------------------------------------
    badge_text1 = "통계학 석사의 정밀 데이터 분석 · 충무공동 한 자리"
    bbox1 = f_badge.getbbox(badge_text1)
    bw1 = bbox1[2] - bbox1[0] + 60
    bh1 = 44
    bx1 = (W - bw1) // 2
    by1 = 120
    draw.rounded_rectangle([bx1, by1, bx1 + bw1, by1 + bh1], radius=22, fill=MINT_BG, outline=MINT_BORDER, width=2)
    # Green indicator dot
    draw.ellipse([bx1 + 22 - 5, by1 + bh1 // 2 - 5, bx1 + 22 + 5, by1 + bh1 // 2 + 5], fill=MINT_TEXT)
    draw.text((bx1 + 38, by1 + 9), badge_text1, font=f_badge, fill=MINT_TEXT)

    # Second badge (Registration number)
    badge_text2 = "등록 48170-2017-00038 · 현장확인 100% 실매물"
    bbox2 = f_subbadge.getbbox(badge_text2)
    bw2 = bbox2[2] - bbox2[0] + 56
    bh2 = 38
    bx2 = (W - bw2) // 2
    by2 = 180
    draw.rounded_rectangle([bx2, by2, bx2 + bw2, by2 + bh2], radius=19, fill=AMBER_PILL_BG, outline=AMBER_PILL_BORDER, width=1)
    draw_shield_icon(draw, bx2 + 16, by2 + 11, size=16, color=AMBER_PILL_TEXT)
    draw.text((bx2 + 40, by2 + 8), badge_text2, font=f_subbadge, fill=AMBER_PILL_TEXT)

    # ----------------------------------------------------
    # MAIN HEADLINE (Y: 245 ~ 380)
    # ----------------------------------------------------
    line1 = "통계학 석사의 정밀 데이터 분석,"
    bb_l1 = f_h1_gold.getbbox(line1)
    w_l1 = bb_l1[2] - bb_l1[0]
    draw.text(((W - w_l1) // 2, 245), line1, font=f_h1_gold, fill=GOLD_MAIN)

    line2 = "2017년부터 충무공동 한 자리를 지켜온"
    bb_l2 = f_h1_white.getbbox(line2)
    w_l2 = bb_l2[2] - bb_l2[0]
    draw.text(((W - w_l2) // 2, 305), line2, font=f_h1_white, fill=WHITE)

    brand_str = "진주퀸공인중개사"
    bb_br = f_h1_brand.getbbox(brand_str)
    w_br = bb_br[2] - bb_br[0]
    bx_br = (W - w_br) // 2
    by_br = 368
    draw.text((bx_br, by_br), brand_str, font=f_h1_brand, fill=WHITE)
    # Underline under 진주퀸공인중개사
    draw.rectangle([bx_br, by_br + 62, bx_br + w_br, by_br + 66], fill=GOLD_LINE)

    # ----------------------------------------------------
    # CEO SHOWCASE CARD (CENTER Y: 460 ~ 680)
    # ----------------------------------------------------
    card_w = 760
    card_h = 220
    card_x = (W - card_w) // 2
    card_y = 460

    # Card background & border
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=(15, 25, 46), outline=(38, 56, 92), width=2)

    # CEO Portrait inside card
    ceo_img_path = os.path.join(IMAGES_DIR, "ceo-square.jpg")
    if os.path.exists(ceo_img_path):
        ceo_raw = Image.open(ceo_img_path).convert('RGB')
        photo_size = 176
        ceo_resized = ceo_raw.resize((photo_size, photo_size), Image.Resampling.LANCZOS)
        # Circular mask for CEO photo
        mask = Image.new('L', (photo_size, photo_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, photo_size, photo_size), fill=255)

        px = card_x + 24
        py = card_y + 22
        canvas.paste(ceo_resized, (px, py), mask)
        # Gold ring around CEO photo
        draw.ellipse([px - 2, py - 2, px + photo_size + 2, py + photo_size + 2], outline=GOLD_MAIN, width=3)

    # Text next to CEO Photo
    tx = card_x + 230
    draw.text((tx, card_y + 25), "대표 공인중개사", font=f_ceo_title, fill=GOLD_MAIN)
    draw.text((tx, card_y + 52), "황선숙 대표", font=f_ceo_name, fill=WHITE)
    draw.text((tx, card_y + 92), "진주시 에나로 146, 105호 (라온프라이빗시티)", font=ImageFont.truetype(FONT_REG, 17), fill=SLATE_300)

    # Royal Blue Call Button Pill inside card
    btn_w = 480
    btn_h = 54
    btn_x = tx
    btn_y = card_y + 135
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=16, fill=BLUE_BTN_TOP, outline=BLUE_BTN_BORDER, width=2)
    btn_label = "📞  010-4670-7248 직접 상담"
    bbox_btn = f_ceo_phone.getbbox(btn_label)
    w_btn = bbox_btn[2] - bbox_btn[0]
    draw.text((btn_x + (btn_w - w_btn) // 2, btn_y + 11), btn_label, font=f_ceo_phone, fill=WHITE)

    # ----------------------------------------------------
    # 3 METRIC MINI-CARDS (Y: 710 ~ 800)
    # ----------------------------------------------------
    metrics = [
        ("통계학 석사", "정밀 데이터 분석"),
        ("충무공동 한 자리", "2017년부터 우직한 신뢰"),
        ("100% 실매물", "현장 검증 책임 중개")
    ]
    mc_w = 236
    mc_h = 80
    gap = 26
    start_x = (W - (mc_w * 3 + gap * 2)) // 2
    my = 710

    for i, (mt, ms) in enumerate(metrics):
        mx = start_x + i * (mc_w + gap)
        draw.rounded_rectangle([mx, my, mx + mc_w, my + mc_h], radius=16, fill=(15, 25, 46), outline=(32, 48, 80), width=1)
        b_mt = f_card_t.getbbox(mt)
        w_mt = b_mt[2] - b_mt[0]
        draw.text((mx + (mc_w - w_mt) // 2, my + 14), mt, font=f_card_t, fill=GOLD_MAIN)
        b_ms = f_card_s.getbbox(ms)
        w_ms = b_ms[2] - b_ms[0]
        draw.text((mx + (mc_w - w_ms) // 2, my + 44), ms, font=f_card_s, fill=SLATE_400)

    # ----------------------------------------------------
    # BOTTOM SAFE AREA (Y: 820 ~ 1200)
    # ----------------------------------------------------
    # Sleek visual divider for Naver Mobile App Profile Overlay Area
    draw.line([(150, 840), (850, 840)], fill=(25, 40, 70), width=1)
    
    hint_text = "진주 혁신도시 아파트 · 오피스텔 · 상가 · 분양권 전문 중개"
    f_hint = ImageFont.truetype(FONT_REG, 20)
    bb_h = f_hint.getbbox(hint_text)
    w_h = bb_h[2] - bb_h[0]
    draw.text(((W - w_h) // 2, 860), hint_text, font=f_hint, fill=SLATE_400)

    # Save to all destinations
    out_art = os.path.join(ARTIFACT_DIR, "naver-blog-app-cover-1000x1200.jpg")
    out_img = os.path.join(IMAGES_DIR, "naver-blog-app-cover-1000x1200.jpg")
    out_desk = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_모바일앱커버_1000x1200.jpg")

    canvas.save(out_art, quality=95)
    canvas.save(out_img, quality=95)
    canvas.save(out_desk, quality=95)
    print("Saved Option A:", out_art)
    return out_art


def create_mobile_cover_option_b():
    """
    Option B: Clean Upper-Third Compact Safe Zone (1000 x 1200)
    Designed specifically for blog app themes where the profile & title overlay is large.
    """
    W, H = 1000, 1200
    canvas = Image.new('RGB', (W, H), BG_NAVY_TOP)
    draw = ImageDraw.Draw(canvas)

    for y in range(H):
        f = y / H
        r = int(BG_NAVY_TOP[0] * (1 - f) + BG_NAVY_BOT[0] * f)
        g = int(BG_NAVY_TOP[1] * (1 - f) + BG_NAVY_BOT[1] * f)
        b = int(BG_NAVY_TOP[2] * (1 - f) + BG_NAVY_BOT[2] * f)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    draw_dot_grid(draw, W, H, step=26)

    # Fonts
    f_badge = ImageFont.truetype(FONT_BD, 22)
    f_h1_gold = ImageFont.truetype(FONT_BD, 40)
    f_h1_white = ImageFont.truetype(FONT_BD, 44)
    f_h1_brand = ImageFont.truetype(FONT_BD, 52)
    f_phone = ImageFont.truetype(FONT_BD, 26)

    # Badge
    b_txt = "🟢 통계학 석사의 정밀 데이터 분석 · 2017년부터 충무공동 한 자리"
    bbox = f_badge.getbbox(b_txt)
    bw = bbox[2] - bbox[0] + 50
    bx = (W - bw) // 2
    draw.rounded_rectangle([bx, 100, bx + bw, 100 + 44], radius=22, fill=MINT_BG, outline=MINT_BORDER, width=2)
    draw.text((bx + 25, 109), b_txt, font=f_badge, fill=MINT_TEXT)

    # Headline
    l1 = "감이 아닌 정확한 통계와 데이터로 분석하는"
    w1 = f_h1_gold.getbbox(l1)[2] - f_h1_gold.getbbox(l1)[0]
    draw.text(((W - w1) // 2, 175), l1, font=f_h1_gold, fill=GOLD_MAIN)

    l2 = "진주 혁신도시 충무공동의 우직한 신뢰"
    w2 = f_h1_white.getbbox(l2)[2] - f_h1_white.getbbox(l2)[0]
    draw.text(((W - w2) // 2, 235), l2, font=f_h1_white, fill=WHITE)

    l3 = "진주퀸공인중개사사무소"
    w3 = f_h1_brand.getbbox(l3)[2] - f_h1_brand.getbbox(l3)[0]
    bx3 = (W - w3) // 2
    draw.text((bx3, 300), l3, font=f_h1_brand, fill=WHITE)
    draw.rectangle([bx3, 368, bx3 + w3, 372], fill=GOLD_LINE)

    # Phone Pill
    pw = 520
    ph = 60
    px = (W - pw) // 2
    py = 410
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=BLUE_BTN_TOP, outline=BLUE_BTN_BORDER, width=2)
    p_txt = "📞  대표 직통: 010-4670-7248"
    wp = f_phone.getbbox(p_txt)[2] - f_phone.getbbox(p_txt)[0]
    draw.text((px + (pw - wp) // 2, py + 14), p_txt, font=f_phone, fill=WHITE)

    # Sub-card in middle
    cw = 800
    ch = 110
    cx = (W - cw) // 2
    cy = 505
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill=(15, 25, 46), outline=(32, 48, 80), width=1)
    
    sub_title = "아파트 · 오피스텔 · 상가 · 분양권 · 택지 매매 / 임대 전문"
    f_sub = ImageFont.truetype(FONT_BD, 23)
    ws = f_sub.getbbox(sub_title)[2] - f_sub.getbbox(sub_title)[0]
    draw.text((cx + (cw - ws) // 2, cy + 24), sub_title, font=f_sub, fill=GOLD_MAIN)

    sub_addr = "경남 진주시 에나로 146, 105호 (라온프라이빗시티) · 등록 48170-2017-00038"
    f_addr = ImageFont.truetype(FONT_REG, 17)
    wa = f_addr.getbbox(sub_addr)[2] - f_addr.getbbox(sub_addr)[0]
    draw.text((cx + (cw - wa) // 2, cy + 64), sub_addr, font=f_addr, fill=SLATE_300)

    # Bottom Area: Clean Deep Dark Navy so Naver App's profile UI is 100% readable
    out_art = os.path.join(ARTIFACT_DIR, "naver-blog-app-cover-compact-1000x1200.jpg")
    out_img = os.path.join(IMAGES_DIR, "naver-blog-app-cover-compact-1000x1200.jpg")
    out_desk = os.path.join(DESKTOP_DIR, "진주퀸_네이버블로그_모바일앱커버_안전영역특화_1000x1200.jpg")

    canvas.save(out_art, quality=95)
    canvas.save(out_img, quality=95)
    canvas.save(out_desk, quality=95)
    print("Saved Option B:", out_art)
    return out_art


if __name__ == '__main__':
    create_mobile_cover_option_a()
    create_mobile_cover_option_b()

