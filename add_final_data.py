"""
Add final detailed data including components, tasks, and documents
This completes the comprehensive data loading process
"""

import os
import sys
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.users import models as user_models
from app.projects import models as project_models
from app.documents import models as document_models
from app.finance import models as finance_models

def add_final_detailed_data():
    """Add components, tasks, and documents to complete the dataset"""
    print("🎯 Adding final detailed data...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get projects without components
        all_projects = session.query(project_models.Project).all()
        projects_with_components = session.query(project_models.Project).join(project_models.ProjectComponent).distinct().all()
        projects_without_components = [p for p in all_projects if p not in projects_with_components]
        
        print(f"📊 Found {len(projects_without_components)} projects needing components...")
        
        # Component templates by project category
        component_templates = {
            "Residential": [
                {"name": "Site Preparation & Excavation", "type": "Site Work", "budget_ratio": 0.08},
                {"name": "Foundation & Concrete Work", "type": "Foundation", "budget_ratio": 0.15},
                {"name": "Framing & Structural", "type": "Framing", "budget_ratio": 0.18},
                {"name": "Roofing & Waterproofing", "type": "Roofing", "budget_ratio": 0.12},
                {"name": "Electrical Systems", "type": "Electrical", "budget_ratio": 0.12},
                {"name": "Plumbing & HVAC", "type": "Mechanical", "budget_ratio": 0.15},
                {"name": "Interior Finishing", "type": "Interior", "budget_ratio": 0.20},
            ],
            "Commercial": [
                {"name": "Site Development", "type": "Site Work", "budget_ratio": 0.06},
                {"name": "Foundation & Structure", "type": "Structural", "budget_ratio": 0.20},
                {"name": "Building Envelope", "type": "Exterior", "budget_ratio": 0.15},
                {"name": "Mechanical Systems", "type": "HVAC", "budget_ratio": 0.15},
                {"name": "Electrical & Technology", "type": "Electrical", "budget_ratio": 0.12},
                {"name": "Interior Systems", "type": "Interior", "budget_ratio": 0.18},
                {"name": "Specialty Equipment", "type": "Specialty", "budget_ratio": 0.14},
            ],
            "Industrial": [
                {"name": "Site Preparation", "type": "Site Work", "budget_ratio": 0.10},
                {"name": "Heavy Foundation", "type": "Foundation", "budget_ratio": 0.18},
                {"name": "Steel Structure", "type": "Structural", "budget_ratio": 0.25},
                {"name": "Industrial Systems", "type": "Process", "budget_ratio": 0.20},
                {"name": "Utilities & Power", "type": "Utilities", "budget_ratio": 0.15},
                {"name": "Finishing & Safety", "type": "Finishing", "budget_ratio": 0.12},
            ],
        }
        
        # Add components to projects
        print("🔧 Adding project components...")
        added_components = 0
        for project in projects_without_components:
            category = getattr(project, 'project_category', None) or "Commercial"
            templates = component_templates.get(category, component_templates["Commercial"])
            
            for template in templates:
                budget = float(getattr(project, 'budget', 0)) * template["budget_ratio"]
                project_status = getattr(project, 'status', 'planned')
                component = project_models.ProjectComponent(
                    name=template["name"],
                    description=f"{template['name']} for {project.name}",
                    type=template["type"],
                    budget=Decimal(str(round(budget, 2))),
                    project_id=project.id,
                    status="planned" if project_status == "planned" else random.choice(["in_progress", "completed", "on_hold"]),
                    completion_percentage=random.randint(0, 95) if project_status == "in_progress" else (100 if project_status == "completed" else 0),
                    allocated_budget=Decimal(str(round(budget, 2))),
                    spent_budget=Decimal(str(round(budget * random.uniform(0.1, 0.8), 2))) if project_status == "in_progress" else 0,
                )
                session.add(component)
                added_components += 1
        
        session.commit()
        print(f"   ✅ Added {added_components} components")
        
        # Add tasks to components
        print("📋 Adding tasks to components...")
        all_components = session.query(project_models.ProjectComponent).all()
        # Get component IDs that already have tasks
        components_with_tasks_ids = session.query(project_models.Task.component_id).distinct().all()
        components_with_tasks_ids = [id[0] for id in components_with_tasks_ids if id[0] is not None]
        components_without_tasks = [c for c in all_components if c.id not in components_with_tasks_ids]
        
        task_templates = [
            {"name": "Planning & Design Review", "priority": "High", "hours": [16, 40]},
            {"name": "Material Procurement", "priority": "Medium", "hours": [8, 24]},
            {"name": "Site Preparation", "priority": "High", "hours": [24, 60]},
            {"name": "Installation Work", "priority": "Critical", "hours": [40, 120]},
            {"name": "Quality Inspection", "priority": "High", "hours": [8, 16]},
            {"name": "Testing & Commissioning", "priority": "Medium", "hours": [16, 32]},
            {"name": "Documentation", "priority": "Low", "hours": [4, 12]},
            {"name": "Client Review", "priority": "Medium", "hours": [4, 8]},
        ]
        
        statuses = ["To Do", "In Progress", "Done", "Blocked"]
        status_weights = [0.3, 0.4, 0.25, 0.05]
        
        added_tasks = 0
        for component in components_without_tasks:
            num_tasks = random.randint(3, 7)
            selected_templates = random.sample(task_templates, min(num_tasks, len(task_templates)))
            
            for template in selected_templates:
                hours_range = template["hours"]
                estimated_hours = random.randint(hours_range[0], hours_range[1])
                status = random.choices(statuses, weights=status_weights)[0]
                
                task = project_models.Task(
                    name=f"{template['name']} - {component.name}",
                    description=f"{template['name']} for {component.name} in {component.project.name}",
                    priority=template["priority"],
                    status=status,
                    component_id=component.id,
                    project_id=component.project_id,
                    estimated_hours=estimated_hours,
                    actual_hours=random.randint(estimated_hours - 10, estimated_hours + 20) if status == "Done" else None,
                )
                session.add(task)
                added_tasks += 1
        
        session.commit()
        print(f"   ✅ Added {added_tasks} tasks")
        
        # Add documents
        print("📄 Adding project documents...")
        users = session.query(user_models.User).all()
        
        document_templates = [
            {"name": "Project Contract Agreement", "file_type": "pdf", "document_type": "contract"},
            {"name": "Architectural Blueprints", "file_type": "dwg", "document_type": "blueprint"},
            {"name": "Building Permit Application", "file_type": "pdf", "document_type": "permit"},
            {"name": "Material Specifications", "file_type": "xlsx", "document_type": "specification"},
            {"name": "Safety Compliance Report", "file_type": "pdf", "document_type": "safety_report"},
            {"name": "Weekly Progress Report", "file_type": "pdf", "document_type": "progress_report"},
            {"name": "Structural Engineering Plans", "file_type": "pdf", "document_type": "blueprint"},
            {"name": "Electrical Schematic", "file_type": "dwg", "document_type": "blueprint"},
            {"name": "HVAC Installation Guide", "file_type": "pdf", "document_type": "guide"},
            {"name": "Project Meeting Minutes", "file_type": "docx", "document_type": "meeting_minutes"},
        ]
        
        added_documents = 0
        for project in all_projects:
            num_docs = random.randint(5, 12)
            for _ in range(num_docs):
                template = random.choice(document_templates)
                uploader = random.choice(users)
                
                document = document_models.Document(
                    name=f"{template['name']} - {project.name}",
                    description=f"{template['name']} for {project.name}",
                    storage_path=f"/documents/{project.id}/{template['name'].lower().replace(' ', '_')}.{template['file_type']}",
                    file_type=template["file_type"],
                    file_size=random.randint(1024, 10485760),  # 1KB to 10MB
                    document_type=template["document_type"],
                    project_id=project.id,
                    uploaded_by_id=uploader.id,
                    is_public=random.choice([True, False]),
                )
                session.add(document)
                added_documents += 1
        
        session.commit()
        print(f"   ✅ Added {added_documents} documents")
        
        # Add contracts for remaining projects
        print("📄 Adding contracts...")
        projects_with_contracts = session.query(project_models.Project).join(finance_models.Contract).distinct().all()
        projects_without_contracts = [p for p in all_projects if p not in projects_with_contracts]
        
        added_contracts = 0
        for project in projects_without_contracts:
            contract = finance_models.Contract(
                name=f"{project.name} Construction Contract",
                client_name=getattr(project, 'client_name', 'Unknown Client'),
                total_value=float(getattr(project, 'budget', 0)),  # Convert Decimal to float
                project_id=project.id,
            )
            session.add(contract)
            added_contracts += 1
        
        session.commit()
        print(f"   ✅ Added {added_contracts} contracts")
        
        # Final comprehensive summary
        print("\\n🎉 FINAL COMPREHENSIVE DATABASE SUMMARY:")
        print("=" * 50)
        print(f"👥 Users: {session.query(user_models.User).count()}")
        print(f"🏗️ Projects: {session.query(project_models.Project).count()}")
        print(f"🔧 Components: {session.query(project_models.ProjectComponent).count()}")
        print(f"📋 Tasks: {session.query(project_models.Task).count()}")
        print(f"🏪 Vendors: {session.query(finance_models.Vendor).count()}")
        print(f"📦 Purchase Orders: {session.query(finance_models.PurchaseOrder).count()}")
        print(f"🔄 Change Orders: {session.query(finance_models.ChangeOrder).count()}")
        print(f"💳 Transactions: {session.query(finance_models.Transaction).count()}")
        print(f"📄 Contracts: {session.query(finance_models.Contract).count()}")
        print(f"📄 Documents: {session.query(document_models.Document).count()}")
        print("=" * 50)
        
        # Role breakdown
        print("\\n👥 USER BREAKDOWN BY ROLE:")
        for role in ["clerk", "business_admin", "project_manager", "accountant", "client"]:
            count = session.query(user_models.User).filter(user_models.User.role == role).count()
            print(f"   {role.replace('_', ' ').title()}: {count}")
        
        # Project breakdown by status
        print("\\n🏗️ PROJECT BREAKDOWN BY STATUS:")
        for status in ["planned", "in_progress", "completed", "on_hold"]:
            count = session.query(project_models.Project).filter(project_models.Project.status == status).count()
            print(f"   {status.replace('_', ' ').title()}: {count}")
        
        print("\\n🚀 BuildBuzz database is now FULLY LOADED with comprehensive data!")
        print("💡 Perfect for testing all API endpoints and workflows!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding final detailed data: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    add_final_detailed_data()