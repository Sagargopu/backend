from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from app.database import get_db

router = APIRouter()

# ===============================
# VENDOR ENDPOINTS
# ===============================

@router.post("/vendors/", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    """Create a new vendor"""
    return crud.create_vendor(db=db, vendor=vendor)

@router.get("/vendors/", response_model=List[schemas.Vendor])
def read_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all vendors"""
    vendors = crud.get_vendors(db, skip=skip, limit=limit)
    return vendors

@router.get("/vendors/{vendor_id}", response_model=schemas.Vendor)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Get vendor by ID"""
    vendor = crud.get_vendor(db, vendor_id=vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@router.get("/vendors/active", response_model=List[schemas.Vendor])
def read_active_vendors(db: Session = Depends(get_db)):
    """Get all active vendors"""
    vendors = crud.get_active_vendors(db)
    return vendors

@router.put("/vendors/{vendor_id}", response_model=schemas.Vendor)
def update_vendor(vendor_id: int, vendor: schemas.VendorUpdate, db: Session = Depends(get_db)):
    """Update vendor by ID"""
    db_vendor = crud.update_vendor(db, vendor_id=vendor_id, vendor_update=vendor)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Delete vendor by ID"""
    deleted = crud.delete_vendor(db, vendor_id=vendor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"detail": "Vendor deleted successfully"}

# ===============================
# PURCHASE ORDER ENDPOINTS
# ===============================

@router.post("/purchase-orders/", response_model=schemas.PurchaseOrder)
def create_purchase_order(po: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    """Create a new purchase order"""
    return crud.create_purchase_order(db=db, po=po)

@router.get("/purchase-orders/", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all purchase orders"""
    pos = crud.get_purchase_orders(db, skip=skip, limit=limit)
    return pos

@router.get("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrder)
def read_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Get purchase order by ID"""
    po = crud.get_purchase_order(db, po_id=po_id)
    if po is None:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po

@router.get("/purchase-orders/by-status/{status}", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders_by_status(status: str, db: Session = Depends(get_db)):
    """Get purchase orders by status"""
    pos = crud.get_purchase_orders_by_status(db, status=status)
    return pos

@router.get("/purchase-orders/by-task/{task_id}", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders_by_task(task_id: int, db: Session = Depends(get_db)):
    """Get purchase orders by task"""
    pos = crud.get_purchase_orders_by_task(db, task_id=task_id)
    return pos

@router.put("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrder)
def update_purchase_order(po_id: int, po: schemas.PurchaseOrderUpdate, db: Session = Depends(get_db)):
    """Update purchase order by ID"""
    db_po = crud.update_purchase_order(db, po_id=po_id, po_update=po)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return db_po

@router.delete("/purchase-orders/{po_id}")
def delete_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Delete purchase order by ID"""
    deleted = crud.delete_purchase_order(db, po_id=po_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return {"detail": "Purchase order deleted successfully"}

# ===============================
# PURCHASE ORDER ITEM ENDPOINTS
# ===============================

@router.post("/purchase-order-items/", response_model=schemas.PurchaseOrderItem)
def create_purchase_order_item(item: schemas.PurchaseOrderItemCreate, db: Session = Depends(get_db)):
    """Create a new purchase order item"""
    return crud.create_purchase_order_item(db=db, item=item)

@router.get("/purchase-order-items/{item_id}", response_model=schemas.PurchaseOrderItem)
def read_purchase_order_item(item_id: int, db: Session = Depends(get_db)):
    """Get purchase order item by ID"""
    item = crud.get_purchase_order_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Purchase order item not found")
    return item

@router.get("/purchase-orders/{po_id}/items", response_model=List[schemas.PurchaseOrderItem])
def read_purchase_order_items(po_id: int, db: Session = Depends(get_db)):
    """Get all items for a purchase order"""
    items = crud.get_purchase_order_items(db, po_id=po_id)
    return items

@router.put("/purchase-order-items/{item_id}", response_model=schemas.PurchaseOrderItem)
def update_purchase_order_item(item_id: int, item: schemas.PurchaseOrderItemUpdate, db: Session = Depends(get_db)):
    """Update purchase order item by ID"""
    db_item = crud.update_purchase_order_item(db, item_id=item_id, item_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Purchase order item not found")
    return db_item

@router.delete("/purchase-order-items/{item_id}")
def delete_purchase_order_item(item_id: int, db: Session = Depends(get_db)):
    """Delete purchase order item by ID"""
    deleted = crud.delete_purchase_order_item(db, item_id=item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Purchase order item not found")
    return {"detail": "Purchase order item deleted successfully"}

# ===============================
# CHANGE ORDER ENDPOINTS
# ===============================

@router.post("/change-orders/", response_model=schemas.ChangeOrder)
def create_change_order(co: schemas.ChangeOrderCreate, db: Session = Depends(get_db)):
    """Create a new change order"""
    return crud.create_change_order(db=db, co=co)

@router.get("/change-orders/", response_model=List[schemas.ChangeOrder])
def read_change_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all change orders"""
    cos = crud.get_change_orders(db, skip=skip, limit=limit)
    return cos

@router.get("/change-orders/{co_id}", response_model=schemas.ChangeOrder)
def read_change_order(co_id: int, db: Session = Depends(get_db)):
    """Get change order by ID"""
    co = crud.get_change_order(db, co_id=co_id)
    if co is None:
        raise HTTPException(status_code=404, detail="Change order not found")
    return co

@router.get("/change-orders/by-status/{status}", response_model=List[schemas.ChangeOrder])
def read_change_orders_by_status(status: str, db: Session = Depends(get_db)):
    """Get change orders by status"""
    cos = crud.get_change_orders_by_status(db, status=status)
    return cos

@router.get("/change-orders/by-task/{task_id}", response_model=List[schemas.ChangeOrder])
def read_change_orders_by_task(task_id: int, db: Session = Depends(get_db)):
    """Get change orders by task"""
    cos = crud.get_change_orders_by_task(db, task_id=task_id)
    return cos

@router.put("/change-orders/{co_id}", response_model=schemas.ChangeOrder)
def update_change_order(co_id: int, co: schemas.ChangeOrderUpdate, db: Session = Depends(get_db)):
    """Update change order by ID"""
    db_co = crud.update_change_order(db, co_id=co_id, co_update=co)
    if db_co is None:
        raise HTTPException(status_code=404, detail="Change order not found")
    return db_co

@router.delete("/change-orders/{co_id}")
def delete_change_order(co_id: int, db: Session = Depends(get_db)):
    """Delete change order by ID"""
    deleted = crud.delete_change_order(db, co_id=co_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Change order not found")
    return {"detail": "Change order deleted successfully"}

# ===============================
# CHANGE ORDER ITEM ENDPOINTS
# ===============================

@router.post("/change-order-items/", response_model=schemas.ChangeOrderItem)
def create_change_order_item(item: schemas.ChangeOrderItemCreate, db: Session = Depends(get_db)):
    """Create a new change order item"""
    return crud.create_change_order_item(db=db, item=item)

@router.get("/change-order-items/{item_id}", response_model=schemas.ChangeOrderItem)
def read_change_order_item(item_id: int, db: Session = Depends(get_db)):
    """Get change order item by ID"""
    item = crud.get_change_order_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Change order item not found")
    return item

@router.get("/change-orders/{co_id}/items", response_model=List[schemas.ChangeOrderItem])
def read_change_order_items(co_id: int, db: Session = Depends(get_db)):
    """Get all items for a change order"""
    items = crud.get_change_order_items(db, co_id=co_id)
    return items

@router.put("/change-order-items/{item_id}", response_model=schemas.ChangeOrderItem)
def update_change_order_item(item_id: int, item: schemas.ChangeOrderItemUpdate, db: Session = Depends(get_db)):
    """Update change order item by ID"""
    db_item = crud.update_change_order_item(db, item_id=item_id, item_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Change order item not found")
    return db_item

@router.delete("/change-order-items/{item_id}")
def delete_change_order_item(item_id: int, db: Session = Depends(get_db)):
    """Delete change order item by ID"""
    deleted = crud.delete_change_order_item(db, item_id=item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Change order item not found")
    return {"detail": "Change order item deleted successfully"}

# ===============================
# TRANSACTION ENDPOINTS
# ===============================

@router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction"""
    return crud.create_transaction(db=db, transaction=transaction)

@router.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all transactions"""
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@router.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get transaction by ID"""
    transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/transactions/by-project/{project_id}", response_model=List[schemas.Transaction])
def read_transactions_by_project(project_id: int, db: Session = Depends(get_db)):
    """Get transactions by project"""
    transactions = crud.get_transactions_by_project(db, project_id=project_id)
    return transactions

@router.get("/transactions/by-task/{task_id}", response_model=List[schemas.Transaction])
def read_transactions_by_task(task_id: int, db: Session = Depends(get_db)):
    """Get transactions by task"""
    transactions = crud.get_transactions_by_task(db, task_id=task_id)
    return transactions

@router.get("/transactions/by-type/{transaction_type}", response_model=List[schemas.Transaction])
def read_transactions_by_type(transaction_type: str, db: Session = Depends(get_db)):
    """Get transactions by type"""
    transactions = crud.get_transactions_by_type(db, transaction_type=transaction_type)
    return transactions
