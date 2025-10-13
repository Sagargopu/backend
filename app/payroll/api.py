from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/timesheets/clock-in", response_model=schemas.Timesheet)
def clock_in_user(user_id: int, project_id: int, db: Session = Depends(get_db)):
    return crud.clock_in(db=db, user_id=user_id, project_id=project_id)

@router.post("/timesheets/{timesheet_id}/clock-out", response_model=schemas.Timesheet)
def clock_out_user(timesheet_id: int, db: Session = Depends(get_db)):
    return crud.clock_out(db=db, timesheet_id=timesheet_id)

@router.post("/timesheets/{timesheet_id}/approve", response_model=schemas.Timesheet)
def approve_timesheet(timesheet_id: int, approver_id: int, db: Session = Depends(get_db)):
    db_timesheet = crud.approve_timesheet(db, timesheet_id=timesheet_id, approver_id=approver_id)
    if db_timesheet is None:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    return db_timesheet

