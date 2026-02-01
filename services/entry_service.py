import time
from database import SessionLocal
from models.entry_gate import EntryGate
from models.entry_log import EntryLog
from models.booking import Booking

def validate_entry(gate_id, qr_token, quantity=1):
    db = SessionLocal()

    gate = db.query(EntryGate).filter(EntryGate.id == gate_id).first()
    if not gate:
        db.close()
        return False, "Invalid gate"

    if gate.current_qr_token != qr_token:
        db.close()
        return False, "Invalid token"

    if gate.token_expiry < int(time.time()):
        db.close()
        return False, "Token expired"

    booking = (
        db.query(Booking)
        .join(EntryLog, isouter=True)
        .filter(Booking.id == gate.event_id)
        .first()
    )

    used_qty = sum(log.quantity_used for log in booking.entry_logs)
    remaining = booking.booked_quantity - used_qty

    if remaining < quantity:
        db.close()
        return False, "Quota exceeded"

    log = EntryLog(
        booking_id=booking.id,
        gate_id=gate.id,
        quantity_used=quantity,
        entry_time=int(time.time()),
        status="success"
    )

    db.add(log)
    db.commit()
    db.close()

    return True, "Entry allowed"
