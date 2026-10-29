
EXPECTED_NUTRIENTS = [
    "Energy",
    "Protein",
    "Carbohydrate",
    "Total Sugars",
    "Added Sugars",
    "Total Fat",
    "Saturated Fat",
    "Trans Fat",
    "Sodium",
]


def check_nutrition_rows(rows: list[dict]) -> list[str]:
    """Return data-quality warnings for extracted nutrient rows."""

    warnings = []
    seen = set()

    for row in rows:
        nutrient = row.get("nutrient")
        value = row.get("value")
        unit = row.get("unit")

        if not nutrient:
            warnings.append("A row has no nutrient name.")
            continue

        if nutrient in seen:
            warnings.append(
                f"Duplicate nutrient detected: {nutrient}"
            )

        seen.add(nutrient)

        if value is None:
            warnings.append(
                f"{nutrient}: numeric value is missing."
            )
        elif not isinstance(value, (int, float)) or isinstance(
            value, bool
        ):
            warnings.append(
                f"{nutrient}: invalid numeric value."
            )
        elif value < 0:
            warnings.append(
                f"{nutrient}: negative value is invalid."
            )

        if value is not None and unit is None:
            warnings.append(
                f"{nutrient}: unit is missing."
            )

    for nutrient in EXPECTED_NUTRIENTS:
        if nutrient not in seen:
            warnings.append(
                f"{nutrient}: nutrient was not detected."
            )

    return warnings
