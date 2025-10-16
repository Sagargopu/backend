from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

# ===============================
# PROFESSION SCHEMAS
# ===============================

class ProfessionBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str

class ProfessionCreate(ProfessionBase):
    pass

class ProfessionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class Profession(ProfessionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ===============================
# WORKER SCHEMAS
# ===============================

class WorkerBase(BaseModel):
    worker_id: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    profession_id: int
    wage_rate: Decimal
    availability: str = "Available"  # "Available", "Assigned", "Unavailable", "On Leave"

class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(BaseModel):
    worker_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    profession_id: Optional[int] = None
    wage_rate: Optional[Decimal] = None
    availability: Optional[str] = None

class Worker(WorkerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WorkerWithProfession(Worker):
    profession: Profession

# ===============================
# PROJECT HISTORY SCHEMAS
# ===============================

class WorkerProjectHistoryBase(BaseModel):
    worker_id: int
    project_id: int
    start_date: date
    end_date: Optional[date] = None
    role: Optional[str] = None
    status: str = "Active"  # "Active", "Completed", "Terminated"

class WorkerProjectHistoryCreate(WorkerProjectHistoryBase):
    pass

class WorkerProjectHistoryUpdate(BaseModel):
    project_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    role: Optional[str] = None
    status: Optional[str] = None

class WorkerProjectHistory(WorkerProjectHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WorkerWithHistory(Worker):
    project_history: List[WorkerProjectHistory] = []

# ===============================
# COMBINED SCHEMAS
# ===============================

class WorkerDetailedView(WorkerWithProfession):
    """Complete worker details with profession and project history"""
    project_history: List[WorkerProjectHistory] = []