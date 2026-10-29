
from pydantic import ValidationError

from nutriscan.extractor import extract_nutrition_row
from nutriscan.models import NutritionRow


# Test with clean sample text
sample_text = "Energy 546 kcal 5%"

# Extract information from text
data = extract_nutrition_row(sample_text)

# Validate the extracted information
row = NutritionRow(**data)

print("VALIDATED NUTRITION DATA")
print(row.model_dump())


# Test whether invalid data is rejected
print("\nTESTING INVALID DATA")

try:
    NutritionRow(
        nutrient="Energy",
        value=-10,
        unit="kcal",
        rda_percent=5
    )
except ValidationError as error:
    print("Invalid data rejected successfully!")
    print(error)
