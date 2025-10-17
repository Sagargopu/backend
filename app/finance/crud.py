from sqlalchemy.orm import Session
# CRUD: Get all transactions by component ID
def get_transactions_by_component(db: Session, component_id: int):
    from app.projects.models import Task
    # Find all tasks for this component (returns list of tuples)
    task_id_rows = db.query(Task.id).filter(Task.component_id == component_id).all()
    task_ids = [row[0] if isinstance(row, tuple) else row.id for row in task_id_rows]
    if not task_ids:
        return []
    return db.query(models.Transaction).filter(models.Transaction.task_id.in_(task_ids)).all()
from typing import List, Optional
from datetime import datetime

from . import models, schemas

# ===============================
# VENDOR CRUD
# ===============================

def create_vendor(db: Session, vendor: schemas.VendorCreate):
    """Create a new vendor"""
    db_vendor = models.Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendor(db: Session, vendor_id: int):
    """Get vendor by ID"""
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    """Get list of all vendors"""
    return db.query(models.Vendor).offset(skip).limit(limit).all()

def get_active_vendors(db: Session):
    """Get all active vendors"""
    return db.query(models.Vendor).filter(models.Vendor.is_active == True).all()

def update_vendor(db: Session, vendor_id: int, vendor_update: schemas.VendorUpdate):
    """Update vendor"""
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if db_vendor:
        update_data = vendor_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_vendor, key, value)
        db.commit()
        db.refresh(db_vendor)
    return db_vendor

def delete_vendor(db: Session, vendor_id: int):
    """Delete vendor"""
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if db_vendor:
        db.delete(db_vendor)
        db.commit()
        return True
    return False

# ===============================
# PURCHASE ORDER CRUD
# ===============================

def generate_po_number(db: Session) -> str:
    """Generate a unique PO number in format PO-YYYY-XXX"""
    from datetime import datetime
    
    current_year = datetime.now().year
    
    # Get the highest PO number for current year
    latest_po = db.query(models.PurchaseOrder)\
        .filter(models.PurchaseOrder.po_number.like(f'PO-{current_year}-%'))\
        .order_by(models.PurchaseOrder.po_number.desc())\
        .first()
    
    if latest_po:
        # Extract the number part and increment
        try:
            last_number = int(latest_po.po_number.split('-')[-1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    return f"PO-{current_year}-{next_number:03d}"

def create_purchase_order(db: Session, po: schemas.PurchaseOrderCreate):
    """Create a new purchase order with auto-generated PO number"""
    # Generate unique PO number
    po_number = generate_po_number(db)
    
    # Create the purchase order data
    po_data = po.dict()
    po_data['po_number'] = po_number
    
    db_po = models.PurchaseOrder(**po_data)
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    return db_po

def get_purchase_order(db: Session, po_id: int):
    """Get purchase order by ID"""
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100):
    """Get list of all purchase orders"""
    return db.query(models.PurchaseOrder).offset(skip).limit(limit).all()

def get_purchase_orders_by_status(db: Session, status: str):
    """Get purchase orders by status"""
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.status == status).all()

def get_purchase_orders_by_task(db: Session, task_id: int):
    """Get purchase orders by task"""
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.task_id == task_id).all()

def get_purchase_orders_by_component(db: Session, component_id: int):
    """Get purchase orders by component"""
    # Join with Task table to filter by component_id
    from app.projects.models import Task
    return db.query(models.PurchaseOrder)\
        .join(Task, models.PurchaseOrder.task_id == Task.id)\
        .filter(Task.component_id == component_id)\
        .all()

def get_purchase_orders_by_creator(db: Session, creator_id: int):
    """Get purchase orders by creator (created_by)"""
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.created_by == creator_id).all()

def get_purchase_orders_by_approver(db: Session, approver_id: int):
    """Get purchase orders by approver (approved_by)"""
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.approved_by == approver_id).all()

def update_purchase_order(db: Session, po_id: int, po_update: schemas.PurchaseOrderUpdate):
    """Update purchase order"""
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
    if db_po:
        old_status = db_po.status if not hasattr(db_po.status, 'compare') else db_po.status.value
        update_data = po_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_po, key, value)
        db.commit()
        db.refresh(db_po)
        # If status changed to 'Approved', create transaction
        new_status = db_po.status if not hasattr(db_po.status, 'compare') else db_po.status.value
        if str(old_status) != 'Approved' and str(new_status) == 'Approved':
            create_purchase_order_transaction(db, db_po)
    return db_po
