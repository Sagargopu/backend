from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean, Date, Numeric
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
    project_id = Column(Integer, ForeignKey("projects.id"))  # Changed to reference projects
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Relationships
    project = relationship("Project", back_populates="contracts")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))  # Changed to reference projects
    amount = Column(Float)
    status = Column(String, default='Pending Approval') # Pending Approval, Approved, Rejected, Paid
    created_by_id = Column(Integer, ForeignKey("users.id"))
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    vendor = relationship("Vendor")
    project = relationship("Project")
    created_by = relationship("User", foreign_keys=[created_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])

class ChangeOrder(Base):
    __tablename__ = "change_orders"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))  # Changed to reference projects
    financial_impact = Column(Float) # Can be positive or negative
    status = Column(String, default='Pending Approval') # Pending Approval, Approved, Rejected
    created_by_id = Column(Integer, ForeignKey("users.id"))
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True) # This could be a client user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project")
    created_by = relationship("User", foreign_keys=[created_by_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])

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

# Transaction Management Models

class TransactionCategory(Base):
    __tablename__ = "transaction_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False, unique=True)
    category_type = Column(String(20), nullable=False)  # 'income' or 'expense'
    description = Column(Text)
    is_project_specific = Column(Boolean, default=False)
    requires_approval = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String(20), nullable=False)  # 'incoming' or 'outgoing'
    expense_name = Column(String(200), nullable=False)
    description = Column(Text)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_date = Column(Date, nullable=False)
    
    # Project Association & Management Hierarchy
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For PM-level reporting
    is_project_specific = Column(Boolean, default=False)
    
    # Category and Classification
    category_id = Column(Integer, ForeignKey("transaction_categories.id"))
    payment_method = Column(String(50))  # 'cash', 'check', 'bank_transfer', 'credit_card', etc.
    
    # Financial Period Tracking (for reporting)
    fiscal_year = Column(Integer)  # Extracted from transaction_date
    fiscal_quarter = Column(String(10))  # Q1, Q2, Q3, Q4
    fiscal_month = Column(Integer)  # 1-12
    
    # Budget and Cost Center Tracking
    budget_line_item = Column(String(100))  # Which budget category this affects
    cost_center = Column(String(50))  # Department/division responsible
    is_budgeted = Column(Boolean, default=True)  # Was this expense planned?
    variance_reason = Column(Text)  # Explanation for budget variances
    
    # Approval Workflow
    status = Column(String(20), default='pending')  # 'pending', 'approved', 'rejected', 'paid', 'cancelled'
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(DateTime(timezone=True), nullable=True)
    approval_notes = Column(Text)
    
    # Enhanced Approval Tracking
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Manager who requested transaction
    request_date = Column(DateTime(timezone=True), server_default=func.now())
    rejection_reason = Column(Text)  # Detailed reason for rejection
    rejection_date = Column(DateTime(timezone=True), nullable=True)
    rejected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Approval Workflow History (for audit trail)
    approval_history = Column(Text)  # JSON array of status changes with timestamps
    
    # Invoicing Integration
    is_invoiceable = Column(Boolean, default=True)  # All transactions can potentially be invoiced
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice_line_item_id = Column(Integer, ForeignKey("invoice_line_items.id"), nullable=True)  # Direct link to line item
    invoice_line_item = Column(String(200))  # Description for invoice line
    client_markup_percentage = Column(Numeric(5, 2), default=0)  # Markup % for client billing
    billable_amount = Column(Numeric(12, 2))  # Amount to bill client (with markup)
    billing_status = Column(String(20), default='unbilled')  # 'unbilled', 'included_in_invoice', 'invoiced', 'paid'
    billing_notes = Column(Text)  # Notes about billing this transaction
    
    # Payment Processing
    payment_due_date = Column(Date, nullable=True)
    payment_processed_date = Column(Date, nullable=True)
    payment_reference = Column(String(100))  # Bank reference, check number, etc.
    
    # Financial Details
    vendor_supplier = Column(String(200))
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)  # Link to vendor table
    invoice_number = Column(String(100))
    receipt_number = Column(String(100))
    purchase_order_number = Column(String(100))
    
    # Amount Breakdown
    subtotal_amount = Column(Numeric(12, 2))  # Amount before tax/discount
    tax_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    shipping_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(12, 2))  # Final amount (could differ from 'amount' field)
    
    # Currency and Exchange (for future international support)
    currency_code = Column(String(3), default='USD')
    exchange_rate = Column(Numeric(10, 4), default=1.0)
    
    # Tracking and Audit
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional Metadata for Reporting
    notes = Column(Text)  # Internal notes
    external_reference = Column(String(200))  # External system reference
    is_recurring = Column(Boolean, default=False)  # Is this a recurring transaction?
    recurring_frequency = Column(String(20))  # monthly, quarterly, annually
    
    # Relationships
    project = relationship("Project", back_populates="transactions")
    project_manager = relationship("User", foreign_keys=[project_manager_id])
    category = relationship("TransactionCategory", back_populates="transactions")
    vendor = relationship("Vendor", foreign_keys=[vendor_id])
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_transactions")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_transactions")
    requester = relationship("User", foreign_keys=[requested_by])
    rejector = relationship("User", foreign_keys=[rejected_by])
    invoice = relationship("Invoice", back_populates="transactions")
    invoice_line_item_ref = relationship("InvoiceLineItem", foreign_keys=[invoice_line_item_id], back_populates="source_transaction")

