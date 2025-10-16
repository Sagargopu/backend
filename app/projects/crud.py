from sqlalchemy.orm import Session
from . import models, schemas

# ProjectType CRUD
def create_project_type(db: Session, project_type: schemas.ProjectTypeCreate):
    db_project_type = models.ProjectType(**project_type.dict())
    db.add(db_project_type)
    db.commit()
    db.refresh(db_project_type)
    return db_project_type

def get_project_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectType).offset(skip).limit(limit).all()

def get_project_type(db: Session, project_type_id: int):
    return db.query(models.ProjectType).filter(models.ProjectType.id == project_type_id).first()

def update_project_type(db: Session, project_type_id: int, project_type_update: schemas.ProjectTypeUpdate):
    db_project_type = db.query(models.ProjectType).filter(models.ProjectType.id == project_type_id).first()
    if db_project_type:
        update_data = project_type_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project_type, field, value)
        db.commit()
        db.refresh(db_project_type)
    return db_project_type

def delete_project_type(db: Session, project_type_id: int):
    db_project_type = db.query(models.ProjectType).filter(models.ProjectType.id == project_type_id).first()
    if db_project_type:
        db.delete(db_project_type)
        db.commit()
    return db_project_type

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

# Project filtering functions
def get_projects_by_client(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.client_id == client_id
    ).offset(skip).limit(limit).all()

def get_projects_by_project_manager(db: Session, project_manager_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.project_manager_id == project_manager_id
    ).offset(skip).limit(limit).all()

def get_projects_by_project_type(db: Session, project_type_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.project_type_id == project_type_id
    ).offset(skip).limit(limit).all()

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

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_component(db: Session, component_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.component_id == component_id).offset(skip).limit(limit).all()

def get_tasks_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.project_id == project_id).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
