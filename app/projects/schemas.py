from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

# Schemas for Assignment
class AssignmentBase(BaseModel):
    task_id: int
    user_id: int

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Task
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = 'To Do'
    priority: str = 'Medium'

class TaskCreate(TaskBase):
    component_id: int

class Task(TaskBase):
    id: int
    component_id: int
    created_at: datetime
    assignments: List[Assignment] = []

    class Config:
        from_attributes = True

# Schemas for Project
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None
    status: str = 'planning'
    client_name: Optional[str] = None
    project_manager_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None
    status: Optional[str] = None
    client_name: Optional[str] = None
    project_manager_id: Optional[int] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas for ProjectComponent
class ProjectComponentBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    budget: Optional[Decimal] = None
    status: str = 'planned'
    details: Optional[dict] = None
    parent_id: Optional[int] = None

class ProjectComponentCreate(ProjectComponentBase):
    project_id: int

class ProjectComponentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    budget: Optional[Decimal] = None
    status: Optional[str] = None
    details: Optional[dict] = None
    parent_id: Optional[int] = None

class ProjectComponent(ProjectComponentBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tasks: List[Task] = []
    children: List['ProjectComponent'] = []  # Recursive model

    class Config:
        from_attributes = True

# Update recursive model reference
ProjectComponent.update_forward_refs()
