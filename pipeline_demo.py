
from pathlib import Path

from nutriscan.pipeline import analyze_label


image_path = Path("data/samples/nutrition_table.png")

try:
    result = analyze_label(str(image_path))

    print("\n========== RAW OCR TEXT ==========\n")
    print(result["raw_ocr_text"])

    print("\n========== NUTRITION DATA ==========\n")
    print(result["nutrition"])

    print("\n========== SOURCE WARNINGS ==========\n")

    if result["warnings"]:
        for warning in result["warnings"]:
            print("-", warning)
    else:
        print("No source-number warnings.")

except Exception as error:
    print("TATVA pipeline failed:", error)
