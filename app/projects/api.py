from fastapi import APIRouter, Depends, HTTPException
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

@router.post("/projects/", response_model=schemas.ProjectComponent)
def create_project_component(component: schemas.ProjectComponentCreate, db: Session = Depends(get_db)):
    return crud.create_project_component(db=db, component=component)

@router.get("/projects/", response_model=List[schemas.ProjectComponent])
def read_project_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_project_components(db, skip=skip, limit=limit)

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)

@router.post("/assignments/", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    return crud.create_assignment(db=db, assignment=assignment)
