from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas, dependencies

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

@router.post("/", response_model=schemas.ContactMessageResponse)
def submit_contact_form(message: schemas.ContactMessageCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_contact_message(db, message)
