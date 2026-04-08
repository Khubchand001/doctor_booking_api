from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/")
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)


@router.get("/")
def list_doctors(db: Session = Depends(get_db)):
    return crud.get_doctors(db)


@router.get("/{doctor_id}")
def doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db, doctor_id)
    rating = crud.calculate_rating(db, doctor_id)

    return {
        "doctor": doctor,
        "average_rating": rating
    }