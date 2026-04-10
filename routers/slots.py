from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud

router = APIRouter(prefix="/slots", tags=["Slots"])


@router.get("/{doctor_id}")
def get_available_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):
    """
    Returns a list of available time slots for a doctor on a specific date.
    Endpoint used by the Flutter mobile app.
    """
    data = crud.get_available_slots(db, doctor_id, date)
    
    # crud.get_available_slots returns a dict with 'available', 'booked', and 'total_slots'
    # or a message if no availability is set.
    # Flutter expects a List[str].
    
    if isinstance(data, dict) and "available" in data:
        return data["available"]
    
    return []
