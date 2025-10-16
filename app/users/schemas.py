from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
from .roles import UserRole

# ===============================
# BASE USER SCHEMAS
# ===============================

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    
    @validator('role')
    def validate_role(cls, v):
        if v not in [role.value for role in UserRole]:
            raise ValueError(f'Invalid role. Must be one of: {[role.value for role in UserRole]}')
        return v

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
    invitation_expires_at: Optional[datetime] = None
    created_at: datetime

    @property
    def full_name(self) -> str:
        """Get full name by combining first and last name"""
        return f"{self.first_name} {self.last_name}".strip()

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    pass

# ===============================
# INVITATION SCHEMAS
# ===============================

class UserInvitation(BaseModel):
    """Schema for sending user invitations"""
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    invitation_message: Optional[str] = None
    
    @validator('role')
    def validate_role(cls, v):
        if v not in [role.value for role in UserRole]:
            raise ValueError(f'Invalid role. Must be one of: {[role.value for role in UserRole]}')
        return v

class InvitationResponse(BaseModel):
    """Response schema for invitation creation"""
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    invitation_token: str
    invitation_status: str
    invitation_sent_date: datetime
    invitation_expires_at: datetime
    invited_by_user_id: int
    
class UserSignup(BaseModel):
    """
    Schema for user signup with invitation token
    
    This is used when a user accepts an invitation and sets up their account.
    The user MUST provide a password during this step.
    """
    invitation_token: str
    password: str  # Required: User sets their own password during signup
    confirm_password: str  # Confirmation to ensure password accuracy
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Ensure password confirmation matches"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str  # Required for login

class PasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str

class PasswordReset(BaseModel):
    """Schema for password reset"""
    email: EmailStr

class SetPassword(BaseModel):
    """Schema for setting password (for users created without passwords)"""
    email: EmailStr
    temporary_password: str
    new_password: str

class LoginResponse(BaseModel):
    """Response schema for successful login"""
    user: User
    navigation_route: str
    access_token: Optional[str] = None  # For future JWT implementation
    token_type: Optional[str] = "bearer"

# ===============================
# LEGACY SCHEMAS (for backward compatibility)
# ===============================

class ClerkUserInvite(UserInvitation):
    """Legacy schema - use UserInvitation instead"""
    pass

class AccountSetup(UserSignup):
    """Legacy schema - use UserSignup instead"""
    pass

class UserInvitationStatus(BaseModel):
    """Schema for tracking invitation status"""
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    invitation_status: str
    invitation_sent_date: Optional[datetime]
    invited_by_user_id: Optional[int]
    account_setup_completed: bool
    
    @property
    def full_name(self) -> str:
        """Get full name by combining first and last name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    class Config:
        from_attributes = True