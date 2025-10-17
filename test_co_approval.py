"""
Test script for Change Order approval and budget automation
"""
import sys
import os

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from datetime import datetime
from app.database import SessionLocal
from app.finance import crud as finance_crud, models as finance_models, schemas as finance_schemas
from app.projects.models import Task, Project

def test_change_order_approval_workflow():
    """Test the complete workflow of CO approval with budget updates"""
    db = SessionLocal()
    
    try:
        print("=== Testing Change Order Approval Workflow ===\n")
        
        # 1. Get or create a test project and task
        project = db.query(Project).first()
        if not project:
            print("No projects found. Please create a project first.")
            return
            
        task = db.query(Task).filter(Task.project_id == project.id).first()
        if not task:
            print("No tasks found. Please create a task first.")
            return
            
        print(f"Using Project: {project.name}")
        print(f"Using Task: {task.name}")
        print(f"Current Task Budget: ${task.budget}")
        
        # 2. Create a change order with items
        co_data = finance_schemas.ChangeOrderCreate(
            task_id=task.id,  # type: ignore
            title='Test Change Order - Budget Impact',
            description='Testing automatic budget updates when CO is approved',
            reason='Testing',
            created_by=1  # Assuming user ID 1 exists
        )
        
        change_order = finance_crud.create_change_order(db, co_data)
        print(f"\nCreated Change Order: {change_order.co_number}")
        
        # 3. Add change order items with budget impact
        items_data = [
            {
                'change_order_id': change_order.id,
                'item_name': 'Additional Materials',
                'description': 'Extra steel beams required',
                'change_type': 'Addition',
                'impact_type': '+',
                'amount': Decimal('5000.00')
            },
            {
                'change_order_id': change_order.id,
                'item_name': 'Labor Savings',
                'description': 'Reduced labor hours due to new method',
                'change_type': 'Modification',
                'impact_type': '-',
                'amount': Decimal('1500.00')
            }
        ]
        
        for item_data in items_data:
            item = finance_models.ChangeOrderItem(**item_data)
            db.add(item)
        
        db.commit()
        print("Added Change Order Items:")
        print("  + $5,000.00 (Additional Materials)")
        print("  - $1,500.00 (Labor Savings)")
        print("  Net Impact: +$3,500.00")
        
        # 4. Calculate expected budget impact
        expected_impact = finance_crud.calculate_co_total_impact(db, change_order.id)  # type: ignore
        print(f"\nCalculated Total Impact: ${expected_impact:,.2f}")
        
        # 5. Store original budget for comparison
        original_budget = float(task.budget) if task.budget else 0.0  # type: ignore
        expected_new_budget = original_budget + expected_impact
        
        print(f"Original Budget: ${original_budget:,.2f}")
        print(f"Expected New Budget: ${expected_new_budget:,.2f}")
        
        # 6. Approve the change order (this should trigger budget update)
        print("\n=== Approving Change Order ===")
        
        # Update CO to approved status
        setattr(change_order, 'status', 'Approved')  # type: ignore
        setattr(change_order, 'approved_by', 1)  # type: ignore
        setattr(change_order, 'approved_date', datetime.now())  # type: ignore
        
        # This is where the automatic transaction should be created
        transaction = finance_crud.create_change_order_transaction(db, change_order)
        
        db.commit()
        db.refresh(task)  # Refresh to get updated budget
        
        # 7. Verify results
        print("\n=== Results ===")
        if transaction:
            print(f"✅ Transaction Created: {transaction.transaction_number}")
            print(f"   Transaction Type: {transaction.transaction_type}")
            print(f"   Amount: ${transaction.amount}")
            print(f"   Impact Type: {transaction.impact_type}")
            print(f"   Budget Before: ${transaction.budget_before}")
            print(f"   Budget After: ${transaction.budget_after}")
            
            # Check if task budget was updated correctly
            updated_budget = float(task.budget) if task.budget else 0.0  # type: ignore
            print(f"\nTask Budget Updated: ${updated_budget:,.2f}")
            
            if abs(updated_budget - expected_new_budget) < 0.01:  # Allow for rounding
                print("✅ Budget update is correct!")
            else:
                print(f"❌ Budget update incorrect. Expected: ${expected_new_budget:,.2f}, Got: ${updated_budget:,.2f}")
        else:
            print("❌ No transaction was created")
            
        print(f"\nChange Order Status: {change_order.status}")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_change_order_approval_workflow()