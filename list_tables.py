#!/usr/bin/env python3
"""
List all database tables that will be created
"""
import sys
import os

# Add parent directory to path so we can import from the main project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base
from app.users import models as user_models
from app.projects import models as project_models
from app.documents import models as document_models
from app.finance import models as finance_models
from app.workforce import models as workforce_models

def list_all_tables():
    """List all tables that will be created"""
    print("📋 BuildBuzz Database Tables")
    print("=" * 50)
    
    # Get all table names from SQLAlchemy metadata
    tables = Base.metadata.tables.keys()
    
    # Group tables by module
    table_groups = {
        'User Management': [],
        'Project Management': [],
        'Finance Management': [],
        'Workforce Management': [],
        'Document Management': []
    }
    
    # Categorize tables
    for table_name in sorted(tables):
        if table_name in ['users']:
            table_groups['User Management'].append(table_name)
        elif table_name in ['projects', 'project_types', 'project_components', 'tasks']:
            table_groups['Project Management'].append(table_name)
        elif table_name in ['vendors', 'purchase_orders', 'purchase_order_items', 'change_orders', 'change_order_items', 'transactions']:
            table_groups['Finance Management'].append(table_name)
        elif table_name in ['professions', 'workers', 'worker_project_history']:
            table_groups['Workforce Management'].append(table_name)
        elif table_name in ['documents', 'document_access']:
            table_groups['Document Management'].append(table_name)
        else:
            # Add to a general category if not categorized
            if 'Other' not in table_groups:
                table_groups['Other'] = []
            table_groups['Other'].append(table_name)
    
    # Display tables by category
    total_tables = 0
    for category, table_list in table_groups.items():
        if table_list:  # Only show categories that have tables
            print(f"\n🏷️  {category}:")
            for table in table_list:
                print(f"   📊 {table}")
                total_tables += 1
    
    print(f"\n✅ Total Tables: {total_tables}")
    
    # Show detailed table information
    print("\n" + "=" * 50)
    print("📝 Detailed Table Information")
    print("=" * 50)
    
    for table_name, table in Base.metadata.tables.items():
        print(f"\n📊 Table: {table_name}")
        print(f"   Columns: {len(table.columns)}")
        
        # List columns
        for column in table.columns:
            nullable = "NULL" if column.nullable else "NOT NULL"
            primary_key = "PK" if column.primary_key else ""
            foreign_key = "FK" if column.foreign_keys else ""
            unique = "UNIQUE" if column.unique else ""
            
            annotations = " ".join(filter(None, [nullable, primary_key, foreign_key, unique]))
            print(f"     • {column.name}: {column.type} {annotations}")
        
        # List foreign keys
        if table.foreign_keys:
            print(f"   Foreign Keys:")
            for fk in table.foreign_keys:
                print(f"     → {fk.column} references {fk.target_fullname}")

if __name__ == "__main__":
    list_all_tables()