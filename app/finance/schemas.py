# Basic ChangeOrder schema for endpoints that do not require extended fields

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChangeOrder(BaseModel):
    id: int
    co_number: str
    task_id: int
    title: str
    description: str
    reason: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_by: int
    approved_by: Optional[int] = None
    approved_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

# ===============================
# VENDOR SCHEMAS
# ===============================

class VendorBase(BaseModel):
    name: str
    representative_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    business_type: Optional[str] = None  # 'Material Supplier', 'Subcontractor', 'Equipment Rental', 'Service Provider'
    is_active: bool = True

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: Optional[str] = None
    representative_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    business_type: Optional[str] = None
    is_active: Optional[bool] = None

class Vendor(VendorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ===============================
# PURCHASE ORDER SCHEMAS
# ===============================

class PurchaseOrderBase(BaseModel):
    task_id: int
    vendor_id: int
    description: str
    delivery_date: Optional[date] = None
    status: str = 'Draft'
    notes: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    created_by: int

class PurchaseOrderUpdate(BaseModel):
    po_number: Optional[str] = None
    task_id: Optional[int] = None
    vendor_id: Optional[int] = None
    description: Optional[str] = None
    delivery_date: Optional[date] = None
    status: Optional[str] = None
    approved_by: Optional[int] = None
    approved_date: Optional[datetime] = None
    notes: Optional[str] = None

class PurchaseOrder(PurchaseOrderBase):
    id: int
    po_number: str
    created_by: int
    approved_by: Optional[int] = None
    approved_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ===============================
# PURCHASE ORDER ITEM SCHEMAS
# ===============================

class PurchaseOrderItemBase(BaseModel):
    item_name: str
    description: Optional[str] = None
    category: Optional[str] = None  # 'Material', 'Labor', 'Equipment', 'Service'
    price: Decimal

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    purchase_order_id: int

class PurchaseOrderItemUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    purchase_order_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ===============================
# CHANGE ORDER SCHEMAS
# ===============================

class ChangeOrderBase(BaseModel):
    task_id: int
    title: str
    description: str
    reason: Optional[str] = None  # 'Client Request', 'Design Change', 'Site Condition', 'Code Requirement'
    status: str = 'Draft'
    notes: Optional[str] = None

class ChangeOrderCreate(ChangeOrderBase):
    created_by: int

class ChangeOrderUpdate(BaseModel):
    co_number: Optional[str] = None
    task_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    approved_by: Optional[int] = None
    approved_date: Optional[datetime] = None
    notes: Optional[str] = None


# Extended ChangeOrder response with project/component/PM info
class ChangeOrderExtended(BaseModel):
    id: int
    co_number: str
    task_id: int
    title: str
    description: str
    reason: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_by: int
    approved_by: Optional[int] = None
    approved_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    # Extra fields
    project_name: Optional[str] = None
    component_name: Optional[str] = None
    pm_name: Optional[str] = None

    class Config:
        orm_mode = True

# ===============================
# CHANGE ORDER ITEM SCHEMAS
# ===============================

class ChangeOrderItemBase(BaseModel):
    item_name: str
    description: Optional[str] = None
    change_type: Optional[str] = None  # 'Addition', 'Deletion', 'Modification'
    impact_type: str  # '+' for cost increase, '-' for cost decrease
    amount: Decimal

class ChangeOrderItemCreate(ChangeOrderItemBase):
    change_order_id: int

class ChangeOrderItemUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    change_type: Optional[str] = None
    impact_type: Optional[str] = None
    amount: Optional[Decimal] = None

class ChangeOrderItem(ChangeOrderItemBase):
    id: int
    change_order_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ===============================
# TRANSACTION SCHEMAS
# ===============================

class TransactionBase(BaseModel):
    transaction_number: str
    project_id: int
    task_id: int
    transaction_type: str  # 'purchase_order', 'change_order'
    source_id: int
    source_number: str
    amount: Decimal
    impact_type: str  # '+' for budget increase, '-' for budget decrease
    description: str
    budget_before: Decimal
    budget_after: Decimal

class TransactionCreate(TransactionBase):
    approved_by: int
    approved_date: datetime

class Transaction(TransactionBase):
    id: int
    approved_by: int
    approved_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ===============================
# COMBINED SCHEMAS
# ===============================

class PurchaseOrderWithItems(PurchaseOrder):
    items: List[PurchaseOrderItem] = []

class ChangeOrderWithItems(ChangeOrder):
    items: List[ChangeOrderItem] = []



