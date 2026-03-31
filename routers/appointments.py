from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter()


@router.post("/appointment")
def book_appointment(app: schemas.AppointmentCreate, db: Session = Depends(get_db)):

    return crud.create_appointment(db, app)


@router.get("/slots/{doctor_id}")

def get_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):

    return crud.get_available_slots(db, doctor_id, date)