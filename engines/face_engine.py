import cv2
import numpy as np

def process_face(image_path: str, prompt: str):
    img = cv2.imread(image_path)

    # simple placeholder: brighten face area simulation
    result = cv2.convertScaleAbs(img, alpha=1.1, beta=10)

    output_path = image_path.replace(".jpg", "_face.jpg")
    cv2.imwrite(output_path, result)

    return output_path