from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, schemas
from ..database import get_db

router = APIRouter()

# ===============================
# BASIC USER MANAGEMENT ONLY
# ===============================

@router.post("/clerk/invite-user/", response_model=schemas.User)
def clerk_invite_user(user_invite: schemas.ClerkUserInvite, clerk_id: int, db: Session = Depends(get_db)):
    """Clerk creates and invites new users (accountants, project managers, clients)"""
    # Verify clerk has permission
    clerk = crud.get_user(db, user_id=clerk_id)
    if clerk is None:
        raise HTTPException(status_code=404, detail="Clerk not found")
    if str(clerk.role) != 'clerk':
        raise HTTPException(status_code=403, detail="Only clerks can invite users")
    
    # Check if user already exists
    if crud.get_user_by_email(db, email=user_invite.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.clerk_invite_user(db=db, user_invite=user_invite, clerk_id=clerk_id)

@router.post("/setup-account/", response_model=schemas.User)
def setup_user_account(account_setup: schemas.AccountSetup, db: Session = Depends(get_db)):
    """User completes account setup using invitation token (no public signup)"""
    db_user = crud.complete_account_setup(db, account_setup=account_setup)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid token or invitation expired")
    return db_user

# ===============================
# BUSINESS ADMIN OPERATIONS
# ===============================

@router.get("/business-admin/overview/", response_model=dict)
def get_business_overview(admin_id: int, db: Session = Depends(get_db)):
    """Business admin gets complete company overview"""
    admin = crud.get_user(db, user_id=admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    if str(admin.role) != 'business_admin':
        raise HTTPException(status_code=403, detail="Only business admins can access company overview")
    
    # Get comprehensive business data
    total_users = crud.get_users(db, skip=0, limit=1000)  # Get all users for count
    
    return {
        "total_users": len(total_users),
        "users_by_role": {
            "clerks": len([u for u in total_users if str(u.role) == 'clerk']),
            "project_managers": len([u for u in total_users if str(u.role) == 'project_manager']),
            "accountants": len([u for u in total_users if str(u.role) == 'accountant']),
            "clients": len([u for u in total_users if str(u.role) == 'client']),
            "business_admins": len([u for u in total_users if str(u.role) == 'business_admin'])
        },
        "company_metrics": {
            "active_users": len([u for u in total_users if getattr(u, 'is_active', False)]),
            "pending_invitations": len(crud.get_pending_invitations(db, skip=0, limit=1000))
        }
    }

@router.get("/business-admin/users/", response_model=List[schemas.User])
def get_all_users_for_admin(admin_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Business admin gets all users with full details"""
    admin = crud.get_user(db, user_id=admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    if str(admin.role) != 'business_admin':
        raise HTTPException(status_code=403, detail="Only business admins can access all user data")
    
    return crud.get_users(db, skip=skip, limit=limit)

# ===============================
# STANDARD USER OPERATIONS
# ===============================

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get specific user details"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/admin/users/{user_id}/activate", response_model=schemas.User)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """Admin activate user account"""
    db_user = crud.activate_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/admin/users/{user_id}/deactivate", response_model=schemas.User)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """Admin deactivate user account"""
    db_user = crud.deactivate_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
