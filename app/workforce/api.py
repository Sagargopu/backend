from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from . import crud, schemas
from ..database import get_db

router = APIRouter()

# ===============================
# PROFESSION ENDPOINTS
# ===============================

@router.post("/professions/", response_model=schemas.Profession)
def create_profession(profession: schemas.ProfessionCreate, db: Session = Depends(get_db)):
    """Create a new construction profession"""
    # Check if profession with same name already exists
    existing = crud.get_profession_by_name(db, profession.name)
    if existing:
        raise HTTPException(status_code=400, detail="Profession with this name already exists")
    
    return crud.create_profession(db=db, profession=profession)

@router.get("/professions/", response_model=List[schemas.Profession])
def get_professions(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all professions"""
    return crud.get_professions(db, skip=skip, limit=limit)

@router.get("/professions/{profession_id}", response_model=schemas.Profession)
def get_profession(profession_id: int, db: Session = Depends(get_db)):
    """Get specific profession by ID"""
    profession = crud.get_profession(db, profession_id=profession_id)
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession

@router.put("/professions/{profession_id}", response_model=schemas.Profession)
def update_profession(profession_id: int, profession_update: schemas.ProfessionUpdate, db: Session = Depends(get_db)):
    """Update profession information"""
    profession = crud.update_profession(db, profession_id=profession_id, profession_update=profession_update)
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession

@router.delete("/professions/{profession_id}")
def delete_profession(profession_id: int, db: Session = Depends(get_db)):
    """Delete a profession"""
    success = crud.delete_profession(db, profession_id=profession_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profession not found")
    return {"message": "Profession deleted successfully"}

# ===============================
# WORKER ENDPOINTS
# ===============================

@router.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    """Create a new worker"""
    # Verify profession exists
    profession = crud.get_profession(db, worker.profession_id)
    if not profession:
        raise HTTPException(status_code=400, detail="Profession not found")
    
    # Check if worker with same worker_id exists
    existing = crud.get_worker_by_worker_id(db, worker.worker_id)
    if existing:
        raise HTTPException(status_code=400, detail="Worker with this worker_id already exists")
    
    # Check if worker with same email exists
    if worker.email:
        existing_email = db.query(crud.models.Worker).filter(crud.models.Worker.email == worker.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Worker with this email already exists")
    
    return crud.create_worker(db=db, worker=worker)

@router.get("/workers/", response_model=List[schemas.WorkerWithProfession])
def get_workers(
    skip: int = 0,
    limit: int = 100,
    profession_id: Optional[int] = Query(None, description="Filter by profession ID"),
    availability: Optional[str] = Query(None, description="Filter by availability status"),
    min_skill_rating: Optional[float] = Query(None, description="Minimum skill rating"),
    max_skill_rating: Optional[float] = Query(10.0, description="Maximum skill rating"),
    db: Session = Depends(get_db)
):
    """Get list of workers with optional filtering"""
    if profession_id:
        return crud.get_workers_by_profession(db, profession_id=profession_id)
    elif availability:
        return crud.get_workers_by_availability(db, availability=availability)
    elif min_skill_rating is not None:
        return crud.get_workers_by_skill_rating(db, min_rating=min_skill_rating, max_rating=max_skill_rating)
    
    return crud.get_workers_with_profession(db, skip=skip, limit=limit)

@router.get("/workers/available", response_model=List[schemas.WorkerWithProfession])
def get_available_workers(db: Session = Depends(get_db)):
    """Get workers who are available for assignment"""
    return crud.get_available_workers(db)

@router.get("/workers/by-project/{project_id}", response_model=List[schemas.WorkerWithProfession])
def get_workers_by_project(project_id: int, db: Session = Depends(get_db)):
    """Get workers currently assigned to a specific project"""
    return crud.get_workers_by_current_project(db, project_id=project_id)

@router.get("/workers/{worker_id}", response_model=schemas.WorkerDetailedView)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get specific worker by ID with complete details"""
    worker = crud.get_worker_with_history(db, worker_id=worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.put("/workers/{worker_id}", response_model=schemas.Worker)
def update_worker(worker_id: int, worker_update: schemas.WorkerUpdate, db: Session = Depends(get_db)):
    """Update worker information"""
    # Verify profession exists if being updated
    if worker_update.profession_id:
        profession = crud.get_profession(db, worker_update.profession_id)
        if not profession:
            raise HTTPException(status_code=400, detail="Profession not found")
    
    worker = crud.update_worker(db, worker_id=worker_id, worker_update=worker_update)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.delete("/workers/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete a worker"""
    success = crud.delete_worker(db, worker_id=worker_id)
    if not success:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"message": "Worker deleted successfully"}

@router.post("/workers/{worker_id}/assign-project")
def assign_worker_to_project(
    worker_id: int,
    project_id: int,
    start_date: date,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Assign worker to a project"""
    worker = crud.assign_worker_to_project(db, worker_id=worker_id, project_id=project_id, start_date=start_date, end_date=end_date)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"message": "Worker assigned to project successfully", "worker": worker}

@router.post("/workers/{worker_id}/unassign-project")
def unassign_worker_from_project(worker_id: int, db: Session = Depends(get_db)):
    """Remove worker from current project"""
    worker = crud.unassign_worker_from_project(db, worker_id=worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"message": "Worker unassigned from project successfully", "worker": worker}

# ===============================
# PROJECT HISTORY ENDPOINTS
# ===============================

@router.post("/project-history/", response_model=schemas.WorkerProjectHistory)
def create_project_history(history: schemas.WorkerProjectHistoryCreate, db: Session = Depends(get_db)):
    """Create a new project history entry"""
    # Verify worker exists
    worker = crud.get_worker(db, history.worker_id)
    if not worker:
        raise HTTPException(status_code=400, detail="Worker not found")
    
    return crud.create_worker_project_history(db=db, history=history)

@router.get("/project-history/worker/{worker_id}", response_model=List[schemas.WorkerProjectHistory])
def get_worker_project_history(worker_id: int, db: Session = Depends(get_db)):
    """Get all project history for a specific worker"""
    worker = crud.get_worker(db, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    return crud.get_worker_project_histories(db, worker_id=worker_id)

@router.get("/project-history/project/{project_id}", response_model=List[schemas.WorkerProjectHistory])
def get_project_worker_history(project_id: int, db: Session = Depends(get_db)):
    """Get all worker history for a specific project"""
    return crud.get_project_worker_histories(db, project_id=project_id)

@router.get("/project-history/active", response_model=List[schemas.WorkerProjectHistory])
def get_active_assignments(db: Session = Depends(get_db)):
    """Get all active worker project assignments"""
    return crud.get_active_worker_assignments(db)

@router.get("/project-history/{history_id}", response_model=schemas.WorkerProjectHistory)
def get_project_history(history_id: int, db: Session = Depends(get_db)):
    """Get specific project history entry"""
    history = crud.get_worker_project_history(db, history_id=history_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Project history not found")
    return history

@router.put("/project-history/{history_id}", response_model=schemas.WorkerProjectHistory)
def update_project_history(history_id: int, history_update: schemas.WorkerProjectHistoryUpdate, db: Session = Depends(get_db)):
    """Update project history entry"""
    history = crud.update_worker_project_history(db, history_id=history_id, history_update=history_update)
    if history is None:
        raise HTTPException(status_code=404, detail="Project history not found")
    return history

@router.post("/project-history/{history_id}/complete")
def complete_project_assignment(
    history_id: int,
    end_date: date,
    performance_rating: Optional[float] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Mark a project assignment as completed"""
    history = crud.complete_worker_project_assignment(
        db, 
        history_id=history_id, 
        end_date=end_date, 
        performance_rating=performance_rating, 
        notes=notes
    )
    if history is None:
        raise HTTPException(status_code=404, detail="Project history not found")
    return {"message": "Project assignment completed successfully", "history": history}

@router.delete("/project-history/{history_id}")
def delete_project_history(history_id: int, db: Session = Depends(get_db)):
    """Delete project history entry"""
    success = crud.delete_worker_project_history(db, history_id=history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project history not found")
    return {"message": "Project history deleted successfully"}