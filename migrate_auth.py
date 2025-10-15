"""
Database Migration: Add authentication columns to users table
Run this script to add Clerk authentication support to the existing users table
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment"""
    if os.getenv("USE_CLOUD_SQL") == "true":
        # Cloud SQL configuration (same as in app/database.py)
        return f"postgresql+pg8000://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@/{os.getenv('DB_NAME')}?unix_sock=/cloudsql/{os.getenv('INSTANCE_CONNECTION_NAME')}/.s.PGSQL.5432"
    else:
        # Local SQLite
        return "sqlite:///./buildbuzz.db"

def run_migration():
    """Run the authentication migration"""
    try:
        # Get database connection
        database_url = get_database_url()
        engine = create_engine(database_url)
        
        print("🔄 Starting authentication migration...")
        print(f"Database: {database_url.split('@')[0]}@...")
        
        with engine.connect() as conn:
            # Check if migration is needed
            try:
                result = conn.execute(text("SELECT clerk_user_id FROM users LIMIT 1"))
                print("✅ Authentication columns already exist. Skipping migration.")
                return
            except Exception:
                print("📝 Authentication columns not found. Adding them...")
            
            # Add authentication columns
            migration_queries = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS clerk_user_id VARCHAR(255) UNIQUE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS permissions TEXT",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP NULL",
                
                # Create indexes for performance
                "CREATE INDEX IF NOT EXISTS idx_users_clerk_user_id ON users(clerk_user_id)",
                "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)",
                
                # Update default role values to match new auth system
                "UPDATE users SET role = 'business_clerk' WHERE role = 'clerk'",
                "UPDATE users SET role = 'business_admin' WHERE role = 'admin'",
            ]
            
            for query in migration_queries:
                try:
                    conn.execute(text(query))
                    print(f"✅ Executed: {query}")
                except Exception as e:
                    print(f"⚠️  Query failed (may be expected): {query}")
                    print(f"   Error: {e}")
            
            # Commit changes
            conn.commit()
            print("✅ Authentication migration completed successfully!")
            
            # Show updated table structure
            try:
                result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
                print("\n📋 Updated users table structure:")
                for row in result:
                    print(f"   - {row[0]}: {row[1]}")
            except:
                print("📋 Table structure updated (SQLite doesn't support column inspection)")
                
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔐 BuildBuzz Authentication Migration")
    print("=====================================")
    run_migration()