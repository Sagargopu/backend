from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class ProjectComponent(Base):
    __tablename__ = "project_components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) # e.g., 'COMMUNITY', 'BUILDING', 'PHASE', 'FLOOR'
    details = Column(JSON)
    
    parent_id = Column(Integer, ForeignKey("project_components.id"))
    parent = relationship("ProjectComponent", remote_side=[id])
    children = relationship("ProjectComponent")

    tasks = relationship("Task", back_populates="component")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String, default='To Do') # To Do, In Progress, Done
    priority = Column(String, default='Medium') # Low, Medium, High

    component_id = Column(Integer, ForeignKey("project_components.id"))
    component = relationship("ProjectComponent", back_populates="tasks")

    assignments = relationship("Assignment", back_populates="task")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    task = relationship("Task", back_populates="assignments")
    assignee = relationship("User")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
