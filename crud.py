from sqlalchemy.orm import Session
import models


# ---------------- DOCTOR ---------------- #

def create_doctor(db: Session, doctor):
    new_doc = models.Doctor(**doctor.dict())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()


# ---------------- APPOINTMENT ---------------- #

def create_appointment(db: Session, appointment):
    print(f"DEBUG: Attempting to create appointment for doctor {appointment.doctor_id} on {appointment.date} at {appointment.time}")
    
    # 🚨 Prevent double booking
    existing = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.date == appointment.date,
        models.Appointment.time == appointment.time
    ).first()

    if existing:
        print("DEBUG: Appointment slot already booked!")
        raise Exception("Slot already booked")

    new_app = models.Appointment(**appointment.dict())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    print(f"DEBUG: Appointment created successfully with ID: {new_app.id}")
    return new_app


def get_appointments(db: Session):
    data = db.query(models.Appointment).all()
    print("DEBUG APPOINTMENTS:", data)
    return data


def get_appointments_by_doctor(db: Session, doctor_id: int):
    return db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id
    ).all()


# ---------------- AVAILABILITY ---------------- #

def create_availability(db: Session, availability):
    new_av = models.Availability(**availability.dict())
    db.add(new_av)
    db.commit()
    db.refresh(new_av)
    return new_av


def get_available_slots(db: Session, doctor_id, date):

    availability = db.query(models.Availability).filter(
        models.Availability.doctor_id == doctor_id,
        models.Availability.date == date
    ).first()

    if not availability:
        return {"slots": [], "message": "No availability set"}

    start = int(availability.start_time.split(":")[0])
    end = int(availability.end_time.split(":")[0])

    slots = []
    for hour in range(start, end):
        slots.append(f"{hour:02d}:00")
        slots.append(f"{hour:02d}:30")

    booked = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.date == date
    ).all()

    booked_times = [b.time for b in booked]

    available = [s for s in slots if s not in booked_times]

    return {
        "total_slots": slots,
        "booked": booked_times,
        "available": available
    }
def calculate_rating(db: Session, doctor_id: int):
    ratings = db.query(models.Rating).filter(
        models.Rating.doctor_id == doctor_id
    ).all()

    if not ratings:
        return 0

    avg = sum(r.stars for r in ratings) / len(ratings)

    return round(avg, 2)

def get_doctor_full_profile(db: Session, doctor_id: int):
    doctor = db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()

    if not doctor:
        return None

    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id
    ).all()

    rating = calculate_rating(db, doctor_id)

    return {
            "doctor": doctor,
            "appointments": appointments,
            "total_appointments": len(appointments),
            "average_rating": rating
        }
    
def get_doctors(db: Session):
        return db.query(models.Doctor).all()

def delete_appointment(db: Session, appointment_id: int):
    app = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()

    if app:
        db.delete(app)
        db.commit()
    return app