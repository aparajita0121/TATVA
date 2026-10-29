
import cv2
import numpy as np
import pytesseract


def extract_region_text(image: np.ndarray) -> str:
    """Extract text from a cropped nutrition-table row."""

    # Convert the image to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Enlarge the row to preserve small characters
    enlarged = cv2.resize(
        gray,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # Adaptive thresholding worked best in our Protein-row test
    processed = cv2.adaptiveThreshold(
        enlarged,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    # Save the processed crop for inspection
    cv2.imwrite(
        "data/processed/last_row_processed.png",
        processed
    )

    # PSM 6 correctly recognized the tested Protein row
    text = pytesseract.image_to_string(
        processed,
        config="--oem 3 --psm 6 -c preserve_interword_spaces=1"
    )

    return text.strip()
