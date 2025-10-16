#!/usr/bin/env python3
"""
Create Admin User for BuildBuzz API
"""

import sys
import os
from datetime import datetime

# Add parent directory to path so we can import from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
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

def create_admin_user():
    """Create the admin user"""
    print("👤 Creating Admin User...")
    
    # Create database session
    db = Session(engine)
    
    try:
        # Check if admin user already exists
        existing_user = db.query(SimpleUser).filter(SimpleUser.email == "admin@buildbuzz.com").first()
        if existing_user:
            print("   ⚠️  Admin user already exists!")
            print(f"   📧 Email: {existing_user.email}")
            print(f"   👤 Name: {existing_user.first_name} {existing_user.last_name}")
            print(f"   🔐 Role: {existing_user.role}")
            return True
        
        # Hash the password
        hashed_password = hash_password("Admin123!")
        
        # Create admin user
        admin_user = SimpleUser(
            first_name="Admin",
            last_name="User",
            email="admin@buildbuzz.com",
            hashed_password=hashed_password,
            role="superadmin",
            is_active=True,
            account_setup_completed=True,
            invitation_status="accepted",
            phone_number="+1-555-0100",
            address="123 BuildBuzz HQ, Construction City, BC 12345"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("   ✅ Admin user created successfully!")
        print(f"   📧 Email: {admin_user.email}")
        print(f"   👤 Name: {admin_user.first_name} {admin_user.last_name}")
        print(f"   🔐 Role: {admin_user.role}")
        print(f"   🆔 ID: {admin_user.id}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("BuildBuzz Admin User Creation")
    print("=" * 35)
    
    success = create_admin_user()
    
    if success:
        print("\n🎉 Admin user setup completed!")
        print("\n🔐 Login Credentials:")
        print("   📧 Email: admin@buildbuzz.com")
        print("   🔑 Password: Admin123!")
        print("   🛡️  Role: SuperAdmin")
        print("\n🚀 You can now login with these credentials!")
    else:
        print("\n❌ Admin user creation failed!")
        sys.exit(1)