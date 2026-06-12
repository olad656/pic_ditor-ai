import cv2

def edit_text(image_path: str, intent: dict):
    img = cv2.imread(image_path)

    # placeholder (real OCR text editing comes later)
    result = cv2.putText(
        img,
        "EDITED",
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    output_path = image_path.replace(".jpg", "_text.jpg")
    cv2.imwrite(output_path, result)

    return output_path