from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from app.database import SessionLocal

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
def create_change_order(co: schemas.ChangeOrderCreate, db: Session = Depends(get_db)):
    return crud.create_change_order(db=db, co=co)

@router.post("/change-orders/{co_id}/approve", response_model=schemas.ChangeOrder)
def approve_change_order(co_id: int, approver_id: int, db: Session = Depends(get_db)):
    db_co = crud.approve_change_order(db, co_id=co_id, approver_id=approver_id)
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



