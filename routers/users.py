from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, dependencies, models

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user

@router.get("/me/events", response_model=List[schemas.RegistrationResponse])
def read_my_events(current_user: models.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
    # This relationship is already loaded if we use lazy='joined' or distinct query
    # But essentially we want current_user.registrations
    # However, registrations usually just link to event_id. We want the event details too.
    # In models.py: user.registrations links to Registration. Registration links to Event.
    return current_user.registrations
