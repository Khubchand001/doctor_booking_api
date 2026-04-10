from typing import Optional
from pydantic import BaseModel



class DoctorCreate(BaseModel):
    name: str
    specialization: str
    experience: str
    image: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_name: str
    age: int
    phone: str
    address: str
    date: str   # use YYYY-MM-DD
    time: str   # use HH:MM
    report: Optional[str] = None


class AppointmentResponse(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True


class AvailabilityCreate(BaseModel):
    doctor_id: int
    date: str
    start_time: str
    end_time: str


class RatingCreate(BaseModel):
    doctor_id: int
    stars: int
    comment: str


class RatingResponse(RatingCreate):
    id: int

    class Config:
        from_attributes = True

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    experience: str
    image: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class DashboardActivities(BaseModel):
    paitent_inflow: int
    doctor_availability: int
    resource_usage: int

class UserMe(BaseModel):
    username: str
    role: str
    doctor_id: Optional[int] = None

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[str] = None
    image: Optional[str] = None