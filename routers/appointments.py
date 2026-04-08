from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/")
def book_appointment(app: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, app)


@router.get("/")
def all_appointments(db: Session = Depends(get_db)):
    return crud.get_appointments(db)


@router.get("/doctor/{doctor_id}")
def doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_by_doctor(db, doctor_id)


@router.get("/slots/{doctor_id}")
def get_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):
    return crud.get_available_slots(db, doctor_id, date)