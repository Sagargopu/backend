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
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="documents")
    component = relationship("ProjectComponent", back_populates="documents")
    task = relationship("Task", back_populates="documents")
    uploader = relationship("User", back_populates="uploaded_documents")
    access_permissions = relationship("DocumentAccess", back_populates="document", cascade="all, delete-orphan")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DocumentAccess(Base):
    __tablename__ = "document_access"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_level = Column(String(20), default="view")  # view, edit, admin
    granted_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_notes = Column(Text, nullable=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    document = relationship("Document", back_populates="access_permissions")
    user = relationship("User", foreign_keys=[user_id], back_populates="document_permissions")
    granted_by = relationship("User", foreign_keys=[granted_by_id])

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


