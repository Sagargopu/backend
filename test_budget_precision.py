#!/usr/bin/env python3
"""
Test Budget Precision
====================
Test that component budget values are returned with exact precision
"""

import requests
import json
from decimal import Decimal

# API base URL
BASE_URL = "http://localhost:8000"

def test_budget_precision():
    """Test that budget values maintain exact precision"""
    print("Testing Budget Precision")
    print("=" * 40)
    
    # Get existing components to check their budget values
    print("📋 Checking existing component budgets...")
    response = requests.get(f"{BASE_URL}/components/")
    
    if response.status_code == 200:
        components = response.json()
        print(f"✅ Found {len(components)} components")
        
        for i, component in enumerate(components[:3]):  # Check first 3 components
            print(f"\n📊 Component {i+1}: {component['name']}")
            print(f"   ID: {component['id']}")
            print(f"   Budget (API response): {component.get('budget', 'None')}")
            print(f"   Budget type: {type(component.get('budget', 'None'))}")
            
        # Test creating a component with precise budget
        print(f"\n🔧 Testing precise budget creation...")
        
        # Get a project
        projects_response = requests.get(f"{BASE_URL}/projects/")
        if projects_response.status_code == 200:
            projects = projects_response.json()
            if projects:
                project_id = projects[0]['id']
                
                # Test with exact value 999999.99
                precise_budget_data = {
                    "name": "Precise Budget Test Component",
                    "description": "Testing exact budget precision",
                    "budget": 999999.99,
                    "status": "planned",
                    "start_date": "2025-02-01",
                    "end_date": "2025-04-30",
                    "project_id": project_id
                }
                
                print(f"📤 Creating component with budget: {precise_budget_data['budget']}")
                create_response = requests.post(f"{BASE_URL}/components/", json=precise_budget_data)
                
                if create_response.status_code in [200, 201]:
                    created_component = create_response.json()
                    print("✅ Component created!")
                    print(f"📊 Created component budget details:")
                    print(f"   Sent budget: {precise_budget_data['budget']}")
                    print(f"   Returned budget: {created_component.get('budget')}")
                    print(f"   Budget type: {type(created_component.get('budget'))}")
                    
                    # Check if they match exactly
                    sent_budget = str(precise_budget_data['budget'])
                    returned_budget = str(created_component.get('budget', ''))
                    
                    print(f"\n🔍 Precision check:")
                    print(f"   Sent as string: '{sent_budget}'")
                    print(f"   Returned as string: '{returned_budget}'")
                    print(f"   Exact match: {'✅' if sent_budget == returned_budget else '❌'}")
                    
                    # Test with even more precise value
                    print(f"\n🔧 Testing with more decimal places...")
                    precise_data_2 = {
                        "name": "Very Precise Budget Test",
                        "description": "Testing with more decimal places",
                        "budget": 123456.789,
                        "status": "planned",
                        "project_id": project_id
                    }
                    
                    create_response_2 = requests.post(f"{BASE_URL}/components/", json=precise_data_2)
                    if create_response_2.status_code in [200, 201]:
                        created_component_2 = create_response_2.json()
                        print(f"   Sent: {precise_data_2['budget']}")
                        print(f"   Returned: {created_component_2.get('budget')}")
                        
                else:
                    print(f"❌ Failed to create component: {create_response.status_code}")
                    print(f"Error: {create_response.text}")
    else:
        print(f"❌ Failed to get components: {response.status_code}")

def check_database_values():
    """Check actual database values vs API responses"""
    print("\n" + "=" * 50)
    print("Checking Database vs API Values")
    print("=" * 50)
    
    # This would require direct database access
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from app.database import engine
        from sqlalchemy import text
        from sqlalchemy.orm import sessionmaker
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Get components from database directly
        result = db.execute(text("SELECT id, name, budget FROM project_components WHERE budget IS NOT NULL"))
        db_components = result.fetchall()
        
        print("📊 Database values:")
        for comp in db_components:
            print(f"   ID {comp[0]}: {comp[1]} - Budget: {comp[2]} (type: {type(comp[2])})")
            
        db.close()
        
        # Compare with API response
        api_response = requests.get(f"{BASE_URL}/components/")
        if api_response.status_code == 200:
            api_components = api_response.json()
            print(f"\n📡 API values:")
            for comp in api_components:
                if comp.get('budget'):
                    print(f"   ID {comp['id']}: {comp['name']} - Budget: {comp['budget']} (type: {type(comp['budget'])})")
                    
    except Exception as e:
        print(f"❌ Database check failed: {e}")

if __name__ == "__main__":
    test_budget_precision()
    check_database_values()