from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/doctors", tags=["Doctors"])




@router.get("/{doctor_id}")
def doctor_profile(doctor_id: int, db: Session = Depends(get_db)):

    data = crud.get_doctor_full_profile(db, doctor_id)

    if not data:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor = data["doctor"]

    return {
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "experience": doctor.experience,
            "image": doctor.image
        },
        "total_appointments": data["total_appointments"],
        "appointments": [
            {
                "patient_name": a.patient_name,
                "date": a.date,
                "time": a.time
            } for a in data["appointments"]
        ],
        "average_rating": data["average_rating"]
    }