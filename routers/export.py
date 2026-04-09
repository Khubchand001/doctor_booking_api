from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd
import models

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/doctor/{doctor_id}")
def export_doctor_data(doctor_id: int, db: Session = Depends(get_db)):

    data = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id
    ).all()

    rows = [{
        "patient": d.patient_name,
        "date": d.date,
        "time": d.time
    } for d in data]

    df = pd.DataFrame(rows)
    file_path = f"doctor_{doctor_id}.xlsx"
    df.to_excel(file_path, index=False)

    return {"file": file_path}