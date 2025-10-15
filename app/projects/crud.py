from sqlalchemy.orm import Session
from . import models, schemas

# Project CRUD
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

# ProjectComponent CRUD
def create_project_component(db: Session, component: schemas.ProjectComponentCreate):
    db_component = models.ProjectComponent(**component.dict())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

def get_project_components(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectComponent).offset(skip).limit(limit).all()

def get_project_components_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectComponent).filter(
        models.ProjectComponent.project_id == project_id
    ).offset(skip).limit(limit).all()

def get_project_component(db: Session, component_id: int):
    return db.query(models.ProjectComponent).filter(models.ProjectComponent.id == component_id).first()

def update_project_component(db: Session, component_id: int, component_update: schemas.ProjectComponentUpdate):
    db_component = db.query(models.ProjectComponent).filter(models.ProjectComponent.id == component_id).first()
    if db_component:
        update_data = component_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_component, field, value)
        db.commit()
        db.refresh(db_component)
    return db_component

def delete_project_component(db: Session, component_id: int):
    db_component = db.query(models.ProjectComponent).filter(models.ProjectComponent.id == component_id).first()
    if db_component:
        db.delete(db_component)
        db.commit()
    return db_component

# Task CRUD
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_tasks_by_component(db: Session, component_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.component_id == component_id).offset(skip).limit(limit).all()

# Assignment CRUD
def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
