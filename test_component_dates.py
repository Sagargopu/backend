#!/usr/bin/env python3
"""
Test Component API Response
===========================
Test that components API returns start_date and end_date fields
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:8000"

def test_component_api_response():
    """Test that component API returns all expected fields"""
    print("Testing Component API Response")
    print("=" * 40)
    
    # Get existing components
    print("📋 Getting existing components...")
    response = requests.get(f"{BASE_URL}/components/")
    
    if response.status_code == 200:
        components = response.json()
        print(f"✅ Found {len(components)} components")
        
        if components:
            component = components[0]
            print(f"\n📊 First component response:")
            print(json.dumps(component, indent=2, default=str))
            
            # Check if start_date and end_date are present
            has_start_date = 'start_date' in component
            has_end_date = 'end_date' in component
            
            print(f"\n🔍 Field Check:")
            print(f"   start_date present: {'✅' if has_start_date else '❌'}")
            print(f"   end_date present: {'✅' if has_end_date else '❌'}")
            
            if has_start_date:
                print(f"   start_date value: {component['start_date']}")
            if has_end_date:
                print(f"   end_date value: {component['end_date']}")
        else:
            print("📝 No components found. Let's create one...")
            
            # Get a project to attach the component to
            projects_response = requests.get(f"{BASE_URL}/projects/")
            if projects_response.status_code == 200:
                projects = projects_response.json()
                if projects:
                    project_id = projects[0]['id']
                    
                    # Create a test component
                    component_data = {
                        "name": "Test Component with Dates",
                        "description": "Testing API response with dates",
                        "budget": 25000.00,
                        "status": "planned",
                        "start_date": "2025-01-15",
                        "end_date": "2025-03-30",
                        "project_id": project_id
                    }
                    
                    print(f"🔧 Creating component for project {project_id}...")
                    create_response = requests.post(f"{BASE_URL}/components/", json=component_data)
                    
                    if create_response.status_code in [200, 201]:
                        created_component = create_response.json()
                        print("✅ Component created successfully!")
                        print(f"📊 Created component response:")
                        print(json.dumps(created_component, indent=2, default=str))
                        
                        # Check if start_date and end_date are in the response
                        has_start_date = 'start_date' in created_component
                        has_end_date = 'end_date' in created_component
                        
                        print(f"\n🔍 Created Component Field Check:")
                        print(f"   start_date present: {'✅' if has_start_date else '❌'}")
                        print(f"   end_date present: {'✅' if has_end_date else '❌'}")
                        
                    else:
                        print(f"❌ Failed to create component: {create_response.status_code}")
                        print(f"Error: {create_response.text}")
    else:
        print(f"❌ Failed to get components: {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_component_api_response()