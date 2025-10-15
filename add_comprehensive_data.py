"""
Add comprehensive sample data to BuildBuzz database
This script adds realistic data for testing and demonstration
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

def add_comprehensive_data():
    """Add comprehensive sample data"""
    print("🚀 Adding comprehensive sample data to BuildBuzz database...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Step 1: Add Users with different roles
        print("👥 Adding users...")
        users_data = [
            # Clerks
            {"full_name": "Alice Admin", "email": "alice@buildbuzz.com", "role": "clerk"},
            {"full_name": "Bob Manager", "email": "bob@buildbuzz.com", "role": "clerk"},
            
            # Business Admins
            {"full_name": "Carol Executive", "email": "carol@buildbuzz.com", "role": "business_admin"},
            {"full_name": "David CEO", "email": "david@buildbuzz.com", "role": "business_admin"},
            
            # Project Managers
            {"full_name": "Eva ProjectLead", "email": "eva@buildbuzz.com", "role": "project_manager"},
            {"full_name": "Frank Supervisor", "email": "frank@buildbuzz.com", "role": "project_manager"},
            {"full_name": "Grace Builder", "email": "grace@buildbuzz.com", "role": "project_manager"},
            {"full_name": "Henry Construction", "email": "henry@buildbuzz.com", "role": "project_manager"},
            
            # Accountants
            {"full_name": "Ivy Finance", "email": "ivy@buildbuzz.com", "role": "accountant"},
            {"full_name": "Jack Numbers", "email": "jack@buildbuzz.com", "role": "accountant"},
            {"full_name": "Kate Budget", "email": "kate@buildbuzz.com", "role": "accountant"},
            
            # Clients
            {"full_name": "Laura Client", "email": "laura@techcorp.com", "role": "client"},
            {"full_name": "Mike Corporate", "email": "mike@megacorp.com", "role": "client"},
            {"full_name": "Nina Owner", "email": "nina@residential.com", "role": "client"},
            {"full_name": "Oscar Investor", "email": "oscar@investments.com", "role": "client"},
            {"full_name": "Paula Developer", "email": "paula@devcompany.com", "role": "client"},
        ]
        
        users = {}
        for i, user_data in enumerate(users_data):
            user = user_models.User(
                **user_data,
                is_active=True,
                account_setup_completed=True,
                phone_number=f"+1-555-{1000 + i:04d}",
                years_experience=random.randint(2, 15) if user_data["role"] != "client" else None,
                current_wage_rate=Decimal(str(random.randint(25, 85))) if user_data["role"] == "project_manager" else None,
                availability_status="available" if user_data["role"] != "client" else None
            )
            session.add(user)
            users[user_data["role"]] = users.get(user_data["role"], []) + [user]
        
        session.commit()
        print(f"   ✅ Added {len(users_data)} users")
        
        # Step 2: Add Project Types
        print("🏗️ Adding project types...")
        project_types_data = [
            {"category": "Residential", "type_name": "Single Family Home", "complexity_level": "Simple", "typical_duration_months": 6},
            {"category": "Residential", "type_name": "Multi-Family Complex", "complexity_level": "Moderate", "typical_duration_months": 12},
            {"category": "Commercial", "type_name": "Office Building", "complexity_level": "Complex", "typical_duration_months": 18},
            {"category": "Commercial", "type_name": "Retail Center", "complexity_level": "Moderate", "typical_duration_months": 10},
            {"category": "Industrial", "type_name": "Warehouse", "complexity_level": "Simple", "typical_duration_months": 8},
            {"category": "Industrial", "type_name": "Manufacturing Plant", "complexity_level": "Complex", "typical_duration_months": 24},
        ]
        
        for pt_data in project_types_data:
            pt = project_models.ProjectType(**pt_data)
            session.add(pt)
        
        session.commit()
        print(f"   ✅ Added {len(project_types_data)} project types")
        
        # Step 3: Add Projects
        print("🏢 Adding projects...")
        projects_data = [
            {
                "name": "Downtown Office Complex",
                "description": "15-story modern office building with underground parking",
                "start_date": date(2024, 1, 15),
                "end_date": date(2024, 12, 31),
                "budget": Decimal("5500000.00"),
                "status": "in_progress",
                "client_name": "TechCorp Solutions",
                "project_category": "Commercial",
                "project_type": "Office Building"
            },
            {
                "name": "Riverside Apartments",
                "description": "120-unit luxury apartment complex with amenities",
                "start_date": date(2024, 3, 1),
                "end_date": date(2025, 6, 30),
                "budget": Decimal("8200000.00"),
                "status": "in_progress",
                "client_name": "MegaCorp Investments",
                "project_category": "Residential",
                "project_type": "Multi-Family Complex"
            },
            {
                "name": "Industrial Warehouse Facility",
                "description": "200,000 sq ft distribution center with loading docks",
                "start_date": date(2024, 2, 10),
                "end_date": date(2024, 10, 15),
                "budget": Decimal("3200000.00"),
                "status": "in_progress",
                "client_name": "Logistics Pro",
                "project_category": "Industrial",
                "project_type": "Warehouse"
            },
            {
                "name": "Suburban Shopping Center",
                "description": "Mixed-use retail and dining complex",
                "start_date": date(2024, 4, 1),
                "end_date": date(2025, 2, 28),
                "budget": Decimal("4100000.00"),
                "status": "planned",
                "client_name": "Retail Developers Inc",
                "project_category": "Commercial",
                "project_type": "Retail Center"
            },
            {
                "name": "Luxury Single Family Home",
                "description": "Custom 5,000 sq ft home with smart features",
                "start_date": date(2024, 5, 15),
                "end_date": date(2024, 11, 30),
                "budget": Decimal("1200000.00"),
                "status": "planned",
                "client_name": "Johnson Family",
                "project_category": "Residential",
                "project_type": "Single Family Home"
            },
            {
                "name": "Manufacturing Plant Expansion", 
                "description": "50,000 sq ft addition to existing facility",
                "start_date": date(2023, 8, 1),
                "end_date": date(2024, 8, 31),
                "budget": Decimal("6800000.00"),
                "status": "completed",
                "client_name": "Industrial Manufacturing Co",
                "project_category": "Industrial",
                "project_type": "Manufacturing Plant"
            }
        ]
        
        projects = []
        pm_list = users.get("project_manager", [])
        for i, proj_data in enumerate(projects_data):
            project = project_models.Project(
                **proj_data,
                project_manager_id=pm_list[i % len(pm_list)].id if pm_list else None
            )
            session.add(project)
            projects.append(project)
        
        session.commit()
        print(f"   ✅ Added {len(projects_data)} projects")
        
        # Step 4: Add Project Components
        print("🔧 Adding project components...")
        components_data = [
            # Downtown Office Complex components
            [
                {"name": "Foundation & Excavation", "type": "Foundation", "budget": Decimal("650000")},
                {"name": "Steel Frame Structure", "type": "Structural", "budget": Decimal("1200000")},
                {"name": "Electrical Systems", "type": "Electrical", "budget": Decimal("800000")},
                {"name": "HVAC Installation", "type": "HVAC", "budget": Decimal("600000")},
                {"name": "Interior Finishing", "type": "Interior", "budget": Decimal("950000")},
                {"name": "Parking Garage", "type": "Concrete", "budget": Decimal("450000")},
            ],
            # Riverside Apartments components
            [
                {"name": "Site Preparation", "type": "Site Work", "budget": Decimal("400000")},
                {"name": "Building Foundation", "type": "Foundation", "budget": Decimal("800000")},
                {"name": "Framing & Structure", "type": "Framing", "budget": Decimal("1500000")},
                {"name": "Plumbing Systems", "type": "Plumbing", "budget": Decimal("700000")},
                {"name": "Electrical & Data", "type": "Electrical", "budget": Decimal("650000")},
                {"name": "Roofing & Waterproofing", "type": "Roofing", "budget": Decimal("450000")},
                {"name": "Amenities Construction", "type": "Specialty", "budget": Decimal("800000")},
            ],
            # Industrial Warehouse components
            [
                {"name": "Site Clearing & Grading", "type": "Site Work", "budget": Decimal("200000")},
                {"name": "Concrete Foundation", "type": "Foundation", "budget": Decimal("500000")},
                {"name": "Steel Building Erection", "type": "Structural", "budget": Decimal("900000")},
                {"name": "Loading Dock Systems", "type": "Specialty", "budget": Decimal("300000")},
                {"name": "Utilities Installation", "type": "Utilities", "budget": Decimal("250000")},
            ],
        ]
        
        all_components = []
        for proj_idx, components in enumerate(components_data[:3]):  # Only for first 3 projects
            for comp_data in components:
                component = project_models.ProjectComponent(
                    **comp_data,
                    project_id=projects[proj_idx].id,
                    status="in_progress" if proj_idx < 2 else "planned",
                    completion_percentage=random.randint(20, 85) if proj_idx < 2 else 0,
                    allocated_budget=comp_data["budget"],
                    spent_budget=comp_data["budget"] * Decimal(str(random.randint(10, 70) / 100)) if proj_idx < 2 else 0,
                )
                session.add(component)
                all_components.append(component)
        
        session.commit()
        print(f"   ✅ Added {sum(len(comps) for comps in components_data[:3])} project components")
        
        # Step 5: Add Tasks
        print("📋 Adding tasks...")
        task_templates = [
            {"name": "Site Survey", "priority": "High"},
            {"name": "Permit Applications", "priority": "High"},
            {"name": "Material Delivery", "priority": "Medium"},
            {"name": "Equipment Setup", "priority": "Medium"},
            {"name": "Quality Inspection", "priority": "High"},
            {"name": "Safety Review", "priority": "Critical"},
            {"name": "Progress Documentation", "priority": "Low"},
            {"name": "Client Walkthrough", "priority": "Medium"},
        ]
        
        tasks = []
        for component in all_components[:12]:  # Add tasks to first 12 components
            for i, task_template in enumerate(task_templates[:random.randint(3, 6)]):
                task = project_models.Task(
                    **task_template,
                    description=f"{task_template['name']} for {component.name}",
                    component_id=component.id,
                    project_id=component.project_id,
                    status=random.choice(["To Do", "In Progress", "Done", "Done", "In Progress"]),
                    estimated_hours=random.randint(8, 40),
                    actual_hours=random.randint(5, 35) if random.choice([True, False]) else None,
                )
                session.add(task)
                tasks.append(task)
        
        session.commit()
        print(f"   ✅ Added {len(tasks)} tasks")
        
        # Step 6: Add Vendors
        print("🏪 Adding vendors...")
        vendors_data = [
            {"name": "Superior Steel Supply", "contact_person": "John Steel", "email": "john@superiorsteel.com", "phone": "+1-555-1001"},
            {"name": "Concrete Masters LLC", "contact_person": "Maria Concrete", "email": "maria@concretemasters.com", "phone": "+1-555-1002"},
            {"name": "Elite Electrical Co", "contact_person": "David Electric", "email": "david@eliteelectric.com", "phone": "+1-555-1003"},
            {"name": "Premier Plumbing Pro", "contact_person": "Sarah Pipes", "email": "sarah@premierplumbing.com", "phone": "+1-555-1004"},
            {"name": "Quality HVAC Systems", "contact_person": "Mike Climate", "email": "mike@qualityhvac.com", "phone": "+1-555-1005"},
            {"name": "BuildRite Materials", "contact_person": "Lisa Build", "email": "lisa@buildrite.com", "phone": "+1-555-1006"},
            {"name": "Heavy Equipment Rentals", "contact_person": "Tom Heavy", "email": "tom@heavyequip.com", "phone": "+1-555-1007"},
        ]
        
        vendors = []
        for vendor_data in vendors_data:
            vendor = finance_models.Vendor(**vendor_data)
            session.add(vendor)
            vendors.append(vendor)
        
        session.commit()
        print(f"   ✅ Added {len(vendors_data)} vendors")
        
        # Step 7: Add Transaction Categories
        print("💰 Adding transaction categories...")
        categories_data = [
            {"category_name": "Materials", "category_type": "expense", "is_project_specific": True},
            {"category_name": "Labor", "category_type": "expense", "is_project_specific": True},
            {"category_name": "Equipment", "category_type": "expense", "is_project_specific": True},
            {"category_name": "Permits & Fees", "category_type": "expense", "is_project_specific": True},
            {"category_name": "Subcontractors", "category_type": "expense", "is_project_specific": True},
            {"category_name": "Project Payments", "category_type": "income", "is_project_specific": True},
            {"category_name": "Change Orders", "category_type": "expense", "is_project_specific": True},
            {"category_name": "Office Expenses", "category_type": "expense", "is_project_specific": False},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = finance_models.TransactionCategory(**cat_data)
            session.add(category)
            categories.append(category)
        
        session.commit()
        print(f"   ✅ Added {len(categories_data)} transaction categories")
        
        # Step 8: Add Purchase Orders
        print("📦 Adding purchase orders...")
        po_data = [
            {"description": "Steel beams for downtown office structure", "amount": 125000.00, "vendor_idx": 0, "project_idx": 0},
            {"description": "Concrete for apartment foundation", "amount": 85000.00, "vendor_idx": 1, "project_idx": 1},
            {"description": "Electrical supplies for warehouse", "amount": 45000.00, "vendor_idx": 2, "project_idx": 2},
            {"description": "HVAC equipment for office building", "amount": 95000.00, "vendor_idx": 4, "project_idx": 0},
            {"description": "Plumbing fixtures for apartments", "amount": 65000.00, "vendor_idx": 3, "project_idx": 1},
            {"description": "Construction materials package", "amount": 75000.00, "vendor_idx": 5, "project_idx": 2},
            {"description": "Equipment rental for site work", "amount": 25000.00, "vendor_idx": 6, "project_idx": 0},
        ]
        
        pm_ids = [pm.id for pm in users.get("project_manager", [])]
        accountant_ids = [acc.id for acc in users.get("accountant", [])]
        
        purchase_orders = []
        for po in po_data:
            purchase_order = finance_models.PurchaseOrder(
                description=po["description"],
                vendor_id=vendors[po["vendor_idx"]].id,
                project_id=projects[po["project_idx"]].id,
                amount=po["amount"],
                status=random.choice(["Pending Approval", "Approved", "Approved", "Paid"]),
                created_by_id=random.choice(pm_ids) if pm_ids else None,
                approved_by_id=random.choice(accountant_ids) if accountant_ids and random.choice([True, False]) else None,
            )
            session.add(purchase_order)
            purchase_orders.append(purchase_order)
        
        session.commit()
        print(f"   ✅ Added {len(po_data)} purchase orders")
        
        # Step 9: Add Change Orders
        print("🔄 Adding change orders...")
        co_data = [
            {"description": "Add extra electrical outlets in office floors 10-15", "financial_impact": 8500.00, "project_idx": 0},
            {"description": "Upgrade apartment kitchen appliances per client request", "financial_impact": 12000.00, "project_idx": 1},
            {"description": "Additional loading dock for warehouse expansion", "financial_impact": 15000.00, "project_idx": 2},
            {"description": "Enhanced security system for office building", "financial_impact": 6500.00, "project_idx": 0},
            {"description": "Premium flooring upgrade in apartment common areas", "financial_impact": 9200.00, "project_idx": 1},
        ]
        
        for co in co_data:
            change_order = finance_models.ChangeOrder(
                description=co["description"],
                project_id=projects[co["project_idx"]].id,
                financial_impact=co["financial_impact"],
                status=random.choice(["Pending Approval", "Approved", "Approved", "Rejected"]),
                created_by_id=random.choice(pm_ids) if pm_ids else None,
                approved_by_id=random.choice(accountant_ids) if accountant_ids and random.choice([True, False]) else None,
            )
            session.add(change_order)
        
        session.commit()
        print(f"   ✅ Added {len(co_data)} change orders")
        
        # Step 10: Add Transactions
        print("💳 Adding transactions...")
        transaction_data = [
            {"expense_name": "Steel Beam Delivery", "amount": 125000.00, "type": "outgoing", "project_idx": 0, "cat_idx": 0},
            {"expense_name": "Foundation Concrete Pour", "amount": 85000.00, "type": "outgoing", "project_idx": 1, "cat_idx": 0},
            {"expense_name": "Electrical Installation Labor", "amount": 35000.00, "type": "outgoing", "project_idx": 0, "cat_idx": 1},
            {"expense_name": "Project Milestone Payment", "amount": 500000.00, "type": "incoming", "project_idx": 0, "cat_idx": 5},
            {"expense_name": "Equipment Rental", "amount": 25000.00, "type": "outgoing", "project_idx": 2, "cat_idx": 2},
            {"expense_name": "Subcontractor Payment", "amount": 65000.00, "type": "outgoing", "project_idx": 1, "cat_idx": 4},
            {"expense_name": "Building Permits", "amount": 8500.00, "type": "outgoing", "project_idx": 0, "cat_idx": 3},
            {"expense_name": "HVAC Installation", "amount": 95000.00, "type": "outgoing", "project_idx": 0, "cat_idx": 0},
        ]
        
        for i, trans in enumerate(transaction_data):
            transaction = finance_models.Transaction(
                expense_name=trans["expense_name"],
                description=f"Transaction for {trans['expense_name']}",
                amount=Decimal(str(trans["amount"])),
                transaction_type=trans["type"],
                transaction_date=date.today() - timedelta(days=random.randint(1, 90)),
                project_id=projects[trans["project_idx"]].id,
                category_id=categories[trans["cat_idx"]].id,
                is_project_specific=True,
                status=random.choice(["approved", "approved", "pending", "paid"]),
                approved_by=random.choice(accountant_ids) if accountant_ids else None,
                created_by=random.choice(pm_ids) if pm_ids else None,
                budget_line_item=categories[trans["cat_idx"]].category_name,
                is_budgeted=random.choice([True, True, False]),
                fiscal_year=2024,
                fiscal_quarter="Q4",
                fiscal_month=10,
            )
            session.add(transaction)
        
        session.commit()
        print(f"   ✅ Added {len(transaction_data)} transactions")
        
        # Step 11: Add Contracts
        print("📄 Adding contracts...")
        contract_data = [
            {"name": "Downtown Office Construction Contract", "client_name": "TechCorp Solutions", "total_value": 5500000.00, "project_idx": 0},
            {"name": "Riverside Apartments Development Agreement", "client_name": "MegaCorp Investments", "total_value": 8200000.00, "project_idx": 1},
            {"name": "Industrial Warehouse Construction Contract", "client_name": "Logistics Pro", "total_value": 3200000.00, "project_idx": 2},
        ]
        
        for contract in contract_data:
            contract_obj = finance_models.Contract(
                name=contract["name"],
                client_name=contract["client_name"],
                total_value=contract["total_value"],
                project_id=projects[contract["project_idx"]].id,
            )
            session.add(contract_obj)
        
        session.commit()
        print(f"   ✅ Added {len(contract_data)} contracts")
        
        # Final verification
        print("\\n📊 Database Summary:")
        print(f"   👥 Users: {session.query(user_models.User).count()}")
        print(f"   🏗️ Projects: {session.query(project_models.Project).count()}")
        print(f"   🔧 Components: {session.query(project_models.ProjectComponent).count()}")
        print(f"   📋 Tasks: {session.query(project_models.Task).count()}")
        print(f"   🏪 Vendors: {session.query(finance_models.Vendor).count()}")
        print(f"   📦 Purchase Orders: {session.query(finance_models.PurchaseOrder).count()}")
        print(f"   🔄 Change Orders: {session.query(finance_models.ChangeOrder).count()}")
        print(f"   💳 Transactions: {session.query(finance_models.Transaction).count()}")
        print(f"   📄 Contracts: {session.query(finance_models.Contract).count()}")
        
        print("\\n🎉 Comprehensive data loading completed successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding sample data: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    add_comprehensive_data()