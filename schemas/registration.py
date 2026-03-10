from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .event import EventResponse
    from .user import UserResponse

class RegistrationBase(BaseModel):
    event_id: int

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    status: str
    registration_date: datetime
    # Use Optional and forward refs to avoid circular imports
    event: Optional['EventResponse'] = None 

    class Config:
        from_attributes = True

class RegistrationWithUser(RegistrationResponse):
    user: Optional['UserResponse'] = None

