from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
# Backward compatibility or forward references might be needed
# from .registration import RegistrationResponse 

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    full_name: str
    phone: str
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    full_name: str
    phone: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserWithEvents(UserResponse):
    registrations: List['RegistrationResponse'] = [] # Forward reference
