from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

# Simple schemas for User references
class UserReference(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    class Config:
        from_attributes = True

# Simple schema for ProjectType reference
class ProjectTypeReference(BaseModel):
    id: int
    category: str
    type_name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

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

# Enhanced Project schema with related object names and financial summary
class ProjectWithDetails(ProjectBase):
    id: int
    actual_budget: Optional[Decimal] = None
    accountant_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Related objects with names
    client: Optional[UserReference] = None
    project_manager: Optional[UserReference] = None
    accountant: Optional[UserReference] = None
    project_type: Optional[ProjectTypeReference] = None
    
    # Computed properties
    client_name: Optional[str] = None
    project_manager_name: Optional[str] = None
    accountant_name: Optional[str] = None
    project_type_name: Optional[str] = None
    
    # Financial summary
    purchase_orders_sum: Optional[float] = 0.0
    change_orders_sum: Optional[float] = 0.0

    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm_with_names(cls, obj, financial_summary=None):
        """Create ProjectWithDetails from ORM object with computed name fields and financial data"""
        data = obj.__dict__.copy()
        
        # Add computed name fields
        data['client_name'] = obj.client.full_name if obj.client else "No Client Assigned"
        data['project_manager_name'] = obj.project_manager.full_name if obj.project_manager else "No PM Assigned"
        data['accountant_name'] = obj.accountant.full_name if obj.accountant else "No Accountant Assigned"
        data['project_type_name'] = obj.project_type.type_name if obj.project_type else "No Type Assigned"
        
        # Include related objects
        if obj.client:
            data['client'] = obj.client
        if obj.project_manager:
            data['project_manager'] = obj.project_manager
        if obj.accountant:
            data['accountant'] = obj.accountant
        if obj.project_type:
            data['project_type'] = obj.project_type
            
        # Add financial summary if provided
        if financial_summary:
            data['purchase_orders_sum'] = financial_summary.get('purchase_orders_sum', 0.0)
            data['change_orders_sum'] = financial_summary.get('change_orders_sum', 0.0)
        else:
            data['purchase_orders_sum'] = 0.0
            data['change_orders_sum'] = 0.0
            
        return cls(**data)

# Schemas for ProjectComponent
class ProjectComponentBase(BaseModel):
    name: str
    description: Optional[str] = None
    budget: Optional[Decimal] = None
    status: str = 'planned'
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    parent_id: Optional[int] = None

class ProjectComponentCreate(ProjectComponentBase):
    project_id: int

class ProjectComponentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[Decimal] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
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
