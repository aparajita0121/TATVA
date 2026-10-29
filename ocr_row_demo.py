
from pathlib import Path

from nutriscan.preprocess import load_image, preprocess_grayscale
from nutriscan.ocr import extract_text


# Load the cropped nutrition row
image_path = Path("data/processed/nutrition_row.png")
img = load_image(str(image_path))

# Enhance the cropped row
processed = preprocess_grayscale(img)

# Save the enhanced row so we can inspect it
output_path = Path("data/processed/nutrition_row_enhanced.png")

import cv2
cv2.imwrite(str(output_path), processed)

print("Cropped row dimensions:", img.shape)

# Test different OCR modes
for psm in [6, 7, 8, 11, 13]:
    text = extract_text(processed, psm=psm)

    print(f"\n{'=' * 10} PSM {psm} {'=' * 10}")
    print(text)

