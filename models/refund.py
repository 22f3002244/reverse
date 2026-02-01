from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class RefundSupport(Base):
    __tablename__ = "refund_support"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)

    status = Column(
        Enum("requested", "approved", "rejected", "refunded", name="refund_status"),
        nullable=False
    )

    booking = relationship("Booking", back_populates="refund")
