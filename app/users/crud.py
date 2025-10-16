from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from . import models, schemas
from .roles import RolePermissions, UserRole
from .password import hash_password, verify_password

# ===============================
# BASIC USER OPERATIONS
# ===============================

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def activate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.query(models.User).filter(models.User.id == user_id).update({
            models.User.is_active: True
        })
        db.commit()
        db.refresh(db_user)
    return db_user

def deactivate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.query(models.User).filter(models.User.id == user_id).update({
            models.User.is_active: False
        })
        db.commit()
        db.refresh(db_user)
    return db_user

# ===============================
# ROLE-BASED INVITATION SYSTEM
# ===============================

def send_user_invitation(db: Session, invitation: schemas.UserInvitation, inviter_id: int):
    """Send invitation to a new user with role-based validation"""
    
    # Get inviter
    inviter = get_user(db, inviter_id)
    if not inviter:
        raise ValueError("Inviter not found")
    
    # Check if inviter has permission to invite this role
    if not RolePermissions.can_invite_role(str(inviter.role), invitation.role):
        raise ValueError(f"User with role '{inviter.role}' cannot invite role '{invitation.role}'")
    
    # Check if user already exists
    existing_user = get_user_by_email(db, invitation.email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Generate invitation token and expiry (7 days from now)
    invitation_token = secrets.token_urlsafe(32)
    invitation_expires = datetime.now() + timedelta(days=7)
    
    # Create user with invitation
    db_user = models.User(
        email=invitation.email,
        first_name=invitation.first_name,
        last_name=invitation.last_name,
        role=invitation.role,
        is_active=False,  # Inactive until they complete signup
        invited_by_user_id=inviter_id,
        invitation_token=invitation_token,
        invitation_status='pending',
        invitation_sent_date=datetime.now(),
        invitation_expires_at=invitation_expires,
        account_setup_completed=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def complete_user_signup(db: Session, signup_data: schemas.UserSignup):
    """Complete user signup using invitation token"""
    
    # Find user by invitation token
    db_user = db.query(models.User).filter(
        models.User.invitation_token == signup_data.invitation_token,
        models.User.invitation_status == 'pending'
    ).first()
    
    if not db_user:
        raise ValueError("Invalid invitation token")
    
    # Check if invitation has expired
    expires_at = getattr(db_user, 'invitation_expires_at', None)
    if expires_at and datetime.now() > expires_at:
        # Mark invitation as expired
        db.query(models.User).filter(models.User.id == db_user.id).update({
            models.User.invitation_status: "expired"
        })
        db.commit()
        raise ValueError("Invitation has expired")
    
    # Update user with signup info
    update_data = {
        models.User.account_setup_completed: True,
        models.User.invitation_status: "accepted",
        models.User.is_active: True,
        models.User.invitation_token: None,  # Clear token after use
        models.User.last_login_at: datetime.now(),
        models.User.hashed_password: hash_password(signup_data.password)  # Hash the password
    }
    
    # Add optional fields if provided
    if signup_data.phone_number:
        update_data[models.User.phone_number] = signup_data.phone_number
    if signup_data.address:
        update_data[models.User.address] = signup_data.address
    if signup_data.emergency_contact_name:
        update_data[models.User.emergency_contact_name] = signup_data.emergency_contact_name
    if signup_data.emergency_contact_phone:
        update_data[models.User.emergency_contact_phone] = signup_data.emergency_contact_phone
    
    db.query(models.User).filter(models.User.id == db_user.id).update(update_data)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, login_data: schemas.UserLogin):
    """Authenticate user and return user with navigation route"""
    
    # Find user by email
    db_user = get_user_by_email(db, login_data.email)
    
    if not db_user:
        raise ValueError("User not found")
    
    if not getattr(db_user, 'is_active', False):
        raise ValueError("User account is not active")
    
    if not getattr(db_user, 'account_setup_completed', False):
        raise ValueError("Account setup not completed")
    
    # Verify password if user has one
    user_password = getattr(db_user, 'hashed_password', None)
    if user_password:
        if not verify_password(login_data.password, user_password):
            raise ValueError("Incorrect password")
    elif login_data.password:
        # User doesn't have a password but one was provided
        raise ValueError("This account doesn't use password authentication")
    # If no password is stored and none provided, allow access (legacy users)
    
    # Update last login time
    db.query(models.User).filter(models.User.id == db_user.id).update({
        models.User.last_login_at: datetime.now()
    })
    db.commit()
    db.refresh(db_user)
    
    # Get navigation route based on role
    user_role = getattr(db_user, 'role', 'client')
    navigation_route = RolePermissions.get_navigation_route(str(user_role))
    
    return db_user, navigation_route

def get_user_by_invitation_token(db: Session, token: str):
    """Get user by invitation token"""
    return db.query(models.User).filter(
        models.User.invitation_token == token,
        models.User.invitation_status == 'pending'
    ).first()

def expire_old_invitations(db: Session):
    """Mark expired invitations as expired"""
    current_time = datetime.now()
    
    expired_users = db.query(models.User).filter(
        models.User.invitation_status == 'pending',
        models.User.invitation_expires_at < current_time
    ).all()
    
    for user in expired_users:
        db.query(models.User).filter(models.User.id == user.id).update({
            models.User.invitation_status: "expired"
        })
    
    db.commit()
    return len(expired_users)

def get_pending_invitations(db: Session, skip: int = 0, limit: int = 100):
    """Get all pending user invitations"""
    return db.query(models.User).filter(
        models.User.invitation_status == 'pending'
    ).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, role: str, skip: int = 0, limit: int = 100):
    """Get users by role"""
    return db.query(models.User).filter(
        models.User.role == role,
        models.User.is_active == True
    ).offset(skip).limit(limit).all()

def create_user_with_password(db: Session, email: str, first_name: str, last_name: str, role: str, password: str):
    """Create a user directly with password (for admin use)"""
    
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Validate role
    if role not in [r.value for r in UserRole]:
        raise ValueError(f"Invalid role: {role}")
    
    # Create user
    db_user = models.User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
        hashed_password=hash_password(password),
        is_active=True,
        account_setup_completed=True,
        invitation_status="accepted"
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# ===============================
# LEGACY FUNCTIONS (for backward compatibility)
# ===============================

def clerk_invite_user(db: Session, user_invite: schemas.ClerkUserInvite, clerk_id: int):
    """Legacy function - use send_user_invitation instead"""
    invitation = schemas.UserInvitation(
        email=user_invite.email,
        first_name=user_invite.first_name,
        last_name=user_invite.last_name,
        role=user_invite.role,
        invitation_message=user_invite.invitation_message
    )
    return send_user_invitation(db, invitation, clerk_id)

def complete_account_setup(db: Session, account_setup: schemas.AccountSetup):
    """Legacy function - use complete_user_signup instead"""
    # AccountSetup inherits from UserSignup, so we can use it directly
    return complete_user_signup(db, account_setup)