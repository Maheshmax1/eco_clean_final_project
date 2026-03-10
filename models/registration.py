from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="registered")

    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
