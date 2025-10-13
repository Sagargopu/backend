from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact_person = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    client_name = Column(String)
    total_value = Column(Float)
    project_id = Column(Integer, ForeignKey("project_components.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    project_id = Column(Integer, ForeignKey("project_components.id"))
    amount = Column(Float)
    status = Column(String, default='Pending Approval') # Pending Approval, Approved, Rejected, Paid
    created_by_id = Column(Integer, ForeignKey("users.id"))
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChangeOrder(Base):
    __tablename__ = "change_orders"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("project_components.id"))
    financial_impact = Column(Float) # Can be positive or negative
    status = Column(String, default='Pending Approval') # Pending Approval, Approved, Rejected
    created_by_id = Column(Integer, ForeignKey("users.id"))
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True) # This could be a client user
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ClientInvoice(Base):
    __tablename__ = "client_invoices"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    amount = Column(Float)
    status = Column(String, default='Draft') # Draft, Sent, Paid, Overdue
    due_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class VendorInvoice(Base):
    __tablename__ = "vendor_invoices"
    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    amount = Column(Float)
    status = Column(String, default='Received') # Received, Verified, Paid
    due_date = Column(DateTime)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
