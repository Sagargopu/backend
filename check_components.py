#!/usr/bin/env python3
"""
Check Project Components
========================
Quick check of project components structure
"""

import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def check_components():
    """Check existing project components in database"""
    print("Checking Project Components in Database")
    print("=" * 45)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check table structure
        result = db.execute(text("PRAGMA table_info(project_components)"))
        columns = result.fetchall()
        
        print("📋 Table Structure:")
        for col in columns:
            print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Check existing data
        result = db.execute(text("SELECT id, name, description, start_date, end_date, budget, status FROM project_components LIMIT 5"))
        components = result.fetchall()
        
        print(f"\n📊 Found {len(components)} components:")
        for comp in components:
            print(f"   ID: {comp[0]}")
            print(f"   Name: {comp[1]}")
            print(f"   Start Date: {comp[2]}")
            print(f"   End Date: {comp[3]}")
            print(f"   Budget: {comp[4]}")
            print(f"   Status: {comp[5]}")
            print("   " + "-" * 30)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_components()