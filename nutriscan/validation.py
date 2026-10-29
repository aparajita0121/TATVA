
import re


def validate_source_values(
    ocr_text: str,
    nutrition_data: dict
) -> list[str]:
    """
    Check whether extracted numeric values appear in OCR text.

    Returns a list of warnings for values that lack source evidence.
    """

    warnings = []

    # Extract numeric tokens from the OCR text.
    source_numbers = re.findall(
        r"\d+(?:\.\d+)?",
        ocr_text
    )

    source_numbers = {
        float(number) for number in source_numbers
    }

    for nutrient, details in nutrition_data.items():

        if not isinstance(details, dict):
            continue

        value = details.get("value")

        if value is None:
            continue

        if isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            warnings.append(
                f"{nutrient}: value is not numeric."
            )
            continue

        if float(value) not in source_numbers:
            warnings.append(
                f"{nutrient}: {value} was not found "
                "among the OCR numbers."
            )

    return warnings
