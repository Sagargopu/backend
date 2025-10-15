from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from . import models, schemas

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
# CLERK-CONTROLLED USER CREATION
# ===============================

def clerk_invite_user(db: Session, user_invite: schemas.ClerkUserInvite, clerk_id: int):
    """Clerk creates and invites professional users (accountants, project managers, clients)"""
    # Generate invitation token
    invitation_token = secrets.token_urlsafe(32)
    
    db_user = models.User(
        email=user_invite.email,
        full_name=user_invite.full_name,
        role=user_invite.role,
        is_active=True,
        invited_by_clerk=clerk_id,
        invitation_token=invitation_token,
        invitation_status='pending',
        invitation_sent_date=datetime.now(),
        account_setup_completed=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def complete_account_setup(db: Session, account_setup: schemas.AccountSetup):
    """User completes account setup using invitation token"""
    db_user = db.query(models.User).filter(
        models.User.invitation_token == account_setup.invitation_token,
        models.User.invitation_status == 'pending'
    ).first()
    
    if not db_user:
        return None
    
    # Update user with account setup info using proper SQLAlchemy update
    db.query(models.User).filter(models.User.id == db_user.id).update({
        models.User.account_setup_completed: True,
        models.User.invitation_status: "accepted",
        models.User.phone_number: account_setup.phone_number,
        models.User.address: account_setup.address,
        models.User.invitation_token: None  # Clear token after use
    })
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_pending_invitations(db: Session, skip: int = 0, limit: int = 100):
    """Get all pending user invitations"""
    return db.query(models.User).filter(
        models.User.invitation_status == 'pending'
    ).offset(skip).limit(limit).all()