from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from app.database import SessionLocal
from app.users import crud as user_crud

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Vendor endpoints
@router.post("/vendors/", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    return crud.create_vendor(db=db, vendor=vendor)

@router.get("/vendors/", response_model=List[schemas.Vendor])
def read_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vendors(db, skip=skip, limit=limit)

# Purchase Order endpoints
@router.post("/purchase-orders/", response_model=schemas.PurchaseOrder)
def create_purchase_order(po: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    return crud.create_purchase_order(db=db, po=po)

@router.get("/purchase-orders/", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_purchase_orders(db, skip=skip, limit=limit)

@router.post("/purchase-orders/{po_id}/approve", response_model=schemas.PurchaseOrder)
def approve_purchase_order(po_id: int, approver_id: int, db: Session = Depends(get_db)):
    db_po = crud.approve_purchase_order(db, po_id=po_id, approver_id=approver_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return db_po


# Change Order endpoints
@router.post("/change-orders/", response_model=schemas.ChangeOrder)
def create_change_order(co: schemas.ChangeOrderCreate, creator_id: int, db: Session = Depends(get_db)):
    """Project Manager creates a change order"""
    # Verify creator is a project manager
    creator = user_crud.get_user(db, user_id=creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")
    if str(creator.role) != 'project_manager':
        raise HTTPException(status_code=403, detail="Only project managers can create change orders")
    
    return crud.create_change_order(db=db, co=co)

@router.get("/change-orders/pending/", response_model=List[schemas.ChangeOrder])
def get_pending_change_orders(accountant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Accountant gets all pending change orders for approval"""
    accountant = user_crud.get_user(db, user_id=accountant_id)
    if accountant is None:
        raise HTTPException(status_code=404, detail="Accountant not found")
    if str(accountant.role) != 'accountant':
        raise HTTPException(status_code=403, detail="Only accountants can view pending change orders")
    
    return crud.get_pending_change_orders(db, skip=skip, limit=limit)

@router.post("/change-orders/{co_id}/approve", response_model=schemas.ChangeOrder)
def approve_change_order(co_id: int, approver_id: int, approval_notes: str = "", db: Session = Depends(get_db)):
    """Accountant approves a change order and creates transaction if needed"""
    # Verify approver is an accountant
    approver = user_crud.get_user(db, user_id=approver_id)
    if approver is None:
        raise HTTPException(status_code=404, detail="Approver not found")
    if str(approver.role) != 'accountant':
        raise HTTPException(status_code=403, detail="Only accountants can approve change orders")
    
    db_co = crud.approve_change_order_with_transaction(db, co_id=co_id, approver_id=approver_id, approval_notes=approval_notes)
    if db_co is None:
        raise HTTPException(status_code=404, detail="Change Order not found")
    return db_co

@router.post("/change-orders/{co_id}/reject", response_model=schemas.ChangeOrder)
def reject_change_order(co_id: int, approver_id: int, rejection_reason: str, db: Session = Depends(get_db)):
    """Accountant rejects a change order"""
    # Verify approver is an accountant
    approver = user_crud.get_user(db, user_id=approver_id)
    if approver is None:
        raise HTTPException(status_code=404, detail="Approver not found")
    if str(approver.role) != 'accountant':
        raise HTTPException(status_code=403, detail="Only accountants can reject change orders")
    
    db_co = crud.reject_change_order(db, co_id=co_id, approver_id=approver_id, rejection_reason=rejection_reason)
    if db_co is None:
        raise HTTPException(status_code=404, detail="Change Order not found")
    return db_co


# Contract endpoints
@router.post("/contracts/", response_model=schemas.Contract)
def create_contract(contract: schemas.ContractCreate, db: Session = Depends(get_db)):
    return crud.create_contract(db=db, contract=contract)

# ClientInvoice Endpoints
@router.post("/client-invoices/", response_model=schemas.ClientInvoice)
def create_client_invoice(invoice: schemas.ClientInvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_client_invoice(db=db, invoice=invoice)

# VendorInvoice Endpoints
@router.post("/vendor-invoices/", response_model=schemas.VendorInvoice)
def create_vendor_invoice(invoice: schemas.VendorInvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_vendor_invoice(db=db, invoice=invoice)

# Transaction endpoints
@router.post("/transactions/", response_model=dict)
def create_transaction(transaction_data: dict, creator_id: int, db: Session = Depends(get_db)):
    """Create a new transaction"""
    # Verify creator permissions (project managers and accountants can create transactions)
    creator = user_crud.get_user(db, user_id=creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")
    if str(creator.role) not in ['project_manager', 'accountant']:
        raise HTTPException(status_code=403, detail="Only project managers and accountants can create transactions")
    
    transaction_data['created_by'] = creator_id
    return crud.create_transaction(db=db, transaction=transaction_data)

@router.get("/projects/{project_id}/transactions/", response_model=List[dict])
def get_project_transactions(project_id: int, user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all transactions for a specific project"""
    # Verify user has access to project transactions
    user = user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if str(user.role) not in ['project_manager', 'accountant', 'business_admin']:
        raise HTTPException(status_code=403, detail="Insufficient permissions to view project transactions")
    
    transactions = crud.get_project_transactions(db, project_id=project_id, skip=skip, limit=limit)
    return [
        {
            "id": getattr(t, 'id', None),
            "expense_name": getattr(t, 'expense_name', ''),
            "description": getattr(t, 'description', ''),
            "amount": float(getattr(t, 'amount', 0)),
            "transaction_date": str(getattr(t, 'transaction_date', '')),
            "transaction_type": getattr(t, 'transaction_type', ''),
            "status": getattr(t, 'status', ''),
            "budget_line_item": getattr(t, 'budget_line_item', '')
        } for t in transactions
    ]



