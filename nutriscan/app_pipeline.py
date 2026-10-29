
import re

import cv2
import numpy as np
import pytesseract

from nutriscan.llm_extractor import extract_with_llm


NUTRIENT_NAMES = [
    "energy",
    "protein",
    "carbohydrate",
    "total sugars",
    "added sugars",
    "total fat",
    "saturated fat",
    "trans fat",
    "sodium",
]


def score_ocr_text(text: str) -> int:
    """Estimate how useful an OCR result is for nutrition extraction."""

    normalized = text.lower()

    nutrient_matches = sum(
        1 for name in NUTRIENT_NAMES
        if name in normalized
    )

    numeric_matches = len(
        re.findall(r"\d+(?:[.,]\d+)?", text)
    )

    return nutrient_matches * 10 + min(numeric_matches, 30)


def analyze_uploaded_image(image_bytes: bytes) -> dict:
    """Run multiple OCR attempts and extract structured nutrition data."""

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Unable to decode the uploaded image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enlarge the image while preserving the original grayscale details.
    enlarged = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC,
    )

    # Try both grayscale and thresholded versions.
    _, otsu = cv2.threshold(
        enlarged,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    candidates = []

    for image_variant, variant_name in [
        (enlarged, "enlarged grayscale"),
        (otsu, "Otsu threshold"),
    ]:
        for psm in [6, 11]:
            text = pytesseract.image_to_string(
                image_variant,
                config=f"--oem 3 --psm {psm}",
            ).strip()

            candidates.append({
                "method": f"{variant_name}, PSM {psm}",
                "text": text,
                "score": score_ocr_text(text),
            })

    # Prefer the OCR result with the most useful label information.
    best = max(candidates, key=lambda item: item["score"])

    if not best["text"]:
        raise ValueError(
            "No text detected. Try a clearer image."
        )

    # Extract structured data using the existing local LLM.
    nutrition = extract_with_llm(best["text"])

    return {
        "ocr_text": best["text"],
        "ocr_method": best["method"],
        "ocr_score": best["score"],
        "nutrition": nutrition,
    }

    '''return {
        "nutrition" : nutrition,
        "ocr_text" : ocr_text,
        "ocr_method" : "Tesseract OCR"
    }'''
