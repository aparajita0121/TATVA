
from pathlib import Path

from nutriscan.preprocess import load_image, preprocess_image
from nutriscan.ocr import extract_text


image_path = Path("data/samples/label_02.jpg")

img = load_image(str(image_path))
processed = preprocess_image(img)

for psm in [6, 11, 12]:
    text = extract_text(processed, psm=psm)

    print(f"\n{'=' * 15} PSM {psm} {'=' * 15}")
    print(text)

    output_path = Path(f"data/processed/label_text_psm{psm}.txt")
    output_path.write_text(text, encoding="utf-8")

    print("Saved to:", output_path)
