"""
Simple Database Reset Script
Run this to clear GCP database and recreate with updated models
"""

import os
import sys
from sqlalchemy import text

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.database import Base, engine

def reset_database():
    """Clear and recreate all database tables"""
    print("🔄 Resetting database...")
    
    try:
        # Import all models to ensure they're registered with Base
        from app.users import models as user_models
        from app.projects import models as project_models  
        from app.documents import models as document_models
        from app.finance import models as finance_models
        
        print("📋 Models imported successfully")
        
        # Connect to database
        with engine.connect() as conn:
            # Check if this is PostgreSQL
            if 'postgresql' in str(engine.url):
                print("🐘 Detected PostgreSQL database")
                
                # Drop all tables manually in the correct order for PostgreSQL
                print("🗑️  Dropping all tables...")
                
                # First, get all table names
                result = conn.execute(text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
                tables = [row[0] for row in result]
                
                if tables:
                    # Disable foreign key checks temporarily
                    for table in tables:
                        try:
                            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                            print(f"   ✅ Dropped table: {table}")
                        except Exception as e:
                            print(f"   ⚠️  Warning dropping {table}: {e}")
                    
                    conn.commit()
                else:
                    print("   ℹ️  No tables found to drop")
            
            else:
                print("🗄️  Detected SQLite database")
                # For SQLite, we can use the standard drop_all
                Base.metadata.drop_all(bind=engine)
        
        print("✅ All tables dropped successfully")
        
        # Create all tables
        print("🏗️  Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        # Verify tables were created
        with engine.connect() as conn:
            if 'postgresql' in str(engine.url):
                result = conn.execute(text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY tablename
                """))
            else:
                result = conn.execute(text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name
                """))
            
            tables = [row[0] for row in result]
            print(f"📋 Created {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
        
        print("🎉 Database reset completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    reset_database()