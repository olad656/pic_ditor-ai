import cv2

def enhance_image(image_path: str):
    img = cv2.imread(image_path)

    # simple lightweight enhancement
    enhanced = cv2.convertScaleAbs(img, alpha=1.2, beta=20)

    output_path = image_path.replace(".jpg", "_enhanced.jpg")
    cv2.imwrite(output_path, enhanced)

    return output_path