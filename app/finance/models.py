from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    representative_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    business_type = Column(String(100))  # 'Material Supplier', 'Subcontractor', 'Equipment Rental', 'Service Provider' 
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(50), unique=True, nullable=False, index=True)  # PO-2025-001
    
    # Task Association
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    # Vendor Information
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    
    # Purchase Details
    description = Column(Text, nullable=False)  # Overall PO description
    delivery_date = Column(Date)
    
    # Status Management
    status = Column(String(50), default='Draft')  # 'Draft', 'Pending Approval', 'Approved', 'Rejected', 'Delivered', 'Paid'
    
    # Approval Workflow
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(DateTime(timezone=True), nullable=True)
    
    # Notes
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vendor = relationship("Vendor")
    task = relationship("Task")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    
    # Item Details
    item_name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # 'Material', 'Labor', 'Equipment', 'Service'
    
    # Pricing
    price = Column(Numeric(10, 2), nullable=False)  # Price per unit
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")

class ChangeOrder(Base):
    __tablename__ = "change_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    co_number = Column(String(50), unique=True, nullable=False, index=True)  # CO-2025-001
    
    # Task Association
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    
    # Change Order Details
    title = Column(String(255), nullable=False)  # Brief title of the change
    description = Column(Text, nullable=False)  # Detailed description
    reason = Column(String(100))  # 'Client Request', 'Design Change', 'Site Condition', 'Code Requirement'
    
    # Status Management
    status = Column(String(50), default='Draft')  # 'Draft', 'Pending Approval', 'Approved', 'Rejected', 'Implemented'
    
    # Approval Workflow
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    task = relationship("Task")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    items = relationship("ChangeOrderItem", back_populates="change_order", cascade="all, delete-orphan")

class ChangeOrderItem(Base):
    __tablename__ = "change_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    change_order_id = Column(Integer, ForeignKey("change_orders.id"), nullable=False)
    
    # Item Details
    item_name = Column(String(255), nullable=False)
    description = Column(Text)
    change_type = Column(String(50))  # 'Addition', 'Deletion', 'Modification'
    impact_type = Column(String(10), nullable=False)  # '+' for cost increase, '-' for cost decrease
    
    # Pricing
    amount = Column(Numeric(12, 2), nullable=False)  # Always positive value, impact_type determines if it's added or subtracted
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    change_order = relationship("ChangeOrder", back_populates="items")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_number = Column(String(50), unique=True, nullable=False, index=True)  # TXN-2025-001
    
    # Project Association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    
    # Transaction Source
    transaction_type = Column(String(20), nullable=False)  # 'purchase_order', 'change_order'
    source_id = Column(Integer, nullable=False)  # PO or CO ID
    source_number = Column(String(50), nullable=False)  # PO-2025-001 or CO-2025-001
    
    # Financial Impact
    amount = Column(Numeric(12, 2), nullable=False)  # Always positive
    impact_type = Column(String(10), nullable=False)  # '+' for budget increase/commitment, '-' for budget decrease
    description = Column(Text, nullable=False)
    
    # Budget Tracking
    budget_before = Column(Numeric(15, 2), nullable=False)  # Actual budget before this transaction
    budget_after = Column(Numeric(15, 2), nullable=False)   # Actual budget after this transaction
    
    # Approval Details
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_date = Column(DateTime(timezone=True), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="transactions")
    task = relationship("Task")
    approver = relationship("User")
