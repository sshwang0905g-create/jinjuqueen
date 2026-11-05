import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('images/complex_cards', exist_ok=True)

# Card Definitions
# Each has:
# - filename
# - complex_name
# - dong_or_type
# - tag_text
# - bg_gradient: (start_rgb, end_rgb) - medium-toned, soft & elegant, not too dark!
# - accent_gold: rgb
# - border_rgb: rgb

cards = [
    {
        "filename": "더힐_505동_클린카드.jpg",
        "complex_name": "진주혁신더힐",
        "dong_or_type": "505동 로열층",
        "tag_text": "진주혁신도시 아파트 실매물",
        "bg_start": (59, 90, 122),    # Soft Slate Mist Blue
        "bg_end": (44, 66, 87),
        "accent": (245, 208, 120),
        "border": (110, 145, 180)
    },
    {
        "filename": "라온프라이빗_204동_클린카드.jpg",
        "complex_name": "라온프라이빗",
        "dong_or_type": "204동 로열동",
        "tag_text": "진주혁신도시 아파트 실매물",
        "bg_start": (58, 99, 81),     # Refined Sage Eucalyptus
        "bg_end": (45, 75, 61),
        "accent": (245, 215, 130),
        "border": (105, 155, 130)
    },
    {
        "filename": "LH8단지_803동_클린카드.jpg",
        "complex_name": "혁신도시LH8단지",
        "dong_or_type": "803동 선호라인",
        "tag_text": "진주혁신도시 아파트 실매물",
        "bg_start": (90, 74, 66),     # Warm Mocha Sand Taupe
        "bg_end": (72, 58, 51),
        "accent": (245, 210, 130),
        "border": (150, 130, 118)
    },
    {
        "filename": "대방노블랜드_더센트럴_클린카드.jpg",
        "complex_name": "진주혁신 대방노블랜드",
        "dong_or_type": "더센트럴 34평 로열동",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_start": (63, 83, 112),    # Soft Royal Indigo
        "bg_end": (47, 62, 84),
        "accent": (245, 208, 120),
        "border": (115, 140, 175)
    },
    {
        "filename": "중흥S클래스_센트럴시티_클린카드.jpg",
        "complex_name": "중흥S-클래스 센트럴시티",
        "dong_or_type": "1단지 84A타입 로열동",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_start": (50, 93, 99),     # Muted Ocean Teal
        "bg_end": (37, 70, 75),
        "accent": (245, 215, 130),
        "border": (100, 150, 158)
    },
    {
        "filename": "한림풀에버_클린카드.jpg",
        "complex_name": "혁신도시 한림풀에버",
        "dong_or_type": "84㎡B 단지내 조경뷰",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_start": (62, 95, 73),     # Forest Laurel Green
        "bg_end": (48, 73, 56),
        "accent": (245, 215, 130),
        "border": (110, 150, 125)
    },
    {
        "filename": "중흥S클래스_더퍼스트_클린카드.jpg",
        "complex_name": "중흥S-클래스 더퍼스트",
        "dong_or_type": "38평 대형평형 귀한 매물",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_start": (94, 73, 62),     # Warm Amber Chestnut
        "bg_end": (73, 56, 47),
        "accent": (245, 210, 130),
        "border": (155, 128, 112)
    },
    {
        "filename": "기본_아파트_클린카드.jpg",
        "complex_name": "진주혁신도시 아파트",
        "dong_or_type": "진주퀸공인중개사 추천 매물",
        "tag_text": "진주혁신도시 정직·신뢰 실매물",
        "bg_start": (71, 85, 105),    # Modern Warm Slate Gray
        "bg_end": (51, 65, 85),
        "accent": (245, 208, 120),
        "border": (120, 140, 168)
    }
]

W, H = 1200, 800

font_path = "C:/Windows/Fonts/malgunbd.ttf"
font_regular_path = "C:/Windows/Fonts/malgun.ttf"

font_title = ImageFont.truetype(font_path, 66)
font_sub = ImageFont.truetype(font_path, 34)
font_badge = ImageFont.truetype(font_path, 22)
font_desc = ImageFont.truetype(font_regular_path, 25)
font_footer = ImageFont.truetype(font_path, 22)

for item in cards:
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # 1. Subtle smooth gradient
    r1, g1, b1 = item["bg_start"]
    r2, g2, b2 = item["bg_end"]
    for y in range(H):
        t = y / (H - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Outer & Inner Decorative Border
    draw.rounded_rectangle([28, 28, W - 28, H - 28], radius=24, outline=item["border"], width=2)
    draw.rounded_rectangle([38, 38, W - 38, H - 38], radius=18, outline=(item["accent"][0], item["accent"][1], item["accent"][2], 120), width=1)

    # 3. Top Tag Pill Badge
    badge_text = item["tag_text"]
    bw = 360
    bh = 42
    bx1 = (W - bw) // 2
    by1 = 120
    draw.rounded_rectangle([bx1, by1, bx1 + bw, by1 + bh], radius=21, fill=(255, 255, 255, 30), outline=item["accent"], width=2)
    draw.text((W // 2, by1 + bh // 2), badge_text, fill=item["accent"], font=font_badge, anchor="mm")

    # 4. Main Apartment Name (Clean & Large)
    title_text = item["complex_name"]
    draw.text((W // 2, 270), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    # 5. Dong or Unit Detail (Gold Accent)
    dong_text = item["dong_or_type"]
    draw.text((W // 2, 360), dong_text, fill=item["accent"], font=font_sub, anchor="mm")

    # 6. Center Accent Divider Line
    div_w = 140
    draw.line([(W // 2 - div_w // 2, 430), (W // 2 + div_w // 2, 430)], fill=item["accent"], width=3)

    # 7. Subtitle Info
    sub_desc = "진주퀸공인중개사사무소 확인 인증 실매물"
    draw.text((W // 2, 480), sub_desc, fill=(230, 238, 248), font=font_desc, anchor="mm")

    # 8. Modern Building Silhouette Icon / Graphic Dot Accents
    draw.circle((W // 2 - 180, 480), 3, fill=item["accent"])
    draw.circle((W // 2 + 180, 480), 3, fill=item["accent"])

    # 9. Bottom Footer Bar
    bar_y = 660
    draw.rounded_rectangle([90, bar_y, W - 90, bar_y + 60], radius=14, fill=(0, 0, 0, 50), outline=item["border"], width=1)
    footer_text = "진주퀸공인중개사사무소  |  대표 황선숙  |  문의 055-761-7248 · 010-4670-7248"
    draw.text((W // 2, bar_y + 30), footer_text, fill=(240, 245, 250), font=font_footer, anchor="mm")

    out_path = os.path.join("images/complex_cards", item["filename"])
    img.save(out_path, quality=95)
    print(f"Generated card: {out_path}")

print("All clean cards successfully generated with distinct, non-dark luxury palettes!")
