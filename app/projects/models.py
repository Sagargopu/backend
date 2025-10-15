from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Date, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class ProjectType(Base):
    __tablename__ = "project_types"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    type_name = Column(String(100), nullable=False)
    description = Column(Text)
    typical_duration_months = Column(Integer)
    complexity_level = Column(String(20))  # Simple, Moderate, Complex
    requires_permits = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Numeric(15, 2))
    status = Column(String(50), default='planned')  # planned, in_progress, completed, on_hold
    client_name = Column(String(255))
    project_manager_id = Column(Integer, ForeignKey("users.id"))
    
    # New categorization fields
    project_category = Column(String(50))  # Residential, Commercial, Industrial, etc.
    project_type = Column(String(100))     # Specific project type within category
    
    # Relationships
    project_manager = relationship("User", back_populates="managed_projects", foreign_keys=[project_manager_id])
    components = relationship("ProjectComponent", back_populates="project", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="project")
    transactions = relationship("Transaction", back_populates="project")
    all_tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProjectComponent(Base):
    __tablename__ = "project_components"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    type = Column(String(100))  # e.g., 'Foundation', 'Framing', 'Electrical', 'Plumbing'
    budget = Column(Numeric(15, 2))
    status = Column(String(50), default='planned')  # planned, in_progress, completed, on_hold
    details = Column(JSON)  # Additional component-specific details
    
    # Enhanced Budget Tracking
    allocated_budget = Column(Numeric(15, 2))  # Total budget allocated to this component
    spent_budget = Column(Numeric(15, 2), default=0)  # Money actually spent
    committed_budget = Column(Numeric(15, 2), default=0)  # Money committed but not yet spent
    remaining_budget = Column(Numeric(15, 2))  # Available budget remaining
    budget_variance = Column(Numeric(15, 2), default=0)  # Over/under budget amount
    budget_variance_percentage = Column(Numeric(5, 2), default=0)  # Percentage over/under
    
    # Component Progress and Deadlines
    completion_percentage = Column(Integer, default=0)  # 0-100% complete
    estimated_duration_days = Column(Integer)  # How long component should take
    actual_duration_days = Column(Integer)  # How long it actually took
    component_deadline = Column(Date, nullable=True)  # When component must be complete
    
    # Component Priority and Dependencies
    component_priority = Column(Integer, default=5)  # 1-10 priority scale
    is_critical_path = Column(Boolean, default=False)  # Is this component on critical path
    blocks_other_components = Column(Boolean, default=False)  # Does this block other work
    
    # Self-referential relationship for component hierarchy
    parent_id = Column(Integer, ForeignKey("project_components.id"))
    parent = relationship("ProjectComponent", remote_side=[id], back_populates="children")
    children = relationship("ProjectComponent", back_populates="parent", cascade="all, delete-orphan")
    
    # Relationships
    project = relationship("Project", back_populates="components")
    tasks = relationship("Task", back_populates="component", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="component")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    status = Column(String(50), default='To Do')  # To Do, In Progress, Done, Blocked, Cancelled, Backlog
    priority = Column(String(50), default='Medium')  # Low, Medium, High, Critical

    # Project and Component Relationships
    component_id = Column(Integer, ForeignKey("project_components.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)  # Direct project link for easier queries
    
    # Task Management Details
    task_type = Column(String(100))  # 'Planning', 'Construction', 'Inspection', 'Documentation'
    estimated_hours = Column(Numeric(8, 2))
    actual_hours = Column(Numeric(8, 2))
    completion_percentage = Column(Integer, default=0)  # 0-100
    
    # Scheduling with Deadlines
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    deadline = Column(Date, nullable=True)  # Hard deadline - task becomes backlog if not completed
    
    # Backlog Management
    moved_to_backlog_date = Column(DateTime(timezone=True), nullable=True)
    backlog_reason = Column(Text)  # Why task moved to backlog
    original_deadline = Column(Date, nullable=True)  # Original deadline before moving to backlog
    backlog_priority = Column(Integer, default=0)  # Priority within backlog (0 = highest)
    target_completion_date = Column(Date, nullable=True)  # New target date for backlog item
    
    # Assignment and Responsibility
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)  # Primary assignee
    created_by = Column(Integer, ForeignKey("users.id"))
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Who oversees this task
    
    # Task Details
    requirements = Column(Text)  # What needs to be done
    deliverables = Column(Text)  # What should be produced
    acceptance_criteria = Column(Text)  # How to determine completion
    notes = Column(Text)  # Additional notes and updates
    
    # Dependencies and Blocking
    is_milestone = Column(Boolean, default=False)  # Critical project milestone
    blocks_project = Column(Boolean, default=False)  # If true, project can't proceed without this
    
    # Resource Requirements
    required_skills = Column(Text)  # JSON array of required skills
    required_tools = Column(Text)  # Tools/equipment needed
    budget_allocation = Column(Numeric(12, 2))  # Budget allocated for this task
    actual_cost = Column(Numeric(12, 2), default=0)  # Actual money spent on this task
    
    # Deadline and Status Tracking
    deadline_status = Column(String(20), default='on_time')  # 'on_time', 'at_risk', 'overdue', 'missed'
    days_overdue = Column(Integer, default=0)  # How many days past deadline
    escalation_level = Column(Integer, default=0)  # 0=normal, 1=attention, 2=urgent, 3=critical
    
    # Quality and Compliance
    requires_inspection = Column(Boolean, default=False)
    inspection_status = Column(String(50))  # 'Not Required', 'Pending', 'Passed', 'Failed'
    quality_notes = Column(Text)
    
    # Relationships
    component = relationship("ProjectComponent", back_populates="tasks")
    project = relationship("Project", back_populates="all_tasks")
    primary_assignee = relationship("User", foreign_keys=[assigned_to])
    creator = relationship("User", foreign_keys=[created_by])
    supervisor = relationship("User", foreign_keys=[supervisor_id])
    assignments = relationship("Assignment", back_populates="task", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="task")
    dependencies = relationship("TaskDependency", foreign_keys="TaskDependency.dependent_task_id", back_populates="dependent_task")
    dependents = relationship("TaskDependency", foreign_keys="TaskDependency.prerequisite_task_id", back_populates="prerequisite_task")
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")
    time_logs = relationship("TaskTimeLog", back_populates="task", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Assignment Details
    role_in_task = Column(String(100))  # 'Lead', 'Assistant', 'Reviewer', 'Approver'
    assigned_date = Column(DateTime(timezone=True), server_default=func.now())
    assignment_notes = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    task = relationship("Task", back_populates="assignments")
    assignee = relationship("User")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    
    id = Column(Integer, primary_key=True, index=True)
    prerequisite_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)  # Task that must be completed first
    dependent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)     # Task that depends on prerequisite
    
    # Dependency Details
    dependency_type = Column(String(50), default='finish_to_start')  
    # 'finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish'
    lag_days = Column(Integer, default=0)  # Days between prerequisite completion and dependent start
    is_hard_dependency = Column(Boolean, default=True)  # Hard = blocking, Soft = preferred
    dependency_notes = Column(Text)
    
    # Relationships
    prerequisite_task = relationship("Task", foreign_keys=[prerequisite_task_id], back_populates="dependents")
    dependent_task = relationship("Task", foreign_keys=[dependent_task_id], back_populates="dependencies")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure no self-dependencies and no duplicate dependencies
    __table_args__ = (
        {"extend_existing": True},
    )

