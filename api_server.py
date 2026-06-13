import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from intent_engine import IntentEngine
from router import route_task

app = FastAPI()

# ---------------- STATIC FRONTEND ----------------
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

intent_engine = IntentEngine()


# ---------------- MAIN IMAGE EDIT ENDPOINT ----------------
@app.post("/edit-image")
async def edit_image(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):

    # save input image
    image_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.png")

    with open(image_path, "wb") as f:
        f.write(await image.read())

    # AI intent
    intent = intent_engine.parse(prompt)

    # run pipeline
    result_path = route_task(intent, image_path, prompt)

    return {
        "status": "success",
        "result": result_path
    }


# ---------------- SERVE UI ----------------
@app.get("/")
def home():
    return FileResponse("frontend/chat.html")