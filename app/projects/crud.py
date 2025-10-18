from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from . import models, schemas

# ProjectType CRUD
def create_project_type(db: Session, project_type: schemas.ProjectTypeCreate):
    db_project_type = models.ProjectType(**project_type.dict())
    db.add(db_project_type)
    db.commit()
    db.refresh(db_project_type)
    return db_project_type

def get_project_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectType).offset(skip).limit(limit).all()

def get_project_type(db: Session, project_type_id: int):
    return db.query(models.ProjectType).filter(models.ProjectType.id == project_type_id).first()

def update_project_type(db: Session, project_type_id: int, project_type_update: schemas.ProjectTypeUpdate):
    db_project_type = db.query(models.ProjectType).filter(models.ProjectType.id == project_type_id).first()
    if db_project_type:
        update_data = project_type_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project_type, field, value)
        db.commit()
        db.refresh(db_project_type)
    return db_project_type

def delete_project_type(db: Session, project_type_id: int):
    db_project_type = db.query(models.ProjectType).filter(models.ProjectType.id == project_type_id).first()
    if db_project_type:
        db.delete(db_project_type)
        db.commit()
    return db_project_type

# Project CRUD
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_projects_with_details(db: Session, skip: int = 0, limit: int = 100):
    """Get projects with all related objects loaded"""
    return db.query(models.Project).options(
        joinedload(models.Project.client),
        joinedload(models.Project.project_manager),
        joinedload(models.Project.accountant),
        joinedload(models.Project.project_type)
    ).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_project_with_details(db: Session, project_id: int):
    """Get a single project with all related objects loaded"""
    return db.query(models.Project).options(
        joinedload(models.Project.client),
        joinedload(models.Project.project_manager),
        joinedload(models.Project.accountant),
        joinedload(models.Project.project_type)
    ).filter(models.Project.id == project_id).first()

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

# Project filtering functions
def get_projects_by_client(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.client_id == client_id
    ).offset(skip).limit(limit).all()

def get_projects_by_client_with_details(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    """Get projects by client with all related objects loaded"""
    return db.query(models.Project).options(
        joinedload(models.Project.client),
        joinedload(models.Project.project_manager),
        joinedload(models.Project.accountant),
        joinedload(models.Project.project_type)
    ).filter(models.Project.client_id == client_id).offset(skip).limit(limit).all()

def get_projects_by_project_manager(db: Session, project_manager_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.project_manager_id == project_manager_id
    ).offset(skip).limit(limit).all()

def get_projects_by_project_manager_with_details(db: Session, project_manager_id: int, skip: int = 0, limit: int = 100):
    """Get projects by project manager with all related objects loaded"""
    return db.query(models.Project).options(
        joinedload(models.Project.client),
        joinedload(models.Project.project_manager),
        joinedload(models.Project.accountant),
        joinedload(models.Project.project_type)
    ).filter(models.Project.project_manager_id == project_manager_id).offset(skip).limit(limit).all()

def get_projects_by_project_type(db: Session, project_type_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.project_type_id == project_type_id
    ).offset(skip).limit(limit).all()

def get_projects_by_project_type_with_details(db: Session, project_type_id: int, skip: int = 0, limit: int = 100):
    """Get projects by project type with all related objects loaded"""
    return db.query(models.Project).options(
        joinedload(models.Project.client),
        joinedload(models.Project.project_manager),
        joinedload(models.Project.accountant),
        joinedload(models.Project.project_type)
    ).filter(models.Project.project_type_id == project_type_id).offset(skip).limit(limit).all()

# ProjectComponent CRUD
def create_project_component(db: Session, component: schemas.ProjectComponentCreate):
    db_component = models.ProjectComponent(**component.dict())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

def get_project_components(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectComponent).offset(skip).limit(limit).all()

def get_project_components_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectComponent).filter(
        models.ProjectComponent.project_id == project_id
    ).offset(skip).limit(limit).all()

def get_project_component(db: Session, component_id: int):
    return db.query(models.ProjectComponent).filter(models.ProjectComponent.id == component_id).first()

def update_project_component(db: Session, component_id: int, component_update: schemas.ProjectComponentUpdate):
    db_component = db.query(models.ProjectComponent).filter(models.ProjectComponent.id == component_id).first()
    if db_component:
        update_data = component_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_component, field, value)
        db.commit()
        db.refresh(db_component)
    return db_component

def delete_project_component(db: Session, component_id: int):
    db_component = db.query(models.ProjectComponent).filter(models.ProjectComponent.id == component_id).first()
    if db_component:
        db.delete(db_component)
        db.commit()
    return db_component

# Task CRUD
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_component(db: Session, component_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.component_id == component_id).offset(skip).limit(limit).all()

def get_tasks_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.project_id == project_id).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

# Finance summary functions
def get_project_purchase_orders_sum(db: Session, project_id: int):
    """Calculate the total sum of all approved purchase order items for a project"""
    from app.finance.models import PurchaseOrder, PurchaseOrderItem
    
    # Include all approved statuses: Approved, Delivered, Paid
    approved_statuses = ['Approved', 'Delivered', 'Paid']
    
    total = db.query(func.sum(PurchaseOrderItem.price)).join(
        PurchaseOrder, PurchaseOrderItem.purchase_order_id == PurchaseOrder.id
    ).join(
        models.Task, PurchaseOrder.task_id == models.Task.id
    ).filter(
        models.Task.project_id == project_id,
        PurchaseOrder.status.in_(approved_statuses)  # Include all approved statuses
    ).scalar()
    
    return float(total) if total else 0.0

def get_project_change_orders_sum(db: Session, project_id: int):
    """Calculate the total sum of all approved change order items for a project (considering impact_type)"""
    from app.finance.models import ChangeOrder, ChangeOrderItem
    
    # Include all approved statuses: Approved, Implemented
    approved_statuses = ['Approved', 'Implemented']
    
    # Get all change order items for approved change orders
    change_items = db.query(
        ChangeOrderItem.amount, 
        ChangeOrderItem.impact_type
    ).join(
        ChangeOrder, ChangeOrderItem.change_order_id == ChangeOrder.id
    ).join(
        models.Task, ChangeOrder.task_id == models.Task.id
    ).filter(
        models.Task.project_id == project_id,
        ChangeOrder.status.in_(approved_statuses)  # Include all approved statuses
    ).all()
    
    total = 0.0
    for amount, impact_type in change_items:
        if impact_type == '+':
            total += float(amount)
        elif impact_type == '-':
            total -= float(amount)
    
    return total

def get_project_financial_summary(db: Session, project_id: int):
    """Get comprehensive financial summary for a project"""
    po_sum = get_project_purchase_orders_sum(db, project_id)
    co_sum = get_project_change_orders_sum(db, project_id)
    
    return {
        'purchase_orders_sum': po_sum,
        'change_orders_sum': co_sum
    }
