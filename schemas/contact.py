from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContactMessageCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    category: str
    subject: str
    message: str
    priority: str = "medium"

class ContactMessageResponse(ContactMessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
