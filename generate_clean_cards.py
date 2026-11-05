from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('images/complex_cards', exist_ok=True)

cards = [
    {
        "filename": "더힐_505동_클린카드.jpg",
        "complex_name": "진주혁신더힐",
        "dong_or_type": "505동 로열층",
        "tag_text": "진주혁신도시 아파트 실매물",
        "bg_top": (225, 239, 250),       # Soft Pastel Powder Sky Blue
        "bg_bottom": (202, 224, 244),
        "border": (160, 195, 228),
        "text_title": (20, 42, 74),       # Deep Navy
        "text_accent": (2, 132, 199),     # Vivid Sky Blue
        "tag_color": (2, 132, 199)
    },
    {
        "filename": "라온프라이빗_204동_클린카드.jpg",
        "complex_name": "라온프라이빗",
        "dong_or_type": "204동 로열동",
        "tag_text": "진주혁신도시 아파트 실매물",
        "bg_top": (226, 245, 234),       # Soft Pastel Mint Sage
        "bg_bottom": (204, 233, 218),
        "border": (155, 208, 180),
        "text_title": (18, 52, 33),       # Deep Forest Slate
        "text_accent": (16, 149, 93),     # Emerald Green
        "tag_color": (16, 149, 93)
    },
    {
        "filename": "LH8단지_803동_클린카드.jpg",
        "complex_name": "혁신도시LH8단지",
        "dong_or_type": "803동 선호라인",
        "tag_text": "진주혁신도시 아파트 실매물",
        "bg_top": (255, 243, 233),       # Soft Pastel Peach Apricot
        "bg_bottom": (253, 228, 210),
        "border": (235, 192, 166),
        "text_title": (68, 36, 18),       # Deep Espresso Mocha
        "text_accent": (217, 119, 6),     # Warm Amber Gold
        "tag_color": (194, 65, 12)
    },
    {
        "filename": "대방노블랜드_더센트럴_클린카드.jpg",
        "complex_name": "진주혁신 대방노블랜드",
        "dong_or_type": "더센트럴 34평 로열동",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_top": (234, 236, 253),       # Soft Pastel Periwinkle Lavender
        "bg_bottom": (214, 219, 248),
        "border": (178, 186, 234),
        "text_title": (28, 36, 76),       # Deep Indigo Navy
        "text_accent": (79, 70, 229),     # Royal Indigo
        "tag_color": (79, 70, 229)
    },
    {
        "filename": "중흥S클래스_센트럴시티_클린카드.jpg",
        "complex_name": "중흥S-클래스 센트럴시티",
        "dong_or_type": "1단지 84A타입 로열동",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_top": (225, 247, 247),       # Soft Pastel Ice Teal
        "bg_bottom": (199, 236, 237),
        "border": (148, 208, 212),
        "text_title": (16, 52, 58),       # Deep Ocean Teal
        "text_accent": (13, 148, 136),    # Teal
        "tag_color": (13, 148, 136)
    },
    {
        "filename": "한림풀에버_클린카드.jpg",
        "complex_name": "혁신도시 한림풀에버",
        "dong_or_type": "84㎡B 단지내 조경뷰",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_top": (236, 247, 228),       # Soft Pastel Pistachio Leaf
        "bg_bottom": (217, 239, 204),
        "border": (172, 214, 152),
        "text_title": (30, 56, 18),       # Deep Leaf Slate
        "text_accent": (85, 139, 47),     # Leaf Olive
        "tag_color": (85, 139, 47)
    },
    {
        "filename": "중흥S클래스_더퍼스트_클린카드.jpg",
        "complex_name": "중흥S-클래스 더퍼스트",
        "dong_or_type": "38평 대형평형 귀한 매물",
        "tag_text": "진주혁신도시 프리미엄 아파트",
        "bg_top": (254, 239, 243),       # Soft Pastel Rose Cream
        "bg_bottom": (251, 221, 228),
        "border": (236, 180, 194),
        "text_title": (72, 24, 38),       # Deep Rose Slate
        "text_accent": (190, 24, 93),     # Rose Accent
        "tag_color": (190, 24, 93)
    },
    {
        "filename": "기본_아파트_클린카드.jpg",
        "complex_name": "진주혁신도시 아파트",
        "dong_or_type": "진주퀸공인중개사 추천 매물",
        "tag_text": "진주혁신도시 정직·신뢰 실매물",
        "bg_top": (242, 246, 250),       # Soft Pastel Silver Mist
        "bg_bottom": (226, 233, 242),
        "border": (188, 198, 214),
        "text_title": (15, 23, 42),       # Slate 900
        "text_accent": (2, 132, 199),     # Sky Blue
        "tag_color": (2, 132, 199)
    },
    {
        "filename": "일반상가_클린카드.jpg",
        "complex_name": "진주혁신도시 일반상가점포",
        "dong_or_type": "LH·한국남동발전 인근 5층 소형사무실",
        "tag_text": "진주혁신도시 상가·사무실 실매물",
        "bg_top": (251, 247, 239),       # Soft Pastel Warm Sand Cream
        "bg_bottom": (244, 236, 221),
        "border": (216, 201, 176),
        "text_title": (52, 40, 24),       # Deep Mocha Slate
        "text_accent": (180, 83, 9),      # Amber Bronze
        "tag_color": (180, 83, 9)
    }
]