# Additional Models for Enhanced Reporting

class BudgetLine(Base):
    __tablename__ = "budget_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)  # Null for company-wide budgets
    category_id = Column(Integer, ForeignKey("transaction_categories.id"))
    budget_name = Column(String(200), nullable=False)
    allocated_amount = Column(Numeric(12, 2), nullable=False)
    spent_amount = Column(Numeric(12, 2), default=0)
    remaining_amount = Column(Numeric(12, 2))
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(String(10))
    
    # Tracking
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    category = relationship("TransactionCategory")
    creator = relationship("User")

class FinancialReport(Base):
    __tablename__ = "financial_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(50), nullable=False)  # 'monthly', 'quarterly', 'project', 'pm_summary'
    report_period = Column(String(50))  # '2025-Q1', '2025-10', 'Project-123'
    
    # Scope
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project_manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Financial Summary
    total_income = Column(Numeric(15, 2), default=0)
    total_expenses = Column(Numeric(15, 2), default=0)
    net_profit = Column(Numeric(15, 2), default=0)
    budget_variance = Column(Numeric(15, 2), default=0)
    
    # Report Data (JSON for flexibility)
    report_data = Column(Text)  # JSON with detailed breakdowns
    
    # Generation Info
    generated_by = Column(Integer, ForeignKey("users.id"))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project")
    project_manager = relationship("User", foreign_keys=[project_manager_id])
    generator = relationship("User", foreign_keys=[generated_by])

