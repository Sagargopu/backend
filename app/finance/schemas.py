from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class VendorBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int

    class Config:
        orm_mode = True

# Schemas for Purchase Order
class PurchaseOrderBase(BaseModel):
    description: str
    vendor_id: int
    project_id: int
    amount: float

class PurchaseOrderCreate(PurchaseOrderBase):
    created_by_id: int

class PurchaseOrder(PurchaseOrderBase):
    id: int
    status: str
    created_by_id: int

    class Config:
        orm_mode = True

# Schemas for Change Order
class ChangeOrderBase(BaseModel):
    description: str
    project_id: int
    financial_impact: float

class ChangeOrderCreate(ChangeOrderBase):
    created_by_id: int

class ChangeOrder(ChangeOrderBase):
    id: int
    status: str
    created_by_id: int

    class Config:
        orm_mode = True

# Schemas for Contract
class ContractBase(BaseModel):
    name: str
    client_name: str
    total_value: float
    project_id: int

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    id: int

    class Config:
        orm_mode = True

# Schemas for ClientInvoice
class ClientInvoiceBase(BaseModel):
    contract_id: int
    amount: float
    due_date: datetime

class ClientInvoiceCreate(ClientInvoiceBase):
    pass

class ClientInvoice(ClientInvoiceBase):
    id: int
    status: str

    class Config:
        orm_mode = True

# Schemas for VendorInvoice
class VendorInvoiceBase(BaseModel):
    po_id: int
    vendor_id: int
    amount: float
    due_date: datetime

class VendorInvoiceCreate(VendorInvoiceBase):
    pass

class VendorInvoice(VendorInvoiceBase):
    id: int
    status: str

    class Config:
        orm_mode = True