W, H = 1200, 800

font_path = "C:/Windows/Fonts/malgunbd.ttf"
font_regular_path = "C:/Windows/Fonts/malgun.ttf"

font_title = ImageFont.truetype(font_path, 66)
font_sub = ImageFont.truetype(font_path, 34)
font_badge = ImageFont.truetype(font_path, 22)
font_footer = ImageFont.truetype(font_path, 22)

for item in cards:
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # 1. Smooth bright pastel vertical gradient
    r1, g1, b1 = item["bg_top"]
    r2, g2, b2 = item["bg_bottom"]
    for y in range(H):
        t = y / (H - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Refined elegant pastel borders
    draw.rounded_rectangle([30, 30, W - 30, H - 30], radius=24, outline=item["border"], width=2)
    draw.rounded_rectangle([40, 40, W - 40, H - 40], radius=18, outline=(255, 255, 255), width=2)

    # 3. Top Tag Pill Badge (Crisp white pill with pastel colored text)
    badge_text = item["tag_text"]
    bw, bh = 360, 44
    bx1 = (W - bw) // 2
    by1 = 140
    # Shadow
    draw.rounded_rectangle([bx1 + 1, by1 + 2, bx1 + bw + 1, by1 + bh + 2], radius=22, fill=(0, 0, 0, 15))
    # White Pill
    draw.rounded_rectangle([bx1, by1, bx1 + bw, by1 + bh], radius=22, fill=(255, 255, 255), outline=item["border"], width=1)
    draw.text((W // 2, by1 + bh // 2), badge_text, fill=item["tag_color"], font=font_badge, anchor="mm")

    # 4. Main Title (Crisp, Large, High Contrast Dark Pastel Hue)
    title_text = item["complex_name"]
    draw.text((W // 2, 310), title_text, fill=item["text_title"], font=font_title, anchor="mm")

    # 5. Dong or Unit Detail (Colored Accent)
    dong_text = item["dong_or_type"]
    draw.text((W // 2, 400), dong_text, fill=item["text_accent"], font=font_sub, anchor="mm")

    # 6. Center Accent Line with Dot
    div_w = 120
    draw.line([(W // 2 - div_w // 2, 470), (W // 2 + div_w // 2, 470)], fill=item["border"], width=2)
    draw.circle((W // 2, 470), 4, fill=item["text_accent"])

    # 7. (진주퀸공인중개사사무소 확인 인증 실매물 문구 완전 삭제!)

    # 8. Bottom Footer Bar (Crisp White Card with Slate Contact Info)
    bar_y = 650
    fw, fh = W - 180, 62
    fx1 = 90
    draw.rounded_rectangle([fx1, bar_y, fx1 + fw, bar_y + fh], radius=14, fill=(255, 255, 255), outline=item["border"], width=1)
    footer_text = "진주퀸공인중개사사무소  |  대표 황선숙  |  문의 055-761-7248 · 010-4670-7248"
    draw.text((W // 2, bar_y + fh // 2), footer_text, fill=(71, 85, 105), font=font_footer, anchor="mm")

    out_path = os.path.join("images/complex_cards", item["filename"])
    img.save(out_path, quality=95)
    print(f"Generated Pastel Card: {out_path}")

print("All 9 cards regenerated with bright pastel colors and unwanted subtitle text deleted!")
