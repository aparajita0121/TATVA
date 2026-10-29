
import cv2

from nutriscan.ocr_regions import extract_region_text
from nutriscan.llm_extractor import extract_with_llm
from nutriscan.llm_models import ExtractedNutrition


image_path = "data/processed/nutrition_row.png"

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(image_path)

ocr_text = extract_region_text(image)

print("\nOCR TEXT:")
print(ocr_text)

raw_result = extract_with_llm(ocr_text)

nutrition = ExtractedNutrition.model_validate(raw_result)

print("\nVALIDATED RESULT:")
print(nutrition.model_dump_json(indent=2))
