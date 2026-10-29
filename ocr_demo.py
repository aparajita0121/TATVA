
from pathlib import Path

from nutriscan.preprocess import load_image, preprocess_image
from nutriscan.ocr import extract_text


# Load the original food-label image
image_path = Path("data/samples/label_01.jpg")
img = load_image(str(image_path))

# Preprocess the image
processed = preprocess_image(img)

# Extract text using Tesseract
text = extract_text(processed)

# Display the result
print("\n========== EXTRACTED TEXT ==========\n")
print(text)
print("\n====================================")

# Save the extracted text for inspection
output_path = Path("data/processed/label_text.txt")
output_path.write_text(text, encoding="utf-8")

print("\nExtracted text saved to:", output_path)
