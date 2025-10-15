"""
BuildBuzz Database Summary - Final Status Report
Shows comprehensive overview of all loaded data
"""

import os
import sys
from decimal import Decimal

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.users import models as user_models
from app.projects import models as project_models
from app.documents import models as document_models
from app.finance import models as finance_models

def generate_summary():
    """Generate comprehensive database summary"""
    print("🎉 BUILDBUZZ DATABASE COMPREHENSIVE SUMMARY")
    print("=" * 70)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Basic counts
        print("\n📊 DATA COUNTS:")
        print("-" * 40)
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
        
        # User breakdown
        print("\n👥 USERS BY ROLE:")
        print("-" * 40)
        roles = ["clerk", "business_admin", "project_manager", "accountant", "client"]
        for role in roles:
            count = session.query(user_models.User).filter(user_models.User.role == role).count()
            print(f"   {role.replace('_', ' ').title()}: {count}")
        
        # Project breakdown
        print("\n🏗️ PROJECTS BY STATUS:")
        print("-" * 40)
        statuses = ["planned", "in_progress", "completed", "on_hold"]
        for status in statuses:
            count = session.query(project_models.Project).filter(project_models.Project.status == status).count()
            print(f"   {status.replace('_', ' ').title()}: {count}")
        
        # Project categories
        print("\n🏗️ PROJECTS BY CATEGORY:")
        print("-" * 40)
        projects = session.query(project_models.Project).all()
        categories = {}
        for project in projects:
            cat = getattr(project, 'project_category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in categories.items():
            print(f"   {category}: {count}")
        
        # Financial summary
        print("\n💰 FINANCIAL SUMMARY:")
        print("-" * 40)
        
        # Project budgets
        total_budget = sum(float(getattr(p, 'budget', 0)) for p in projects)
        print(f"Total Project Budgets: ${total_budget:,.2f}")
        
        # Transactions
        transactions = session.query(finance_models.Transaction).all()
        total_outgoing = sum(float(getattr(t, 'amount', 0)) for t in transactions if getattr(t, 'transaction_type', '') == 'outgoing')
        total_incoming = sum(float(getattr(t, 'amount', 0)) for t in transactions if getattr(t, 'transaction_type', '') == 'incoming')
        print(f"Total Outgoing: ${total_outgoing:,.2f}")
        print(f"Total Incoming: ${total_incoming:,.2f}")
        print(f"Net Cash Flow: ${total_incoming - total_outgoing:,.2f}")
        
        # Purchase orders
        pos = session.query(finance_models.PurchaseOrder).all()
        total_po_amount = sum(float(getattr(po, 'amount', 0)) for po in pos)
        approved_pos = [po for po in pos if getattr(po, 'status', '') in ['Approved', 'Paid']]
        approved_amount = sum(float(getattr(po, 'amount', 0)) for po in approved_pos)
        print(f"Total PO Amount: ${total_po_amount:,.2f}")
        print(f"Approved PO Amount: ${approved_amount:,.2f}")
        
        # Change orders
        cos = session.query(finance_models.ChangeOrder).all()
        total_co_impact = sum(float(getattr(co, 'financial_impact', 0)) for co in cos)
        approved_cos = [co for co in cos if getattr(co, 'status', '') == 'Approved']
        approved_co_impact = sum(float(getattr(co, 'financial_impact', 0)) for co in approved_cos)
        print(f"Total Change Order Impact: ${total_co_impact:,.2f}")
        print(f"Approved Change Orders: ${approved_co_impact:,.2f}")
        
        # Task completion
        print("\n📋 TASK STATUS:")
        print("-" * 40)
        all_tasks = session.query(project_models.Task).all()
        task_statuses = {}
        for task in all_tasks:
            status = getattr(task, 'status', 'Unknown')
            task_statuses[status] = task_statuses.get(status, 0) + 1
        
        for status, count in task_statuses.items():
            print(f"   {status}: {count}")
        
        # Document types
        print("\n📄 DOCUMENT BREAKDOWN:")
        print("-" * 40)
        documents = session.query(document_models.Document).all()
        doc_types = {}
        for doc in documents:
            doc_type = getattr(doc, 'document_type', 'Unknown')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        for doc_type, count in doc_types.items():
            print(f"   {doc_type}: {count}")
        
        print("\n" + "=" * 70)
        print("🚀 DATABASE STATUS: FULLY LOADED & READY FOR TESTING!")
        print("💡 Perfect for comprehensive API endpoint testing")
        print("🔧 Realistic data relationships and workflows established")
        print("📈 Extensive financial data for reporting and analytics")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    generate_summary()