import json
from pathlib import Path
from nutriscan.extractor import extract_nutrition_rows
from nutriscan.quality_check import check_nutrition_rows
ocr_path = Path("data/processed/selected_rows_ocr.txt")
output_path = Path("data/processed/nutrition_results.json")
if not ocr_path.exists():
    raise FileNotFoundError(f"OCR text not found: {ocr_path}")
ocr_text = ocr_path.read_text(encoding="utf-8")
rows = extract_nutrition_rows(ocr_text)
warnings = check_nutrition_rows(rows)
report = {
    "source_file": str(ocr_path),
    "nutrients": rows,
    "warnings": warnings,
    "ready_for_scoring": False,
}
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(
    json.dumps(report, indent=2, ensure_ascii=False),encoding="utf-8")
print("\n========== EXTRACTION SUMMARY ==========\n")
print(f"Nutrient rows detected: {len(rows)}")
for row in rows:
    print(
        f"{row['nutrient']}: "
        f"{row['value']} {row['unit'] or ''}"
    )
print("\n========== QUALITY WARNINGS ==========\n")
if warnings:
    for warning in warnings:
        print("-", warning)
else:
    print("No basic data-quality warnings.")
print(f"\nJSON report saved to: {output_path}")
print("Ready for scoring: No")