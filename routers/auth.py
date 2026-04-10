from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, SECRET_KEY, ALGORITHM
from jose import jwt
from passlib.context import CryptContext
import models
import schemas
from dependencies import get_current_user, admin_required


router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": user.username, "role": user.role, "doctor_id": user.doctor_id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register-admin")
def register_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = pwd_context.hash(user.password[:72])  # ✅ SAFE LIMIT

    new_user = models.User(
        username=user.username,
        password=hashed,
        role="admin"
    )

    db.add(new_user)
    db.commit()

    return {"message": "Admin created"}


@router.post("/register-doctor", dependencies=[Depends(admin_required)])
def register_doctor(user: schemas.UserCreate, doctor_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if doctor exists
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found. Create doctor profile first.")

    hashed = pwd_context.hash(user.password)
    new_user = models.User(
        username=user.username,
        password=hashed,
        role="doctor",
        doctor_id=doctor_id
    )
    db.add(new_user)
    db.commit()
    return {"message": "Doctor account created and linked"}


@router.get("/me", response_model=schemas.UserMe)
def get_me(current_user=Depends(get_current_user)):
    return current_user