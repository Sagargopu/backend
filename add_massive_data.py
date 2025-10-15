"""
Add massive amounts of realistic data to BuildBuzz database
This script adds extensive data for performance testing and realistic scenarios
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

def generate_fake_data():
    """Generate extensive fake data for comprehensive testing"""
    print("🚀 Adding massive amounts of realistic data...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get existing data counts
        existing_users = session.query(user_models.User).count()
        existing_projects = session.query(project_models.Project).count()
        existing_vendors = session.query(finance_models.Vendor).count()
        
        print(f"📊 Current database state:")
        print(f"   Users: {existing_users}")
        print(f"   Projects: {existing_projects}")
        print(f"   Vendors: {existing_vendors}")
        
        # Get existing users by role
        clerks = session.query(user_models.User).filter(user_models.User.role == "clerk").all()
        business_admins = session.query(user_models.User).filter(user_models.User.role == "business_admin").all()
        project_managers = session.query(user_models.User).filter(user_models.User.role == "project_manager").all()
        accountants = session.query(user_models.User).filter(user_models.User.role == "accountant").all()
        clients = session.query(user_models.User).filter(user_models.User.role == "client").all()
        
        # Add more users
        print("👥 Adding more users...")
        additional_users = [
            # More Project Managers
            {"full_name": "Sarah Construction", "email": "sarah@builders.com", "role": "project_manager"},
            {"full_name": "Tom Foreman", "email": "tom@construction.com", "role": "project_manager"},
            {"full_name": "Lisa Site", "email": "lisa@sitework.com", "role": "project_manager"},
            {"full_name": "Mark Builder", "email": "mark@buildpro.com", "role": "project_manager"},
            {"full_name": "Amy Contractor", "email": "amy@contractor.com", "role": "project_manager"},
            
            # More Clients
            {"full_name": "Robert Developer", "email": "robert@realestate.com", "role": "client"},
            {"full_name": "Jennifer Property", "email": "jennifer@propertygroup.com", "role": "client"},
            {"full_name": "Kevin Investor", "email": "kevin@investmentfirm.com", "role": "client"},
            {"full_name": "Michelle Corporate", "email": "michelle@corporatedev.com", "role": "client"},
            {"full_name": "Brian Holdings", "email": "brian@holdings.com", "role": "client"},
            {"full_name": "Andrea Ventures", "email": "andrea@ventures.com", "role": "client"},
            
            # More Accountants
            {"full_name": "Charles Financial", "email": "charles@finance.com", "role": "accountant"},
            {"full_name": "Diana Budget", "email": "diana@budgetpro.com", "role": "accountant"},
            {"full_name": "Eric Numbers", "email": "eric@accounting.com", "role": "accountant"},
            
            # More Clerks
            {"full_name": "Fiona Admin", "email": "fiona@buildbuzz.com", "role": "clerk"},
            {"full_name": "George Office", "email": "george@buildbuzz.com", "role": "clerk"},
        ]
        
        new_users = {}
        for i, user_data in enumerate(additional_users):
            user = user_models.User(
                **user_data,
                is_active=True,
                account_setup_completed=True,
                phone_number=f"+1-555-{2000 + i:04d}",
                years_experience=random.randint(3, 20) if user_data["role"] != "client" else None,
                current_wage_rate=Decimal(str(random.randint(30, 95))) if user_data["role"] == "project_manager" else None,
                availability_status="available" if user_data["role"] != "client" else None
            )
            session.add(user)
            new_users[user_data["role"]] = new_users.get(user_data["role"], []) + [user]
        
        session.commit()
        
        # Update user lists
        project_managers.extend(new_users.get("project_manager", []))
        clients.extend(new_users.get("client", []))
        accountants.extend(new_users.get("accountant", []))
        
        print(f"   ✅ Added {len(additional_users)} additional users")
        
        # Add more projects
        print("🏢 Adding more projects...")
        more_projects_data = [
            {
                "name": "Coastal Resort Development",
                "description": "Luxury beachfront resort with 200 rooms and conference facilities",
                "start_date": date(2024, 6, 1),
                "end_date": date(2025, 12, 31),
                "budget": Decimal("25000000.00"),
                "status": "planned",
                "client_name": "Resort Development Corp",
                "project_category": "Commercial",
                "project_type": "Resort"
            },
            {
                "name": "Urban High-Rise Apartments",
                "description": "35-story luxury apartment tower with 300 units",
                "start_date": date(2024, 8, 15),
                "end_date": date(2026, 6, 30),
                "budget": Decimal("45000000.00"),
                "status": "planned",
                "client_name": "Urban Development LLC",
                "project_category": "Residential",
                "project_type": "High-Rise"
            },
            {
                "name": "Medical Center Expansion",
                "description": "Hospital expansion with new surgery wing and parking structure",
                "start_date": date(2024, 7, 1),
                "end_date": date(2025, 8, 31),
                "budget": Decimal("18000000.00"),
                "status": "in_progress",
                "client_name": "Regional Medical Center",
                "project_category": "Healthcare",
                "project_type": "Medical Facility"
            },
            {
                "name": "Corporate Campus Phase 2",
                "description": "Second phase of tech campus with 4 office buildings",
                "start_date": date(2024, 9, 1),
                "end_date": date(2025, 12, 31),
                "budget": Decimal("35000000.00"),
                "status": "planned",
                "client_name": "Tech Innovation Corp",
                "project_category": "Commercial",
                "project_type": "Corporate Campus"
            },
            {
                "name": "Mixed-Use Development Downtown",
                "description": "20-story mixed retail/residential/office complex",
                "start_date": date(2024, 5, 15),
                "end_date": date(2026, 3, 31),
                "budget": Decimal("42000000.00"),
                "status": "in_progress",
                "client_name": "Downtown Development Authority",
                "project_category": "Mixed-Use",
                "project_type": "Mixed Development"
            },
            {
                "name": "Suburban Family Homes - Phase 1",
                "description": "50-home subdivision development with community amenities",
                "start_date": date(2024, 4, 1),
                "end_date": date(2025, 10, 31),
                "budget": Decimal("15000000.00"),
                "status": "in_progress",
                "client_name": "Family Homes Developer",
                "project_category": "Residential",
                "project_type": "Subdivision"
            },
            {
                "name": "Data Center Construction",
                "description": "100,000 sq ft enterprise data center with redundant systems",
                "start_date": date(2024, 3, 1),
                "end_date": date(2024, 11, 30),
                "budget": Decimal("28000000.00"),
                "status": "in_progress",
                "client_name": "Cloud Computing Solutions",
                "project_category": "Technology",
                "project_type": "Data Center"
            },
            {
                "name": "Airport Terminal Renovation",
                "description": "Complete renovation of passenger terminal and baggage systems",
                "start_date": date(2024, 10, 1),
                "end_date": date(2026, 4, 30),
                "budget": Decimal("75000000.00"),
                "status": "planned",
                "client_name": "Metropolitan Airport Authority",
                "project_category": "Transportation",
                "project_type": "Airport"
            }
        ]
        
        new_projects = []
        for i, proj_data in enumerate(more_projects_data):
            project = project_models.Project(
                **proj_data,
                project_manager_id=project_managers[i % len(project_managers)].id if project_managers else None
            )
            session.add(project)
            new_projects.append(project)
        
        session.commit()
        print(f"   ✅ Added {len(more_projects_data)} additional projects")
        
        # Add more vendors
        print("🏪 Adding more vendors...")
        more_vendors_data = [
            {"name": "Advanced Electrical Systems", "contact_person": "Robert Volt", "email": "robert@advancedelectric.com", "phone": "+1-555-2001"},
            {"name": "Precision Plumbing Corp", "contact_person": "Linda Flow", "email": "linda@precisionplumbing.com", "phone": "+1-555-2002"},
            {"name": "Structural Steel Specialists", "contact_person": "Carlos Steel", "email": "carlos@structuralsteel.com", "phone": "+1-555-2003"},
            {"name": "Green Building Materials", "contact_person": "Amanda Green", "email": "amanda@greenbuild.com", "phone": "+1-555-2004"},
            {"name": "Heavy Machinery Rentals", "contact_person": "Derek Machine", "email": "derek@heavymachinery.com", "phone": "+1-555-2005"},
            {"name": "Architectural Glass & Windows", "contact_person": "Nicole Glass", "email": "nicole@archglass.com", "phone": "+1-555-2006"},
            {"name": "Commercial Roofing Pros", "contact_person": "James Roof", "email": "james@commercialroofing.com", "phone": "+1-555-2007"},
            {"name": "Smart Building Technology", "contact_person": "Patricia Tech", "email": "patricia@smartbuilding.com", "phone": "+1-555-2008"},
            {"name": "Flooring Solutions Unlimited", "contact_person": "Michael Floor", "email": "michael@flooringsolutions.com", "phone": "+1-555-2009"},
            {"name": "Safety Equipment Supply", "contact_person": "Rachel Safety", "email": "rachel@safetyequip.com", "phone": "+1-555-2010"},
        ]
        
        more_vendors = []
        for vendor_data in more_vendors_data:
            vendor = finance_models.Vendor(**vendor_data)
            session.add(vendor)
            more_vendors.append(vendor)
        
        session.commit()
        print(f"   ✅ Added {len(more_vendors_data)} additional vendors")
        
        # Add extensive purchase orders
        print("📦 Adding extensive purchase orders...")
        all_projects = session.query(project_models.Project).all()
        all_vendors = session.query(finance_models.Vendor).all()
        pm_ids = [pm.id for pm in project_managers]
        accountant_ids = [acc.id for acc in accountants]
        
        po_templates = [
            {"description": "Foundation concrete and rebar materials", "base_amount": 50000, "category": "materials"},
            {"description": "Structural steel beams and connections", "base_amount": 120000, "category": "materials"},
            {"description": "Electrical wiring and panel systems", "base_amount": 75000, "category": "electrical"},
            {"description": "Plumbing fixtures and piping", "base_amount": 45000, "category": "plumbing"},
            {"description": "HVAC equipment and ductwork", "base_amount": 85000, "category": "hvac"},
            {"description": "Roofing materials and insulation", "base_amount": 35000, "category": "roofing"},
            {"description": "Windows and exterior doors", "base_amount": 65000, "category": "materials"},
            {"description": "Interior finishing materials", "base_amount": 40000, "category": "finishing"},
            {"description": "Equipment rental for excavation", "base_amount": 25000, "category": "equipment"},
            {"description": "Safety equipment and supplies", "base_amount": 15000, "category": "safety"},
        ]
        
        statuses = ["Pending Approval", "Approved", "Paid", "Cancelled"]
        status_weights = [0.2, 0.4, 0.3, 0.1]  # More likely to be approved/paid
        
        for project in all_projects[-5:]:  # Add POs for latest 5 projects
            num_pos = random.randint(8, 15)
            for _ in range(num_pos):
                template = random.choice(po_templates)
                amount_variation = random.uniform(0.7, 1.5)  # ±50% variation
                amount = template["base_amount"] * amount_variation
                
                po = finance_models.PurchaseOrder(
                    description=f"{template['description']} for {project.name}",
                    vendor_id=random.choice(all_vendors).id,
                    project_id=project.id,
                    amount=round(amount, 2),
                    status=random.choices(statuses, weights=status_weights)[0],
                    created_by_id=random.choice(pm_ids) if pm_ids else None,
                    approved_by_id=random.choice(accountant_ids) if accountant_ids and random.random() > 0.3 else None,
                )
                session.add(po)
        
        session.commit()
        print(f"   ✅ Added extensive purchase orders")
        
        # Add many more transactions
        print("💳 Adding extensive transactions...")
        categories = session.query(finance_models.TransactionCategory).all()
        
        transaction_templates = [
            {"name": "Material delivery", "type": "outgoing", "base_amount": 25000, "frequency": 0.3},
            {"name": "Labor costs", "type": "outgoing", "base_amount": 35000, "frequency": 0.25},
            {"name": "Equipment rental", "type": "outgoing", "base_amount": 15000, "frequency": 0.2},
            {"name": "Subcontractor payment", "type": "outgoing", "base_amount": 65000, "frequency": 0.15},
            {"name": "Project milestone payment", "type": "incoming", "base_amount": 250000, "frequency": 0.1},
        ]
        
        for project in all_projects:
            # Each project gets 15-30 transactions
            num_transactions = random.randint(15, 30)
            project_start = getattr(project, 'start_date', date.today())
            project_end = getattr(project, 'end_date', date.today() + timedelta(days=365))
            project_duration = (project_end - project_start).days
            
            for _ in range(num_transactions):
                template = random.choice(transaction_templates)
                amount_variation = random.uniform(0.5, 2.0)
                amount = template["base_amount"] * amount_variation
                
                # Random date within project timeline
                days_offset = random.randint(0, min(project_duration, 180))
                transaction_date = project_start + timedelta(days=days_offset)
                
                if transaction_date > date.today():
                    transaction_date = date.today() - timedelta(days=random.randint(1, 30))
                
                transaction = finance_models.Transaction(
                    expense_name=f"{template['name']} - {project.name}",
                    description=f"{template['name']} for project {project.name}",
                    amount=Decimal(str(round(amount, 2))),
                    transaction_type=template["type"],
                    transaction_date=transaction_date,
                    project_id=project.id,
                    category_id=random.choice(categories).id,
                    is_project_specific=True,
                    status=random.choices(["approved", "pending", "paid"], weights=[0.5, 0.2, 0.3])[0],
                    approved_by=random.choice(accountant_ids) if accountant_ids else None,
                    created_by=random.choice(pm_ids) if pm_ids else None,
                    budget_line_item=random.choice(categories).category_name,
                    is_budgeted=random.choice([True, True, False]),  # 2/3 budgeted
                    fiscal_year=transaction_date.year,
                    fiscal_quarter=f"Q{(transaction_date.month - 1) // 3 + 1}",
                    fiscal_month=transaction_date.month,
                )
                session.add(transaction)
        
        session.commit()
        print(f"   ✅ Added extensive transactions")
        
        # Add more change orders
        print("🔄 Adding more change orders...")
        co_templates = [
            "Additional electrical outlets and data ports",
            "Upgrade HVAC system for energy efficiency",
            "Enhanced security system installation",
            "Premium finish materials upgrade",
            "Additional parking spaces",
            "Structural reinforcement for wind load",
            "Fire suppression system upgrade",
            "Smart building automation features",
            "Additional loading dock installation",
            "Accessibility compliance improvements",
        ]
        
        for project in all_projects:
            # Each project gets 2-6 change orders
            num_cos = random.randint(2, 6)
            for _ in range(num_cos):
                description = random.choice(co_templates)
                impact = random.uniform(5000, 50000)
                
                co = finance_models.ChangeOrder(
                    description=f"{description} for {project.name}",
                    project_id=project.id,
                    financial_impact=round(impact, 2),
                    status=random.choices(["Pending Approval", "Approved", "Rejected"], weights=[0.3, 0.6, 0.1])[0],
                    created_by_id=random.choice(pm_ids) if pm_ids else None,
                    approved_by_id=random.choice(accountant_ids) if accountant_ids and random.random() > 0.4 else None,
                )
                session.add(co)
        
        session.commit()
        print(f"   ✅ Added extensive change orders")
        
        # Final count
        print("\\n📊 Final Database Summary:")
        print(f"   👥 Users: {session.query(user_models.User).count()}")
        print(f"   🏗️ Projects: {session.query(project_models.Project).count()}")
        print(f"   🔧 Components: {session.query(project_models.ProjectComponent).count()}")
        print(f"   📋 Tasks: {session.query(project_models.Task).count()}")
        print(f"   🏪 Vendors: {session.query(finance_models.Vendor).count()}")
        print(f"   📦 Purchase Orders: {session.query(finance_models.PurchaseOrder).count()}")
        print(f"   🔄 Change Orders: {session.query(finance_models.ChangeOrder).count()}")
        print(f"   💳 Transactions: {session.query(finance_models.Transaction).count()}")
        print(f"   📄 Contracts: {session.query(finance_models.Contract).count()}")
        
        print("\\n🎉 Massive data loading completed successfully!")
        print("🚀 Your BuildBuzz database is now packed with realistic data for comprehensive testing!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding massive data: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    generate_fake_data()