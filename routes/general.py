from flask import Blueprint, jsonify

general_bp = Blueprint("general", __name__)

@general_bp.get("/health")
def health():
    return jsonify({"status": "ok"})
