import os
import uuid
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------- MAIN ENTRY ----------------
def route_task(intent, image_path, prompt):

    if intent.get("task") != "pipeline":
        return image_path

    steps = intent.get("steps", [])

    current_path = image_path

    for step in steps:
        op = step.get("operation")

        if op == "background.remove":
            current_path = remove_bg(current_path)

        elif op == "image.enhance":
            current_path = enhance(current_path)

        elif op == "image.blur":
            current_path = blur(current_path)

        elif op == "image.sharpen":
            current_path = sharpen(current_path)

        elif op == "resize":
            current_path = resize(current_path)

        elif op == "style.cartoon":
            current_path = cartoon(current_path)

    return current_path


# ---------------- HELPERS ----------------
def load(img_path):
    return Image.open(img_path)


def save(img):
    path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.png")
    img.save(path)
    return path


# ---------------- OPERATIONS ----------------

def remove_bg(path):
    img = load(path).convert("RGBA")
    out = remove(img)
    return save(out)


def enhance(path):
    img = load(path)
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    return save(img)


def blur(path):
    img = load(path).filter(ImageFilter.BLUR)
    return save(img)


def sharpen(path):
    img = load(path).filter(ImageFilter.SHARPEN)
    return save(img)


def resize(path):
    img = load(path)
    img = img.resize((1024, 1024))
    return save(img)


def cartoon(path):
    img = load(path)
    img = img.convert("RGB").filter(ImageFilter.CONTOUR)
    return save(img)