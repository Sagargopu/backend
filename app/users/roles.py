from enum import Enum
from typing import List, Dict

class UserRole(str, Enum):
    """User role definitions"""
    SUPERADMIN = "superadmin"
    BUSINESS_ADMIN = "business_admin"
    CLERK = "clerk"
    PROJECT_MANAGER = "project_manager"
    ACCOUNTANT = "accountant"
    CLIENT = "client"

class RolePermissions:
    """Role-based permissions and capabilities"""
    
    # Define who can invite users
    CAN_INVITE_USERS = [UserRole.SUPERADMIN, UserRole.CLERK]
    
    # Define role hierarchy for access control
    ROLE_HIERARCHY = {
        UserRole.SUPERADMIN: 100,
        UserRole.BUSINESS_ADMIN: 80,
        UserRole.CLERK: 60,
        UserRole.PROJECT_MANAGER: 40,
        UserRole.ACCOUNTANT: 30,
        UserRole.CLIENT: 10
    }
    
    # Define what roles each role can invite
    INVITATION_PERMISSIONS = {
        UserRole.SUPERADMIN: [
            UserRole.BUSINESS_ADMIN, 
            UserRole.CLERK, 
            UserRole.PROJECT_MANAGER, 
            UserRole.ACCOUNTANT, 
            UserRole.CLIENT
        ],
        UserRole.CLERK: [
            UserRole.PROJECT_MANAGER, 
            UserRole.ACCOUNTANT, 
            UserRole.CLIENT
        ]
    }
    
    # Navigation routes based on roles
    ROLE_NAVIGATION = {
        UserRole.SUPERADMIN: "/admin/dashboard",
        UserRole.BUSINESS_ADMIN: "/business/dashboard", 
        UserRole.CLERK: "/clerk/dashboard",
        UserRole.PROJECT_MANAGER: "/projects/dashboard",
        UserRole.ACCOUNTANT: "/finance/dashboard",
        UserRole.CLIENT: "/client/dashboard"
    }
    
    @classmethod
    def can_invite_role(cls, inviter_role: str, target_role: str) -> bool:
        """Check if a user role can invite another role"""
        inviter_enum = UserRole(inviter_role)
        target_enum = UserRole(target_role)
        
        if inviter_enum not in cls.INVITATION_PERMISSIONS:
            return False
            
        return target_enum in cls.INVITATION_PERMISSIONS[inviter_enum]
    
    @classmethod
    def get_navigation_route(cls, role: str) -> str:
        """Get the default navigation route for a role"""
        role_enum = UserRole(role)
        return cls.ROLE_NAVIGATION.get(role_enum, "/dashboard")
    
    @classmethod
    def has_higher_or_equal_permission(cls, user_role: str, required_role: str) -> bool:
        """Check if user role has higher or equal permission level"""
        user_level = cls.ROLE_HIERARCHY.get(UserRole(user_role), 0)
        required_level = cls.ROLE_HIERARCHY.get(UserRole(required_role), 0)
        return user_level >= required_level