from database import SessionLocal
from models.refund import RefundSupport

def request_refund(user_id, booking_id):
    db = SessionLocal()

    existing = (
        db.query(RefundSupport)
        .filter(RefundSupport.booking_id == booking_id)
        .first()
    )

    if existing:
        db.close()
        raise ValueError("Refund already exists")

    refund = RefundSupport(
        user_id=user_id,
        booking_id=booking_id,
        status="requested"
    )

    db.add(refund)
    db.commit()
    db.refresh(refund)
    db.close()

    return refund
