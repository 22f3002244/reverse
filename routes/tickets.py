from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Ticket

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")

@tickets_bp.post("/")
def create_ticket():
    db = SessionLocal()
    data = request.json

    ticket = Ticket(
        event_id=data["event_id"],
        venue_id=data["venue_id"],
        ticket_category=data["category"],
        ticket_price=data["price"],
        ticket_quantity=data["quantity"]
    )
    db.add(ticket)
    db.commit()

    return jsonify({"id": ticket.id}), 201
