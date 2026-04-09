from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# ✅ 1. GET ALL DOCTORS (MAIN API)
@router.get("")
def get_all_doctors(db: Session = Depends(get_db)):
    return crud.get_doctors(db)


# ✅ 2. GET SINGLE DOCTOR (OPTIONAL)
@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


# ✅ 3. ADD DOCTOR
@router.post("")
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)