#!/usr/bin/env python3
"""
Test Component Creation
=======================
Tests creating a project component to verify the API works
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:8000"

def test_component_creation():
    """Test creating a project component"""
    print("Testing Project Component Creation")
    print("=" * 40)
    
    # First, let's get a list of projects to use
    print("📋 Getting projects...")
    projects_response = requests.get(f"{BASE_URL}/projects/with-details/")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        if projects:
            project = projects[0]  # Use the first project
            print(f"✅ Using project: {project['name']} (ID: {project['id']})")
            print(f"   Client: {project.get('client_name', 'N/A')}")
            
            # Create a test component
            component_data = {
                "name": "Test Component from API",
                "description": "Testing component creation via API",
                "budget": 50000.00,
                "status": "planned",
                "start_date": "2025-01-15",
                "end_date": "2025-03-30",
                "project_id": project['id'],
                "parent_id": None
            }
            
            print(f"\n🔧 Creating component with data:")
            print(json.dumps(component_data, indent=2))
            
            # Send POST request to create component
            create_response = requests.post(
                f"{BASE_URL}/components/",
                json=component_data
            )
            
            print(f"\n📊 Response Status: {create_response.status_code}")
            
            if create_response.status_code == 200 or create_response.status_code == 201:
                component = create_response.json()
                print("✅ Component created successfully!")
                print(f"   Component ID: {component['id']}")
                print(f"   Name: {component['name']}")
                print(f"   Status: {component['status']}")
                print(f"   Budget: ${component['budget']}")
            else:
                print("❌ Component creation failed!")
                print(f"Error: {create_response.text}")
                
        else:
            print("❌ No projects found in the database")
    else:
        print(f"❌ Failed to get projects: {projects_response.status_code}")
        print(f"Error: {projects_response.text}")

def test_projects_with_details():
    """Test getting projects with details to see client names"""
    print("\n" + "=" * 50)
    print("Testing Projects with Details")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/projects/with-details/")
    
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Found {len(projects)} projects")
        
        for project in projects[:3]:  # Show first 3 projects
            print(f"\n📋 Project: {project['name']}")
            print(f"   ID: {project['id']}")
            print(f"   Client: {project.get('client_name', 'N/A')}")
            print(f"   PM: {project.get('project_manager_name', 'N/A')}")
            print(f"   Type: {project.get('project_type_name', 'N/A')}")
            print(f"   Status: {project['status']}")
    else:
        print(f"❌ Failed to get projects with details: {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_projects_with_details()
    test_component_creation()