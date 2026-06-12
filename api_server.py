import os
import uuid

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

from intent_engine import IntentEngine
from router import route_task

from database import init_db, create_user, get_user, save_message, get_chat
from auth import hash_password, verify_password, create_access_token, decode_token


# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- FOLDERS ----------------
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
FRONTEND_DIR = "frontend"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- STATIC FILES (IMPORTANT FIX) ----------------
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")


# ---------------- INIT ----------------
init_db()
intent_engine = IntentEngine()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------------- HOME ----------------
@app.get("/")
def home():
    return FileResponse("frontend/chat.html")


# ---------------- AUTH ----------------
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):

    if get_user(username):
        return {"status": "error", "message": "User already exists"}

    hashed = hash_password(password)
    create_user(username, hashed)

    return {"status": "success"}


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    user = get_user(username)

    if not user:
        return {"status": "error", "message": "Invalid credentials"}

    user_id, uname, hashed = user

    if not verify_password(password, hashed):
        return {"status": "error", "message": "Invalid credentials"}

    token = create_access_token({"user_id": user_id})

    return {"access_token": token, "token_type": "bearer"}


# ---------------- USER ----------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- SAVE IMAGE ----------------
def save_image(file: UploadFile):
    ext = file.filename.split(".")[-1]
    name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, name)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path


# ---------------- MAIN EDIT ----------------
@app.post("/edit-image")
async def edit_image(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    token: str = Depends(oauth2_scheme)
):

    user_id = get_current_user(token)

    print("\n===== NEW REQUEST =====")
    print("Prompt:", prompt)

    image_path = save_image(image)

    save_message(user_id, "user", prompt, image_path=image_path)

    intent = intent_engine.parse(prompt)
    result_path = route_task(intent, image_path, prompt)

    save_message(user_id, "ai", "processed", output_path=result_path)

    return {
        "status": "success",
        "image": f"/outputs/{os.path.basename(result_path)}"
    }


# ---------------- CHAT HISTORY ----------------
@app.get("/chat-history")
def chat_history(token: str = Depends(oauth2_scheme)):

    user_id = get_current_user(token)

    return {
        "status": "success",
        "history": get_chat(user_id)
    }