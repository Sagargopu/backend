from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from . import crud, models, schemas
from app.database import get_db

router = APIRouter()

# ===============================
# PROFESSION ENDPOINTS
# ===============================

@router.post("/professions/", response_model=schemas.Profession)
def create_profession(profession: schemas.ProfessionCreate, db: Session = Depends(get_db)):
    """Create a new profession"""
    return crud.create_profession(db=db, profession=profession)

@router.get("/professions/", response_model=List[schemas.Profession])
def read_professions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all professions"""
    professions = crud.get_professions(db, skip=skip, limit=limit)
    return professions

@router.get("/professions/{profession_id}", response_model=schemas.Profession)
def read_profession(profession_id: int, db: Session = Depends(get_db)):
    """Get profession by ID"""
    profession = crud.get_profession(db, profession_id=profession_id)
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession

@router.put("/professions/{profession_id}", response_model=schemas.Profession)
def update_profession(profession_id: int, profession: schemas.ProfessionUpdate, db: Session = Depends(get_db)):
    """Update profession by ID"""
    db_profession = crud.update_profession(db, profession_id=profession_id, profession_update=profession)
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return db_profession

@router.delete("/professions/{profession_id}")
def delete_profession(profession_id: int, db: Session = Depends(get_db)):
    """Delete profession by ID"""
    deleted = crud.delete_profession(db, profession_id=profession_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Profession not found")
    return {"detail": "Profession deleted successfully"}

# ===============================
# WORKER ENDPOINTS
# ===============================

@router.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    """Create a new worker"""
    return crud.create_worker(db=db, worker=worker)

@router.get("/workers/", response_model=List[schemas.WorkerWithProfession])
def read_workers(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all workers with profession details (no limit by default, use limit parameter for pagination)"""
    workers = crud.get_workers_with_profession(db, skip=skip, limit=limit)
    return workers

@router.get("/workers/{worker_id}", response_model=schemas.WorkerWithProfession)
def read_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get worker by ID with profession details"""
    worker = crud.get_worker_with_profession(db, worker_id=worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.get("/workers/by-profession/{profession_id}", response_model=List[schemas.WorkerWithProfession])
def read_workers_by_profession(profession_id: int, db: Session = Depends(get_db)):
    """Get all workers by profession ID with profession details"""
    workers = crud.get_workers_by_profession(db, profession_id=profession_id)
    return workers

@router.get("/workers/by-availability/{availability}", response_model=List[schemas.WorkerWithProfession])
def read_workers_by_availability(availability: str, db: Session = Depends(get_db)):
    """Get workers by availability status with profession details"""
    workers = crud.get_workers_by_availability(db, availability=availability)
    return workers

@router.get("/workers/available", response_model=List[schemas.WorkerWithProfession])
def read_available_workers(db: Session = Depends(get_db)):
    """Get all available workers with profession details"""
    workers = crud.get_available_workers(db)
    return workers

@router.put("/workers/{worker_id}", response_model=schemas.Worker)
def update_worker(worker_id: int, worker: schemas.WorkerUpdate, db: Session = Depends(get_db)):
    """Update worker by ID"""
    db_worker = crud.update_worker(db, worker_id=worker_id, worker_update=worker)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker

@router.delete("/workers/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete worker by ID"""
    deleted = crud.delete_worker(db, worker_id=worker_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"detail": "Worker deleted successfully"}

# ===============================
# WORKER PROJECT HISTORY ENDPOINTS
# ===============================

@router.post("/worker-history/", response_model=schemas.WorkerProjectHistory)
def create_worker_project_history(history: schemas.WorkerProjectHistoryCreate, db: Session = Depends(get_db)):
    """Create a new worker project history entry"""
    return crud.create_worker_project_history(db=db, history=history)

@router.get("/worker-history/{history_id}", response_model=schemas.WorkerProjectHistory)
def read_worker_project_history(history_id: int, db: Session = Depends(get_db)):
    """Get worker project history by ID"""
    history = crud.get_worker_project_history(db, history_id=history_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Worker project history not found")
    return history

@router.get("/workers/{worker_id}/history", response_model=List[schemas.WorkerProjectHistory])
def read_worker_histories(worker_id: int, db: Session = Depends(get_db)):
    """Get all project histories for a specific worker"""
    histories = crud.get_worker_project_histories(db, worker_id=worker_id)
    return histories

@router.get("/projects/{project_id}/worker-history", response_model=List[schemas.WorkerProjectHistoryWithName])
def read_project_worker_histories(project_id: int, db: Session = Depends(get_db)):
    """Get all worker histories for a specific project with worker names"""
    histories = crud.get_project_worker_histories_with_names(db, project_id=project_id)
    return histories

@router.put("/worker-history/{history_id}", response_model=schemas.WorkerProjectHistory)
def update_worker_project_history(history_id: int, history: schemas.WorkerProjectHistoryUpdate, db: Session = Depends(get_db)):
    """Update worker project history by ID"""
    db_history = crud.update_worker_project_history(db, history_id=history_id, history_update=history)
    if db_history is None:
        raise HTTPException(status_code=404, detail="Worker project history not found")
    return db_history

@router.delete("/worker-history/{history_id}")
def delete_worker_project_history(history_id: int, db: Session = Depends(get_db)):
    """Delete worker project history by ID"""
    deleted = crud.delete_worker_project_history(db, history_id=history_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Worker project history not found")
    return {"detail": "Worker project history deleted successfully"}
