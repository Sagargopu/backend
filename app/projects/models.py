from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Date, Numeric, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from app.database import Base

class ProjectType(Base):
    __tablename__ = "project_types"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    type_name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="project_type")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    planned_budget = Column(Numeric(15, 2))  # Initial planned budget
    actual_budget = Column(Numeric(15, 2), default=0)  # Actual spent budget
    status = Column(String(50), default='planned')  # planned, in_progress, completed, on_hold
    client_id = Column(Integer, ForeignKey("users.id"))  # Client as FK to User
    project_manager_id = Column(Integer, ForeignKey("users.id"))  # PM as FK to User
    project_type_id = Column(Integer, ForeignKey("project_types.id"))  # ProjectType as FK

    # Relationships
    client = relationship("User", foreign_keys=[client_id])
    project_manager = relationship("User", foreign_keys=[project_manager_id], back_populates="managed_projects")
    project_type = relationship("ProjectType", back_populates="projects")
    components = relationship("ProjectComponent", back_populates="project", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="project")
    all_tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @validates('start_date', 'end_date')
    def validate_project_dates(self, key, value):
        if key == 'end_date' and value is not None and hasattr(self, 'start_date') and self.start_date is not None:
            if value < self.start_date:
                raise ValueError("Project end date must be after start date")
        return value

class ProjectComponent(Base):
    __tablename__ = "project_components"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    budget = Column(Numeric(15, 2))
    status = Column(String(50), default='planned')  # planned, in_progress, completed, on_hold
    start_date = Column(Date)
    end_date = Column(Date)
    
    # Self-referential relationship for component hierarchy
    parent_id = Column(Integer, ForeignKey("project_components.id"))
    parent = relationship("ProjectComponent", remote_side=[id], back_populates="children")
    children = relationship("ProjectComponent", back_populates="parent", cascade="all, delete-orphan")
    
    # Relationships
    project = relationship("Project", back_populates="components")
    tasks = relationship("Task", back_populates="component", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="component")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @validates('start_date', 'end_date')
    def validate_component_dates(self, key, value):
        if value is None:
            return value
            
        # Validate component dates are within project dates
        if self.project:
            if key == 'start_date' and self.project.start_date and value < self.project.start_date:
                raise ValueError("Component start date must be after project start date")
            if key == 'end_date' and self.project.end_date and value > self.project.end_date:
                raise ValueError("Component end date must be before project end date")
        
        # Validate start_date < end_date
        if key == 'end_date' and hasattr(self, 'start_date') and self.start_date is not None:
            if value < self.start_date:
                raise ValueError("Component end date must be after start date")
                
        return value

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    status = Column(String(50), default='To Do')  # To Do, In Progress, Done, Blocked, Cancelled, Backlog
    priority = Column(String(50), default='Medium')  # Low, Medium, High, Critical

    # Project and Component Relationships
    component_id = Column(Integer, ForeignKey("project_components.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)  # Direct project link for easier queries
    
    # Task Management Details
    task_type = Column(String(100))  # 'Planning', 'Construction', 'Inspection', 'Documentation'
    budget = Column(Numeric(15, 2))  # Task budget allocation
    start_date = Column(Date)  # Task start date
    end_date = Column(Date)  # Task end date
    
    # Relationships
    component = relationship("ProjectComponent", back_populates="tasks")
    project = relationship("Project", back_populates="all_tasks")
    documents = relationship("Document", back_populates="task")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @validates('start_date', 'end_date')
    def validate_task_dates(self, key, value):
        if value is None:
            return value
            
        # Validate task dates are within component dates (if task has component)
        if self.component:
            if key == 'start_date' and self.component.start_date and value < self.component.start_date:
                raise ValueError("Task start date must be after component start date")
            if key == 'end_date' and self.component.end_date and value > self.component.end_date:
                raise ValueError("Task end date must be before component end date")
        
        # Validate task dates are within project dates
        elif self.project:
            if key == 'start_date' and self.project.start_date and value < self.project.start_date:
                raise ValueError("Task start date must be after project start date")
            if key == 'end_date' and self.project.end_date and value > self.project.end_date:
                raise ValueError("Task end date must be before project end date")
        
        # Validate start_date < end_date
        if key == 'end_date' and hasattr(self, 'start_date') and self.start_date is not None:
            if value < self.start_date:
                raise ValueError("Task end date must be after start date")
                
        return value




