from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from app.database import get_db

router = APIRouter()

# ProjectType endpoints
@router.post("/project-types/", response_model=schemas.ProjectType)
def create_project_type(project_type: schemas.ProjectTypeCreate, db: Session = Depends(get_db)):
    """Create a new project type"""
    return crud.create_project_type(db=db, project_type=project_type)

@router.get("/project-types/", response_model=List[schemas.ProjectType])
def read_project_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all project types"""
    project_types = crud.get_project_types(db, skip=skip, limit=limit)
    return project_types

@router.get("/project-types/{project_type_id}", response_model=schemas.ProjectType)
def read_project_type(project_type_id: int, db: Session = Depends(get_db)):
    """Get project type by ID"""
    project_type = crud.get_project_type(db, project_type_id=project_type_id)
    if project_type is None:
        raise HTTPException(status_code=404, detail="Project type not found")
    return project_type

@router.put("/project-types/{project_type_id}", response_model=schemas.ProjectType)
def update_project_type(project_type_id: int, project_type: schemas.ProjectTypeUpdate, db: Session = Depends(get_db)):
    """Update project type by ID"""
    db_project_type = crud.update_project_type(db, project_type_id=project_type_id, project_type_update=project_type)
    if db_project_type is None:
        raise HTTPException(status_code=404, detail="Project type not found")
    return db_project_type

@router.delete("/project-types/{project_type_id}")
def delete_project_type(project_type_id: int, db: Session = Depends(get_db)):
    """Delete project type by ID"""
    db_project_type = crud.delete_project_type(db, project_type_id=project_type_id)
    if db_project_type is None:
        raise HTTPException(status_code=404, detail="Project type not found")
    return {"detail": "Project type deleted successfully"}

# Project endpoints
@router.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    return crud.create_project(db=db, project=project)

@router.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects"""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by ID"""
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    """Update project by ID"""
    db_project = crud.update_project(db, project_id=project_id, project_update=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete project by ID"""
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted successfully"}

# Project filtering endpoints
@router.get("/projects/by-client/{client_id}", response_model=List[schemas.Project])
def read_projects_by_client(client_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects by client ID"""
    projects = crud.get_projects_by_client(db, client_id=client_id, skip=skip, limit=limit)
    return projects

@router.get("/projects/by-manager/{project_manager_id}", response_model=List[schemas.Project])
def read_projects_by_manager(project_manager_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects by project manager ID"""
    projects = crud.get_projects_by_project_manager(db, project_manager_id=project_manager_id, skip=skip, limit=limit)
    return projects

@router.get("/projects/by-type/{project_type_id}", response_model=List[schemas.Project])
def read_projects_by_type(project_type_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects by project type ID"""
    projects = crud.get_projects_by_project_type(db, project_type_id=project_type_id, skip=skip, limit=limit)
    return projects

# Project Component endpoints
@router.post("/components/", response_model=schemas.ProjectComponent)
def create_component(component: schemas.ProjectComponentCreate, db: Session = Depends(get_db)):
    """Create a new project component"""
    return crud.create_project_component(db=db, component=component)

@router.get("/components/", response_model=List[schemas.ProjectComponent])
def read_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all project components"""
    components = crud.get_project_components(db, skip=skip, limit=limit)
    return components

@router.get("/components/{component_id}", response_model=schemas.ProjectComponent)
def read_component(component_id: int, db: Session = Depends(get_db)):
    """Get component by ID"""
    component = crud.get_project_component(db, component_id=component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return component

@router.get("/projects/{project_id}/components", response_model=List[schemas.ProjectComponent])
def read_components_by_project(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all components for a specific project"""
    components = crud.get_project_components_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return components

@router.put("/components/{component_id}", response_model=schemas.ProjectComponent)
def update_component(component_id: int, component: schemas.ProjectComponentUpdate, db: Session = Depends(get_db)):
    """Update component by ID"""
    db_component = crud.update_project_component(db, component_id=component_id, component_update=component)
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return db_component

@router.delete("/components/{component_id}")
def delete_component(component_id: int, db: Session = Depends(get_db)):
    """Delete component by ID"""
    db_component = crud.delete_project_component(db, component_id=component_id)
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"detail": "Component deleted successfully"}

# Task endpoints
@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    return crud.create_task(db=db, task=task)

@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tasks"""
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID"""
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/components/{component_id}/tasks", response_model=List[schemas.Task])
def read_tasks_by_component(component_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tasks for a specific component"""
    tasks = crud.get_tasks_by_component(db, component_id=component_id, skip=skip, limit=limit)
    return tasks

@router.get("/projects/{project_id}/tasks", response_model=List[schemas.Task])
def read_tasks_by_project(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tasks for a specific project"""
    tasks = crud.get_tasks_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return tasks

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update task by ID"""
    db_task = crud.update_task(db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete task by ID"""
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}
