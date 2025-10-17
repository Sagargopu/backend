#!/usr/bin/env python3
"""
Test Component POST with Dates
===============================
Test creating a component with start_date and end_date via POST
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:8000"

def test_component_post_with_dates():
    """Test POST /components/ with start_date and end_date"""
    print("Testing Component POST with Dates")
    print("=" * 40)
    
    # Get a project to attach the component to
    print("📋 Getting projects...")
    projects_response = requests.get(f"{BASE_URL}/projects/")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        if projects:
            project_id = projects[0]['id']
            print(f"✅ Using project ID: {project_id}")
            
            # Test data with start_date and end_date
            component_data = {
                "name": "POST Test Component with Dates",
                "description": "Testing POST with start and end dates",
                "budget": 75000.00,
                "status": "planned",
                "start_date": "2025-02-01",
                "end_date": "2025-04-30",
                "project_id": project_id,
                "parent_id": None
            }
            
            print(f"\n🔧 POST data:")
            print(json.dumps(component_data, indent=2))
            
            # Send POST request
            print(f"\n📤 Sending POST to {BASE_URL}/components/...")
            response = requests.post(
                f"{BASE_URL}/components/",
                json=component_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response Headers: {dict(response.headers)}")
            
            if response.status_code in [200, 201]:
                created_component = response.json()
                print("✅ Component created successfully!")
                print(f"\n📋 Created component:")
                print(json.dumps(created_component, indent=2, default=str))
                
                # Verify the dates were saved
                print(f"\n🔍 Date verification:")
                print(f"   Sent start_date: {component_data['start_date']}")
                print(f"   Returned start_date: {created_component.get('start_date', 'MISSING')}")
                print(f"   Sent end_date: {component_data['end_date']}")
                print(f"   Returned end_date: {created_component.get('end_date', 'MISSING')}")
                
                # Check if dates match
                dates_match = (
                    created_component.get('start_date') == component_data['start_date'] and
                    created_component.get('end_date') == component_data['end_date']
                )
                print(f"   Dates match: {'✅' if dates_match else '❌'}")
                
            else:
                print("❌ Component creation failed!")
                print(f"📄 Response body: {response.text}")
                
                # Try to parse error details
                try:
                    error_data = response.json()
                    print(f"📊 Error details:")
                    print(json.dumps(error_data, indent=2))
                except:
                    print("Could not parse error response as JSON")
        else:
            print("❌ No projects found")
    else:
        print(f"❌ Failed to get projects: {projects_response.status_code}")
        print(f"Error: {projects_response.text}")

def test_minimal_component_post():
    """Test POST with minimal required fields only"""
    print("\n" + "=" * 50)
    print("Testing Minimal Component POST")
    print("=" * 50)
    
    # Get a project
    projects_response = requests.get(f"{BASE_URL}/projects/")
    if projects_response.status_code == 200:
        projects = projects_response.json()
        if projects:
            project_id = projects[0]['id']
            
            # Minimal data
            minimal_data = {
                "name": "Minimal Test Component",
                "project_id": project_id
            }
            
            print(f"🔧 Minimal POST data:")
            print(json.dumps(minimal_data, indent=2))
            
            response = requests.post(f"{BASE_URL}/components/", json=minimal_data)
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print("✅ Minimal component created!")
                component = response.json()
                print(f"📋 Default values:")
                print(f"   start_date: {component.get('start_date', 'NOT SET')}")
                print(f"   end_date: {component.get('end_date', 'NOT SET')}")
                print(f"   status: {component.get('status', 'NOT SET')}")
            else:
                print("❌ Minimal component creation failed!")
                print(f"Error: {response.text}")

if __name__ == "__main__":
    test_component_post_with_dates()
    test_minimal_component_post()