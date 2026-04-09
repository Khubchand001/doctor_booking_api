from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas
from dependencies import admin_required, doctor_required, get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# ✅ Admin: see all
@router.get("/", dependencies=[Depends(admin_required)])
def get_all(db: Session = Depends(get_db)):
    return crud.get_appointments(db)


# ✅ Doctor: see own patients only
@router.get("/my")
def my_patients(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_appointments_by_doctor(db, user["doctor_id"])


# ✅ Add appointment
@router.post("/")
def create(app: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, app)


# ✅ Delete appointment
@router.delete("/{appointment_id}", dependencies=[Depends(admin_required)])
def delete(appointment_id: int, db: Session = Depends(get_db)):
    return crud.delete_appointment(db, appointment_id)