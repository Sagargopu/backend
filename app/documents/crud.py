from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from . import models, schemas

# ===============================
# DOCUMENT CRUD OPERATIONS
# ===============================

def create_document(db: Session, document: schemas.DocumentCreate, uploaded_by_id: int):
    """Create a new document with hierarchy support"""
    db_document = models.Document(
        name=document.name,
        description=document.description,
        storage_path=document.storage_path,
        file_type=document.file_type,
        file_size=document.file_size,
        document_type=document.document_type,
        project_id=document.project_id,
        component_id=document.component_id,
        task_id=document.task_id,
        uploaded_by_id=uploaded_by_id,
        is_public=document.is_public
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int):
    """Get document by ID with all relationships"""
    return db.query(models.Document).options(
        joinedload(models.Document.uploader),
        joinedload(models.Document.project),
        joinedload(models.Document.component),
        joinedload(models.Document.task),
        joinedload(models.Document.access_permissions)
    ).filter(models.Document.id == document_id).first()

def get_documents_accessible_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all documents a user can access (uploaded by them, public, or explicitly granted access)"""
    return db.query(models.Document).outerjoin(
        models.DocumentAccess,
        models.Document.id == models.DocumentAccess.document_id
    ).filter(
        or_(
            models.Document.uploaded_by_id == user_id,  # User uploaded it
            models.Document.is_public == True,  # Public document
            models.DocumentAccess.user_id == user_id  # Explicitly granted access
        )
    ).options(
        joinedload(models.Document.uploader),
        joinedload(models.Document.project),
        joinedload(models.Document.component),
        joinedload(models.Document.task)
    ).distinct().offset(skip).limit(limit).all()

def get_documents_by_project(db: Session, project_id: int, user_id: int, skip: int = 0, limit: int = 100):
    """Get documents for a specific project that user can access"""
    return db.query(models.Document).outerjoin(
        models.DocumentAccess,
        models.Document.id == models.DocumentAccess.document_id
    ).filter(
        and_(
            models.Document.project_id == project_id,
            or_(
                models.Document.uploaded_by_id == user_id,
                models.Document.is_public == True,
                models.DocumentAccess.user_id == user_id
            )
        )
    ).options(
        joinedload(models.Document.uploader),
        joinedload(models.Document.component),
        joinedload(models.Document.task)
    ).distinct().offset(skip).limit(limit).all()

def get_documents_by_component(db: Session, component_id: int, user_id: int, skip: int = 0, limit: int = 100):
    """Get documents for a specific component that user can access"""
    return db.query(models.Document).outerjoin(
        models.DocumentAccess,
        models.Document.id == models.DocumentAccess.document_id
    ).filter(
        and_(
            models.Document.component_id == component_id,
            or_(
                models.Document.uploaded_by_id == user_id,
                models.Document.is_public == True,
                models.DocumentAccess.user_id == user_id
            )
        )
    ).options(
        joinedload(models.Document.uploader),
        joinedload(models.Document.project),
        joinedload(models.Document.task)
    ).distinct().offset(skip).limit(limit).all()

def update_document(db: Session, document_id: int, document_update: schemas.DocumentUpdate, user_id: int):
    """Update document (only if user has edit access)"""
    document = get_document(db, document_id)
    if not document:
        return None
    
    # Check if user can edit
    if not can_user_edit_document(db, document_id, user_id):
        return None
    
    for field, value in document_update.dict(exclude_unset=True).items():
        setattr(document, field, value)
    
    db.commit()
    db.refresh(document)
    return document

def delete_document(db: Session, document_id: int, user_id: int):
    """Delete document (only uploader or admin access)"""
    document = get_document(db, document_id)
    if not document:
        return False
    
    # Only uploader or users with admin access can delete
    uploader_id = getattr(document, 'uploaded_by_id', None)
    if (uploader_id != user_id) and not has_admin_access(db, document_id, user_id):
        return False
    
    db.delete(document)
    db.commit()
    return True

# ===============================
# DOCUMENT ACCESS CONTROL
# ===============================

def grant_document_access(db: Session, document_id: int, user_id: int, access_level: str, granted_by_id: int, access_notes: Optional[str] = None):
    """Grant access to a document for a user"""
    # Check if access already exists
    existing_access = db.query(models.DocumentAccess).filter(
        and_(
            models.DocumentAccess.document_id == document_id,
            models.DocumentAccess.user_id == user_id
        )
    ).first()
    
    if existing_access:
        # Update existing access
        setattr(existing_access, 'access_level', access_level)
        setattr(existing_access, 'access_notes', access_notes)
        setattr(existing_access, 'granted_by_id', granted_by_id)
        db.commit()
        db.refresh(existing_access)
        return existing_access
    else:
        # Create new access
        db_access = models.DocumentAccess(
            document_id=document_id,
            user_id=user_id,
            access_level=access_level,
            granted_by_id=granted_by_id,
            access_notes=access_notes
        )
        db.add(db_access)
        db.commit()
        db.refresh(db_access)
        return db_access

def revoke_document_access(db: Session, document_id: int, user_id: int, revoked_by_id: int):
    """Revoke access to a document for a user"""
    # Check if revoker has permission
    if not can_user_manage_access(db, document_id, revoked_by_id):
        return False
    
    access = db.query(models.DocumentAccess).filter(
        and_(
            models.DocumentAccess.document_id == document_id,
            models.DocumentAccess.user_id == user_id
        )
    ).first()
    
    if access:
        db.delete(access)
        db.commit()
        return True
    return False

def get_document_access_list(db: Session, document_id: int, user_id: int):
    """Get list of users who have access to a document"""
    # Check if user can view access list
    if not can_user_view_document(db, document_id, user_id):
        return []
    
    return db.query(models.DocumentAccess).options(
        joinedload(models.DocumentAccess.user),
        joinedload(models.DocumentAccess.granted_by)
    ).filter(models.DocumentAccess.document_id == document_id).all()

def can_user_view_document(db: Session, document_id: int, user_id: int) -> bool:
    """Check if user can view a document"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return False
    
    # Uploader can always view
    uploader_id = getattr(document, 'uploaded_by_id', None)
    if uploader_id == user_id:
        return True
    
    # Public documents can be viewed by anyone
    is_public = getattr(document, 'is_public', False)
    if is_public:
        return True
    
    # Check explicit access
    access = db.query(models.DocumentAccess).filter(
        and_(
            models.DocumentAccess.document_id == document_id,
            models.DocumentAccess.user_id == user_id
        )
    ).first()
    
    return access is not None

