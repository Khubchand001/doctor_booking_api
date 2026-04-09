from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from passlib.context import CryptContext
import models
import schemas


router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": user.username, "role": user.role, "doctor_id": user.doctor_id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}

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