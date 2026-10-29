
import cv2
import pytesseract
import numpy as np


def extract_text(img: np.ndarray, psm: int = 6) -> str:
    """Extract text from a food-label image."""

    config = f"--oem 3 --psm {psm}"

    text = pytesseract.image_to_string(
        img,
        config=config
    )

    return text.strip()
