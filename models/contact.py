from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    category = Column(String)
    subject = Column(String)
    message = Column(Text)
    priority = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
