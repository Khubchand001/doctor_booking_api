from fastapi import FastAPI
from database import engine
import models

from routers import doctors, appointments, ratings, upload, availability
from fastapi.staticfiles import StaticFiles
from routers import analytics

app = FastAPI(title="Doctor Booking API")

models.Base.metadata.create_all(bind=engine)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(ratings.router)
app.include_router(upload.router)
app.include_router(availability.router)
app.include_router(analytics.router)