class TaskComment(Base):
    __tablename__ = "task_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Comment Details
    comment_text = Column(Text, nullable=False)
    comment_type = Column(String(50), default='general')  # 'general', 'status_update', 'issue', 'resolution'
    is_internal = Column(Boolean, default=True)  # Internal vs client-visible
    
    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TaskTimeLog(Base):
    __tablename__ = "task_time_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Time Tracking
    work_date = Column(Date, nullable=False)
    hours_worked = Column(Numeric(5, 2), nullable=False)
    description = Column(Text)
    
    # Time Entry Details
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    is_billable = Column(Boolean, default=True)
    hourly_rate = Column(Numeric(8, 2))
    
    # Approval
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_status = Column(String(20), default='pending')  # 'pending', 'approved', 'rejected'
    
    # Relationships
    task = relationship("Task", back_populates="time_logs")
    worker = relationship("User", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TaskBacklogHistory(Base):
    __tablename__ = "task_backlog_history"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    
    # Backlog Event Details
    event_type = Column(String(50), nullable=False)  # 'moved_to_backlog', 'removed_from_backlog', 'priority_changed'
    event_date = Column(DateTime(timezone=True), server_default=func.now())
    event_reason = Column(Text)
    
    # Status at time of event
    previous_status = Column(String(50))
    new_status = Column(String(50))
    previous_deadline = Column(Date)
    new_deadline = Column(Date)
    
    # Who made the change
    changed_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Manager approval for backlog moves
    
    # Impact Assessment
    impact_on_project = Column(Text)  # How this affects the overall project
    mitigation_plan = Column(Text)  # Plan to address the delay
    
    # Relationships
    task = relationship("Task")
    changer = relationship("User", foreign_keys=[changed_by])
    approver = relationship("User", foreign_keys=[approved_by])

class ComponentBudgetTracking(Base):
    __tablename__ = "component_budget_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("project_components.id"), nullable=False)
    
    # Budget Entry Details
    entry_date = Column(Date, nullable=False)
    entry_type = Column(String(50), nullable=False)  # 'allocation', 'expense', 'adjustment', 'transfer'
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(Text, nullable=False)
    
    # Reference Information
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)  # Link to actual transaction
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)  # Which task this relates to
    
    # Approval and Authorization
    authorized_by = Column(Integer, ForeignKey("users.id"))
    approval_status = Column(String(20), default='pending')  # 'pending', 'approved', 'rejected'
    
    # Budget Categories
    budget_category = Column(String(100))  # 'Materials', 'Labor', 'Equipment', 'Subcontractor', 'Other'
    budget_subcategory = Column(String(100))  # More specific categorization
    
    # Running Totals (calculated fields)
    running_allocated = Column(Numeric(15, 2))
    running_spent = Column(Numeric(15, 2))
    running_remaining = Column(Numeric(15, 2))
    
    # Relationships
    component = relationship("ProjectComponent")
    transaction = relationship("Transaction")
    task = relationship("Task")
    authorizer = relationship("User")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DeadlineAlert(Base):
    __tablename__ = "deadline_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    component_id = Column(Integer, ForeignKey("project_components.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Alert Details
    alert_type = Column(String(50), nullable=False)  # 'approaching_deadline', 'missed_deadline', 'at_risk'
    alert_level = Column(String(20), nullable=False)  # 'info', 'warning', 'critical'
    alert_message = Column(Text, nullable=False)
    
    # Timing
    deadline_date = Column(Date, nullable=False)
    days_until_deadline = Column(Integer)  # Negative if overdue
    alert_generated_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status and Resolution
    alert_status = Column(String(20), default='active')  # 'active', 'acknowledged', 'resolved', 'dismissed'
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_date = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text)
    
    # Escalation
    escalation_level = Column(Integer, default=0)  # 0=normal, 1=manager, 2=senior, 3=executive
    escalated_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    task = relationship("Task")
    component = relationship("ProjectComponent") 
    project = relationship("Project")
    acknowledger = relationship("User", foreign_keys=[acknowledged_by])
    escalated_user = relationship("User", foreign_keys=[escalated_to])


