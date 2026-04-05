from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter()


# ---------------- DOCTOR APIs ---------------- #

@router.post("/doctors")
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)


@router.get("/doctors")
def list_doctors(db: Session = Depends(get_db)):
    return crud.get_doctors(db)


@router.get("/doctor/{doctor_id}")
def doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db, doctor_id)
    rating = crud.calculate_rating(db, doctor_id)

    return {
        "doctor": doctor,
        "average_rating": rating
    }


# ---------------- NEW: AVAILABILITY APIs ---------------- #

@router.post("/availability")
def add_availability(data: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    return crud.create_availability(db, data)


@router.get("/availability/{doctor_id}")
def get_availability(doctor_id: int, db: Session = Depends(get_db)):
    return db.query(crud.models.Availability).filter(
        crud.models.Availability.doctor_id == doctor_id
    ).all()