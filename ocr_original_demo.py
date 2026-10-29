
from pathlib import Path

import cv2
from nutriscan.preprocess import load_image
from nutriscan.ocr import extract_text


image_path = Path("data/samples/nutrition_table.png")

# Load the nutrition table
img = load_image(str(image_path))

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Enlarge the image 3 times
enlarged = cv2.resize(
    gray,
    None,
    fx=3,
    fy=3,
    interpolation=cv2.INTER_CUBIC
)

# Save the enlarged grayscale image
cv2.imwrite(
    "data/processed/nutrition_original_gray.png",
    enlarged
)

# Compare two OCR modes
for psm in [6, 11]:
    text = extract_text(enlarged, psm=psm)

    print(f"\n{'=' * 12} ORIGINAL GRAYSCALE PSM {psm} {'=' * 12}")
    print(text)

    Path(
        f"data/processed/nutrition_original_psm{psm}.txt"
    ).write_text(text, encoding="utf-8")
