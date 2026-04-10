from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas
from dependencies import admin_required, doctor_required, get_current_user

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


# ✅ 3. ADD DOCTOR (Admin only)
@router.post("", dependencies=[Depends(admin_required)])
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)


# ✅ 4. UPDATE OWN PROFILE (Doctor only)
@router.patch("/profile")
def update_profile(
    profile: schemas.DoctorUpdate, 
    user=Depends(doctor_required), 
    db: Session = Depends(get_db)
):
    doctor_id = user["doctor_id"]
    if not doctor_id:
        raise HTTPException(status_code=400, detail="User is not linked to any doctor profile")
        
    db_doctor = crud.get_doctor(db, doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
        
    # Update fields
    for field, value in profile.dict(exclude_unset=True).items():
        setattr(db_doctor, field, value)
        
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# ✅ 5. ADMIN UPDATE DOCTOR (Admin only)
@router.patch("/{doctor_id}", dependencies=[Depends(admin_required)])
def admin_update_doctor(
    doctor_id: int,
    profile: schemas.DoctorUpdate,
    db: Session = Depends(get_db)
):
    db_doctor = crud.get_doctor(db, doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    # Update fields
    for field, value in profile.dict(exclude_unset=True).items():
        setattr(db_doctor, field, value)
        
    db.commit()
    db.refresh(db_doctor)
    return db_doctor