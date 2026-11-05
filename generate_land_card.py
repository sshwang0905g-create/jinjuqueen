from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 800
font_path = "C:/Windows/Fonts/malgunbd.ttf"
font_regular_path = "C:/Windows/Fonts/malgun.ttf"

font_title = ImageFont.truetype(font_path, 60)
font_sub = ImageFont.truetype(font_path, 32)
font_badge = ImageFont.truetype(font_path, 22)
font_footer = ImageFont.truetype(font_path, 22)

# 토지 / 택지 전용 화사한 파스텔 카드 (오트밀 & 소프트 세이지)
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# Pastel Warm Oatmeal to Soft Sage
bg_top = (252, 248, 238)
bg_bottom = (238, 243, 230)
border = (205, 218, 192)
text_title = (45, 55, 32)       # Deep Olive Slate
text_accent = (101, 140, 52)    # Olive Green
tag_color = (101, 140, 52)

for y in range(H):
    t = y / (H - 1)
    r = int(bg_top[0] + (bg_bottom[0] - bg_top[0]) * t)
    g = int(bg_top[1] + (bg_bottom[1] - bg_top[1]) * t)
    b = int(bg_top[2] + (bg_bottom[2] - bg_top[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

draw.rounded_rectangle([30, 30, W - 30, H - 30], radius=24, outline=border, width=2)
draw.rounded_rectangle([40, 40, W - 40, H - 40], radius=18, outline=(255, 255, 255), width=2)

# Top Badge
badge_text = "진주혁신도시 토지·택지 실매물"
bw, bh = 360, 44
bx1, by1 = (W - bw) // 2, 140
draw.rounded_rectangle([bx1 + 1, by1 + 2, bx1 + bw + 1, by1 + bh + 2], radius=22, fill=(0, 0, 0, 15))
draw.rounded_rectangle([bx1, by1, bx1 + bw, by1 + bh], radius=22, fill=(255, 255, 255), outline=border, width=1)
draw.text((W // 2, by1 + bh // 2), badge_text, fill=tag_color, font=font_badge, anchor="mm")

# Title
draw.text((W // 2, 310), "진주혁신도시 단독주택·상가용지", fill=text_title, font=font_title, anchor="mm")

# Subtitle
draw.text((W // 2, 400), "네모반듯 즉시 건축 가능한 우량 필지 (택지)", fill=text_accent, font=font_sub, anchor="mm")

# Center Divider
div_w = 120
draw.line([(W // 2 - div_w // 2, 470), (W // 2 + div_w // 2, 470)], fill=border, width=2)
draw.circle((W // 2, 470), 4, fill=text_accent)

# Footer
bar_y = 650
fw, fh = W - 180, 62
fx1 = 90
draw.rounded_rectangle([fx1, bar_y, fx1 + fw, bar_y + fh], radius=14, fill=(255, 255, 255), outline=border, width=1)
footer_text = "진주퀸공인중개사사무소  |  대표 황선숙  |  문의 055-761-7248 · 010-4670-7248"
draw.text((W // 2, bar_y + fh // 2), footer_text, fill=(71, 85, 105), font=font_footer, anchor="mm")

out_path = "images/complex_cards/토지_클린카드.jpg"
img.save(out_path, quality=95)
print(f"Generated Land Card: {out_path}")
