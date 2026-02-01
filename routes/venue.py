from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Venue

venue_bp = Blueprint("venue", __name__, url_prefix="/venues")

@venue_bp.post("/")
def create_venue():
    db = SessionLocal()
    data = request.json

    venue = Venue(
        venue_name=data["venue_name"],
        venue_city=data["venue_city"],
        venue_capacity=data["venue_capacity"]
    )
    db.add(venue)
    db.commit()

    return jsonify({"id": venue.id}), 201
