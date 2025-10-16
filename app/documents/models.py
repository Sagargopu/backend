from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    doc_type = Column(String, nullable=False)  # pdf, doc, docx, xlsx, jpg, png, etc.
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    component_id = Column(Integer, ForeignKey("project_components.id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="documents")
    component = relationship("ProjectComponent", back_populates="documents")
    uploader = relationship("User", back_populates="uploaded_documents")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


