
import json
from pathlib import Path

from nutriscan.extractor import extract_nutrition_rows
from nutriscan.quality_check import check_nutrition_rows


def analyze_ocr_text(ocr_text: str) -> dict:
    """Parse OCR text and produce a quality-checked report."""

    if not ocr_text.strip():
        raise ValueError("OCR text is empty.")

    # Step 1: Parse the nutrient rows.
    nutrients = extract_nutrition_rows(ocr_text)

    # Step 2: Run basic data-quality checks.
    warnings = check_nutrition_rows(nutrients)

    # Step 3: Determine which nutrient rows need review.
    for nutrient in nutrients:
        nutrient["review_status"] = (
            "needs_review"
            if nutrient.get("value") is None
            or nutrient.get("unit") is None
            else "pending_verification"
        )

    # Step 4: Create the structured report.
    report = {
        "source": "OCR",
        "nutrients": nutrients,
        "warnings": warnings,
        "ready_for_scoring": False,
    }

    return report


def analyze_ocr_file(
    input_path: str,
    output_path: str = "data/processed/nutrition_results.json",
) -> dict:
    """Read OCR text, analyze it, and save a JSON report."""

    source = Path(input_path)
    destination = Path(output_path)

    if not source.exists():
        raise FileNotFoundError(
            f"OCR file not found: {source}"
        )

    ocr_text = source.read_text(encoding="utf-8")

    report = analyze_ocr_text(ocr_text)
    report["source_file"] = str(source)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    destination.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    report["output_file"] = str(destination.resolve())

    return report
