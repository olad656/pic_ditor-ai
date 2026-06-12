import cv2

def remove_background(image_path: str):
    img = cv2.imread(image_path)

    # SIMPLE placeholder (we upgrade later)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    output = cv2.bitwise_and(img, img, mask=mask)

    output_path = image_path.replace(".jpg", "_nobg.jpg")
    cv2.imwrite(output_path, output)

    return output_path