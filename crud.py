from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- User Operations ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Event Operations ---
def get_events(db: Session, status: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Event)
    if status:
        query = query.filter(models.Event.status == status)
    return query.offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        # Use exclude_unset=True to only update what was provided in the JSON body
        update_data = event_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

# --- Registration Operations ---
def register_user_for_event(db: Session, user_id: int, event_id: int):
    # Check if already registered
    existing = db.query(models.Registration).filter(
        models.Registration.user_id == user_id, 
        models.Registration.event_id == event_id
    ).first()
    if existing:
        return existing
        
    db_reg = models.Registration(user_id=user_id, event_id=event_id)
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg

def unregister_user_from_event(db: Session, user_id: int, event_id: int):
    registration = db.query(models.Registration).filter(
        models.Registration.user_id == user_id, 
        models.Registration.event_id == event_id
    ).first()
    if registration:
        db.delete(registration)
        db.commit()
        return True
    return False

# --- Contact Operations ---
def create_contact_message(db: Session, message: schemas.ContactMessageCreate):
    db_message = models.ContactMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_contact_messages(db: Session):
    return db.query(models.ContactMessage).all()

# --- Admin Stats ---
def get_stats(db: Session):
    return {
        "users_count": db.query(models.User).count(),
        "events_count": db.query(models.Event).count(),
        "upcoming_events": db.query(models.Event).filter(models.Event.status == "upcoming").count(),
        "completed_events": db.query(models.Event).filter(models.Event.status == "completed").count(),
        "messages_count": db.query(models.ContactMessage).count()
    }

def delete_contact_message(db: Session, message_id: int):
    db_message = db.query(models.ContactMessage).filter(models.ContactMessage.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message
