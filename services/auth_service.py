from database import SessionLocal
from models.user import User
from utils.security import create_token, verify_password

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return {
            "token": create_token(user),
            "user_id": user.id,
            "is_lister": user.is_lister
        }

    finally:
        db.close()
