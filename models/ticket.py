from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    ticket_category = Column(String(100), nullable=False)
    ticket_price = Column(Numeric(10, 2), nullable=False)
    ticket_quantity = Column(Integer, nullable=False)
    discount = Column(Numeric(5, 2), default=0)

    event = relationship("Event", back_populates="tickets")
    bookings = relationship("Booking", back_populates="ticket")
