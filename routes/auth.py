from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
    db = SessionLocal()
    data = request.json

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data["password"],  # hash later
        is_lister=data.get("is_lister", False)
    )
    db.add(user)
    db.commit()

    return jsonify({"message": "User registered"}), 201



