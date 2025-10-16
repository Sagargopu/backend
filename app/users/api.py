from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, schemas
from .roles import RolePermissions, UserRole
from ..database import get_db

router = APIRouter()

# ===============================
# ROLE-BASED INVITATION SYSTEM
# ===============================

@router.post("/invite/", response_model=schemas.User)
def send_invitation(
    invitation: schemas.UserInvitation, 
    inviter_id: int, 
    db: Session = Depends(get_db)
):
    """Send role-based invitation to a new user"""
    try:
        invited_user = crud.send_user_invitation(db=db, invitation=invitation, inviter_id=inviter_id)
        return invited_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signup/", response_model=schemas.User)
def user_signup(
    signup_data: schemas.UserSignup, 
    db: Session = Depends(get_db)
):
    """Complete user signup using invitation token"""
    try:
        user = crud.complete_user_signup(db=db, signup_data=signup_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login/", response_model=schemas.LoginResponse)
def user_login(
    login_data: schemas.UserLogin, 
    db: Session = Depends(get_db)
):
    """Authenticate user and get navigation route based on role"""
    try:
        user, navigation_route = crud.authenticate_user(db=db, login_data=login_data)
        return schemas.LoginResponse(
            user=user,
            navigation_route=navigation_route
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/invitation/{token}/", response_model=schemas.User)
def get_invitation_details(token: str, db: Session = Depends(get_db)):
    """Get invitation details by token for signup form"""
    user = crud.get_user_by_invitation_token(db, token)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired invitation token")
    return user

@router.get("/invitations/pending/", response_model=List[schemas.User])
def get_pending_invitations(
    requester_id: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get pending invitations (admin/clerk only)"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only superadmin and clerks can view pending invitations
    if str(requester.role) not in [UserRole.SUPERADMIN.value, UserRole.CLERK.value]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    invitations = crud.get_pending_invitations(db, skip=skip, limit=limit)
    return invitations

@router.post("/invitations/expire/")
def expire_old_invitations(
    requester_id: int,
    db: Session = Depends(get_db)
):
    """Expire old invitations (admin only)"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only superadmin can expire invitations
    if str(requester.role) != UserRole.SUPERADMIN.value:
        raise HTTPException(status_code=403, detail="Only superadmin can expire invitations")
    
    expired_count = crud.expire_old_invitations(db)
    return {"message": f"Expired {expired_count} old invitations"}

@router.get("/roles/", response_model=List[str])
def get_available_roles(
    requester_id: int,
    db: Session = Depends(get_db)
):
    """Get roles that the current user can invite"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get roles this user can invite
    available_roles = RolePermissions.INVITATION_PERMISSIONS.get(
        UserRole(str(requester.role)), 
        []
    )
    
    return [role.value for role in available_roles]

# ===============================
# USER MANAGEMENT
# ===============================

@router.get("/users/", response_model=List[schemas.User])
def get_users(
    requester_id: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get users (admin/clerk only)"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only admin and clerk can view all users
    if str(requester.role) not in [UserRole.SUPERADMIN.value, UserRole.BUSINESS_ADMIN.value, UserRole.CLERK.value]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/role/{role}/", response_model=List[schemas.User])
def get_users_by_role(
    role: str,
    requester_id: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get users by role (admin/clerk only)"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only admin and clerk can view users by role
    if str(requester.role) not in [UserRole.SUPERADMIN.value, UserRole.BUSINESS_ADMIN.value, UserRole.CLERK.value]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Validate role
    if role not in [r.value for r in UserRole]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    users = crud.get_users_by_role(db, role, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}/activate/")
def activate_user_account(
    user_id: int,
    requester_id: int,
    db: Session = Depends(get_db)
):
    """Activate user account (admin only)"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only superadmin and business admin can activate users
    if str(requester.role) not in [UserRole.SUPERADMIN.value, UserRole.BUSINESS_ADMIN.value]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    user = crud.activate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User activated successfully"}

@router.put("/users/{user_id}/deactivate/")
def deactivate_user_account(
    user_id: int,
    requester_id: int,
    db: Session = Depends(get_db)
):
    """Deactivate user account (admin only)"""
    requester = crud.get_user(db, requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only superadmin and business admin can deactivate users
    if str(requester.role) not in [UserRole.SUPERADMIN.value, UserRole.BUSINESS_ADMIN.value]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    user = crud.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deactivated successfully"}

# ===============================
# LEGACY ENDPOINTS (for backward compatibility)
# ===============================

@router.post("/clerk/invite-user/", response_model=schemas.User)
def clerk_invite_user(user_invite: schemas.ClerkUserInvite, clerk_id: int, db: Session = Depends(get_db)):
    """Legacy endpoint - use /invite/ instead"""
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
