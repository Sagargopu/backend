#!/usr/bin/env python3
"""
Add Multiple Tasks Script
=========================
Creates 10 tasks for component ID 1 and project ID 7
"""

import requests
import json
from datetime import date, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def create_multiple_tasks():
    """Create 10 tasks for the specified component and project"""
    print("Creating Multiple Tasks")
    print("=" * 40)
    
    # Task data templates
    tasks_data = [
        {
            "name": "Electrical Rough-in",
            "description": "Install electrical wiring and outlets before drywall",
            "status": "To Do",
            "priority": "High",
            "task_type": "Construction",
            "budget": 8500.00,
            "start_date": "2025-10-17",
            "end_date": "2025-10-20"
        },
        {
            "name": "Plumbing Rough-in", 
            "description": "Install plumbing pipes and fixtures before drywall",
            "status": "To Do",
            "priority": "High",
            "task_type": "Construction",
            "budget": 6200.00,
            "start_date": "2025-10-18",
            "end_date": "2025-10-22"
        },
        {
            "name": "HVAC Ductwork",
            "description": "Install HVAC ducts and vents",
            "status": "To Do", 
            "priority": "Medium",
            "task_type": "Construction",
            "budget": 12000.00,
            "start_date": "2025-10-21",
            "end_date": "2025-10-25"
        },
        {
            "name": "Insulation Installation",
            "description": "Install wall and ceiling insulation",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Construction", 
            "budget": 4500.00,
            "start_date": "2025-10-26",
            "end_date": "2025-10-28"
        },
        {
            "name": "Drywall Hanging",
            "description": "Hang drywall sheets on walls and ceiling",
            "status": "To Do",
            "priority": "High",
            "task_type": "Construction",
            "budget": 7800.00,
            "start_date": "2025-10-29",
            "end_date": "2025-11-01"
        },
        {
            "name": "Drywall Taping & Mudding",
            "description": "Tape joints and apply mud compound",
            "status": "To Do",
            "priority": "High", 
            "task_type": "Construction",
            "budget": 5600.00,
            "start_date": "2025-11-02",
            "end_date": "2025-11-05"
        },
        {
            "name": "Drywall Sanding",
            "description": "Sand drywall smooth and prepare for painting",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Construction",
            "budget": 2800.00,
            "start_date": "2025-11-06",
            "end_date": "2025-11-08"
        },
        {
            "name": "Prime Walls",
            "description": "Apply primer to all drywall surfaces",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Construction",
            "budget": 3200.00,
            "start_date": "2025-11-09",
            "end_date": "2025-11-11"
        },
        {
            "name": "Interior Painting",
            "description": "Apply finish paint to all interior walls",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Construction",
            "budget": 8900.00,
            "start_date": "2025-11-12",
            "end_date": "2025-11-16"
        },
        {
            "name": "Final Electrical Install",
            "description": "Install switches, outlets, and light fixtures",
            "status": "To Do",
            "priority": "High",
            "task_type": "Construction",
            "budget": 6700.00,
            "start_date": "2025-11-17",
            "end_date": "2025-11-20"
        }
    ]
    
    # Component and Project IDs from your example
    component_id = 1
    project_id = 7
    
    print(f"📋 Creating {len(tasks_data)} tasks for:")
    print(f"   Project ID: {project_id}")
    print(f"   Component ID: {component_id}")
    print()
    
    created_tasks = []
    failed_tasks = []
    
    for i, task_data in enumerate(tasks_data, 1):
        # Add component and project IDs
        task_data["component_id"] = component_id
        task_data["project_id"] = project_id
        
        print(f"🔧 Creating Task {i}: {task_data['name']}")
        print(f"   📅 {task_data['start_date']} → {task_data['end_date']}")
        print(f"   💰 Budget: ${task_data['budget']:,.2f}")
        
        # Send POST request
        try:
            response = requests.post(
                f"{BASE_URL}/tasks/",
                json=task_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                created_task = response.json()
                created_tasks.append(created_task)
                print(f"   ✅ Created successfully! Task ID: {created_task['id']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Error: {response.text}")
                failed_tasks.append({"task_name": task_data['name'], "error": response.text})
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            failed_tasks.append({"task_name": task_data['name'], "error": str(e)})
        
        print()  # Empty line between tasks
    
    # Summary
    print("=" * 50)
    print("📊 TASK CREATION SUMMARY")
    print("=" * 50)
    print(f"✅ Successfully created: {len(created_tasks)} tasks")
    print(f"❌ Failed to create: {len(failed_tasks)} tasks")
    
    if created_tasks:
        print(f"\n📋 Created Tasks:")
        for task in created_tasks:
            print(f"   ID {task['id']}: {task['name']} - {task['status']}")
    
    if failed_tasks:
        print(f"\n⚠️  Failed Tasks:")
        for failure in failed_tasks:
            print(f"   {failure['task_name']}: {failure['error'][:100]}...")
    
    # Calculate total budget
    total_budget = sum(float(task.get('budget', 0)) for task in created_tasks if task.get('budget'))
    print(f"\n💰 Total Budget for Created Tasks: ${total_budget:,.2f}")
    
    return created_tasks, failed_tasks

def verify_tasks():
    """Verify the created tasks by fetching them"""
    print("\n" + "=" * 50)
    print("🔍 VERIFICATION - Fetching Tasks by Component")
    print("=" * 50)
    
    component_id = 1
    response = requests.get(f"{BASE_URL}/components/{component_id}/tasks")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Found {len(tasks)} tasks for component {component_id}")
        
        for task in tasks:
            print(f"   📋 {task['name']} (ID: {task['id']})")
            print(f"      Status: {task['status']} | Priority: {task['priority']}")
            print(f"      Dates: {task['start_date']} → {task['end_date']}")
            print(f"      Budget: ${float(task['budget']):,.2f}" if task['budget'] else "      Budget: None")
            print()
    else:
        print(f"❌ Failed to fetch tasks: {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    created, failed = create_multiple_tasks()
    
    if created:
        verify_tasks()
    
    print("\n🎉 Task creation process completed!")