'''
from pathlib import Path

import cv2

from nutriscan.ocr_regions import extract_region_text


image_path = Path("data/processed/nutrition_row.png")
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Image not found: {image_path}")

text = extract_region_text(image)

print("\n========== REGION OCR ==========\n")
print(text)
'''


from pathlib import Path

import cv2
import pytesseract

image_path = Path("data/processed/nutrition_row.png")

image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Could not load: {image_path}")

print("Image shape:", image.shape)
print("Pixel range:", image.min(), "to", image.max())

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save an enlarged version for visual inspection
enlarged = cv2.resize(
    gray,
    None,
    fx=4,
    fy=4,
    interpolation=cv2.INTER_CUBIC
)

cv2.imwrite(
    "data/processed/nutrition_row_debug.png",
    enlarged
)

# Test several OCR modes directly
for psm in [6, 7, 11, 13]:
    text = pytesseract.image_to_string(
        enlarged,
        config=f"--oem 3 --psm {psm}"
    )

    print(f"\n===== PSM {psm} =====")
    print(repr(text))
