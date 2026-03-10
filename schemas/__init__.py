from .user import UserBase, UserCreate, UserLogin, UserResponse, UserWithEvents
from .user import UserBase, UserCreate, UserLogin, UserResponse, UserWithEvents
from .event import EventBase, EventCreate, EventUpdate, EventStatusUpdate, EventResponse, EventWithRegistrations
from .registration import RegistrationBase, RegistrationCreate, RegistrationResponse, RegistrationWithUser
from .contact import ContactMessageCreate, ContactMessageResponse
from .token import Token, TokenData

# Fix forward references for Pydantic v2
try:
    UserWithEvents.model_rebuild()
    EventWithRegistrations.model_rebuild()
    RegistrationResponse.model_rebuild()
    RegistrationWithUser.model_rebuild()
except AttributeError:
    # Pydantic v1 compatibility
    UserWithEvents.update_forward_refs(RegistrationResponse=RegistrationResponse)
    EventWithRegistrations.update_forward_refs(RegistrationWithUser=RegistrationWithUser)
    RegistrationResponse.update_forward_refs(EventResponse=EventResponse)
    RegistrationWithUser.update_forward_refs(UserResponse=UserResponse)
