from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

from . import models, schemas

# ===============================
# PROFESSION CRUD
# ===============================

def create_profession(db: Session, profession: schemas.ProfessionCreate):
    """Create a new profession"""
    db_profession = models.Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession

def get_profession(db: Session, profession_id: int):
    """Get profession by ID"""
    return db.query(models.Profession).filter(models.Profession.id == profession_id).first()

def get_professions(db: Session, skip: int = 0, limit: int = 100):
    """Get list of all professions"""
    return db.query(models.Profession).offset(skip).limit(limit).all()

def get_profession_by_name(db: Session, name: str):
    """Get profession by name"""
    return db.query(models.Profession).filter(models.Profession.name == name).first()

def update_profession(db: Session, profession_id: int, profession_update: schemas.ProfessionUpdate):
    """Update profession"""
    db_profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if db_profession:
        update_data = profession_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_profession, key, value)
        db.commit()
        db.refresh(db_profession)
    return db_profession

def delete_profession(db: Session, profession_id: int):
    """Delete profession"""
    db_profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if db_profession:
        db.delete(db_profession)
        db.commit()
        return True
    return False

# ===============================
# WORKER CRUD
# ===============================

def create_worker(db: Session, worker: schemas.WorkerCreate):
    """Create a new worker"""
    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def get_worker(db: Session, worker_id: int):
    """Get worker by ID with profession"""
    return db.query(models.Worker).filter(models.Worker.id == worker_id).first()

def get_worker_with_profession(db: Session, worker_id: int):
    """Get worker by ID with profession details"""
    return db.query(models.Worker).options(joinedload(models.Worker.profession)).filter(models.Worker.id == worker_id).first()

def get_worker_by_worker_id(db: Session, worker_id: str):
    """Get worker by worker_id"""
    return db.query(models.Worker).filter(models.Worker.worker_id == worker_id).first()

def get_workers(db: Session, skip: int = 0, limit: Optional[int] = None):
    """Get list of all workers"""
    query = db.query(models.Worker).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def get_workers_with_profession(db: Session, skip: int = 0, limit: Optional[int] = None):
    """Get list of all workers with profession details"""
    query = db.query(models.Worker).options(joinedload(models.Worker.profession)).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def get_workers_by_profession(db: Session, profession_id: int):
    """Get workers by profession"""
    return db.query(models.Worker).options(joinedload(models.Worker.profession)).filter(models.Worker.profession_id == profession_id).all()

def get_workers_by_availability(db: Session, availability: str):
    """Get workers by availability status"""
    return db.query(models.Worker).options(joinedload(models.Worker.profession)).filter(models.Worker.availability == availability).all()

def get_available_workers(db: Session):
    """Get all available workers"""
    return db.query(models.Worker).options(joinedload(models.Worker.profession)).filter(models.Worker.availability == "Available").all()

def update_worker(db: Session, worker_id: int, worker_update: schemas.WorkerUpdate):
    """Update worker"""
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if db_worker:
        update_data = worker_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_worker, key, value)
        db.commit()
        db.refresh(db_worker)
    return db_worker

def delete_worker(db: Session, worker_id: int):
    """Delete worker"""
    db_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if db_worker:
        db.delete(db_worker)
        db.commit()
        return True
    return False

# ===============================
# WORKER PROJECT HISTORY CRUD
# ===============================

def create_worker_project_history(db: Session, history: schemas.WorkerProjectHistoryCreate):
    """Create worker project history entry"""
    db_history = models.WorkerProjectHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_worker_project_history(db: Session, history_id: int):
    """Get project history by ID"""
    return db.query(models.WorkerProjectHistory).filter(models.WorkerProjectHistory.id == history_id).first()

def get_worker_project_histories(db: Session, worker_id: int):
    """Get all project histories for a worker"""
    return db.query(models.WorkerProjectHistory).filter(models.WorkerProjectHistory.worker_id == worker_id).all()

def get_project_worker_histories(db: Session, project_id: int):
    """Get all worker histories for a project"""
    return db.query(models.WorkerProjectHistory).filter(models.WorkerProjectHistory.project_id == project_id).all()

def get_project_worker_histories_with_names(db: Session, project_id: int):
    """Get all worker histories for a project with worker names"""
    histories = db.query(
        models.WorkerProjectHistory,
        models.Worker.first_name,
        models.Worker.last_name
    ).join(
        models.Worker, 
        models.WorkerProjectHistory.worker_id == models.Worker.id
    ).filter(
        models.WorkerProjectHistory.project_id == project_id
    ).all()
    
    result = []
    for history, first_name, last_name in histories:
        history_dict = {
            "id": history.id,
            "worker_id": history.worker_id,
            "project_id": history.project_id,
            "start_date": history.start_date,
            "end_date": history.end_date,
            "role": history.role,
            "status": history.status,
            "worker_first_name": first_name,
            "worker_last_name": last_name,
            "worker_full_name": f"{first_name} {last_name}",
            "created_at": history.created_at,
            "updated_at": history.updated_at
        }
        result.append(history_dict)
    
    return result

def get_active_worker_assignments(db: Session):
    """Get all active worker project assignments"""
    return db.query(models.WorkerProjectHistory).filter(models.WorkerProjectHistory.status == "Active").all()

def update_worker_project_history(db: Session, history_id: int, history_update: schemas.WorkerProjectHistoryUpdate):
    """Update worker project history"""
    db_history = db.query(models.WorkerProjectHistory).filter(models.WorkerProjectHistory.id == history_id).first()
    if db_history:
        update_data = history_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_history, key, value)
        db.commit()
        db.refresh(db_history)
    return db_history

def delete_worker_project_history(db: Session, history_id: int):
    """Delete worker project history"""
    db_history = db.query(models.WorkerProjectHistory).filter(models.WorkerProjectHistory.id == history_id).first()
    if db_history:
        db.delete(db_history)
        db.commit()
        return True
    return False
