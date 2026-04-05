from typing import Optional

from pydantic import BaseModel


class DoctorCreate(BaseModel):

    name: str
    specialization: str
    experience: str
    image: str


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_name: str
    age: int
    phone: str
    address: str
    date: str
    time: str
    report: Optional[str] = None


class RatingCreate(BaseModel):

    doctor_id: int
    stars: int
    comment: str

class AvailabilityCreate(BaseModel):
    doctor_id: int
    day: str
    start_time: str
    end_time: str

