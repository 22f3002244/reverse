from database import SessionLocal
from models.booking import Booking
from models.ticket import Ticket
from decimal import Decimal

def create_booking(user_id, ticket_id, quantity):
    db = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        db.close()
        raise ValueError("Ticket not found")

    if ticket.ticket_quantity < quantity:
        db.close()
        raise ValueError("Insufficient tickets")

    price = ticket.ticket_price
    discount = ticket.discount or Decimal("0.00")

    final_price = (price - discount) * quantity

    booking = Booking(
        user_id=user_id,
        ticket_id=ticket_id,
        booked_quantity=quantity,
        amount_paid=final_price
    )

    ticket.ticket_quantity -= quantity

    db.add(booking)
    db.commit()
    db.refresh(booking)
    db.close()

    return booking
