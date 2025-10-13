from sqlalchemy.orm import Session
from . import models, schemas

# ProjectComponent CRUD
def create_project_component(db: Session, component: schemas.ProjectComponentCreate):
    db_component = models.ProjectComponent(**component.dict())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

def get_project_components(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectComponent).offset(skip).limit(limit).all()

# Task CRUD
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

# Assignment CRUD
def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
