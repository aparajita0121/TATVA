
from pathlib import Path

import cv2
from nutriscan.preprocess import load_image, preprocess_image
from nutriscan.ocr import extract_text


image_path = Path("data/samples/nutrition_table.png")

img = load_image(str(image_path))
processed = preprocess_image(img)

# Save the processed table so we can inspect it
cv2.imwrite(
    "data/processed/nutrition_table_processed.png",
    processed
)

# Compare OCR modes on the table alone
for psm in [6, 11, 12]:
    text = extract_text(processed, psm=psm)

    print(f"\n{'=' * 12} PSM {psm} {'=' * 12}")
    print(text)
