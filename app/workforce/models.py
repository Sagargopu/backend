from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Profession(Base):
    """
    Separate profession table for different construction trades
    """
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)  # "Electrician", "Plumber", "Carpenter"
    description = Column(Text)
    category = Column(String(50), nullable=False)  # "Electrical", "Plumbing", "Structural", "Finishing"
    
    # Relationships
    workers = relationship("Worker", back_populates="profession")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Worker(Base):
    """
    Worker details with wages, project history, and availability
    """
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(String(20), unique=True, nullable=False, index=True)  # Custom worker ID
    
    # Personal Information
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    phone_number = Column(String(20))
    email = Column(String(100), unique=True, index=True)
    
    # Profession and Skills
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False)
    
    # Wages
    wage_rate = Column(DECIMAL(10, 2), nullable=False)  # Hourly wage rate
    
    # Availability Status
    availability = Column(String(20), default="Available")  # "Available", "Assigned", "Unavailable", "On Leave"
    
    # Relationships
    profession = relationship("Profession", back_populates="workers")
    project_history = relationship("WorkerProjectHistory", back_populates="worker")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WorkerProjectHistory(Base):
    """
    Track worker's past and current project assignments
    """
    __tablename__ = "worker_project_history"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)  # Reference to project
    
    # Project assignment details
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Null if currently active
    role = Column(String(100))  # Role in the project
    
    # Project status
    status = Column(String(20), default="Active")  # "Active", "Completed", "Terminated"
    
    # Relationships
    worker = relationship("Worker", back_populates="project_history")
    project = relationship("Project")  # Relationship to Project
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())