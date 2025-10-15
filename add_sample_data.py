"""
Add sample users to the database
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.users import models as user_models

def add_sample_users():
    """Add sample users for testing"""
    print("📝 Adding sample users...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create sample users with the updated role structure
        users = [
            {
                "full_name": "System Administrator",
                "email": "admin@buildbuzz.com",
                "role": "clerk",
                "is_active": True,
                "account_setup_completed": True
            },
            {
                "full_name": "Business Administrator", 
                "email": "business@buildbuzz.com",
                "role": "business_admin",
                "is_active": True,
                "account_setup_completed": True
            },
            {
                "full_name": "Project Manager",
                "email": "pm@buildbuzz.com", 
                "role": "project_manager",
                "is_active": True,
                "account_setup_completed": True
            },
            {
                "full_name": "Chief Accountant",
                "email": "accountant@buildbuzz.com",
                "role": "accountant", 
                "is_active": True,
                "account_setup_completed": True
            },
            {
                "full_name": "Client Representative",
                "email": "client@buildbuzz.com",
                "role": "client",
                "is_active": True,
                "account_setup_completed": True
            }
        ]
        
        for user_data in users:
            user = user_models.User(**user_data)
            session.add(user)
            print(f"   ✅ Added {user_data['role']}: {user_data['full_name']}")
        
        session.commit()
        print("✅ Sample users added successfully")
        
        # Verify users were created
        user_count = session.query(user_models.User).count()
        print(f"📊 Total users in database: {user_count}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding sample users: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    add_sample_users()