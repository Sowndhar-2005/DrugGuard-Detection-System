import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
PAPER_IMG_DIR = os.path.join(BASE_DIR, "..", "paper", "image", "paper_image")

os.makedirs(ASSETS_DIR, exist_ok=True)

# Normalize space in warning .png
warn_space_path = os.path.join(ASSETS_DIR, "warning .png")
warn_clean_path = os.path.join(ASSETS_DIR, "warning.png")
if os.path.exists(warn_space_path) and not os.path.exists(warn_clean_path):
    shutil.copy(warn_space_path, warn_clean_path)
    print("Copied 'warning .png' -> 'warning.png'")

if os.path.exists(PAPER_IMG_DIR):
    for filename in os.listdir(PAPER_IMG_DIR):
        src_path = os.path.join(PAPER_IMG_DIR, filename)
        if os.path.isfile(src_path):
            clean_name = filename.lower().replace(" ", "_")
            dst_path = os.path.join(ASSETS_DIR, clean_name)
            shutil.copy(src_path, dst_path)
            dst_orig_path = os.path.join(ASSETS_DIR, filename)
            shutil.copy(src_path, dst_orig_path)
            print(f"Copied {filename} -> {clean_name}")

print("Assets directory synchronized successfully!")
