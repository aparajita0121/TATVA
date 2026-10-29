
from pathlib import Path

from nutriscan.extractor import extract_nutrition_rows


ocr_path = Path("data/processed/selected_rows_ocr.txt")

if not ocr_path.exists():
    raise FileNotFoundError(
        f"OCR text not found: {ocr_path}"
    )

text = ocr_path.read_text(encoding="utf-8")

rows = extract_nutrition_rows(text)

print("\n========== FORMATTED NUTRITION TABLE ==========\n")

if not rows:
    print("No recognizable nutrient rows found.")

for row in rows:
    print(
        f"{row['nutrient']:<16} | "
        f"Value: {row['value']} "
        f"{row['unit'] or ''} | "
        f"RDA: {row['rda_percent']}%"
    )
