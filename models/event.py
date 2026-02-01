from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_image = Column(String(500))
    event_name = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=False)

    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)

    venue = relationship("Venue", back_populates="events")
    tickets = relationship("Ticket", back_populates="event")
    entry_gates = relationship("EntryGate", back_populates="event")
