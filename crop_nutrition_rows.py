
from pathlib import Path

import cv2

from nutriscan.preprocess import load_image


image_path = Path("data/samples/nutrition_table.png")
img = load_image(str(image_path))

print("Image dimensions:", img.shape)

# Open a window where you can select the nutrition table rows
region = cv2.selectROI(
    "Select a nutrition row",
    img,
    showCrosshair=True,
    fromCenter=False
)

cv2.destroyAllWindows()

x, y, width, height = region

if width == 0 or height == 0:
    print("No region selected.")
else:
    cropped = img[y:y + height, x:x + width]

    output_path = Path("data/processed/nutrition_row.png")
    cv2.imwrite(str(output_path), cropped)

    print("Saved crop to:", output_path)
    print("Crop dimensions:", cropped.shape)
