# Endpoint: Get all transactions by component ID
from fastapi import APIRouter, Depends
router = APIRouter()
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .dependencies import get_db

@router.get("/transactions/by-component/{component_id}", response_model=List[schemas.Transaction])
def read_transactions_by_component(component_id: int, db: Session = Depends(get_db)):
    """Get transactions by component"""
    transactions = crud.get_transactions_by_component(db, component_id=component_id)
    return transactions
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from app.projects import crud as project_crud, models as project_models
from app.users import models as user_models
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

@router.get("/purchase-orders/by-component/{component_id}", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders_by_component(component_id: int, db: Session = Depends(get_db)):
    """Get purchase orders by component"""
    pos = crud.get_purchase_orders_by_component(db, component_id=component_id)
    return pos

@router.get("/purchase-orders/by-creator/{creator_id}", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders_by_creator(creator_id: int, db: Session = Depends(get_db)):
    """Get purchase orders by creator (created_by)"""
    pos = crud.get_purchase_orders_by_creator(db, creator_id=creator_id)
    return pos

@router.get("/purchase-orders/by-approver/{approver_id}", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders_by_approver(approver_id: int, db: Session = Depends(get_db)):
    """Get purchase orders by approver (approved_by)"""
    pos = crud.get_purchase_orders_by_approver(db, approver_id=approver_id)
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


@router.get("/change-orders/", response_model=List[schemas.ChangeOrderExtended])
def read_change_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all change orders with project/component/PM info"""
    cos = crud.get_change_orders(db, skip=skip, limit=limit)
    results = []
    for co in cos:
        # Get related task
        task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
        project_name = None
        component_name = None
        pm_name = None
        if task:
            # Project
            project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
            if project:
                project_name = getattr(project, "name", None)
                pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
                if pm:
                    pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
            # Component
            if getattr(task, "component_id", None):
                component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
                if component:
                    component_name = getattr(component, "name", None)
        # Build extended response
        ext = schemas.ChangeOrderExtended(
            id=co.__dict__["id"],
            co_number=co.__dict__["co_number"],
            task_id=co.__dict__["task_id"],
            title=co.__dict__["title"],
            description=co.__dict__["description"],
            reason=co.__dict__["reason"],
            status=co.__dict__["status"],
            notes=co.__dict__["notes"],
            created_by=co.__dict__["created_by"],
            approved_by=co.__dict__["approved_by"],
            approved_date=co.__dict__["approved_date"],
            created_at=co.__dict__["created_at"],
            updated_at=co.__dict__["updated_at"],
            project_name=project_name,
            component_name=component_name,
            pm_name=pm_name
        )
        results.append(ext)
    return results


@router.get("/change-orders/{co_id}", response_model=schemas.ChangeOrderExtended)
def read_change_order(co_id: int, db: Session = Depends(get_db)):
    """Get change order by ID with project/component/PM info"""
    co = crud.get_change_order(db, co_id=co_id)
    if co is None:
        print(f"[DEBUG] ChangeOrder with id={co_id} not found.")
        raise HTTPException(status_code=404, detail="Change order not found")
    # Get related task
    task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
    print(f"[DEBUG] Lookup Task for ChangeOrder id={co_id}, task_id={co.task_id}: {task}")
    project_name = None
    component_name = None
    pm_name = None
    if task:
        project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
        print(f"[DEBUG] Lookup Project for Task id={task.id}, project_id={getattr(task, 'project_id', None)}: {project}")
        if project:
            project_name = getattr(project, "name", None)
            pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
            print(f"[DEBUG] Lookup PM for Project id={project.id}, pm_id={getattr(project, 'project_manager_id', None)}: {pm}")
            if pm:
                pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
        if getattr(task, "component_id", None):
            component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
            print(f"[DEBUG] Lookup Component for Task id={task.id}, component_id={getattr(task, 'component_id', None)}: {component}")
            if component:
                component_name = getattr(component, "name", None)
    return schemas.ChangeOrderExtended(
        id=co.__dict__["id"],
        co_number=co.__dict__["co_number"],
        task_id=co.__dict__["task_id"],
        title=co.__dict__["title"],
        description=co.__dict__["description"],
        reason=co.__dict__["reason"],
        status=co.__dict__["status"],
        notes=co.__dict__["notes"],
        created_by=co.__dict__["created_by"],
        approved_by=co.__dict__["approved_by"],
        approved_date=co.__dict__["approved_date"],
        created_at=co.__dict__["created_at"],
        updated_at=co.__dict__["updated_at"],
        project_name=project_name,
        component_name=component_name,
        pm_name=pm_name
    )

@router.get("/change-orders/by-status/{status}", response_model=List[schemas.ChangeOrderExtended])
def read_change_orders_by_status(status: str, db: Session = Depends(get_db)):
    """Get change orders by status"""
    cos = crud.get_change_orders_by_status(db, status=status)
    results = []
    for co in cos:
        task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
        project_name = None
        component_name = None
        pm_name = None
        if task:
            project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
            if project:
                project_name = getattr(project, "name", None)
                pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
                if pm:
                    pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
            if getattr(task, "component_id", None):
                component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
                if component:
                    component_name = getattr(component, "name", None)
        ext = schemas.ChangeOrderExtended(
            id=co.__dict__["id"],
            co_number=co.__dict__["co_number"],
            task_id=co.__dict__["task_id"],
            title=co.__dict__["title"],
            description=co.__dict__["description"],
            reason=co.__dict__["reason"],
            status=co.__dict__["status"],
            notes=co.__dict__["notes"],
            created_by=co.__dict__["created_by"],
            approved_by=co.__dict__["approved_by"],
            approved_date=co.__dict__["approved_date"],
            created_at=co.__dict__["created_at"],
            updated_at=co.__dict__["updated_at"],
            project_name=project_name,
            component_name=component_name,
            pm_name=pm_name
        )
        results.append(ext)
    return results

@router.get("/change-orders/by-task/{task_id}", response_model=List[schemas.ChangeOrderExtended])
def read_change_orders_by_task(task_id: int, db: Session = Depends(get_db)):
    """Get change orders by task"""
    cos = crud.get_change_orders_by_task(db, task_id=task_id)
    results = []
    for co in cos:
        task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
        project_name = None
        component_name = None
        pm_name = None
        if task:
            project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
            if project:
                project_name = getattr(project, "name", None)
                pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
                if pm:
                    pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
            if getattr(task, "component_id", None):
                component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
                if component:
                    component_name = getattr(component, "name", None)
        ext = schemas.ChangeOrderExtended(
            id=co.__dict__["id"],
            co_number=co.__dict__["co_number"],
            task_id=co.__dict__["task_id"],
            title=co.__dict__["title"],
            description=co.__dict__["description"],
            reason=co.__dict__["reason"],
            status=co.__dict__["status"],
            notes=co.__dict__["notes"],
            created_by=co.__dict__["created_by"],
            approved_by=co.__dict__["approved_by"],
            approved_date=co.__dict__["approved_date"],
            created_at=co.__dict__["created_at"],
            updated_at=co.__dict__["updated_at"],
            project_name=project_name,
            component_name=component_name,
            pm_name=pm_name
        )
        results.append(ext)
    return results

@router.get("/change-orders/by-component/{component_id}", response_model=List[schemas.ChangeOrderExtended])
def read_change_orders_by_component(component_id: int, db: Session = Depends(get_db)):
    """Get change orders by component"""
    cos = crud.get_change_orders_by_component(db, component_id=component_id)
    results = []
    for co in cos:
        task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
        project_name = None
        component_name = None
        pm_name = None
        if task:
            project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
            if project:
                project_name = getattr(project, "name", None)
                pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
                if pm:
                    pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
            if getattr(task, "component_id", None):
                component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
                if component:
                    component_name = getattr(component, "name", None)
        ext = schemas.ChangeOrderExtended(
            id=co.__dict__["id"],
            co_number=co.__dict__["co_number"],
            task_id=co.__dict__["task_id"],
            title=co.__dict__["title"],
            description=co.__dict__["description"],
            reason=co.__dict__["reason"],
            status=co.__dict__["status"],
            notes=co.__dict__["notes"],
            created_by=co.__dict__["created_by"],
            approved_by=co.__dict__["approved_by"],
            approved_date=co.__dict__["approved_date"],
            created_at=co.__dict__["created_at"],
            updated_at=co.__dict__["updated_at"],
            project_name=project_name,
            component_name=component_name,
            pm_name=pm_name
        )
        results.append(ext)
    return results

@router.get("/change-orders/by-creator/{creator_id}", response_model=List[schemas.ChangeOrderExtended])
def read_change_orders_by_creator(creator_id: int, db: Session = Depends(get_db)):
    """Get change orders by creator (created_by)"""
    cos = crud.get_change_orders_by_creator(db, creator_id=creator_id)
    results = []
    for co in cos:
        task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
        project_name = None
        component_name = None
        pm_name = None
        if task:
            project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
            if project:
                project_name = getattr(project, "name", None)
                pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
                if pm:
                    pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
            if getattr(task, "component_id", None):
                component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
                if component:
                    component_name = getattr(component, "name", None)
        ext = schemas.ChangeOrderExtended(
            id=co.__dict__["id"],
            co_number=co.__dict__["co_number"],
            task_id=co.__dict__["task_id"],
            title=co.__dict__["title"],
            description=co.__dict__["description"],
            reason=co.__dict__["reason"],
            status=co.__dict__["status"],
            notes=co.__dict__["notes"],
            created_by=co.__dict__["created_by"],
            approved_by=co.__dict__["approved_by"],
            approved_date=co.__dict__["approved_date"],
            created_at=co.__dict__["created_at"],
            updated_at=co.__dict__["updated_at"],
            project_name=project_name,
            component_name=component_name,
            pm_name=pm_name
        )
        results.append(ext)
    return results

@router.get("/change-orders/by-approver/{approver_id}", response_model=List[schemas.ChangeOrderExtended])
def read_change_orders_by_approver(approver_id: int, db: Session = Depends(get_db)):
    """Get change orders by approver (approved_by)"""
    cos = crud.get_change_orders_by_approver(db, approver_id=approver_id)
    results = []
    for co in cos:
        task = db.query(project_models.Task).filter(project_models.Task.id == co.task_id).first()
        project_name = None
        component_name = None
        pm_name = None
        if task:
            project = db.query(project_models.Project).filter(project_models.Project.id == task.project_id).first()
            if project:
                project_name = getattr(project, "name", None)
                pm = db.query(user_models.User).filter(user_models.User.id == project.project_manager_id).first()
                if pm:
                    pm_name = f"{getattr(pm, 'first_name', '')} {getattr(pm, 'last_name', '')}".strip()
            if getattr(task, "component_id", None):
                component = db.query(project_models.ProjectComponent).filter(project_models.ProjectComponent.id == task.component_id).first()
                if component:
                    component_name = getattr(component, "name", None)
        ext = schemas.ChangeOrderExtended(
            id=co.__dict__["id"],
            co_number=co.__dict__["co_number"],
            task_id=co.__dict__["task_id"],
            title=co.__dict__["title"],
            description=co.__dict__["description"],
            reason=co.__dict__["reason"],
            status=co.__dict__["status"],
            notes=co.__dict__["notes"],
            created_by=co.__dict__["created_by"],
            approved_by=co.__dict__["approved_by"],
            approved_date=co.__dict__["approved_date"],
            created_at=co.__dict__["created_at"],
            updated_at=co.__dict__["updated_at"],
            project_name=project_name,
            component_name=component_name,
            pm_name=pm_name
        )
        results.append(ext)
    return results

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

@router.get("/change-orders/{co_id}/total-impact", response_model=float)
def get_change_order_total_impact(co_id: int, db: Session = Depends(get_db)):
    """Get the sum (total impact) of all change order line items for a given change order ID"""
    # Optionally, check if the change order exists
    co = crud.get_change_order(db, co_id=co_id)
    if co is None:
        raise HTTPException(status_code=404, detail="Change order not found")
    total_impact = crud.calculate_co_total_impact(db, co_id)
    return total_impact
