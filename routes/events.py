from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Event

events_bp = Blueprint("events", __name__, url_prefix="/events")

@events_bp.post("/")
def create_event():
    db = SessionLocal()
    data = request.json

    event = Event(
        event_name=data["event_name"],
        event_date=data["event_date"],
        event_time=data["event_time"],
        venue_id=data["venue_id"]
    )
    db.add(event)
    db.commit()

    return jsonify({"id": event.id}), 201


@events_bp.get("/")
def list_events():
    db = SessionLocal()
    events = db.query(Event).all()

    return jsonify([
        {"id": e.id, "name": e.event_name}
        for e in events
    ])
