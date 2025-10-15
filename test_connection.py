#!/usr/bin/env python3
"""
Test database connection script
"""
import os
import sys
from sqlalchemy import text

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.database import engine, get_database_url
    
    print("🔍 Testing Database Connection...")
    print(f"Environment: GOOGLE_APPLICATION_CREDENTIALS = {os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'Not Set')}")
    print(f"Environment: USE_CLOUD_SQL = {os.getenv('USE_CLOUD_SQL', 'Not Set')}")
    print(f"Environment: GAE_APPLICATION = {os.getenv('GAE_APPLICATION', 'Not Set')}")
    print(f"Environment: K_SERVICE = {os.getenv('K_SERVICE', 'Not Set')}")
    
    # Test database URL generation
    db_url = get_database_url()
    print(f"Database URL type: {type(db_url)}")
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test"))
        test_value = result.fetchone()[0]
        print(f"✅ Database connection successful! Test query returned: {test_value}")
        
        # Test if we can query database info
        if hasattr(engine.url, 'database'):
            print(f"Connected to database: {engine.url.database}")
        
        # Check if we're using SQLite or PostgreSQL
        db_name = conn.execute(text("SELECT version()")).fetchone()
        if db_name:
            print(f"Database version: {db_name[0]}")
        else:
            # For SQLite
            db_name = conn.execute(text("SELECT sqlite_version()")).fetchone()
            print(f"SQLite version: {db_name[0]}")
            
except Exception as e:
    print(f"❌ Database connection failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    
    # Provide helpful suggestions based on error type
    if "DefaultCredentialsError" in str(type(e)):
        print("\n💡 Suggestions:")
        print("1. Make sure GOOGLE_APPLICATION_CREDENTIALS is set correctly")
        print("2. Verify the credentials file exists and is readable")
        print("3. Try using local SQLite by setting USE_CLOUD_SQL=false")
    elif "connection" in str(e).lower():
        print("\n💡 Suggestions:")
        print("1. Check your internet connection")
        print("2. Verify Cloud SQL instance is running")
        print("3. Check database credentials and permissions")
    
    sys.exit(1)