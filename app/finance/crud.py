from sqlalchemy.orm import Session
from . import models, schemas

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
        db_po.status = "Approved"
        db_po.approved_by_id = approver_id
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
        db_co.status = "Approved"
        db_co.approved_by_id = approver_id
        db.commit()
        db.refresh(db_co)
        
        # Update project budget (simplified for now)
        db_project_component = db.query(models.ProjectComponent).filter(models.ProjectComponent.id == db_co.project_id).first()
        if db_project_component:
            # This is a simplified budget update. In a real app, budget would be a separate entity.
            # For now, we'll assume a 'budget' field in ProjectComponent's details JSON.
            if db_project_component.details is None:
                db_project_component.details = {}
            current_budget = db_project_component.details.get("budget", 0.0)
            db_project_component.details["budget"] = current_budget + db_co.financial_impact
            db.commit()
            db.refresh(db_project_component)

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



