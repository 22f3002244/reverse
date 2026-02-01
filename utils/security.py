import jwt
import time
from functools import wraps
from flask import request
from database import SessionLocal
from models.user import User

SECRET_KEY = "change-this-secret"
ALGORITHM = "HS256"


def create_token(user):
    payload = {
        "sub": user.id,
        "is_lister": user.is_lister,
        "exp": int(time.time()) + 60 * 60 * 24  # 24h
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None

    token = auth.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None

    db = SessionLocal()
    user = db.query(User).get(payload["sub"])
    db.close()

    return user

def require_lister(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()

        if not user:
            return {"error": "Unauthorized"}, 401

        if not user.is_lister:
            return {"error": "Forbidden"}, 403

        return fn(user, *args, **kwargs)
    return wrapper


def require_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()

        if not user:
            return {"error": "Unauthorized"}, 401

        return fn(user, *args, **kwargs)
    return wrapper
