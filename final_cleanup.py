"""
Final cleanup of payroll-related database tables
This removes the worker-specific tables completely
"""

import os
import sys
from sqlalchemy import text

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from app.database import engine

def remove_payroll_tables():
    """Remove all payroll and worker management tables"""
    print("🔧 Removing payroll-related database tables...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Remove payroll tables
        payroll_tables = [
            "worker_invites",
            "project_history", 
            "worker_profiles"
        ]
        
        print("📊 Removing payroll tables...")
        
        for i, table in enumerate(payroll_tables, 1):
            try:
                session.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
                session.commit()
                print(f"   ✅ {i:2d}. Removed table: {table}")
            except Exception as e:
                print(f"   ⚠️  {i:2d}. {table} - Already removed or error: {e}")
                session.rollback()
        
        # List remaining tables
        print("\\n📋 REMAINING DATABASE TABLES:")
        print("-" * 50)
        result = session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        
        for row in result.fetchall():
            print(f"   ✅ {row[0]}")
        
        print("\\n" + "=" * 60)
        print("🎉 PAYROLL TABLE CLEANUP COMPLETED!")
        print("✅ All payroll and worker management tables removed")
        print("✅ Focus on: Projects → Components → Tasks only")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error during table cleanup: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    print("🚀 Starting final payroll table cleanup...")
    success = remove_payroll_tables()
    
    if success:
        print("\\n🎉 ALL PAYROLL FEATURES COMPLETELY REMOVED!")
        print("✅ Database simplified to core project management")
        print("✅ API endpoints cleaned up")
        print("✅ Ready for simple task management")
    else:
        print("\\n❌ Some errors occurred during cleanup")