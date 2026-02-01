from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Booking

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bookings_bp.post("/")
def create_booking():
    db = SessionLocal()
    data = request.json

    booking = Booking(
        user_id=data["user_id"],
        ticket_id=data["ticket_id"],
        booked_quantity=data["quantity"],
        amount_paid=data["amount"]
    )
    db.add(booking)
    db.commit()

    return jsonify({"booking_id": booking.id}), 201
