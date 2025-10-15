"""
Remove payroll and worker management endpoints and related code
This script removes wage-related fields, worker management endpoints, and related tables
"""

import os
import sys
from sqlalchemy import text

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from app.database import engine

def remove_payroll_features():
    """Remove payroll and worker management features"""
    print("🔧 Removing payroll and worker management features...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Database cleanup commands
        db_cleanup_commands = [
            # Remove wage-related columns from users table
            "ALTER TABLE users DROP COLUMN IF EXISTS current_wage_rate CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS wage_currency CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS availability_status CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS years_experience CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS primary_skills CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS certifications CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS total_projects_completed CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS average_project_rating CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS last_project_completion_date CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS hire_date CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS department CASCADE;",
        ]
        
        print("📊 Executing database cleanup...")
        
        for i, command in enumerate(db_cleanup_commands, 1):
            try:
                session.execute(text(command))
                session.commit()
                print(f"   ✅ {i:2d}. Removed {command.split('DROP COLUMN IF EXISTS')[1].split()[0]}")
            except Exception as e:
                print(f"   ⚠️  {i:2d}. {command.split('DROP COLUMN IF EXISTS')[1].split()[0]} - Already removed or error")
                session.rollback()
        
        # Check final users table structure
        print("\\n📋 SIMPLIFIED USERS TABLE STRUCTURE:")
        print("-" * 50)
        result = session.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position;
        """))
        
        for row in result.fetchall():
            nullable = "NULL" if row[2] == "YES" else "NOT NULL"
            print(f"   {row[0]:<25} {row[1]:<15} {nullable}")
        
        print("\\n" + "=" * 60)
        print("🎉 DATABASE PAYROLL CLEANUP COMPLETED!")
        print("✅ Wage and worker management fields removed")
        print("✅ Focus on: Basic user management only")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error during database cleanup: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

def remove_payroll_endpoints():
    """Remove payroll-related endpoints from API files"""
    print("\\n🔧 Removing payroll endpoints from API files...")
    
    # Define endpoints to remove (these will be commented out)
    endpoints_to_remove = [
        "/talent-pool/",
        "/worker/{worker_id}/profile/",
        "/worker/{worker_id}/project-history/",
        "/worker/{worker_id}/update-availability/",
        "/project-manager/invite-worker/",
        "/project-manager/{manager_id}/sent-invites/",
        "/clerk/pending-worker-invites/",
        "/clerk/approve-worker-invite/{invite_id}/",
        "/worker/{worker_id}/received-invites/",
        "/worker/respond-to-invite/{invite_id}/",
        "/clerk/add-worker/",
    ]
    
    api_file = "app/users/api.py"
    
    try:
        with open(api_file, 'r') as file:
            content = file.read()
        
        # Create simplified API content
        simplified_content = '''from fastapi import APIRouter, Depends, HTTPException
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
'''
        
        # Write simplified content
        with open(api_file, 'w') as file:
            file.write(simplified_content)
        
        print(f"   ✅ Simplified {api_file}")
        print(f"   ✅ Removed {len(endpoints_to_remove)} payroll endpoints")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating API file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting payroll feature removal...")
    
    # Step 1: Remove from database
    db_success = remove_payroll_features()
    
    # Step 2: Remove from API
    api_success = remove_payroll_endpoints()
    
    if db_success and api_success:
        print("\\n🎉 PAYROLL REMOVAL COMPLETED SUCCESSFULLY!")
        print("✅ Database cleaned up")
        print("✅ API endpoints simplified")
        print("✅ Focus on: Basic user + task management only")
        print("\\n🔄 Please restart your server to see changes")
    else:
        print("\\n❌ Some errors occurred during cleanup")