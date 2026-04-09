from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    experience = Column(String)
    image = Column(String)

    ratings = relationship("Rating", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    stars = Column(Integer)
    comment = Column(String)
    doctor = relationship("Doctor", back_populates="ratings") 

class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_name = Column(String)
    age = Column(Integer)
    phone = Column(String)
    address = Column(String)
    date = Column(String)
    time = Column(String)
    report = Column(String, nullable=True)  
    doctor = relationship("Doctor", back_populates="appointments")


class Availability(Base):

    __tablename__ = "availability"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # admin / doctor
    doctor_id = Column(Integer, nullable=True)  # link doctor