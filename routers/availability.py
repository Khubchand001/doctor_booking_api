from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter(prefix="/availability", tags=["Availability"])

@router.post("/")
def add_availability(data: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    return crud.create_availability(db, data)