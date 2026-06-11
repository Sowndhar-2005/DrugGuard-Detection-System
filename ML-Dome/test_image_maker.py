"""
test_image_maker.py
Generates drug_image.png and safe_image.png with embedded text to verify
the DrugGuard OCR scanning feature.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Get paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRUG_IMAGE_PATH = os.path.join(BASE_DIR, "drug_image.png")
SAFE_IMAGE_PATH = os.path.join(BASE_DIR, "safe_image.png")

# Standard Windows Font
FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None  # fallback to default font if not windows/missing

def create_text_image(filename, text_lines, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    # Create blank canvas
    width, height = 600, 250
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Load Font
    try:
        if FONT_PATH:
            font = ImageFont.truetype(FONT_PATH, size=22)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
        
    # Draw multiline text
    y_text = 40
    for line in text_lines:
        draw.text((30, y_text), line, font=font, fill=text_color)
        y_text += 35
        
    image.save(filename)
    print(f"Generated test image: {filename}")

if __name__ == "__main__":
    # 1. Illicit text (Drug sales flyer)
    drug_text = [
        "🔥 SPECIAL OFFER FOR TONIGHT 🔥",
        "High quality cocaine and powder available.",
        "Overnight shipping, discreet delivery.",
        "Contact supplier now: Wickr me at drugdealer99",
        "DM for bulk price discounts! Fast delivery."
    ]
    
    # 2. Safe text (Marketing flyer)
    safe_text = [
        "🍃 ORGANIC JAPANESE MATCHA TEA 🍃",
        "100% natural stone-ground green tea leaves.",
        "Rich in antioxidants, boosts energy and focus.",
        "Order now at www.matchatea-organic.com",
        "Get 15% discount on your first order!"
    ]
    
    create_text_image(DRUG_IMAGE_PATH, drug_text, bg_color=(253, 244, 245), text_color=(190, 24, 74)) # reddish style
    create_text_image(SAFE_IMAGE_PATH, safe_text, bg_color=(240, 253, 244), text_color=(21, 128, 61))  # greenish style
