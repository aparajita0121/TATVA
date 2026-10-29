
import cv2
import pytesseract


def test_ocr_methods(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Method 1: Original grayscale, enlarged
    enlarged = cv2.resize(
        gray,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # Method 2: Otsu thresholding
    _, otsu = cv2.threshold(
        enlarged,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Method 3: Adaptive thresholding
    adaptive = cv2.adaptiveThreshold(
        enlarged,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    methods = {
        "grayscale": enlarged,
        "otsu": otsu,
        "adaptive": adaptive
    }

    for name, processed in methods.items():
        cv2.imwrite(
            f"data/processed/protein_{name}.png",
            processed
        )

        for psm in [6, 7, 11]:
            text = pytesseract.image_to_string(
                processed,
                config=(
                    f"--oem 3 --psm {psm} "
                    "-c preserve_interword_spaces=1"
                )
            )

            print(f"\n===== {name.upper()} / PSM {psm} =====")
            print(repr(text.strip()))


if __name__ == "__main__":
    test_ocr_methods("data/processed/nutrition_row.png")