def can_user_edit_document(db: Session, document_id: int, user_id: int) -> bool:
    """Check if user can edit a document"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return False
    
    # Uploader can always edit
    uploader_id = getattr(document, 'uploaded_by_id', None)
    if uploader_id == user_id:
        return True
    
    # Check explicit edit access
    access = db.query(models.DocumentAccess).filter(
        and_(
            models.DocumentAccess.document_id == document_id,
            models.DocumentAccess.user_id == user_id,
            models.DocumentAccess.access_level.in_(['edit', 'admin'])
        )
    ).first()
    
    return access is not None

def can_user_manage_access(db: Session, document_id: int, user_id: int) -> bool:
    """Check if user can manage access to a document"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return False
    
    # Uploader can always manage access
    uploader_id = getattr(document, 'uploaded_by_id', None)
    if uploader_id == user_id:
        return True
    
    # Check admin access
    return has_admin_access(db, document_id, user_id)

def has_admin_access(db: Session, document_id: int, user_id: int) -> bool:
    """Check if user has admin access to a document"""
    access = db.query(models.DocumentAccess).filter(
        and_(
            models.DocumentAccess.document_id == document_id,
            models.DocumentAccess.user_id == user_id,
            models.DocumentAccess.access_level == 'admin'
        )
    ).first()
    
    return access is not None

# ===============================
# DOCUMENT SHARING
# ===============================

