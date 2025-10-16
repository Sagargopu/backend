#!/usr/bin/env python3
"""
Create Core Team Users for BuildBuzz API
"""

import sys
import os

# Add parent directory to path so we can import from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, func
from app.database import engine, Base
from app.users.password import hash_password

# Simple User model just for creation
class SimpleUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, nullable=False, default='clerk')
    is_active = Column(Boolean, default=True)
    account_setup_completed = Column(Boolean, default=False)
    invitation_status = Column(String, default='pending')
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)

def create_user(db: Session, first_name: str, last_name: str, email: str, password: str, role: str):
    """Create a single user"""
    
    # Check if user already exists
    existing_user = db.query(SimpleUser).filter(SimpleUser.email == email).first()
    if existing_user:
        print(f"   ⚠️  User {email} already exists, skipping...")
        return existing_user
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Create new user
    db_user = SimpleUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hashed_password,
        role=role.lower().replace(' ', '_'),  # Convert to snake_case
        is_active=True,
        account_setup_completed=True,
        invitation_status='accepted',
        phone_number=f"+1-555-{1000 + hash(email) % 9000}",  # Generate unique phone
        address=f"{hash(email) % 999 + 1} {first_name} St, BuildBuzz City, BC {10000 + hash(email) % 90000}"
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    print(f"   ✅ Created {role}: {first_name} {last_name} ({email})")
    return db_user

def create_core_team():
    """Create all core team users"""
    print("👥 Creating BuildBuzz Core Team...")
    print("=" * 50)
    
    # Create database session
    db = Session(engine)
    
    try:
        # Core team users data
        users_data = [
            ("Alex", "Super", "alex.admin@buildbuzz.com", "alexadmin2024", "superadmin"),
            ("Maria", "Business", "maria.business@buildbuzz.com", "mariabiz2024", "business_admin"),
            ("Tom", "Office", "tom.clerk@buildbuzz.com", "tomclerk2024", "clerk"),
            ("Emma", "Project", "emma.pm@buildbuzz.com", "emmapm2024", "project_manager"),
            ("Robert", "Finance", "robert.finance@buildbuzz.com", "robertfin2024", "accountant"),
            ("Linda", "Customer", "linda.client@buildbuzz.com", "lindaclient2024", "client")
        ]
        
        print("👑 Creating Core Team Members:")
        created_users = []
        
        for first_name, last_name, email, password, role in users_data:
            user = create_user(db, first_name, last_name, email, password, role)
            created_users.append(user)
        
        print("\n" + "=" * 50)
        print("📊 Team Summary:")
        
        # Count users by role
        roles = db.query(SimpleUser.role, func.count(SimpleUser.id)).group_by(SimpleUser.role).all()
        for role, count in roles:
            print(f"   {role.upper().replace('_', ' ')}: {count} users")
        
        total_users = db.query(SimpleUser).count()
        print(f"\n✅ Total Users in System: {total_users}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("BuildBuzz Core Team Creation")
    print("=" * 35)
    
    success = create_core_team()
    
    if success:
        print("\n🎉 Core team creation completed successfully!")
        print("\n🔐 Login Credentials:")
        print("   📧 alex.admin@buildbuzz.com | 🔑 alexadmin2024 (SuperAdmin)")
        print("   📧 maria.business@buildbuzz.com | 🔑 mariabiz2024 (Business Admin)")
        print("   📧 tom.clerk@buildbuzz.com | 🔑 tomclerk2024 (Clerk)")
        print("   📧 emma.pm@buildbuzz.com | 🔑 emmapm2024 (Project Manager)")
        print("   📧 robert.finance@buildbuzz.com | 🔑 robertfin2024 (Accountant)")
        print("   📧 linda.client@buildbuzz.com | 🔑 lindaclient2024 (Client)")
        print("\n🚀 All team members can now login!")
    else:
        print("\n❌ Core team creation failed!")
        sys.exit(1)