
from pathlib import Path

import cv2

from nutriscan.preprocess import load_image, crop_image


# Load the sample food-label image
image_path = Path("data/samples/label_01.jpg")

img = load_image(str(image_path))

# Inspect image dimensions
height, width = img.shape[:2]

print("Image loaded successfully!")
print("Width:", width, "pixels")
print("Height:", height, "pixels")
print("Image shape:", img.shape)

# Crop the centre half of the image
top = height // 4
bottom = 3 * height // 4
left = width // 4
right = 3 * width // 4

cropped = crop_image(
    img,
    (top, bottom, left, right)
)

# Save the cropped image
output_path = Path("data/processed/label_crop.jpg")
cv2.imwrite(str(output_path), cropped)

print("Cropped image saved to:", output_path)
print("Cropped image shape:", cropped.shape)
