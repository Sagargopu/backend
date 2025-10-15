from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ===============================
# BASE USER SCHEMAS
# ===============================

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    invitation_status: Optional[str] = None
    account_setup_completed: bool = False
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    pass

# ===============================
# CLERK INVITATION SCHEMAS
# ===============================

class ClerkUserInvite(BaseModel):
    """Schema for clerk inviting professional users (accountants, project managers, clients)"""
    email: EmailStr
    full_name: str
    role: str  # 'accountant', 'project_manager', 'client', 'business_admin'
    invitation_message: Optional[str] = None

class UserInvitationStatus(BaseModel):
    """Schema for tracking invitation status"""
    id: int
    email: EmailStr
    full_name: str
    role: str
    invitation_status: str
    invitation_sent_date: Optional[datetime]
    invited_by_clerk: Optional[int]
    account_setup_completed: bool
    
    class Config:
        from_attributes = True

class AccountSetup(BaseModel):
    """Schema for user completing account setup"""
    invitation_token: str
    password: str
    phone_number: Optional[str] = None
    address: Optional[str] = None