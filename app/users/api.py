from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/admin/onboard/", response_model=dict)
def onboard_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    result = crud.onboard_user(db=db, user=user)
    if result is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return result

@router.post("/setup-account/{user_id}", response_model=schemas.User)
def setup_user_account(user_id: int, new_password: str, token: str, db: Session = Depends(get_db)):
    db_user = crud.set_user_password(db, user_id=user_id, new_password=new_password, token=token)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid token or user not found")
    return db_user

@router.get("/talent-pool/", response_model=list[schemas.User])
def get_talent_pool(role: str | None = None, available: bool | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_talent_pool(db, role=role, available=available, skip=skip, limit=limit)
    return users

@router.post("/admin/users/{user_id}/activate", response_model=schemas.User)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.activate_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/admin/users/{user_id}/deactivate", response_model=schemas.User)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.deactivate_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