def share_document_with_user(db: Session, document_id: int, shared_with_id: int, shared_by_id: int, share_data: schemas.DocumentShareCreate):
    """Share a document with a specific user"""
    # Check if sharer has permission
    if not can_user_manage_access(db, document_id, shared_by_id):
        return None
    
    # Create share record
    db_share = models.DocumentShare(
        document_id=document_id,
        shared_by_id=shared_by_id,
        shared_with_id=shared_with_id,
        share_message=share_data.share_message,
        share_type=share_data.share_type,
        is_temporary=share_data.is_temporary,
        expires_at=share_data.expires_at
    )
    db.add(db_share)
    
    # Grant access to the document
    grant_document_access(db, document_id, shared_with_id, "view", shared_by_id)
    
    db.commit()
    db.refresh(db_share)
    return db_share

def share_document_with_multiple_users(db: Session, share_data: schemas.DocumentShareMultiple, shared_by_id: int):
    """Share a document with multiple users"""
    if not can_user_manage_access(db, share_data.document_id, shared_by_id):
        return {"successful_shares": [], "failed_shares": [], "total_attempted": 0, "total_successful": 0}
    
    successful_shares = []
    failed_shares = []
    
    for user_id in share_data.user_ids:
        try:
            # Create share record
            db_share = models.DocumentShare(
                document_id=share_data.document_id,
                shared_by_id=shared_by_id,
                shared_with_id=user_id,
                share_message=share_data.share_message,
                share_type=share_data.share_type
            )
            db.add(db_share)
            
            # Grant access
            grant_document_access(db, share_data.document_id, user_id, share_data.access_level, shared_by_id)
            successful_shares.append(user_id)
            
        except Exception as e:
            failed_shares.append({"user_id": user_id, "error": str(e)})
    
    db.commit()
    
    return {
        "successful_shares": successful_shares,
        "failed_shares": failed_shares,
        "total_attempted": len(share_data.user_ids),
        "total_successful": len(successful_shares)
    }

def get_document_shares(db: Session, document_id: int, user_id: int):
    """Get sharing history for a document"""
    if not can_user_view_document(db, document_id, user_id):
        return []
    
    return db.query(models.DocumentShare).options(
        joinedload(models.DocumentShare.shared_by),
        joinedload(models.DocumentShare.shared_with),
        joinedload(models.DocumentShare.document)
    ).filter(models.DocumentShare.document_id == document_id).order_by(desc(models.DocumentShare.created_at)).all()

# ===============================
# USER SEARCH FOR SHARING
# ===============================

def search_users_for_sharing(db: Session, search_term: str, exclude_user_ids: Optional[List[int]] = None, limit: int = 20):
    """Search users by name or email for document sharing"""
    from app.users.models import User
    
    if exclude_user_ids is None:
        exclude_user_ids = []
    
    query = db.query(User).filter(
        and_(
            User.is_active == True,
            User.id.notin_(exclude_user_ids),
            or_(
                User.full_name.ilike(f"%{search_term}%"),
                User.email.ilike(f"%{search_term}%")
            )
        )
    )
    
    return query.limit(limit).all()

def get_document_permissions_summary(db: Session, document_id: int, user_id: int):
    """Get summary of document permissions and recent activity"""
    if not can_user_manage_access(db, document_id, user_id):
        return None
    
    document = get_document(db, document_id)
    if not document:
        return None
    
    # Get access permissions
    access_list = get_document_access_list(db, document_id, user_id)
    access_levels = {}
    for access in access_list:
        level = access.access_level
        access_levels[level] = access_levels.get(level, 0) + 1
    
    # Get recent shares
    recent_shares = db.query(models.DocumentShare).options(
        joinedload(models.DocumentShare.shared_by),
        joinedload(models.DocumentShare.shared_with)
    ).filter(models.DocumentShare.document_id == document_id).order_by(
        desc(models.DocumentShare.created_at)
    ).limit(5).all()
    
    return {
        "document_id": document_id,
        "document_name": document.name,
        "is_public": document.is_public,
        "total_users_with_access": len(access_list),
        "access_levels": access_levels,
        "recent_shares": recent_shares
    }
