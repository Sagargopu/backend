from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    storage_path = Column(String, nullable=False) # Path in Google Cloud Storage
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)  # File size in bytes
    document_type = Column(String, nullable=True)  # blueprint, contract, report, etc.

    # Hierarchy: A document can be linked to project, component, or task
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    component_id = Column(Integer, ForeignKey("project_components.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Access control
    is_public = Column(Boolean, default=False)  # If true, all users can view
    
    # Relationships
    project = relationship("Project", back_populates="documents")
    component = relationship("ProjectComponent", back_populates="documents")
    task = relationship("Task", back_populates="documents")
    uploader = relationship("User", back_populates="uploaded_documents")
    
    # Document access permissions
    access_permissions = relationship("DocumentAccess", back_populates="document", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DocumentAccess(Base):
    __tablename__ = "document_access"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    granted_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Access levels
    access_level = Column(String, default="view")  # view, edit, admin
    
    # Optional access notes
    access_notes = Column(Text, nullable=True)
    
    # Relationships
    document = relationship("Document", back_populates="access_permissions")
    user = relationship("User", foreign_keys=[user_id], back_populates="document_permissions")
    granted_by = relationship("User", foreign_keys=[granted_by_id])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DocumentShare(Base):
    __tablename__ = "document_shares"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    shared_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shared_with_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Share details
    share_message = Column(Text, nullable=True)
    share_type = Column(String, default="direct")  # direct, project_wide, component_wide
    is_temporary = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    document = relationship("Document")
    shared_by = relationship("User", foreign_keys=[shared_by_id])
    shared_with = relationship("User", foreign_keys=[shared_with_id])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
