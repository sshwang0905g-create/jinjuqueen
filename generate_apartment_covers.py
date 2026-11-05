import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs('images/complexes', exist_ok=True)

# Base background images for different apartment styles
BASE_BACKGROUNDS = {
    "더힐": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1400&q=85",
    "라온": "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?auto=format&fit=crop&w=1400&q=85",
    "LH8": "https://images.unsplash.com/photo-1565182999561-18d7dc61c393?auto=format&fit=crop&w=1400&q=85",
    "대방": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1400&q=85",
    "중흥": "https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1400&q=85",
    "default": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1400&q=85"
}

def create_complex_image(complex_name, dong="", output_filename="complex.jpg", bg_key="default"):
    bg_url = BASE_BACKGROUNDS.get(bg_key, BASE_BACKGROUNDS["default"])
    temp_bg = "temp_bg.jpg"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(bg_url, headers=headers)
    with urllib.request.urlopen(req) as resp, open(temp_bg, "wb") as f:
        f.write(resp.read())

    # Open and resize to standard 1200x800
    base_img = Image.open(temp_bg).convert("RGBA")
    base_img = base_img.resize((1200, 800), Image.Resampling.LANCZOS)

    # Create dark gradient overlay at the bottom and top
    overlay = Image.new("RGBA", (1200, 800), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Bottom dark gradient
    for y in range(400, 800):
        alpha = int(((y - 400) / 400) ** 1.3 * 220)
        draw_overlay.line([(0, y), (1200, y)], fill=(10, 20, 35, alpha))

    # Top subtle dark gradient
    for y in range(0, 180):
        alpha = int(((180 - y) / 180) ** 1.5 * 140)
        draw_overlay.line([(0, y), (1200, y)], fill=(10, 20, 35, alpha))

    # Composite gradient
    combined = Image.alpha_composite(base_img, overlay)
    draw = ImageDraw.Draw(combined)

    # Font setup
    font_path_bold = "C:/Windows/Fonts/malgunbd.ttf"
    font_path_reg = "C:/Windows/Fonts/malgun.ttf"

    font_badge = ImageFont.truetype(font_path_bold, 20)
    font_title = ImageFont.truetype(font_path_bold, 52)
    font_sub = ImageFont.truetype(font_path_reg, 24)
    font_watermark = ImageFont.truetype(font_path_bold, 20)

    # 1. Top Left Badge: [진주혁신도시 프리미엄 아파트]
    tag_text = "진주혁신도시 프리미엄 단지 전경"
    tag_bbox = font_badge.getbbox(tag_text)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_h = tag_bbox[3] - tag_bbox[1]

    # Draw rounded badge background
    badge_x0, badge_y0 = 60, 50
    badge_x1, badge_y1 = badge_x0 + tag_w + 36, badge_y0 + tag_h + 20
    draw.rounded_rectangle([badge_x0, badge_y0, badge_x1, badge_y1], radius=12, fill=(245, 158, 11, 230), outline=(255, 255, 255, 180), width=1)
    draw.text((badge_x0 + 18, badge_y0 + 10), tag_text, fill=(15, 23, 42, 255), font=font_badge)

    # 2. Main Title at Bottom Left
    full_title = f"{complex_name} {dong}".strip()
    title_y = 570

    # Glow shadow
    shadow_color = (0, 0, 0, 220)
    for ox, oy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3), (3, 0)]:
        draw.text((60 + ox, title_y + oy), full_title, fill=shadow_color, font=font_title)
    draw.text((60, title_y), full_title, fill=(255, 255, 255, 255), font=font_title)

    # Subtitle
    sub_text = "쾌적한 주거환경 · 명품 조경 단지 전경 | 실매물 현장안내"
    draw.text((60, title_y + 70), sub_text, fill=(226, 232, 240, 240), font=font_sub)

    # 3. Bottom Right Office Watermark Badge
    office_text = "진주퀸공인중개사사무소  |  055-761-7248"
    wm_bbox = font_watermark.getbbox(office_text)
    wm_w = wm_bbox[2] - wm_bbox[0]
    wm_h = wm_bbox[3] - wm_bbox[1]

    wm_x1, wm_y1 = 1140, 740
    wm_x0, wm_y0 = wm_x1 - wm_w - 36, wm_y1 - wm_h - 20
    draw.rounded_rectangle([wm_x0, wm_y0, wm_x1, wm_y1], radius=12, fill=(15, 23, 42, 220), outline=(217, 119, 6, 200), width=2)
    draw.text((wm_x0 + 18, wm_y0 + 10), office_text, fill=(251, 191, 36, 255), font=font_watermark)

    # Save
    out_path = os.path.join("images", "complexes", output_filename)
    final_rgb = combined.convert("RGB")
    final_rgb.save(out_path, "JPEG", quality=92)
    print(f"Generated: {out_path} for {full_title}")

    if os.path.exists(temp_bg):
        os.remove(temp_bg)

    return out_path

# Generate for Jinju Innovation complexes
create_complex_image("진주혁신더힐", "505동", "더힐_505동_전경.jpg", "더힐")
create_complex_image("라온프라이빗", "204동", "라온프라이빗_204동_전경.jpg", "라온")
create_complex_image("혁신도시LH8단지", "803동", "LH8단지_803동_전경.jpg", "LH8")
create_complex_image("진주혁신 대방노블랜드", "더센트럴", "대방노블랜드_전경.jpg", "대방")
create_complex_image("중흥S-클래스", "센트럴시티", "중흥S클래스_전경.jpg", "중흥")
create_complex_image("진주혁신도시", "아파트 단지 전경", "기본_아파트전경.jpg", "default")

