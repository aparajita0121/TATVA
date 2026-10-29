
from pathlib import Path

import cv2
import numpy as np


def load_image(path: str) -> np.ndarray:
    """Load an image and return it as an OpenCV array."""

    file = Path(path)

    if not file.exists():
        raise FileNotFoundError(f"No image found at: {file}")

    img = cv2.imread(str(file))

    if img is None:
        raise ValueError(f"OpenCV could not read the image: {file}")

    return img


def crop_image(img: np.ndarray, box: tuple) -> np.ndarray:
    """Crop an image using (top, bottom, left, right) coordinates."""

    top, bottom, left, right = box

    height, width = img.shape[:2]

    if not (0 <= top < bottom <= height and
            0 <= left < right <= width):
        raise ValueError("Crop coordinates are outside the image.")

    return img[top:bottom, left:right]



def preprocess_image(img: np.ndarray) -> np.ndarray:
    """Prepare an image for OCR."""

    # 1. Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Enlarge the image to make small text easier to read
    enlarged = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # 3. Improve contrast without immediately removing grayscale details
    enhanced = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    ).apply(enlarged)

    # 4. Reduce small visual noise
    denoised = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # 5. Convert to black and white using adaptive thresholding
    processed = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        7
    )

    return processed


def preprocess_grayscale(img: np.ndarray) -> np.ndarray:
    """Enlarge and enhance an image while preserving grayscale details."""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    enlarged = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    enhanced = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    ).apply(enlarged)

    return enhanced
