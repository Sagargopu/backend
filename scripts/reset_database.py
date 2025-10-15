"""
Database Reset Script for BuildBuzz API
This script will:
1. Drop all existing tables
2. Recreate all tables with updated models
3. Optionally add sample data
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, MetaData
from app.database import engine, Base
from app.users import models as user_models
from app.projects import models as project_models
from app.documents import models as document_models
from app.finance import models as finance_models

def drop_all_tables():
    """Drop all existing tables"""
    print("🗑️  Dropping all existing tables...")
    
    # Reflect the existing database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    # Drop all tables in reverse order of dependencies
    metadata.drop_all(bind=engine)
    print("✅ All tables dropped successfully")

def create_all_tables():
    """Create all tables with updated models"""
    print("🏗️  Creating all tables with updated models...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully")

def verify_tables():
    """Verify that all tables were created"""
    print("🔍 Verifying table creation...")
    
    with engine.connect() as conn:
        # Check if we're using PostgreSQL or SQLite
        if 'postgresql' in str(engine.url):
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
        else:  # SQLite
            result = conn.execute(text("""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """))
        
        tables = [row[0] for row in result]
        
        print(f"📋 Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        return tables

def add_sample_data():
    """Add sample data for testing"""
    print("📝 Adding sample data...")
    
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create sample clerk user
        sample_clerk = user_models.User(
            full_name="System Administrator",
            email="admin@buildbuzz.com",
            role="clerk",
            is_active=True,
            account_setup_completed=True
        )
        session.add(sample_clerk)
        
        # Create sample business admin
        sample_business_admin = user_models.User(
            full_name="Business Administrator",
            email="business@buildbuzz.com", 
            role="business_admin",
            is_active=True,
            account_setup_completed=True
        )
        session.add(sample_business_admin)
        
        # Create sample project manager
        sample_pm = user_models.User(
            full_name="Project Manager",
            email="pm@buildbuzz.com",
            role="project_manager",
            is_active=True,
            account_setup_completed=True
        )
        session.add(sample_pm)
        
        # Create sample accountant
        sample_accountant = user_models.User(
            full_name="Chief Accountant",
            email="accountant@buildbuzz.com",
            role="accountant",
            is_active=True,
            account_setup_completed=True
        )
        session.add(sample_accountant)
        
        # Create sample client
        sample_client = user_models.User(
            full_name="Client Representative",
            email="client@buildbuzz.com",
            role="client",
            is_active=True,
            account_setup_completed=True
        )
        session.add(sample_client)
        
        session.commit()
        print("✅ Sample data added successfully")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding sample data: {e}")
    finally:
        session.close()

def main():
    """Main function to reset the database"""
    print("🚀 Starting BuildBuzz Database Reset...")
    print(f"🔗 Database URL: {engine.url}")
    
    try:
        # Step 1: Drop all tables
        drop_all_tables()
        
        # Step 2: Create all tables with updated models
        create_all_tables()
        
        # Step 3: Verify tables were created
        tables = verify_tables()
        
        # Step 4: Add sample data
        response = input("\\n❓ Do you want to add sample data? (y/N): ")
        if response.lower() in ['y', 'yes']:
            add_sample_data()
        
        print("\\n🎉 Database reset completed successfully!")
        print(f"📊 Total tables created: {len(tables)}")
        
        # Show expected tables
        expected_tables = [
            'users', 'worker_profiles', 'project_history', 'worker_invites',
            'projects', 'project_components', 'tasks', 'assignments', 'project_assignments',
            'documents', 'document_access', 'document_shares',
            'vendors', 'contracts', 'purchase_orders', 'change_orders', 
            'client_invoices', 'vendor_invoices', 'transaction_categories', 'transactions'
        ]
        
        missing_tables = set(expected_tables) - set(tables)
        if missing_tables:
            print(f"⚠️  Warning: Some expected tables were not created: {missing_tables}")
        else:
            print("✅ All expected tables were created successfully")
            
    except Exception as e:
        print(f"❌ Error during database reset: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)