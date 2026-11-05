import os
from PIL import Image, ImageEnhance, ImageFilter

def enhance_and_crop():
    # 1. Image 2: Lake Park Bench (Best Frontal Smile)
    img2 = Image.open('C:/Users/User/.gemini/antigravity/brain/22ad999b-b105-4739-9ac9-9c3b7b7fc818/.user_uploaded/media_1793855025577_87218d51.jpg')
    # Focus on CEO: x: 90 to 330, y: 95 to 410 (Square 300x300 roughly)
    # Head center is around (210, 240)
    box2 = (80, 100, 340, 420) # 260w x 320h
    crop2 = img2.crop(box2)
    
    # Square crop for profile: 260 x 260
    # Head at upper center
    sq_box2 = (80, 95, 340, 355) # 260 x 260
    crop2_sq = img2.crop(sq_box2)

    # Clean retouching: increase brightness, contrast, and subtle warmth
    def retouch(im):
        # Brightness +12%
        enh_b = ImageEnhance.Brightness(im)
        im = enh_b.enhance(1.10)
        # Contrast +8%
        enh_c = ImageEnhance.Contrast(im)
        im = enh_c.enhance(1.08)
        # Color vibrancy +10%
        enh_col = ImageEnhance.Color(im)
        im = enh_col.enhance(1.10)
        # Subtle sharpness
        enh_s = ImageEnhance.Sharpness(im)
        im = enh_s.enhance(1.25)
        return im

    retouched2_sq = retouch(crop2_sq)
    retouched2_sq = retouched2_sq.resize((600, 600), Image.Resampling.LANCZOS)
    retouched2_sq.save('images/ceo-real-lake-square.jpg', quality=95)

    retouched2_full = retouch(crop2)
    retouched2_full = retouched2_full.resize((600, 740), Image.Resampling.LANCZOS)
    retouched2_full.save('images/ceo-real-lake-portrait.jpg', quality=95)

    # 2. Image 1: Tree Avenue (Warm, Dignified Smile)
    img1 = Image.open('C:/Users/User/.gemini/antigravity/brain/22ad999b-b105-4739-9ac9-9c3b7b7fc818/.user_uploaded/media_1793854934961_0248d850.jpg')
    # CEO is on right: x roughly 370 to 600, y roughly 170 to 480
    sq_box1 = (370, 170, 600, 400) # 230 x 230
    crop1_sq = img1.crop(sq_box1)
    
    box1_full = (360, 160, 600, 480) # 240 x 320
    crop1_full = img1.crop(box1_full)

    retouched1_sq = retouch(crop1_sq)
    retouched1_sq = retouched1_sq.resize((600, 600), Image.Resampling.LANCZOS)
    retouched1_sq.save('images/ceo-real-tree-square.jpg', quality=95)

    retouched1_full = retouch(crop1_full)
    retouched1_full = retouched1_full.resize((600, 800), Image.Resampling.LANCZOS)
    retouched1_full.save('images/ceo-real-tree-portrait.jpg', quality=95)

    # Copy to artifacts directory for inline display
    artifact_dir = "C:/Users/User/.gemini/antigravity/brain/22ad999b-b105-4739-9ac9-9c3b7b7fc818"
    retouched2_sq.save(os.path.join(artifact_dir, "ceo-real-lake-square.jpg"), quality=95)
    retouched2_full.save(os.path.join(artifact_dir, "ceo-real-lake-portrait.jpg"), quality=95)
    retouched1_sq.save(os.path.join(artifact_dir, "ceo-real-tree-square.jpg"), quality=95)
    retouched1_full.save(os.path.join(artifact_dir, "ceo-real-tree-portrait.jpg"), quality=95)

    print("Successfully generated all real photo single profiles!")

if __name__ == "__main__":
    enhance_and_crop()

