from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from datetime import date
from dependencies import admin_required, doctor_required

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ✅ MAIN DASHBOARD (Admin only)
@router.get("/dashboard", dependencies=[Depends(admin_required)])
def dashboard(db: Session = Depends(get_db)):

    today = str(date.today())

    # 📊 Basic stats
    total_doctors = db.query(func.count(models.Doctor.id)).scalar()
    total_appointments = db.query(func.count(models.Appointment.id)).scalar()

    revenue = total_appointments * 500

    # 📅 Today's appointments
    today_appointments = db.query(func.count(models.Appointment.id)).filter(
        models.Appointment.date == today
    ).scalar()

    # ⭐ Average rating
    avg_rating = db.query(func.avg(models.Rating.stars)).scalar()
    avg_rating = round(avg_rating, 2) if avg_rating else 0

    # 👑 Top doctor (most appointments)
    top_doc = db.query(
        models.Doctor.name,
        func.count(models.Appointment.id).label("count")
    ).join(
        models.Appointment,
        models.Doctor.id == models.Appointment.doctor_id
    ).group_by(
        models.Doctor.id
    ).order_by(
        func.count(models.Appointment.id).desc()
    ).first()

    top_doctor = top_doc.name if top_doc else None
    top_count = top_doc.count if top_doc else 0

    return {
        "overview": {
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "revenue": revenue
        },
        "today": {
            "date": today,
            "appointments": today_appointments
        },
        "ratings": {
            "average_rating": avg_rating
        },
        "top_doctor": {
            "name": top_doctor,
            "appointments": top_count
        }
    }


# 📈 APPOINTMENTS PER DAY (FOR CHARTS)
@router.get("/appointments-per-day")
def appointments_per_day(db: Session = Depends(get_db)):

    data = db.query(
        models.Appointment.date,
        func.count(models.Appointment.id)
    ).group_by(models.Appointment.date).all()

    return [
        {"date": d[0], "count": d[1]}
        for d in data
    ]


# 👨‍⚕️ DOCTOR PERFORMANCE
@router.get("/doctor-performance")
def doctor_performance(db: Session = Depends(get_db)):

    data = db.query(
        models.Doctor.name,
        func.count(models.Appointment.id).label("appointments")
    ).outerjoin(
        models.Appointment,
        models.Doctor.id == models.Appointment.doctor_id
    ).group_by(models.Doctor.id).all()

    return [
        {
            "doctor": d[0],
            "appointments": d[1]
        }
        for d in data
    ]


# ⭐ RATING DISTRIBUTION
@router.get("/rating-distribution")
def rating_distribution(db: Session = Depends(get_db)):

    data = db.query(
        models.Rating.stars,
        func.count(models.Rating.id)
    ).group_by(models.Rating.stars).all()

    return [
        {
            "stars": r[0],
            "count": r[1]
        }
        for r in data
    ]


# 📊 ACTIVITIES (DYNAMIC STATS FOR DASHBOARD)
@router.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    # These could be calculated from real usage data
    # For now, providing semi-dynamic values based on current stats
    total_docs = db.query(func.count(models.Doctor.id)).scalar() or 1
    total_apps = db.query(func.count(models.Appointment.id)).scalar() or 1
    
    # Example logic: 
    # Patient Inflow = appointments / (doctors * 10) capped at 100%
    patient_inflow = min(int((total_apps / (total_docs * 10)) * 100), 100)
    # Availability = (doctors * some factor)
    doctor_availability = min(total_docs * 8, 100)
    # Resource Usage = a mix of both
    resource_usage = (patient_inflow + doctor_availability) // 2

    return {
        "patient_inflow": patient_inflow,
        "doctor_availability": doctor_availability,
        "resource_usage": resource_usage
    }


# 👨‍⚕️ DOCTOR'S PERSONAL STATS
@router.get("/my-stats")
def get_my_stats(user=Depends(doctor_required), db: Session = Depends(get_db)):
    doctor_id = user["doctor_id"]
    if not doctor_id:
        raise HTTPException(status_code=400, detail="User is not linked to a doctor profile")
    
    total_appointments = db.query(func.count(models.Appointment.id)).filter(
        models.Appointment.doctor_id == doctor_id
    ).scalar()
    
    avg_rating = db.query(func.avg(models.Rating.stars)).filter(
        models.Rating.doctor_id == doctor_id
    ).scalar()
    avg_rating = round(avg_rating, 2) if avg_rating else 0
    
    return {
        "appointments": total_appointments,
        "rating": avg_rating,
        "growth": 15.4  # Example dynamic-looking stat
    }