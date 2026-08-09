import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAPER_IMG_DIR = os.path.join(BASE_DIR, "..", "paper", "image", "paper_image")
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

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

print("All paper diagram images copied to assets directory successfully!")
