from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, date

# Vendor CRUD
def create_vendor(db: Session, vendor: schemas.VendorCreate):
    db_vendor = models.Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vendor).offset(skip).limit(limit).all()

# Purchase Order CRUD
def create_purchase_order(db: Session, po: schemas.PurchaseOrderCreate):
    db_po = models.PurchaseOrder(**po.dict())
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    return db_po

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PurchaseOrder).offset(skip).limit(limit).all()

def approve_purchase_order(db: Session, po_id: int, approver_id: int):
    db_po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
    if db_po:
        # Use SQLAlchemy update method instead of direct assignment
        db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).update({
            "status": "Approved",
            "approved_by_id": approver_id
        })
        db.commit()
        db.refresh(db_po)
    return db_po


# Change Order CRUD
def create_change_order(db: Session, co: schemas.ChangeOrderCreate):
    db_co = models.ChangeOrder(**co.dict())
    db.add(db_co)
    db.commit()
    db.refresh(db_co)
    return db_co

def approve_change_order(db: Session, co_id: int, approver_id: int):
    db_co = db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()
    if db_co:
        # Use SQLAlchemy update method instead of direct assignment
        db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).update({
            "status": "Approved",
            "approved_by_id": approver_id
        })
        db.commit()
        db.refresh(db_co)
        
        # Note: Project budget updates are now handled in the enhanced function
        # This function is kept for backward compatibility

    return db_co


# Contract CRUD
def create_contract(db: Session, contract: schemas.ContractCreate):
    db_contract = models.Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

# ClientInvoice CRUD
def create_client_invoice(db: Session, invoice: schemas.ClientInvoiceCreate):
    db_invoice = models.ClientInvoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

# VendorInvoice CRUD
def create_vendor_invoice(db: Session, invoice: schemas.VendorInvoiceCreate):
    db_invoice = models.VendorInvoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

# Enhanced Change Order CRUD Functions

def get_pending_change_orders(db: Session, skip: int = 0, limit: int = 100):
    """Get all pending change orders for accountant approval"""
    return db.query(models.ChangeOrder).filter(
        models.ChangeOrder.status == 'Pending Approval'
    ).offset(skip).limit(limit).all()

def approve_change_order_with_transaction(db: Session, co_id: int, approver_id: int, approval_notes: str = ""):
    """Approve change order and create transaction if extra funds needed"""
    db_co = db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()
    if not db_co:
        return None
    
    # Update change order status
    db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).update({
        "status": "Approved",
        "approved_by_id": approver_id
    })
    
    # If change order requires extra funds (positive financial impact), create a transaction
    if getattr(db_co, 'financial_impact', 0) > 0:
        transaction_data = {
            "transaction_type": "outgoing",
            "expense_name": f"Change Order #{co_id}: {str(getattr(db_co, 'description', 'N/A'))[:50]}...",
            "description": f"Additional funds for change order: {getattr(db_co, 'description', 'N/A')}",
            "amount": getattr(db_co, 'financial_impact', 0),
            "transaction_date": date.today(),
            "project_id": getattr(db_co, 'project_id', None),
            "is_project_specific": True,
            "status": "approved",
            "approved_by": approver_id,
            "approved_date": datetime.now(),
            "approval_notes": approval_notes,
            "budget_line_item": "Change Orders",
            "is_budgeted": False,
            "variance_reason": f"Approved change order #{co_id}"
        }
        
        db_transaction = models.Transaction(**transaction_data)
        db.add(db_transaction)
    
    db.commit()
    db.refresh(db_co)
    return db_co

def reject_change_order(db: Session, co_id: int, approver_id: int, rejection_reason: str):
    """Reject a change order with reason"""
    db_co = db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).first()
    if not db_co:
        return None
    
    # Update change order status
    db.query(models.ChangeOrder).filter(models.ChangeOrder.id == co_id).update({
        "status": "Rejected",
        "approved_by_id": approver_id
    })
    
    # Note: In a full implementation, you might want to add rejection_reason 
    # and rejection_date fields to the ChangeOrder model
    
    db.commit()
    db.refresh(db_co)
    return db_co

# Transaction CRUD Functions

def create_transaction(db: Session, transaction: dict):
    """Create a new transaction"""
    db_transaction = models.Transaction(**transaction)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_project_transactions(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    """Get all transactions for a specific project"""
    return db.query(models.Transaction).filter(
        models.Transaction.project_id == project_id
    ).offset(skip).limit(limit).all()



