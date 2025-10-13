from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    storage_path = Column(String) # Path in Google Cloud Storage
    file_type = Column(String)

    # A document can be linked to a project component or a task
    component_id = Column(Integer, ForeignKey("project_components.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    uploader = relationship("User")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
