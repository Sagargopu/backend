from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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
        orm_mode = True

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
        orm_mode = True

# Schemas for ProjectComponent
class ProjectComponentBase(BaseModel):
    name: str
    type: str
    details: Optional[dict] = None
    parent_id: Optional[int] = None

class ProjectComponentCreate(ProjectComponentBase):
    pass

class ProjectComponent(ProjectComponentBase):
    id: int
    created_at: datetime
    tasks: List[Task] = []
    # children: List['ProjectComponent'] = [] # Recursive model

    class Config:
        orm_mode = True

# Update recursive model reference
# ProjectComponent.update_forward_refs()
