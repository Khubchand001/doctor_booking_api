from fastapi import FastAPI
from database import Base, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import doctors, appointments, ratings, upload, availability
from fastapi.staticfiles import StaticFiles
from routers import analytics
from routers import export
from routers import auth



app = FastAPI(title="Doctor Booking API")

models.Base.metadata.create_all(bind=engine)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(ratings.router)
app.include_router(upload.router)
app.include_router(availability.router)
app.include_router(analytics.router)
app.include_router(export.router)
app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev ke liye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)