from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from .crud import get_user_by_email, get_user
from .models import User
from .roles import UserRole, RolePermissions
from ..database import get_db

# ===============================
# AUTHENTICATION DEPENDENCIES
# ===============================

async def get_current_user_from_header(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from authorization header
    This is a placeholder for future JWT implementation
    For now, expects "Bearer user_id" format
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, user_identifier = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
            )
        
        # For now, treat user_identifier as user_id
        # In production, this would be a JWT token
        user_id = int(user_identifier)
        user = get_user(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        if not getattr(user, 'is_active', False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive",
            )
        
        if not getattr(user, 'account_setup_completed', False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account setup not completed",
            )
        
        return user
        
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format",
        )

async def get_current_user_from_email(
    user_email: str,
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user by email (for simple authentication)
    """
    user = get_user_by_email(db, user_email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not getattr(user, 'is_active', False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )
    
    if not getattr(user, 'account_setup_completed', False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account setup not completed",
        )
    
    return user

# ===============================
# ROLE-BASED ACCESS CONTROL
# ===============================

def require_role(required_role: UserRole):
    """
    Dependency factory to require specific role
    """
    def role_checker(current_user: User = Depends(get_current_user_from_header)):
        if str(current_user.role) != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role.value}",
            )
        return current_user
    return role_checker

def require_roles(allowed_roles: list[UserRole]):
    """
    Dependency factory to require one of multiple roles
    """
    def roles_checker(current_user: User = Depends(get_current_user_from_header)):
        if str(current_user.role) not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed roles: {[role.value for role in allowed_roles]}",
            )
        return current_user
    return roles_checker

def require_minimum_role(minimum_role: UserRole):
    """
    Dependency factory to require minimum role level
    """
    def min_role_checker(current_user: User = Depends(get_current_user_from_header)):
        if not RolePermissions.has_higher_or_equal_permission(str(current_user.role), minimum_role.value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Minimum required role: {minimum_role.value}",
            )
        return current_user
    return min_role_checker

# ===============================
# COMMON ROLE DEPENDENCIES
# ===============================

# Superadmin only
require_superadmin = require_role(UserRole.SUPERADMIN)

# Business admin or higher
require_business_admin = require_roles([UserRole.SUPERADMIN, UserRole.BUSINESS_ADMIN])

# Clerk or higher (for invitations)
require_clerk_or_higher = require_roles([UserRole.SUPERADMIN, UserRole.CLERK])

# Admin roles (superadmin, business admin, clerk)
require_admin_role = require_roles([UserRole.SUPERADMIN, UserRole.BUSINESS_ADMIN, UserRole.CLERK])

# Project manager or higher
require_pm_or_higher = require_roles([
    UserRole.SUPERADMIN, 
    UserRole.BUSINESS_ADMIN, 
    UserRole.CLERK, 
    UserRole.PROJECT_MANAGER
])

# Accountant or higher (for finance operations)
require_accountant_or_higher = require_roles([
    UserRole.SUPERADMIN, 
    UserRole.BUSINESS_ADMIN, 
    UserRole.CLERK, 
    UserRole.ACCOUNTANT
])

# Any authenticated user
require_authenticated = get_current_user_from_header

# ===============================
# PERMISSION HELPERS
# ===============================

def can_manage_user(manager: User, target_user: User) -> bool:
    """Check if manager can manage target user"""
    manager_level = RolePermissions.ROLE_HIERARCHY.get(UserRole(str(manager.role)), 0)
    target_level = RolePermissions.ROLE_HIERARCHY.get(UserRole(str(target_user.role)), 0)
    
    # Can only manage users with lower permission level
    return manager_level > target_level

def can_invite_role(inviter: User, target_role: str) -> bool:
    """Check if inviter can invite target role"""
    return RolePermissions.can_invite_role(str(inviter.role), target_role)

def get_user_navigation_route(user: User) -> str:
    """Get navigation route for user based on role"""
    return RolePermissions.get_navigation_route(str(user.role))