from database import SessionLocal
from models.user import User
from utils.security import create_token

def authenticate_user(email: str, password: str):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user:
        return None

    # NOTE: replace with hash check later
    if user.password != password:
        return None

    return create_token(user)
