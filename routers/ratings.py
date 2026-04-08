from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/")
def add_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    return crud.add_rating(db, rating)