class CostCenter(Base):
    __tablename__ = "cost_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    center_name = Column(String(100), nullable=False, unique=True)
    center_code = Column(String(20), nullable=False, unique=True)
    description = Column(Text)
    manager_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    
    # Budget Allocation
    annual_budget = Column(Numeric(15, 2))
    current_spent = Column(Numeric(15, 2), default=0)
    
    # Relationships
    manager = relationship("User")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Enhanced Invoicing System

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    invoice_type = Column(String(20), nullable=False)  # 'client_billing', 'vendor_payment', 'internal'
    
    # Client/Vendor Information
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    client_name = Column(String(200))
    client_address = Column(Text)
    client_email = Column(String(200))
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    
    # Invoice Details
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    payment_terms = Column(String(50))  # 'Net 30', 'Due on Receipt', etc.
    
    # Financial Summary
    subtotal = Column(Numeric(12, 2), nullable=False)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)
    
    # Payment Tracking
    status = Column(String(20), default='draft')  # 'draft', 'sent', 'viewed', 'paid', 'overdue', 'cancelled'
    payment_status = Column(String(20), default='unpaid')  # 'unpaid', 'partial', 'paid', 'refunded'
    paid_amount = Column(Numeric(12, 2), default=0)
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String(50))
    payment_reference = Column(String(100))
    
    # Approval and Generation
    created_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(DateTime(timezone=True), nullable=True)
    sent_date = Column(DateTime(timezone=True), nullable=True)
    
    # Additional Information
    notes = Column(Text)
    internal_notes = Column(Text)  # Notes not visible to client
    currency_code = Column(String(3), default='USD')
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    vendor = relationship("Vendor")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    transactions = relationship("Transaction", back_populates="invoice")  # All transactions linked to this invoice
    line_items = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    
    # Line Item Details
    description = Column(String(500), nullable=False)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    line_total = Column(Numeric(12, 2), nullable=False)
    
    # Categorization
    category = Column(String(100))
    project_component = Column(String(200))  # Which part of project this relates to
    
    # Transaction Grouping - Multiple transactions can be grouped into one line item
    line_item_type = Column(String(50), default='transaction_group')  # 'single_transaction', 'transaction_group', 'manual_entry'
    transaction_summary = Column(Text)  # Summary of what transactions are included
    
    # Dates
    service_date_from = Column(Date)  # Start date for services in this line item
    service_date_to = Column(Date)    # End date for services in this line item
    
    # Billing Details
    markup_percentage = Column(Numeric(5, 2), default=0)
    cost_amount = Column(Numeric(12, 2))  # Total cost from source transactions
    markup_amount = Column(Numeric(10, 2))  # Calculated markup
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    invoice = relationship("Invoice", back_populates="line_items")
    source_transaction = relationship("Transaction", foreign_keys="Transaction.invoice_line_item_id", back_populates="invoice_line_item_ref")
    related_transactions = relationship("TransactionLineItemLink", back_populates="line_item")

class TransactionLineItemLink(Base):
    __tablename__ = "transaction_line_item_links"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    invoice_line_item_id = Column(Integer, ForeignKey("invoice_line_items.id"), nullable=False)
    
    # Link Details
    portion_of_transaction = Column(Numeric(5, 2), default=100.00)  # What % of transaction is in this line item
    allocated_amount = Column(Numeric(12, 2))  # Amount from transaction allocated to this line item
    notes = Column(Text)  # Notes about this allocation
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    transaction = relationship("Transaction")
    line_item = relationship("InvoiceLineItem", back_populates="related_transactions")
    
    # Ensure unique combination of transaction and line item
    __table_args__ = (
        {"extend_existing": True},
    )

class InvoicePayment(Base):
    __tablename__ = "invoice_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    
    # Payment Details
    payment_amount = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_reference = Column(String(100))
    
    # Bank/Processing Information
    bank_reference = Column(String(100))
    transaction_fee = Column(Numeric(8, 2), default=0)
    
    # Tracking
    recorded_by = Column(Integer, ForeignKey("users.id"))
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    recorder = relationship("User")

class ApprovalWorkflow(Base):
    __tablename__ = "approval_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    
    # Workflow Details
    workflow_type = Column(String(20), nullable=False)  # 'transaction', 'invoice', 'budget_change'
    current_status = Column(String(20), nullable=False)
    previous_status = Column(String(20))
    
    # Approval Information
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(String(20), nullable=False)  # 'submitted', 'approved', 'rejected', 'revised'
    action_date = Column(DateTime(timezone=True), server_default=func.now())
    comments = Column(Text)
    
    # Additional Context
    amount_involved = Column(Numeric(12, 2))
    approval_level = Column(String(20))  # 'basic', 'senior', 'executive'
    
    # Relationships
    transaction = relationship("Transaction")
    invoice = relationship("Invoice")
    action_user = relationship("User")
