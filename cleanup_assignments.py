"""
Remove assignments and dependencies from BuildBuzz database
This script removes assignment-related tables and fields to simplify task management
"""

import os
import sys
from sqlalchemy import text

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from app.database import engine

def remove_assignments_and_dependencies():
    """Remove assignment and dependency tables and related fields"""
    print("🔧 Removing assignments and dependencies from BuildBuzz database...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # List of SQL commands to clean up the database
        cleanup_commands = [
            # Drop assignment-related tables
            "DROP TABLE IF EXISTS assignments CASCADE;",
            "DROP TABLE IF EXISTS task_dependencies CASCADE;",
            "DROP TABLE IF EXISTS task_comments CASCADE;",
            "DROP TABLE IF EXISTS task_time_logs CASCADE;",
            "DROP TABLE IF EXISTS project_assignments CASCADE;",
            
            # Remove assignment-related columns from tasks table
            "ALTER TABLE tasks DROP COLUMN IF EXISTS assigned_to CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS supervisor_id CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS requirements CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS deliverables CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS acceptance_criteria CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS is_milestone CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS blocks_project CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS required_skills CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS required_tools CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS budget_allocation CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS actual_cost CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS deadline_status CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS days_overdue CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS escalation_level CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS requires_inspection CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS inspection_status CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS quality_notes CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS backlog_reason CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS original_deadline CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS backlog_priority CASCADE;",
            "ALTER TABLE tasks DROP COLUMN IF EXISTS target_completion_date CASCADE;",
            
            # Remove assignment-related columns from users table
            "ALTER TABLE users DROP COLUMN IF EXISTS supervisor_id CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS current_project_id CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS current_project_start_date CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS current_project_end_date CASCADE;",
            "ALTER TABLE users DROP COLUMN IF EXISTS current_project_role CASCADE;",
            
            # Remove unnecessary worker tables
            "DROP TABLE IF EXISTS worker_profiles CASCADE;",
            "DROP TABLE IF EXISTS worker_invites CASCADE;",
            "DROP TABLE IF EXISTS project_history CASCADE;",
        ]
        
        print("📊 Executing cleanup commands...")
        
        for i, command in enumerate(cleanup_commands, 1):
            try:
                session.execute(text(command))
                session.commit()
                print(f"   ✅ {i:2d}. {command.split()[0:3]} {''.join(command.split()[3:5])}")
            except Exception as e:
                print(f"   ⚠️  {i:2d}. {command.split()[0:3]} {''.join(command.split()[3:5])} - {str(e)[:50]}...")
                session.rollback()
        
        # Get simplified table structure
        print("\\n📋 Checking remaining tables...")
        result = session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        
        tables = [row[0] for row in result.fetchall()]
        print(f"   Remaining tables: {len(tables)}")
        
        for table in tables:
            print(f"   - {table}")
        
        # Check tasks table structure
        print("\\n📋 SIMPLIFIED TASKS TABLE STRUCTURE:")
        print("-" * 50)
        result = session.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'tasks' 
            ORDER BY ordinal_position;
        """))
        
        for row in result.fetchall():
            nullable = "NULL" if row[2] == "YES" else "NOT NULL"
            print(f"   {row[0]:<25} {row[1]:<15} {nullable}")
        
        # Show task count and status distribution
        print("\\n📊 TASK STATUS SUMMARY:")
        print("-" * 50)
        result = session.execute(text("""
            SELECT status, COUNT(*) as count
            FROM tasks 
            GROUP BY status 
            ORDER BY count DESC;
        """))
        
        for row in result.fetchall():
            print(f"   {row[0]:<15}: {row[1]} tasks")
        
        total_result = session.execute(text("SELECT COUNT(*) FROM tasks")).fetchone()
        total_tasks = total_result[0] if total_result else 0
        print(f"\\n   Total Tasks: {total_tasks}")
        
        print("\\n" + "=" * 60)
        print("🎉 DATABASE CLEANUP COMPLETED!")
        print("✅ Assignments and dependencies removed")
        print("✅ Task management simplified")
        print("✅ Focus on: Projects → Components → Tasks → Status")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    remove_assignments_and_dependencies()