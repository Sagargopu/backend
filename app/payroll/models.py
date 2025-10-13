from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Timesheet(Base):
    __tablename__ = "timesheets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("project_components.id"))
    clock_in_time = Column(DateTime)
    clock_out_time = Column(DateTime, nullable=True)
    status = Column(String, default="Clocked In") # Clocked In, Submitted, Approved, Rejected

class LaborCost(Base):
    __tablename__ = "labor_costs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project_components.id"))
    amount = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

