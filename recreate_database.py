#!/usr/bin/env python3
"""
Database Recreation Script for BuildBuzz API

This script will recreate all database tables with the current model schema.
"""

import sys
import os

# Add parent directory to path so we can import from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.users import models as user_models
from app.projects import models as project_models
from app.documents import models as document_models
from app.finance import models as finance_models
from app.workforce import models as workforce_models

def create_all_tables():
    """Create all database tables"""
    print("🚀 Creating all database tables...")
    
    try:
        # Create all tables defined in the models
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # List all created tables
        print("\n📊 Created Tables:")
        print("=" * 50)
        
        # User Management
        print("👤 User Management:")
        print("   - users")
        
        # Project Management  
        print("\n🏗️ Project Management:")
        print("   - project_types")
        print("   - projects") 
        print("   - project_components")
        print("   - tasks")
        
        # Finance Management
        print("\n💰 Finance Management:")
        print("   - vendors")
        print("   - purchase_orders")
        print("   - purchase_order_items")
        print("   - change_orders")
        print("   - change_order_items")
        print("   - transactions")
        
        # Workforce Management
        print("\n👷 Workforce Management:")
        print("   - professions")
        print("   - workers")
        print("   - worker_project_history")
        
        # Document Management
        print("\n📄 Document Management:")
        print("   - documents")
        print("   - document_access")
        
        print("\n" + "=" * 50)
        print("🎉 Database is ready for use!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("BuildBuzz Database Recreation")
    print("=" * 40)
    
    success = create_all_tables()
    
    if success:
        print("\n✅ Database recreation completed successfully!")
        print("🚀 You can now start your FastAPI application.")
    else:
        print("\n❌ Database recreation failed!")
        sys.exit(1)