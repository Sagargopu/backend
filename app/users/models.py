from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # Hashed password will be added in the final security phase
    # hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) 
    # Roles: 'clerk', 'project_manager', 'accountant', 'client', 'business_admin'
    
    # Clerk-Controlled User Management
    is_active = Column(Boolean, default=True)
    invited_by_clerk = Column(Integer, ForeignKey("users.id"), nullable=True)  # Which clerk invited this user
    invitation_token = Column(String, nullable=True)  # Token for account setup
    invitation_status = Column(String, default='pending')  # 'pending', 'accepted', 'expired'
    invitation_sent_date = Column(DateTime(timezone=True), nullable=True)
    account_setup_completed = Column(Boolean, default=False)
    
    # Basic Contact Information
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    
    # Relationships
    managed_projects = relationship("Project", back_populates="project_manager", foreign_keys="Project.project_manager_id")
    invited_by = relationship("User", remote_side=[id], foreign_keys=[invited_by_clerk])
    
    approved_transactions = relationship("Transaction", foreign_keys="Transaction.approved_by", back_populates="approver")
    created_transactions = relationship("Transaction", foreign_keys="Transaction.created_by", back_populates="creator")
    
    # Document relationships
    uploaded_documents = relationship("Document", back_populates="uploader")
    document_permissions = relationship("DocumentAccess", foreign_keys="DocumentAccess.user_id", back_populates="user")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
