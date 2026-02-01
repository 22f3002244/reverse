from flask import Blueprint, jsonify

lister_bp = Blueprint("lister", __name__, url_prefix="/lister")

@lister_bp.get("/dashboard")
def dashboard():
    return jsonify({"message": "Lister dashboard"})
