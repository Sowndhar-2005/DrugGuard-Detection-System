"""
pdf_to_md.py
Converts a PDF to Markdown using PyMuPDF (fitz).
- Extracts text with basic formatting (headings, paragraphs)
- Extracts all embedded images and saves to algospeak_media/
- Embeds image references in the Markdown output
"""

# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF
import os
import re

PDF_PATH = "algospeak..pdf"
MD_PATH = "algospeak.md"
MEDIA_DIR = "algospeak_media"

os.makedirs(MEDIA_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
md_lines = []
image_counter = 0

print(f"Processing {len(doc)} pages...")

for page_num, page in enumerate(doc, start=1):
    print(f"  Page {page_num}/{len(doc)}...", end="\r")

    # ── Extract images ──────────────────────────────────────
    image_list = page.get_images(full=True)
    page_img_refs = {}

    for img_index, img in enumerate(image_list):
        xref = img[0]
        try:
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_ext = base_image["ext"]
            image_counter += 1
            img_filename = f"img_{image_counter:04d}.{img_ext}"
            img_path = os.path.join(MEDIA_DIR, img_filename)
            with open(img_path, "wb") as f:
                f.write(img_bytes)
            page_img_refs[xref] = img_filename
        except Exception:
            pass

    # ── Extract text blocks ─────────────────────────────────
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

    for block in blocks:
        if block["type"] == 1:
            # Image block — insert markdown image reference
            xref = block.get("xref", None)
            fname = page_img_refs.get(xref)
            if fname:
                md_lines.append(f"\n![Figure]({MEDIA_DIR}/{fname})\n")
            continue

        if block["type"] != 0:
            continue

        for line in block["lines"]:
            line_text = ""
            max_size = 0
            is_bold = False

            for span in line["spans"]:
                text = span["text"].strip()
                if not text:
                    continue
                size = span["size"]
                flags = span["flags"]
                bold = bool(flags & 2**4)  # bold flag

                if size > max_size:
                    max_size = size
                    is_bold = bold

                line_text += text + " "

            line_text = line_text.strip()
            if not line_text:
                continue

            # Heuristic heading detection based on font size
            if max_size >= 18:
                md_lines.append(f"\n# {line_text}\n")
            elif max_size >= 15:
                md_lines.append(f"\n## {line_text}\n")
            elif max_size >= 13:
                md_lines.append(f"\n### {line_text}\n")
            elif is_bold and max_size >= 11:
                md_lines.append(f"\n**{line_text}**\n")
            else:
                md_lines.append(line_text + "  ")

    md_lines.append("\n\n---\n")  # page separator

doc.close()

# ── Write Markdown file ─────────────────────────────────────
markdown_content = "\n".join(md_lines)

# Clean up excessive blank lines
markdown_content = re.sub(r'\n{4,}', '\n\n', markdown_content)

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"\nDone!")
print(f"   Markdown  -> {MD_PATH}")
print(f"   Images    -> {MEDIA_DIR}/ ({image_counter} images extracted)")
