from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True)
    venue_city = Column(String(100), nullable=False)
    venue_name = Column(String(255), nullable=False)
    gmap_url = Column(String(500))
    venue_capacity = Column(Integer, nullable=False)

    events = relationship("Event", back_populates="venue")
