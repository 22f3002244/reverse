from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class EntryLog(Base):
    __tablename__ = "entry_logs"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    gate_id = Column(Integer, ForeignKey("entry_gates.id"), nullable=False)

    quantity_used = Column(Integer, nullable=False)
    entry_time = Column(Integer, nullable=False)

    status = Column(
        Enum("success", "denied", name="entry_status"),
        nullable=False
    )

    booking = relationship("Booking", back_populates="entry_logs")
    gate = relationship("EntryGate", back_populates="entry_logs")
