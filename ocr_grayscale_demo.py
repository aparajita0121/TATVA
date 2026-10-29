
from pathlib import Path

from nutriscan.preprocess import load_image, preprocess_grayscale
from nutriscan.ocr import extract_text


image_path = Path("data/samples/nutrition_table.png")

img = load_image(str(image_path))
processed = preprocess_grayscale(img)

# Save the enhanced grayscale image
output_path = Path("data/processed/nutrition_grayscale.png")

import cv2
cv2.imwrite(str(output_path), processed)

# Test different OCR modes
for psm in [6, 11]:
    text = extract_text(processed, psm=psm)

    print(f"\n{'=' * 12} GRAYSCALE PSM {psm} {'=' * 12}")
    print(text)
