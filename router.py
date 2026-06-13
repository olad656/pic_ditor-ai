import os
import uuid

from rembg import remove
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------- INTENT NORMALIZER ----------------
def parse_intent(raw_intent):

    if not isinstance(raw_intent, dict):
        return {"task": "clarify"}

    return raw_intent


# ---------------- MAIN ROUTER ----------------
def route_task(intent, image_path, prompt):

    task = intent.get("task", "")

    print("ROUTER TASK:", task)

    # ---------------- SINGLE TASKS ----------------

    if task == "remove_background":
        return remove_bg(image_path)

    if task == "enhance_image":
        return enhance(image_path)

    if task == "blur_object":
        return blur(image_path)

    if task == "sharpen_image":
        return sharpen(image_path)

    if task == "resize_image":
        return resize(image_path)

    if task == "cartoon_effect":
        return cartoon(image_path)

    # ---------------- MULTI STEP PIPELINE ----------------

    if task == "pipeline":

        current = image_path

        for step in intent.get("steps", []):

            op = step.get("operation", "")

            print("PIPELINE STEP:", op)

            if op == "background.remove":
                current = remove_bg(current)

            elif op == "image.enhance":
                current = enhance(current)

            elif op == "image.blur":
                current = blur(current)

            elif op == "image.sharpen":
                current = sharpen(current)

            elif op == "resize":
                current = resize(current)

            elif op == "style.cartoon":
                current = cartoon(current)

        return current

    print("UNKNOWN TASK - RETURNING ORIGINAL")

    return image_path


# ---------------- IMAGE HELPERS ----------------

def load(path):
    return Image.open(path)


def save(img):

    filename = f"{uuid.uuid4()}.png"

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    img.save(output_path)

    print("SAVED:", output_path)

    return output_path


# ---------------- OPERATIONS ----------------

def remove_bg(path):

    print("Removing background...")

    img = load(path).convert("RGBA")

    result = remove(img)

    return save(result)


def enhance(path):

    print("Enhancing image...")

    img = load(path)

    img = ImageEnhance.Contrast(img).enhance(1.3)

    img = ImageEnhance.Sharpness(img).enhance(1.2)

    return save(img)


def blur(path):

    print("Blurring image...")

    img = load(path)

    img = img.filter(ImageFilter.BLUR)

    return save(img)


def sharpen(path):

    print("Sharpening image...")

    img = load(path)

    img = img.filter(ImageFilter.SHARPEN)

    return save(img)


def resize(path):

    print("Resizing image...")

    img = load(path)

    img = img.resize((1024, 1024))

    return save(img)


def cartoon(path):

    print("Applying cartoon effect...")

    img = load(path)

    img = img.convert("RGB")

    img = img.filter(ImageFilter.CONTOUR)

    return save(img)