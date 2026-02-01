from flask import Blueprint, jsonify
from database import SessionLocal
from models import User

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.get("/<int:user_id>")
def get_user(user_id):
    db = SessionLocal()
    user = db.query(User).get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": f"{user.first_name} {user.last_name}",
        "email": user.email
    })
