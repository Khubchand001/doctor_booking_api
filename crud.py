from sqlalchemy.orm import Session
import models


def create_doctor(db: Session, doctor):

    new_doc = models.Doctor(**doctor.dict())

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc


def get_doctors(db: Session):

    return db.query(models.Doctor).all()


def get_doctor(db: Session, doctor_id: int):

    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


def add_rating(db: Session, rating):

    new_rating = models.Rating(**rating.dict())

    db.add(new_rating)
    db.commit()

    return new_rating


def calculate_rating(db: Session, doctor_id: int):

    ratings = db.query(models.Rating).filter(models.Rating.doctor_id == doctor_id).all()

    if not ratings:
        return 0

    avg = sum(r.stars for r in ratings) / len(ratings)

    return round(avg, 2)


def create_appointment(db: Session, appointment):

    new_app = models.Appointment(**appointment.dict())

    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    return new_app


def get_available_slots(db: Session, doctor_id, date):

    slots = [
        "09:00","09:30","10:00","10:30",
        "11:00","11:30","12:00","12:30"
    ]

    booked = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.date == date
    ).all()

    booked_times = [b.time for b in booked]

    available = [s for s in slots if s not in booked_times]

    return available