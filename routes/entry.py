from flask import Blueprint, request, jsonify

entry_bp = Blueprint("entry", __name__, url_prefix="/entry")

@entry_bp.post("/scan")
def scan_qr():
    data = request.json
    token = data["qr_token"]

    # validation logic later
    return jsonify({"status": "success"})
