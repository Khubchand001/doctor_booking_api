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
def my_patients(user=Depends(doctor_required), db: Session = Depends(get_db)):
    return crud.get_appointments_by_doctor(db, user["doctor_id"])


# ✅ Add appointment
@router.post("/")
def create(app: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, app)


# ✅ Delete appointment
@router.delete("/{appointment_id}", dependencies=[Depends(admin_required)])
def delete(appointment_id: int, db: Session = Depends(get_db)):
    return crud.delete_appointment(db, appointment_id)


# ✅ Update appointment
@router.patch("/{appointment_id}", dependencies=[Depends(admin_required)])
def update(appointment_id: int, app_update: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    db_app = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    for field, value in app_update.dict(exclude_unset=True).items():
        setattr(db_app, field, value)
        
    db.commit()
    db.refresh(db_app)
    return db_app