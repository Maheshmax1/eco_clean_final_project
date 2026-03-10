from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .registration import RegistrationWithUser

class EventBase(BaseModel):
    title: str
    description: str
    location: str
    event_date: str
    start_time: str
    end_time: str
    image_url: Optional[str] = None
    status: str = "upcoming"

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None

class EventStatusUpdate(BaseModel):
    status: str

class EventResponse(EventBase):
    id: int
    created_at: datetime
    is_registered: bool = False
    
    class Config:
        from_attributes = True

class EventWithRegistrations(EventResponse):
    registrations: List['RegistrationWithUser'] = []

