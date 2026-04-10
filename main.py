from fastapi import FastAPI
from database import Base, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import Routers
from routers import (
    auth,
    doctors,
    appointments,
    analytics,
    availability,
    ratings,
    upload,
    export,
    slots
)

# Initialize Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediSync Doctor Booking API", version="2.0.0")

# Static Files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 1. Auth & Identity
app.include_router(auth.router)

# ✅ 2. Core Resources
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(availability.router)

# ✅ 3. Analytics & Export
app.include_router(analytics.router)
app.include_router(export.router)

# ✅ 4. Misc
app.include_router(ratings.router)
app.include_router(upload.router)
app.include_router(slots.router)


@app.get("/")
def health_check():
    return {"status": "online", "version": "2.0.0", "system": "MediSync"}