# Helper: Create transaction when purchase order is approved
def create_purchase_order_transaction(db: Session, purchase_order):
    from datetime import datetime
    from decimal import Decimal
    from app.projects.models import Task

    # Calculate total PO amount (sum of all items)
    items = db.query(models.PurchaseOrderItem).filter(models.PurchaseOrderItem.purchase_order_id == purchase_order.id).all()
    def get_price(item):
        # SQLAlchemy may return a column, so use .__float__ if available
        try:
            return float(item.price)
        except Exception:
            return float(item.price if hasattr(item.price, '__float__') else 0.0)
    total_amount = sum(get_price(item) if item.price is not None else 0.0 for item in items)
    if total_amount == 0:
        return None

    # Get task and project
    task = db.query(Task).filter(Task.id == purchase_order.task_id).first()
    if not task:
        return None
    try:
        current_budget = float(str(task.budget)) if task.budget is not None else 0.0
    except Exception:
        current_budget = 0.0
    new_budget = current_budget - total_amount

    # Generate transaction number
    transaction_number = generate_transaction_number(db)

    # Create transaction record
    transaction = models.Transaction(
        transaction_number=transaction_number,
        project_id=task.project_id,
        task_id=purchase_order.task_id,
        transaction_type='purchase_order',
        source_id=purchase_order.id,
        source_number=purchase_order.po_number,
        amount=Decimal(str(total_amount)),
        impact_type='-',
        description=f"Purchase Order: {purchase_order.description}",
        budget_before=Decimal(str(current_budget)),
        budget_after=Decimal(str(new_budget)),
        created_by=purchase_order.created_by,
        approved_by=purchase_order.approved_by,
        approved_date=purchase_order.approved_date or datetime.now()
    )
    db.add(transaction)
    # Update task budget
    setattr(task, 'budget', Decimal(str(new_budget)))
    db.commit()
    db.refresh(transaction)
    return transaction

def delete_purchase_order(db: Session, po_id: int):
    """Delete purchase order"""
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
    if db_po:
        db.delete(db_po)
        db.commit()
        return True
    return False

# ===============================
# PURCHASE ORDER ITEM CRUD
# ===============================

def create_purchase_order_item(db: Session, item: schemas.PurchaseOrderItemCreate):
    """Create a new purchase order item"""
    db_item = models.PurchaseOrderItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_purchase_order_item(db: Session, item_id: int):
    """Get purchase order item by ID"""
    return db.query(models.PurchaseOrderItem).filter(models.PurchaseOrderItem.id == item_id).first()

def get_purchase_order_items(db: Session, po_id: int):
    """Get all items for a purchase order"""
    return db.query(models.PurchaseOrderItem).filter(models.PurchaseOrderItem.purchase_order_id == po_id).all()

