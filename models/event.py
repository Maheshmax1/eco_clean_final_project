from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    event_date = Column(String)  # Storing as string for simplicity, or use Date
    start_time = Column(String)
    end_time = Column(String)
    image_url = Column(String)
    status = Column(String, default="upcoming")  # "upcoming", "completed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    registrations = relationship("Registration", back_populates="event")
