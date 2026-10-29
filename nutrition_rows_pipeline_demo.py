
from pathlib import Path

import cv2

from nutriscan.ocr_regions import extract_region_text
from nutriscan.llm_extractor import extract_with_llm
from nutriscan.llm_models import ExtractedNutrition
from nutriscan.validation import validate_source_values


IMAGE_PATH = "data/samples/nutrition_table.png"


def main():
    image = cv2.imread(IMAGE_PATH)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {IMAGE_PATH}"
        )

    extracted_rows = []

    print("\nTATVA: NUTRITION ROW OCR")
    print("Select one complete nutrition row at a time.")
    print("Press ENTER to confirm each crop.")
    print("Press ESC when you have finished selecting rows.\n")

    while True:
        roi = cv2.selectROI(
            "Select nutrition row - ESC to finish",
            image,
            showCrosshair=True,
            fromCenter=False
        )

        x, y, width, height = roi

        if width == 0 or height == 0:
            break

        row_image = image[y:y + height, x:x + width]

        row_text = extract_region_text(row_image)

        if row_text.strip():
            extracted_rows.append(row_text)
            print(f"\nRecognized row {len(extracted_rows)}:")
            print(row_text)
        else:
            print("\nNo text recognized in this crop.")

    cv2.destroyAllWindows()

    if not extracted_rows:
        print("\nNo rows were extracted. Nothing to analyze.")
        return

    combined_text = "\n".join(extracted_rows)

    output_path = Path("data/processed/selected_rows_ocr.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(combined_text, encoding="utf-8")

    print("\n========== COMBINED OCR TEXT ==========\n")
    print(combined_text)

    print("\nSending extracted text to the local LLM...")

    raw_result = extract_with_llm(combined_text)
    nutrition = ExtractedNutrition.model_validate(raw_result)
    nutrition_data = nutrition.model_dump()

    warnings = validate_source_values(
        combined_text,
        nutrition_data
    )

    print("\n========== NUTRITION DATA ==========\n")
    print(nutrition.model_dump_json(indent=2))

    print("\n========== WARNINGS ==========\n")

    numeric_values = [
        details["value"]
        for key, details in nutrition_data.items()
        if isinstance(details, dict)
        and details.get("value") is not None
    ]

    if not numeric_values:
        print("No numeric nutrition values were extracted.")

    if warnings:
        for warning in warnings:
            print("-", warning)
    elif numeric_values:
        print("No source-number warnings.")

    print(f"\nOCR text saved to: {output_path}")


if __name__ == "__main__":
    main()
