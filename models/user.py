from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_no = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    city = Column(String(100))

    is_lister = Column(Boolean, default=False)
    org_name = Column(String(255))

    bookings = relationship("Booking", back_populates="user")
