from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
import crud, schemas, dependencies, models

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/stats")
def get_dashboard_stats(current_user: models.User = Depends(dependencies.get_current_admin), db: Session = Depends(dependencies.get_db)):
    return crud.get_stats(db)

@router.get("/volunteers", response_model=List[schemas.UserResponse])
def get_volunteers(current_user: models.User = Depends(dependencies.get_current_admin), db: Session = Depends(dependencies.get_db)):
    # For now returning all users, assuming all non-admins are volunteers
    # Real implementation might filter by role="volunteer"
    users = db.query(models.User).filter(models.User.role == "volunteer").all()
    return users

@router.get("/messages", response_model=List[schemas.ContactMessageResponse])
def get_messages(current_user: models.User = Depends(dependencies.get_current_admin), db: Session = Depends(dependencies.get_db)):
    return crud.get_contact_messages(db)

@router.get("/event-registrations", response_model=List[schemas.EventWithRegistrations])
def get_event_registrations(current_user: models.User = Depends(dependencies.get_current_admin), db: Session = Depends(dependencies.get_db)):
    # Fetch all events with their registrations eagerly
    events = db.query(models.Event).all()
    return events

@router.delete("/messages/{message_id}")
def delete_message(message_id: int, current_user: models.User = Depends(dependencies.get_current_admin), db: Session = Depends(dependencies.get_db)):
    db_message = crud.delete_contact_message(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message solved and removed"}
