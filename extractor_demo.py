
from nutriscan.extractor import extract_nutrition_rows
from nutriscan.models import NutritionRow


sample_text = """
Energy 546 kcal 5%
Protein 0.7 g 1%
Total Fat 14.9 g 14%
Saturated Fat 7.6 g 7%
Carbohydrate 12.2 g
Sodium
"""

results = extract_nutrition_rows(sample_text)

print("\nEXTRACTED NUTRITION DATA\n")

for item in results:
    row = NutritionRow(**item)
    print(row.model_dump())
