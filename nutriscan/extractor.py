
import re


NUTRIENT_PATTERNS = [
    ("Added Sugars", r"added\s+sugars?"),
    ("Total Sugars", r"total\s+sugars?"),
    ("Saturated Fat", r"saturated\s+fat"),
    ("Trans Fat", r"trans\s+fat"),
    ("Total Fat", r"total\s+fat"),
    ("Carbohydrate", r"carbohydrates?"),
    ("Protein", r"protein"),
    ("Energy", r"energy"),
    ("Sodium", r"sodium"),
]


def extract_nutrition_rows(text: str) -> list[dict]:
    """Extract nutrient values and RDA percentages from OCR lines."""

    results = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        nutrient = None
        remaining = line

        # Match the most specific nutrient name first.
        for name, pattern in NUTRIENT_PATTERNS:
            match = re.search(pattern, line, re.IGNORECASE)

            if match:
                nutrient = name
                remaining = line[match.end():]
                break

        if nutrient is None:
            continue

        # Handle saturated fat when its value is on the next line.
        if nutrient == "Saturated Fat":
            results.append(extract_saturated_fat_block(text))
            continue

        # Extract numeric values and optional units.
        matches = re.findall(
            r"(?<!\w)(\d+(?:\.\d+)?)\s*(kcal|mg|g|%)?",
            remaining,
            re.IGNORECASE
        )

        value = None
        unit = None
        rda_percent = None

        for number, detected_unit in matches:
            detected_unit = detected_unit.lower()

            if detected_unit == "%":
                rda_percent = float(number)

            elif detected_unit in ("kcal", "mg", "g"):
                if value is None:
                    value = float(number)
                    unit = detected_unit

        results.append({
            "nutrient": nutrient,
            "value": value,
            "unit": unit,
            "rda_percent": rda_percent,
            "raw_text": line,
        })

    return results


def extract_saturated_fat_block(text: str) -> dict:
    """Extract saturated-fat values without borrowing the row above."""

    lines = text.splitlines()

    for index, line in enumerate(lines):
        if re.search(r"saturated\s+fat", line, re.IGNORECASE):

            # Inspect only the saturated-fat line and the line below.
            block = "\n".join(lines[index:index + 2])

            # OCR may misread the unit 'g' as '9'.
            value_match = re.search(
                r"(\d+(?:\.\d+)?)\s*(?:g|9)\b",
                block,
                re.IGNORECASE
            )

            percentages = re.findall(
                r"(\d+(?:\.\d+)?)\s*%",
                block
            )

            value = (
                float(value_match.group(1))
                if value_match else None
            )

            rda_percent = (
                float(percentages[0])
                if len(percentages) == 1 else None
            )

            return {
                "nutrient": "Saturated Fat",
                "value": value,
                "unit": "g" if value is not None else None,
                "rda_percent": rda_percent,
                "raw_text": block,
            }

    return {
        "nutrient": "Saturated Fat",
        "value": None,
        "unit": None,
        "rda_percent": None,
        "raw_text": "",
    }
