#!/usr/bin/env python3
"""
Test Task Creation Error
========================
Debug the 422 error when creating tasks
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_task_creation_error():
    """Test task creation to reproduce the 422 error"""
    print("Testing Task Creation - Debugging 422 Error")
    print("=" * 50)
    
    # Get a project first
    print("📋 Getting projects...")
    projects_response = requests.get(f"{BASE_URL}/projects/")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        if projects:
            project_id = projects[0]['id']
            print(f"✅ Using project ID: {project_id}")
            
            # Get components for this project
            components_response = requests.get(f"{BASE_URL}/projects/{project_id}/components")
            component_id = None
            
            if components_response.status_code == 200:
                components = components_response.json()
                if components:
                    component_id = components[0]['id']
                    print(f"✅ Found component ID: {component_id}")
                else:
                    print("⚠️  No components found for this project")
            
            # Test 1: Minimal required fields only
            print(f"\n🔧 Test 1: Minimal task creation")
            minimal_task = {
                "name": "Test Task Minimal",
                "project_id": project_id
            }
            
            print(f"📤 POST data: {json.dumps(minimal_task, indent=2)}")
            response = requests.post(f"{BASE_URL}/tasks/", json=minimal_task)
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code != 200 and response.status_code != 201:
                print(f"❌ Error response:")
                try:
                    error_detail = response.json()
                    print(json.dumps(error_detail, indent=2))
                except:
                    print(response.text)
            else:
                print("✅ Minimal task created successfully!")
                task = response.json()
                print(f"Created task ID: {task['id']}")
            
            # Test 2: Full task with all fields
            print(f"\n🔧 Test 2: Full task creation")
            full_task = {
                "name": "Test Task Full",
                "description": "Full task with all fields",
                "status": "To Do",
                "priority": "Medium",
                "task_type": "Planning",
                "budget": 5000.00,
                "start_date": "2025-02-01",
                "end_date": "2025-02-15",
                "project_id": project_id,
                "component_id": component_id
            }
            
            print(f"📤 POST data: {json.dumps(full_task, indent=2)}")
            response = requests.post(f"{BASE_URL}/tasks/", json=full_task)
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code != 200 and response.status_code != 201:
                print(f"❌ Error response:")
                try:
                    error_detail = response.json()
                    print(json.dumps(error_detail, indent=2))
                except:
                    print(response.text)
            else:
                print("✅ Full task created successfully!")
                task = response.json()
                print(f"Created task ID: {task['id']}")
            
            # Test 3: Task without component (should work)
            print(f"\n🔧 Test 3: Task without component")
            no_component_task = {
                "name": "Test Task No Component",
                "description": "Task without component",
                "project_id": project_id
            }
            
            print(f"📤 POST data: {json.dumps(no_component_task, indent=2)}")
            response = requests.post(f"{BASE_URL}/tasks/", json=no_component_task)
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code != 200 and response.status_code != 201:
                print(f"❌ Error response:")
                try:
                    error_detail = response.json()
                    print(json.dumps(error_detail, indent=2))
                except:
                    print(response.text)
            else:
                print("✅ Task without component created successfully!")
                task = response.json()
                print(f"Created task ID: {task['id']}")
                
            # Test 4: Invalid status value
            print(f"\n🔧 Test 4: Invalid status value")
            invalid_task = {
                "name": "Test Invalid Status",
                "status": "InvalidStatus",
                "project_id": project_id
            }
            
            print(f"📤 POST data: {json.dumps(invalid_task, indent=2)}")
            response = requests.post(f"{BASE_URL}/tasks/", json=invalid_task)
            print(f"📊 Response: {response.status_code}")
            
            if response.status_code != 200 and response.status_code != 201:
                print(f"❌ Expected error response:")
                try:
                    error_detail = response.json()
                    print(json.dumps(error_detail, indent=2))
                except:
                    print(response.text)
        else:
            print("❌ No projects found")
    else:
        print(f"❌ Failed to get projects: {projects_response.status_code}")

def check_existing_tasks():
    """Check what tasks already exist"""
    print("\n" + "=" * 50)
    print("Checking Existing Tasks")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/tasks/")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Found {len(tasks)} existing tasks")
        
        for task in tasks[:3]:  # Show first 3 tasks
            print(f"\n📋 Task: {task['name']}")
            print(f"   ID: {task['id']}")
            print(f"   Status: {task['status']}")
            print(f"   Priority: {task['priority']}")
            print(f"   Project ID: {task['project_id']}")
            print(f"   Component ID: {task.get('component_id', 'None')}")
    else:
        print(f"❌ Failed to get tasks: {response.status_code}")

if __name__ == "__main__":
    check_existing_tasks()
    test_task_creation_error()