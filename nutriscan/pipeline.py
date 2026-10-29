
from pathlib import Path

from nutriscan.preprocess import load_image, preprocess_image
from nutriscan.ocr import extract_text
from nutriscan.llm_extractor import extract_with_llm
from nutriscan.llm_models import ExtractedNutrition
from nutriscan.validation import validate_source_values


def analyze_label(image_path: str) -> dict:
    """Run the TATVA image-to-nutrition pipeline."""

    image_file = Path(image_path)

    if not image_file.exists():
        raise FileNotFoundError(
            f"Image not found: {image_file}"
        )

    # 1. Load the image
    image = load_image(str(image_file))

    # 2. Preprocess the image
    processed_image = preprocess_image(image)

    # 3. Extract text with Tesseract
    raw_text = extract_text(processed_image, psm=11)

    if not raw_text.strip():
        raise ValueError(
            "OCR could not extract readable text."
        )

    # Save OCR output for debugging
    output_path = Path("data/processed/pipeline_ocr.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(raw_text, encoding="utf-8")

    # 4. Extract structured data with Ollama
    extracted_data = extract_with_llm(raw_text)

    # 5. Validate the response structure and types
    nutrition = ExtractedNutrition.model_validate(
        extracted_data
    )

    nutrition_data = nutrition.model_dump()

    # 6. Check whether numeric values have source evidence
    warnings = validate_source_values(
        raw_text,
        nutrition_data
    )

    return {
        "image_path": str(image_file),
        "raw_ocr_text": raw_text,
        "nutrition": nutrition_data,
        "warnings": warnings,
    }
