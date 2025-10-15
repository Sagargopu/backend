from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional

from . import crud, models, schemas
from app.database import get_db

router = APIRouter()

# Project endpoints
@router.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@router.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id=project_id, project_update=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted successfully"}

# Project Component endpoints
@router.post("/components/", response_model=schemas.ProjectComponent)
def create_component(component: schemas.ProjectComponentCreate, db: Session = Depends(get_db)):
    return crud.create_project_component(db=db, component=component)

@router.get("/components/", response_model=List[schemas.ProjectComponent])
def read_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    components = crud.get_project_components(db, skip=skip, limit=limit)
    return components

@router.get("/projects/{project_id}/components/", response_model=List[schemas.ProjectComponent])
def read_project_components(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Verify project exists first
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    components = crud.get_project_components_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return components

@router.get("/components/{component_id}", response_model=schemas.ProjectComponent)
def read_component(component_id: int, db: Session = Depends(get_db)):
    component = crud.get_project_component(db, component_id=component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return component

@router.put("/components/{component_id}", response_model=schemas.ProjectComponent)
def update_component(component_id: int, component: schemas.ProjectComponentUpdate, db: Session = Depends(get_db)):
    db_component = crud.update_project_component(db, component_id=component_id, component_update=component)
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return db_component

@router.delete("/components/{component_id}")
def delete_component(component_id: int, db: Session = Depends(get_db)):
    db_component = crud.delete_project_component(db, component_id=component_id)
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"detail": "Component deleted successfully"}

# Task endpoints  
@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/components/{component_id}/tasks/", response_model=List[schemas.Task])
def read_component_tasks(component_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Verify component exists first
    component = crud.get_project_component(db, component_id=component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    
    tasks = crud.get_tasks_by_component(db, component_id=component_id, skip=skip, limit=limit)
    return tasks

# Assignment endpoints
@router.post("/assignments/", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    return crud.create_assignment(db=db, assignment=assignment)

# Advanced task retrieval endpoints
@router.get("/projects/{project_id}/tasks/", response_model=List[schemas.Task])
def get_all_project_tasks(project_id: int, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """Get ALL tasks for a project, including tasks from all nested components"""
    # Verify project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all tasks for all components in this project
    tasks = db.query(models.Task).join(models.ProjectComponent).filter(
        models.ProjectComponent.project_id == project_id
    ).offset(skip).limit(limit).all()
    
    return tasks

@router.get("/projects/{project_id}/tasks/by-hierarchy/")
def get_project_tasks_by_hierarchy(project_id: int, db: Session = Depends(get_db)):
    """Get all project tasks organized by component hierarchy"""
    # Verify project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get hierarchical task data
    result = db.execute(text("""
        WITH RECURSIVE component_hierarchy AS (
            SELECT 
                id, name, type, parent_id, project_id, 0 as level,
                ARRAY[id] as path,
                name as full_path
            FROM project_components 
            WHERE project_id = :project_id AND parent_id IS NULL
            
            UNION ALL
            
            SELECT 
                pc.id, pc.name, pc.type, pc.parent_id, pc.project_id, ch.level + 1,
                ch.path || pc.id,
                ch.full_path || ' → ' || pc.name
            FROM project_components pc
            JOIN component_hierarchy ch ON pc.parent_id = ch.id
        )
        SELECT 
            ch.id as component_id,
            ch.name as component_name,
            ch.type as component_type,
            ch.level as hierarchy_level,
            ch.full_path,
            t.id as task_id,
            t.name as task_name,
            t.description,
            t.status,
            t.priority
        FROM component_hierarchy ch
        LEFT JOIN tasks t ON t.component_id = ch.id
        ORDER BY ch.level, ch.name, t.priority DESC, t.name
    """), {"project_id": project_id}).fetchall()
    
    # Organize results by component
    hierarchy = {}
    for row in result:
        comp_id = row.component_id
        if comp_id not in hierarchy:
            hierarchy[comp_id] = {
                "component_id": comp_id,
                "component_name": row.component_name,
                "component_type": row.component_type,
                "hierarchy_level": row.hierarchy_level,
                "full_path": row.full_path,
                "tasks": []
            }
        
        if row.task_id:
            hierarchy[comp_id]["tasks"].append({
                "task_id": row.task_id,
                "task_name": row.task_name,
                "description": row.description,
                "status": row.status,
                "priority": row.priority
            })
    
    return {"project_id": project_id, "hierarchy": list(hierarchy.values())}

@router.get("/components/{component_id}/tasks/recursive/", response_model=List[schemas.Task])
def get_component_tasks_recursive(component_id: int, db: Session = Depends(get_db)):
    """Get all tasks for a component AND all its sub-components recursively"""
    # Verify component exists
    component = crud.get_project_component(db, component_id=component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Get all tasks for this component and its children recursively
    result = db.execute(text("""
        WITH RECURSIVE component_tree AS (
            -- Start with the specified component
            SELECT id, name, parent_id
            FROM project_components 
            WHERE id = :component_id
            
            UNION ALL
            
            -- Get all child components recursively
            SELECT pc.id, pc.name, pc.parent_id
            FROM project_components pc
            JOIN component_tree ct ON pc.parent_id = ct.id
        )
        SELECT t.*
        FROM component_tree ct
        JOIN tasks t ON t.component_id = ct.id
        ORDER BY t.priority DESC, t.name
    """), {"component_id": component_id}).fetchall()
    
    # Convert to Task objects
    tasks = []
    for row in result:
        task = models.Task(
            id=row.id,
            name=row.name,
            description=row.description,
            status=row.status,
            priority=row.priority,
            component_id=row.component_id,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
        tasks.append(task)
    
    return tasks

@router.get("/projects/{project_id}/tasks/summary/")
def get_project_task_summary(project_id: int, db: Session = Depends(get_db)):
    """Get task summary statistics for a project"""
    # Verify project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get summary statistics
    result = db.execute(text("""
        SELECT 
            COUNT(*) as total_tasks,
            COUNT(DISTINCT pc.id) as components_with_tasks,
            COUNT(CASE WHEN t.status = 'To Do' THEN 1 END) as todo_tasks,
            COUNT(CASE WHEN t.status = 'In Progress' THEN 1 END) as in_progress_tasks,
            COUNT(CASE WHEN t.status = 'Completed' THEN 1 END) as completed_tasks,
            COUNT(CASE WHEN t.status = 'On Hold' THEN 1 END) as on_hold_tasks,
            COUNT(CASE WHEN t.status = 'Cancelled' THEN 1 END) as cancelled_tasks,
            COUNT(CASE WHEN t.priority = 'Urgent' THEN 1 END) as urgent_tasks,
            COUNT(CASE WHEN t.priority = 'High' THEN 1 END) as high_priority_tasks,
            COUNT(CASE WHEN t.priority = 'Medium' THEN 1 END) as medium_priority_tasks,
            COUNT(CASE WHEN t.priority = 'Low' THEN 1 END) as low_priority_tasks
        FROM tasks t
        JOIN project_components pc ON pc.id = t.component_id
        WHERE pc.project_id = :project_id
    """), {"project_id": project_id}).fetchone()
    
    return {
        "project_id": project_id,
        "total_tasks": result.total_tasks if result else 0,
        "components_with_tasks": result.components_with_tasks if result else 0,
        "by_status": {
            "todo": result.todo_tasks if result else 0,
            "in_progress": result.in_progress_tasks if result else 0,
            "completed": result.completed_tasks if result else 0,
            "on_hold": result.on_hold_tasks if result else 0,
            "cancelled": result.cancelled_tasks if result else 0
        },
        "by_priority": {
            "urgent": result.urgent_tasks if result else 0,
            "high": result.high_priority_tasks if result else 0,
            "medium": result.medium_priority_tasks if result else 0,
            "low": result.low_priority_tasks if result else 0
        },
        "completion_rate": round((result.completed_tasks / result.total_tasks * 100) if (result and result.total_tasks > 0) else 0, 2)
    }

@router.get("/projects/{project_id}/tasks/filter/")
def get_filtered_project_tasks(
    project_id: int, 
    status: Optional[str] = None, 
    priority: Optional[str] = None, 
    component_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get filtered tasks for a project"""
    # Verify project exists
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build dynamic query
    query = db.query(models.Task).join(models.ProjectComponent).filter(
        models.ProjectComponent.project_id == project_id
    )
    
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if component_type:
        query = query.filter(models.ProjectComponent.type == component_type)
    
    tasks = query.order_by(models.Task.priority.desc(), models.Task.name).all()
    
    return {
        "project_id": project_id,
        "filters": {
            "status": status,
            "priority": priority,
            "component_type": component_type
        },
        "task_count": len(tasks),
        "tasks": tasks
    }
