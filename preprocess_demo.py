
from pathlib import Path

import cv2

from nutriscan.preprocess import load_image, preprocess_image


# Path to the original food-label image
image_path = Path("data/samples/label_01.jpg")

# Load the original image
img = load_image(str(image_path))

print("Original image shape:", img.shape)

# Prepare the image for OCR
processed = preprocess_image(img)

print("Processed image shape:", processed.shape)

# Save the processed image
output_path = Path("data/processed/label_preprocessed.png")

success = cv2.imwrite(str(output_path), processed)

if success:
    print("Preprocessed image saved successfully!")
    print("Location:", output_path)
else:
    print("Could not save the preprocessed image.")
