from fastapi import Depends, HTTPException

def get_current_user():
    # dummy for now (later JWT add karenge)
    return {"role": "admin"}


def admin_required(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
def get_current_user():
    # later JWT add karenge
    return {"role": "admin", "doctor_id": 1}


def admin_required(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user


def doctor_required(user=Depends(get_current_user)):
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor only")
    return user