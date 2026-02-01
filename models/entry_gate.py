from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class EntryGate(Base):
    __tablename__ = "entry_gates"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    gate_name = Column(String(100), nullable=False)
    current_qr_token = Column(String(255), nullable=False)
    token_expiry = Column(Integer, nullable=False)

    event = relationship("Event", back_populates="entry_gates")
    entry_logs = relationship("EntryLog", back_populates="gate")
