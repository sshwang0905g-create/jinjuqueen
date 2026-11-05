import sys
from PIL import Image, ImageDraw, ImageFont

def create_fresh_spacious_youtube_banner():
    # YouTube recommended banner specs
    W, H = 2560, 1440
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2   # 507
    safe_y1 = (H - safe_h) // 2   # 508
    safe_x2 = safe_x1 + safe_w    # 2053
    safe_y2 = safe_y1 + safe_h    # 931

    # Exact YouTube Dark Theme Base Background: RGB(15, 15, 15)
    YT_BG = (15, 15, 15)

    img = Image.new('RGB', (W, H), YT_BG)
    draw = ImageDraw.Draw(img)

    # Ambient Fresh Glow in the center (Deep Sapphire / Elegant Navy radial tint)
    # This brings freshness and vibrancy instead of a dull flat black, while blending seamlessly to (15,15,15) at edges
    center_x = (safe_x1 + safe_x2) // 2
    center_y = (safe_y1 + safe_y2) // 2

    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Soft ambient horizontal wash across the safe area
    for x in range(safe_x1 - 100, safe_x2 + 100):
        rel = (x - safe_x1) / safe_w
        factor = 1.0 - abs(rel - 0.5) * 1.8
        factor = max(0.0, min(1.0, factor))
        # Crisp deep oceanic sapphire ambient glow
        alpha = int(55 * factor)
        overlay_draw.line([(x, safe_y1 - 40), (x, safe_y2 + 40)], fill=(15, 30, 58, alpha))

    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Fonts - Larger & More Confident
    font_path_bd = "C:/Windows/Fonts/malgunbd.ttf"
    font_path_reg = "C:/Windows/Fonts/malgun.ttf"

    font_title = ImageFont.truetype(font_path_bd, 82)
    font_sub = ImageFont.truetype(font_path_bd, 32)
    font_phone = ImageFont.truetype(font_path_bd, 46)
    font_btn_label = ImageFont.truetype(font_path_bd, 28)

    # Fresh Luxury Gold Palette
    gold_bright = (255, 222, 115)
    gold_rich = (220, 180, 60)
    text_white = (255, 255, 255)
    text_sub = (195, 215, 235)

    # 1. Place Golden Logo - Larger (210px) with Breathing Space
    logo_size = 210
    try:
        logo_img = Image.open("images/logo.png").convert("RGBA")
        logo_resized = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        logo_x = safe_x1 + 80
        logo_y = safe_y1 + (safe_h - logo_size) // 2 - 5
        img.paste(logo_resized, (logo_x, logo_y), logo_resized)
    except Exception as e:
        print(f"Logo error: {e}")
        logo_x = safe_x1 + 80
        logo_size = 0

    # 2. Text layout - Big, Bold, Fresh & Spacious
    content_x = logo_x + logo_size + 65

    # Main Brand Title (Large 82pt bold)
    title_text = "진주퀸공인중개사"
    title_y = safe_y1 + 55
    draw.text((content_x, title_y), title_text, font=font_title, fill=text_white)

    # Subtitle with Fresh Accent Color
    sub_text = "진주 혁신도시 아파트 · 상가 · 오피스텔 · 토지 전문"
    sub_y = title_y + 105
    draw.text((content_x, sub_y), sub_text, font=font_sub, fill=text_sub)

    # Fresh Golden Pill Button with 055-761-7248
    btn_y = sub_y + 60
    btn_text = "055-761-7248"
    
    # Measure dimensions
    bbox_label = font_btn_label.getbbox("상담 문의")
    bbox_phone = font_phone.getbbox(btn_text)
    
    label_w = bbox_label[2] - bbox_label[0]
    phone_w = bbox_phone[2] - bbox_phone[0]
    
    btn_w = label_w + phone_w + 90
    btn_h = 76
    
    # Gradient / Glowing rounded rectangle
    draw.rounded_rectangle(
        [content_x, btn_y, content_x + btn_w, btn_y + btn_h],
        radius=38,
        fill=(22, 28, 40),
        outline=gold_rich,
        width=3
    )
    
    # Inner Badge for "상담 문의"
    draw.rounded_rectangle(
        [content_x + 8, btn_y + 8, content_x + label_w + 35, btn_y + btn_h - 8],
        radius=30,
        fill=(35, 48, 72)
    )
    draw.text((content_x + 22, btn_y + 20), "상담 문의", font=font_btn_label, fill=gold_bright)
    
    # Phone Number in Crisp Bright Gold/White
    draw.text((content_x + label_w + 55, btn_y + 11), btn_text, font=font_phone, fill=text_white)

    # Save final high-res fresh banner
    output_path = "images/youtube-channel-banner-2560.jpg"
    img.save(output_path, "JPEG", quality=98)
    print(f"Successfully generated Fresh Spacious YouTube Banner: {output_path}")

if __name__ == "__main__":
    create_fresh_spacious_youtube_banner()
