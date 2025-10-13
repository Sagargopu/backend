from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This is a simplified endpoint. A real implementation would upload the file to GCS
# and then call the crud function.
@router.post("/documents/upload/", response_model=schemas.Document)
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    # 1. In a real app: Upload file.file to Google Cloud Storage.
    # 2. Get the storage_path from the upload result.
    # 3. For now, we'll just simulate this.
    fake_storage_path = f"gcs/fake_path/{file.filename}"
    
    doc_create = schemas.DocumentCreate(
        name=file.filename,
        file_type=file.content_type,
        storage_path=fake_storage_path,
        uploaded_by_id=1 # Placeholder for actual user ID
    )
    return crud.create_document(db=db, document=doc_create)

@router.get("/documents/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_documents(db, skip=skip, limit=limit)
