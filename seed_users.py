#!/usr/bin/env python3
"""
User Seeding Script for BuildBuzz API

This script will add initial users to the database with proper roles and hashed passwords.
"""

import sys
import os

# Add parent directory to path so we can import from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.users.models import User
from app.users.password import hash_password

def create_user(db: Session, first_name: str, last_name: str, email: str, password: str, role: str):
    """Create a single user with hashed password"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        print(f"   ⚠️  User {email} already exists, skipping...")
        return existing_user
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Create new user
    db_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=hashed_password,
        role=role.lower().replace(' ', '_'),  # Convert to snake_case
        is_active=True,
        account_setup_completed=True,
        invitation_status='accepted'
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    print(f"   ✅ Created {role}: {first_name} {last_name} ({email})")
    return db_user

def seed_users():
    """Add all initial users to the database"""
    print("👥 Seeding BuildBuzz Users...")
    print("=" * 50)
    
    # Create database session
    db = Session(engine)
    
    try:
        # Initial Admin User
        print("🔑 Creating Admin User:")
        create_user(db, "Admin", "User", "admin@buildbuzz.com", "Admin123!", "superadmin")
        
        print("\n👑 Creating Core Team:")
        # Core Team - First Set
        create_user(db, "Alex", "Super", "alex.admin@buildbuzz.com", "alexadmin2024", "superadmin")
        create_user(db, "Maria", "Business", "maria.business@buildbuzz.com", "mariabiz2024", "business_admin")
        create_user(db, "Tom", "Office", "tom.clerk@buildbuzz.com", "tomclerk2024", "clerk")
        create_user(db, "Emma", "Project", "emma.pm@buildbuzz.com", "emmapm2024", "project_manager")
        create_user(db, "Robert", "Finance", "robert.finance@buildbuzz.com", "robertfin2024", "accountant")
        create_user(db, "Linda", "Customer", "linda.client@buildbuzz.com", "lindaclient2024", "client")
        
        print("\n🏗️ Creating Extended Team:")
        # Extended Team - Second Set
        create_user(db, "Carlos", "Builder", "carlos.builder@buildbuzz.com", "carlospm2024", "project_manager")
        create_user(db, "Jennifer", "Admin", "jennifer.admin@buildbuzz.com", "jenclerk2024", "clerk")
        create_user(db, "Michael", "Corp", "michael.corp@buildbuzz.com", "michaelcorp2024", "client")
        create_user(db, "Susan", "Numbers", "susan.numbers@buildbuzz.com", "susanfin2024", "accountant")
        
        print("\n" + "=" * 50)
        print("📊 User Summary:")
        
        # Count users by role
        roles = db.query(User.role, db.func.count(User.id)).group_by(User.role).all()
        for role, count in roles:
            print(f"   {role.upper().replace('_', ' ')}: {count} users")
        
        total_users = db.query(User).count()
        print(f"\n✅ Total Users Created: {total_users}")
        
    except Exception as e:
        print(f"❌ Error seeding users: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    print("BuildBuzz User Seeding")
    print("=" * 30)
    
    success = seed_users()
    
    if success:
        print("\n🎉 User seeding completed successfully!")
        print("\n🔐 Login Credentials Available:")
        print("   📧 admin@buildbuzz.com | 🔑 Admin123!")
        print("   📧 alex.admin@buildbuzz.com | 🔑 alexadmin2024")
        print("   📧 emma.pm@buildbuzz.com | 🔑 emmapm2024")
        print("   📧 robert.finance@buildbuzz.com | 🔑 robertfin2024")
        print("\n🚀 You can now login with these credentials!")
    else:
        print("\n❌ User seeding failed!")
        sys.exit(1)