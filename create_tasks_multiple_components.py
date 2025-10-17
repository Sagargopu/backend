#!/usr/bin/env python3
"""
Add Multiple Tasks for Multiple Components
==========================================
Creates 10 tasks each for components 2, 3, 4, 5, 6 under project ID 7
Total: 50 tasks (10 per component)
"""

import requests
import json
from datetime import date, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def create_tasks_for_multiple_components():
    """Create 10 tasks each for components 2, 3, 4, 5, 6"""
    print("Creating Tasks for Multiple Components")
    print("=" * 50)
    
    # Component IDs to create tasks for
    component_ids = [2, 3, 4, 5, 6]
    project_id = 7
    
    # Different task templates for variety
    task_templates = [
        {
            "name": "Site Preparation",
            "description": "Prepare the work area and set up safety barriers",
            "status": "To Do",
            "priority": "High",
            "task_type": "Planning",
            "budget": 2500.00,
            "days_duration": 2
        },
        {
            "name": "Material Delivery",
            "description": "Coordinate and receive material delivery",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Planning",
            "budget": 1500.00,
            "days_duration": 1
        },
        {
            "name": "Foundation Work",
            "description": "Complete foundation and base preparation",
            "status": "To Do",
            "priority": "Critical",
            "task_type": "Construction",
            "budget": 8500.00,
            "days_duration": 5
        },
        {
            "name": "Structural Installation",
            "description": "Install main structural components",
            "status": "To Do",
            "priority": "High",
            "task_type": "Construction",
            "budget": 12000.00,
            "days_duration": 7
        },
        {
            "name": "Utility Rough-in",
            "description": "Install electrical, plumbing, and HVAC rough-in",
            "status": "To Do",
            "priority": "High",
            "task_type": "Construction",
            "budget": 9500.00,
            "days_duration": 4
        },
        {
            "name": "Insulation & Drywall",
            "description": "Install insulation and complete drywall work",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Construction",
            "budget": 6800.00,
            "days_duration": 6
        },
        {
            "name": "Finish Work",
            "description": "Complete painting, flooring, and trim work",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Construction",
            "budget": 7200.00,
            "days_duration": 8
        },
        {
            "name": "Final Inspections",
            "description": "Coordinate and complete all required inspections",
            "status": "To Do",
            "priority": "Critical",
            "task_type": "Inspection",
            "budget": 1800.00,
            "days_duration": 2
        },
        {
            "name": "Quality Control",
            "description": "Perform final quality control and punch list",
            "status": "To Do",
            "priority": "High",
            "task_type": "Inspection",
            "budget": 2200.00,
            "days_duration": 3
        },
        {
            "name": "Project Closeout",
            "description": "Complete documentation and project handover",
            "status": "To Do",
            "priority": "Medium",
            "task_type": "Documentation",
            "budget": 1200.00,
            "days_duration": 2
        }
    ]
    
    all_created_tasks = []
    all_failed_tasks = []
    component_summaries = {}
    
    print(f"📋 Creating tasks for {len(component_ids)} components")
    print(f"📋 Project ID: {project_id}")
    print(f"📋 Tasks per component: {len(task_templates)}")
    print(f"📋 Total tasks to create: {len(component_ids) * len(task_templates)}")
    print()
    
    # Create tasks for each component
    for comp_index, component_id in enumerate(component_ids, 1):
        print(f"🔧 COMPONENT {component_id} ({comp_index}/{len(component_ids)})")
        print("=" * 30)
        
        component_tasks = []
        component_failures = []
        start_date = date(2025, 11, 1)  # Different start date for each component
        current_date = start_date
        
        for task_index, template in enumerate(task_templates, 1):
            # Calculate dates
            task_start_date = current_date
            task_end_date = current_date + timedelta(days=template["days_duration"])
            
            # Create task data
            task_data = {
                "name": f"{template['name']} - Component {component_id}",
                "description": f"[Component {component_id}] {template['description']}",
                "status": template["status"],
                "priority": template["priority"],
                "task_type": template["task_type"],
                "budget": template["budget"],
                "start_date": task_start_date.strftime("%Y-%m-%d"),
                "end_date": task_end_date.strftime("%Y-%m-%d"),
                "component_id": component_id,
                "project_id": project_id
            }
            
            print(f"   📋 Task {task_index}: {template['name']}")
            print(f"      📅 {task_data['start_date']} → {task_data['end_date']}")
            print(f"      💰 ${template['budget']:,.2f}")
            
            # Send POST request
            try:
                response = requests.post(
                    f"{BASE_URL}/tasks/",
                    json=task_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code in [200, 201]:
                    created_task = response.json()
                    component_tasks.append(created_task)
                    all_created_tasks.append(created_task)
                    print(f"      ✅ Created! ID: {created_task['id']}")
                else:
                    print(f"      ❌ Failed: {response.status_code}")
                    error_info = {"task_name": task_data['name'], "component_id": component_id, "error": response.text}
                    component_failures.append(error_info)
                    all_failed_tasks.append(error_info)
                    
            except Exception as e:
                print(f"      ❌ Exception: {str(e)}")
                error_info = {"task_name": task_data['name'], "component_id": component_id, "error": str(e)}
                component_failures.append(error_info)
                all_failed_tasks.append(error_info)
            
            # Move to next start date (add 1 day buffer between tasks)
            current_date = task_end_date + timedelta(days=1)
        
        # Store component summary
        component_summaries[component_id] = {
            "created": len(component_tasks),
            "failed": len(component_failures),
            "total_budget": sum(float(task.get('budget', 0)) for task in component_tasks if task.get('budget'))
        }
        
        print(f"   📊 Component {component_id} Summary:")
        print(f"      ✅ Created: {len(component_tasks)} tasks")
        print(f"      ❌ Failed: {len(component_failures)} tasks") 
        print(f"      💰 Total Budget: ${component_summaries[component_id]['total_budget']:,.2f}")
        print()
    
    # Overall Summary
    print("=" * 60)
    print("📊 OVERALL SUMMARY")
    print("=" * 60)
    
    total_created = len(all_created_tasks)
    total_failed = len(all_failed_tasks)
    total_budget = sum(float(task.get('budget', 0)) for task in all_created_tasks if task.get('budget'))
    
    print(f"✅ Total Tasks Created: {total_created}")
    print(f"❌ Total Tasks Failed: {total_failed}")
    print(f"💰 Total Budget: ${total_budget:,.2f}")
    print()
    
    print("📋 Per Component Breakdown:")
    for component_id in component_ids:
        summary = component_summaries[component_id]
        print(f"   Component {component_id}: {summary['created']} tasks, ${summary['total_budget']:,.2f}")
    
    if all_failed_tasks:
        print(f"\n⚠️  Failed Tasks ({len(all_failed_tasks)}):")
        for failure in all_failed_tasks:
            print(f"   Component {failure['component_id']}: {failure['task_name']}")
    
    return all_created_tasks, all_failed_tasks, component_summaries

def verify_created_tasks():
    """Verify the created tasks by component"""
    print("\n" + "=" * 60)
    print("🔍 VERIFICATION - Tasks by Component")
    print("=" * 60)
    
    component_ids = [2, 3, 4, 5, 6]
    
    for component_id in component_ids:
        print(f"\n📋 Component {component_id} Tasks:")
        print("-" * 30)
        
        response = requests.get(f"{BASE_URL}/components/{component_id}/tasks")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Found {len(tasks)} tasks")
            
            total_budget = 0
            for i, task in enumerate(tasks, 1):
                budget = float(task.get('budget', 0)) if task.get('budget') else 0
                total_budget += budget
                
                print(f"   {i:2d}. {task['name']}")
                print(f"       Status: {task['status']} | Priority: {task['priority']}")
                print(f"       Dates: {task['start_date']} → {task['end_date']}")
                print(f"       Budget: ${budget:,.2f}")
            
            print(f"   💰 Component Total: ${total_budget:,.2f}")
        else:
            print(f"❌ Failed to fetch tasks: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Starting Multi-Component Task Creation...")
    print()
    
    created_tasks, failed_tasks, summaries = create_tasks_for_multiple_components()
    
    if created_tasks:
        verify_created_tasks()
    
    print("\n🎉 Multi-component task creation completed!")
    print(f"📈 Successfully created {len(created_tasks)} tasks across 5 components!")