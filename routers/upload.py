import os
from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"

# ✅ create folder automatically
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_image(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"image_url": path}


@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_url": path}