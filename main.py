from fastapi import FastAPI
from database import engine
import models

from routers import doctors, appointments, ratings, upload,availability

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Doctor Booking API")


app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(ratings.router)
app.include_router(upload.router)
app.include_router(availability.router)