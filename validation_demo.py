
from nutriscan.validation import validate_source_values


ocr_text = "| Energy | 546 kcal | 5% |"

nutrition_data = {
    "energy": {
        "value": 546,
        "unit": "kcal",
        "basis": "unknown"
    },
    "protein": {
        "value": 0.7,
        "unit": "g",
        "basis": "unknown"
    }
}

warnings = validate_source_values(
    ocr_text,
    nutrition_data
)

print("\nSOURCE VALIDATION WARNINGS\n")

if warnings:
    for warning in warnings:
        print("-", warning)
else:
    print("All extracted values have source evidence.")
