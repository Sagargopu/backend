from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

# Schemas for ProjectType
class ProjectTypeBase(BaseModel):
    category: str
    type_name: str
    description: Optional[str] = None

class ProjectTypeCreate(ProjectTypeBase):
    pass

class ProjectTypeUpdate(BaseModel):
    category: Optional[str] = None
    type_name: Optional[str] = None
    description: Optional[str] = None

class ProjectType(ProjectTypeBase):
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
    task_type: Optional[str] = None
    budget: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TaskCreate(TaskBase):
    component_id: Optional[int] = None
    project_id: int

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    task_type: Optional[str] = None
    budget: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    component_id: Optional[int] = None

class Task(TaskBase):
    id: int
    component_id: Optional[int] = None
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas for Project
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    planned_budget: Optional[Decimal] = None
    status: str = 'planned'
    client_id: Optional[int] = None
    project_manager_id: Optional[int] = None
    project_type_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    planned_budget: Optional[Decimal] = None
    actual_budget: Optional[Decimal] = None
    status: Optional[str] = None
    client_id: Optional[int] = None
    project_manager_id: Optional[int] = None
    project_type_id: Optional[int] = None

class Project(ProjectBase):
    id: int
    actual_budget: Optional[Decimal] = None
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
