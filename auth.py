import jwt
import hashlib
import datetime
from fastapi import Header, HTTPException

SECRET = "supersecretkey"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    return hash_password(password) == hashed


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = authorization.split(" ")[1]
        data = decode_token(token)
        return data["user_id"]

    except:
        raise HTTPException(status_code=401, detail="Invalid token")