
from nutriscan.llm_extractor import extract_with_llm
from nutriscan.llm_models import ExtractedNutrition


sample_ocr = """
NUTRITIONAL INFORMATION

Serving size: 20 g

Nutrients | Per 100 g | %RDA Per Serve
Energy | 546 kcal | 5%
Protein | 0.7 g | 1%
Total Fat | 14.9 g | 14%
Saturated Fat | 7.6 g | 7%
"""

try:
    result = extract_with_llm(sample_ocr)
    nutrition = ExtractedNutrition.model_validate(result)

    print("\nLLM EXTRACTION TEST\n")
    print(nutrition.model_dump_json(indent=2))

except Exception as error:
    print("Test failed:", error)
