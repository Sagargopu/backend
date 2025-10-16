from sqlalchemy.orm import Session
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

def create_purchase_order(db: Session, po: schemas.PurchaseOrderCreate):
    """Create a new purchase order"""
    db_po = models.PurchaseOrder(**po.dict())
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

def update_purchase_order(db: Session, po_id: int, po_update: schemas.PurchaseOrderUpdate):
    """Update purchase order"""
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
    if db_po:
        update_data = po_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_po, key, value)
        db.commit()
        db.refresh(db_po)
    return db_po

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

def create_change_order(db: Session, co: schemas.ChangeOrderCreate):
    """Create a new change order"""
    db_co = models.ChangeOrder(**co.dict())
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

def update_change_order(db: Session, co_id: int, co_update: schemas.ChangeOrderUpdate):
    """Update change order"""
    db_co = db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()
    if db_co:
        update_data = co_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_co, key, value)
        db.commit()
        db.refresh(db_co)
    return db_co

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
