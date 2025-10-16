from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Optional for invitation-based signup
    
    # Role and authentication fields
    role = Column(String, nullable=False, default='clerk')  # superadmin, business_admin, clerk, project_manager, accountant, client
    last_login_at = Column(DateTime(timezone=True), nullable=True)  # Track last login time
    
    
    # Invitation Management
    is_active = Column(Boolean, default=True)
    invited_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Which user invited this user
    invitation_token = Column(String, nullable=True, unique=True)  # Token for account setup
    invitation_status = Column(String, default='pending')  # 'pending', 'accepted', 'expired'
    invitation_sent_date = Column(DateTime(timezone=True), nullable=True)
    invitation_expires_at = Column(DateTime(timezone=True), nullable=True)  # Invitation expiry
    account_setup_completed = Column(Boolean, default=False)
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    
    # Relationships (using string references to avoid circular imports)
    invited_by = relationship("User", remote_side=[id], foreign_keys=[invited_by_user_id])
    
    # Cross-model relationships (using string references)
    managed_projects = relationship("Project", foreign_keys="Project.project_manager_id", lazy="dynamic")
    uploaded_documents = relationship("Document", back_populates="uploader")
    document_permissions = relationship("DocumentAccess", foreign_keys="DocumentAccess.user_id", back_populates="user")
    approved_transactions = relationship("Transaction", foreign_keys="Transaction.approved_by", back_populates="approver")
    created_transactions = relationship("Transaction", foreign_keys="Transaction.created_by", back_populates="creator")
    
    # Computed properties
    @property
    def full_name(self) -> str:
        """Get full name by combining first and last name"""
        return f"{self.first_name} {self.last_name}".strip()

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
