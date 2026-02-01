from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)

    booked_quantity = Column(Integer, nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="bookings")
    ticket = relationship("Ticket", back_populates="bookings")
    entry_logs = relationship("EntryLog", back_populates="booking")
    refund = relationship("RefundSupport", uselist=False, back_populates="booking")