def update_purchase_order_item(db: Session, item_id: int, item_update: schemas.PurchaseOrderItemUpdate):
    """Update purchase order item"""
    db_item = db.query(models.PurchaseOrderItem).filter(models.PurchaseOrderItem.id == item_id).first()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_purchase_order_item(db: Session, item_id: int):
    """Delete purchase order item"""
    db_item = db.query(models.PurchaseOrderItem).filter(models.PurchaseOrderItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

# ===============================
# CHANGE ORDER CRUD
# ===============================

def generate_co_number(db: Session) -> str:
    """Generate a unique CO number in format CO-YYYY-XXX"""
    from datetime import datetime
    
    current_year = datetime.now().year
    
    # Get the highest CO number for current year
    latest_co = db.query(models.ChangeOrder)\
        .filter(models.ChangeOrder.co_number.like(f'CO-{current_year}-%'))\
        .order_by(models.ChangeOrder.co_number.desc())\
        .first()
    
    if latest_co:
        # Extract the number part and increment
        try:
            last_number = int(latest_co.co_number.split('-')[-1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    return f"CO-{current_year}-{next_number:03d}"

def create_change_order(db: Session, co: schemas.ChangeOrderCreate):
    """Create a new change order with auto-generated CO number"""
    # Generate unique CO number
    co_number = generate_co_number(db)
    
    # Create the change order data
    co_data = co.dict()
    co_data['co_number'] = co_number
    
    db_co = models.ChangeOrder(**co_data)
    db.add(db_co)
    db.commit()
    db.refresh(db_co)
    return db_co

def get_change_order(db: Session, co_id: int):
    """Get change order by ID"""
    return db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()

def get_change_orders(db: Session, skip: int = 0, limit: int = 100):
    """Get list of all change orders"""
    return db.query(models.ChangeOrder).offset(skip).limit(limit).all()

def get_change_orders_by_status(db: Session, status: str):
    """Get change orders by status"""
    return db.query(models.ChangeOrder).filter(models.ChangeOrder.status == status).all()

def get_change_orders_by_task(db: Session, task_id: int):
    """Get change orders by task"""
    return db.query(models.ChangeOrder).filter(models.ChangeOrder.task_id == task_id).all()

def get_change_orders_by_component(db: Session, component_id: int):
    """Get change orders by component"""
    # Join with Task table to filter by component_id
    from app.projects.models import Task
    return db.query(models.ChangeOrder)\
        .join(Task, models.ChangeOrder.task_id == Task.id)\
        .filter(Task.component_id == component_id)\
        .all()

def get_change_orders_by_creator(db: Session, creator_id: int):
    """Get change orders by creator (created_by)"""
    return db.query(models.ChangeOrder).filter(models.ChangeOrder.created_by == creator_id).all()

def get_change_orders_by_approver(db: Session, approver_id: int):
    """Get change orders by approver (approved_by)"""
    return db.query(models.ChangeOrder).filter(models.ChangeOrder.approved_by == approver_id).all()

def update_change_order(db: Session, co_id: int, co_update: schemas.ChangeOrderUpdate):
    """Update change order and create transaction if approved"""
    db_co = db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()
    if db_co:
        # Get the old status before update
        old_status = db_co.status
        
        update_data = co_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_co, key, value)
        db.commit()
        db.refresh(db_co)
        
        # If status changed to 'Approved', create transaction
        if old_status != 'Approved' and db_co.status == 'Approved':  # type: ignore
            create_change_order_transaction(db, db_co)
        
    return db_co

def create_change_order_transaction(db: Session, change_order):
    """Create transaction when change order is approved"""
    from datetime import datetime
    from decimal import Decimal
    from app.projects.models import Task
    
    # Calculate total impact from all CO items
    total_impact = calculate_co_total_impact(db, change_order.id)
    
    if total_impact == 0:
        return None  # No financial impact
    
    # Get current task budget
    task = db.query(Task).filter(Task.id == change_order.task_id).first()
    if not task:
        return None
    
    # Convert task budget to float for calculations
    current_budget = float(task.budget) if task.budget is not None else 0.0  # type: ignore
    impact_type = '+' if total_impact > 0 else '-'
    new_budget = current_budget + total_impact
    
    # Generate transaction number
    transaction_number = generate_transaction_number(db)
    
    # Create transaction record
    transaction = models.Transaction(
        transaction_number=transaction_number,
        project_id=task.project_id,
        task_id=change_order.task_id,
        transaction_type='change_order',
        source_id=change_order.id,
        source_number=change_order.co_number,
        amount=Decimal(str(abs(total_impact))),
        impact_type=impact_type,
        description=f"Change Order: {change_order.title}",
        budget_before=Decimal(str(current_budget)),
        budget_after=Decimal(str(new_budget)),
        created_by=change_order.created_by,
        approved_by=change_order.approved_by,
        approved_date=change_order.approved_date or datetime.now()
    )
    
    db.add(transaction)
    
    # Update task budget using proper assignment
    setattr(task, 'budget', Decimal(str(new_budget)))
    
    db.commit()
    db.refresh(transaction)
    
    return transaction

def calculate_co_total_impact(db: Session, change_order_id: int) -> float:
    """Calculate total financial impact of a change order"""
    items = db.query(models.ChangeOrderItem).filter(
        models.ChangeOrderItem.change_order_id == change_order_id
    ).all()
    
    total = 0.0
    for item in items:
        amount = float(item.amount) if item.amount is not None else 0.0  # type: ignore
        if item.impact_type == '+':  # type: ignore
            total += amount
        else:
            total -= amount
    
    return total

def generate_transaction_number(db: Session) -> str:
    """Generate unique transaction number"""
    from datetime import datetime
    
    current_year = datetime.now().year
    
    # Get the highest transaction number for current year
    latest_txn = db.query(models.Transaction)\
        .filter(models.Transaction.transaction_number.like(f'TXN-{current_year}-%'))\
        .order_by(models.Transaction.transaction_number.desc())\
        .first()
    
    if latest_txn:
        try:
            last_number = int(latest_txn.transaction_number.split('-')[-1])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    return f"TXN-{current_year}-{next_number:04d}"

def delete_change_order(db: Session, co_id: int):
    """Delete change order"""
    db_co = db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()
    if db_co:
        db.delete(db_co)
        db.commit()
        return True
    return False

# ===============================
# CHANGE ORDER ITEM CRUD
# ===============================

def create_change_order_item(db: Session, item: schemas.ChangeOrderItemCreate):
    """Create a new change order item"""
    db_item = models.ChangeOrderItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_change_order_item(db: Session, item_id: int):
    """Get change order item by ID"""
    return db.query(models.ChangeOrderItem).filter(models.ChangeOrderItem.id == item_id).first()

def get_change_order_items(db: Session, co_id: int):
    """Get all items for a change order"""
    return db.query(models.ChangeOrderItem).filter(models.ChangeOrderItem.change_order_id == co_id).all()

def update_change_order_item(db: Session, item_id: int, item_update: schemas.ChangeOrderItemUpdate):
    """Update change order item"""
    db_item = db.query(models.ChangeOrderItem).filter(models.ChangeOrderItem.id == item_id).first()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_change_order_item(db: Session, item_id: int):
    """Delete change order item"""
    db_item = db.query(models.ChangeOrderItem).filter(models.ChangeOrderItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

# ===============================
# TRANSACTION CRUD
# ===============================

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    """Create a new transaction"""
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: int):
    """Get transaction by ID"""
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    """Get list of all transactions"""
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def get_transactions_by_project(db: Session, project_id: int):
    """Get transactions by project"""
    return db.query(models.Transaction).filter(models.Transaction.project_id == project_id).all()

def get_transactions_by_task(db: Session, task_id: int):
    """Get transactions by task"""
    return db.query(models.Transaction).filter(models.Transaction.task_id == task_id).all()

def get_transactions_by_type(db: Session, transaction_type: str):
    """Get transactions by type"""
    return db.query(models.Transaction).filter(models.Transaction.transaction_type == transaction_type).all()
