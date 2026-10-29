from nutriscan.extractor import extract_nutrition_rows


sample_text = """
Energy | 546 kcal | 5%
Protein | 6.9 g
Carbohydrate | 54.9 g
Total Sugars | 1.1 g
Added Sugars | 0.7 g | 0.3%
Total Fat | 33.2 g | 10%
Saturated Fat
7.6 g | 7%
Trans Fat | 0.1 g | 1%
Sodium | 663 mg | 7%
"""

rows = extract_nutrition_rows(sample_text)

found = {row["nutrient"]: row for row in rows}

expected_values = {
    "Energy": 546.0,
    "Protein": 6.9,
    "Carbohydrate": 54.9,
    "Total Sugars": 1.1,
    "Added Sugars": 0.7,
    "Total Fat": 33.2,
    "Saturated Fat": 7.6,
    "Trans Fat": 0.1,
    "Sodium": 663.0,
}

print("\n========== PARSER REGRESSION TEST ==========\n")

failed = False

for nutrient, expected in expected_values.items():
    actual = found.get(nutrient, {}).get("value")

    if actual == expected:
        print(f"PASS: {nutrient} = {actual}")
    else:
        print(
            f"FAIL: {nutrient}: expected {expected}, "
            f"got {actual}"
        )
        failed = True

if failed:
    raise SystemExit(
        "\nSome parser tests failed. Fix the parser before proceeding."
    )

print("\nAll parser tests passed.")
