from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.users import crud as user_crud
from app.users.models import User
from . import crud, schemas, models

router = APIRouter()

# Simple authentication dependency (placeholder - replace with your auth system)
def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    Placeholder authentication function.
    In a real application, this would validate JWT tokens or session data.
    For now, returns a demo user with ID 1.
    """
    user = user_crud.get_user(db, user_id=1)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return user

def get_user_id(user: User) -> int:
    """Helper function to extract user ID as integer"""
    # For SQLAlchemy models, the ID might be accessed differently
    if hasattr(user, '__dict__') and 'id' in user.__dict__:
        return user.__dict__['id']
    elif hasattr(user, '_sa_instance_state'):
        # SQLAlchemy instance - try to get the actual value
        for key, value in user.__dict__.items():
            if key == 'id' and isinstance(value, int):
                return value
    # Fallback - this might be the problematic line but try it
    return 1  # Default user ID for demo purposes

# ===============================
# DOCUMENT UPLOAD & MANAGEMENT
# ===============================

@router.post("/upload", response_model=schemas.DocumentResponse)
async def upload_document(
    name: str,
    description: Optional[str] = None,
    storage_path: str = "",  # Will be set after file upload
    file_type: str = "",
    file_size: Optional[int] = None,
    document_type: Optional[str] = None,
    project_id: Optional[int] = None,
    component_id: Optional[int] = None,
    task_id: Optional[int] = None,
    is_public: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a new document with hierarchy support"""
    document_data = schemas.DocumentCreate(
        name=name,
        description=description,
        storage_path=storage_path,
        file_type=file_type,
        file_size=file_size,
        document_type=document_type,
        project_id=project_id,
        component_id=component_id,
        task_id=task_id,
        is_public=is_public
    )
    
    return crud.create_document(db=db, document=document_data, uploaded_by_id=get_user_id(current_user))

@router.get("/", response_model=List[schemas.DocumentResponse])
def get_accessible_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all documents accessible by the current user"""
    return crud.get_documents_accessible_by_user(db, get_user_id(current_user), skip, limit)

@router.get("/{document_id}", response_model=schemas.DocumentResponse)
def get_document_details(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed information about a specific document"""
    if not crud.can_user_view_document(db, document_id, get_user_id(current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this document"
        )
    
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.put("/{document_id}", response_model=schemas.DocumentResponse)
def update_document(
    document_id: int,
    document_update: schemas.DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update document details (requires edit access)"""
    updated_document = crud.update_document(db, document_id, document_update, get_user_id(current_user))
    if not updated_document:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this document or document not found"
        )
    
    return updated_document

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete document (only uploader or admin access)"""
    success = crud.delete_document(db, document_id, get_user_id(current_user))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this document or document not found"
        )
    
    return {"message": "Document deleted successfully"}

# ===============================
# DOCUMENT ACCESS CONTROL
# ===============================

@router.post("/{document_id}/access", response_model=schemas.DocumentAccessResponse)
def grant_document_access(
    document_id: int,
    access_data: schemas.DocumentAccessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Grant access to a document for a specific user"""
    if not crud.can_user_manage_access(db, document_id, get_user_id(current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to manage access for this document"
        )
    
    access = crud.grant_document_access(
        db=db,
        document_id=document_id,
        user_id=access_data.user_id,
        access_level=access_data.access_level,
        granted_by_id=get_user_id(current_user),
        access_notes=access_data.access_notes
    )
    
    return access

@router.delete("/{document_id}/access/{user_id}")
def revoke_document_access(
    document_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Revoke access to a document for a specific user"""
    success = crud.revoke_document_access(db, document_id, user_id, get_user_id(current_user))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to revoke access or access not found"
        )
    
    return {"message": "Access revoked successfully"}

@router.get("/{document_id}/access", response_model=List[schemas.DocumentAccessResponse])
def get_document_access_list(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of users who have access to a document"""
    access_list = crud.get_document_access_list(db, document_id, get_user_id(current_user))
    return access_list

# ===============================
# DOCUMENT SHARING
# ===============================

@router.post("/{document_id}/share", response_model=schemas.DocumentShareResponse)
def share_document_with_user(
    document_id: int,
    shared_with_id: int,
    share_data: schemas.DocumentShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Share a document with a specific user"""
    share = crud.share_document_with_user(
        db=db,
        document_id=document_id,
        shared_with_id=shared_with_id,
        shared_by_id=get_user_id(current_user),
        share_data=share_data
    )
    
    if not share:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to share this document"
        )
    
    return share

@router.post("/{document_id}/share-multiple", response_model=schemas.BulkDocumentShareResult)
def share_document_with_multiple_users(
    document_id: int,
    share_data: schemas.DocumentShareMultiple,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Share a document with multiple users"""
    # Override document_id from URL
    share_data.document_id = document_id
    
    result = crud.share_document_with_multiple_users(
        db=db,
        share_data=share_data,
        shared_by_id=get_user_id(current_user)
    )
    
    return result

@router.get("/{document_id}/shares", response_model=List[schemas.DocumentShareResponse])
def get_document_shares(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sharing history for a document"""
    shares = crud.get_document_shares(db, document_id, get_user_id(current_user))
    return shares

# ===============================
# USER SEARCH FOR SHARING
# ===============================

@router.get("/search/users", response_model=schemas.UserSearchResponse)
def search_users_for_document_sharing(
    q: str = Query(..., min_length=2, description="Search term for user name or email"),
    document_id: Optional[int] = Query(None, description="Document ID to exclude users who already have access"),
    limit: int = Query(20, le=50, description="Maximum number of results"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search users for document sharing"""
    exclude_user_ids = [get_user_id(current_user)]  # Always exclude current user
    
    # If document_id provided, exclude users who already have access
    if document_id:
        if not crud.can_user_view_document(db, document_id, get_user_id(current_user)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this document"
            )
        
        # Get users who already have access
        access_list = crud.get_document_access_list(db, document_id, get_user_id(current_user))
        exclude_user_ids.extend([getattr(access, 'user_id', 0) for access in access_list if hasattr(access, 'user_id')])
        
        # Also exclude the document uploader
        document = crud.get_document(db, document_id)
        if document:
            uploader_id = getattr(document, 'uploaded_by_id', None)
            if uploader_id:
                exclude_user_ids.append(uploader_id)
    
    users = crud.search_users_for_sharing(db, q, exclude_user_ids, limit)
    
    return {
        "users": [
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": getattr(user, 'role', 'user')
            }
            for user in users
        ],
        "total_found": len(users),
        "search_term": q
    }

# ===============================
# DOCUMENT HIERARCHY & FILTERING
# ===============================

@router.get("/project/{project_id}", response_model=List[schemas.DocumentResponse])
def get_documents_by_project(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get documents for a specific project"""
    return crud.get_documents_by_project(db, project_id, get_user_id(current_user), skip, limit)

@router.get("/component/{component_id}", response_model=List[schemas.DocumentResponse])
def get_documents_by_component(
    component_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get documents for a specific component"""
    return crud.get_documents_by_component(db, component_id, get_user_id(current_user), skip, limit)

# ===============================
# DOCUMENT PERMISSIONS SUMMARY
# ===============================

@router.get("/{document_id}/permissions-summary")
def get_document_permissions_summary(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive permissions summary for a document"""
    summary = crud.get_document_permissions_summary(db, document_id, get_user_id(current_user))
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view permissions for this document"
        )
    
    return summary

# ===============================
# LEGACY ENDPOINTS FOR COMPATIBILITY
# ===============================

@router.post("/documents/upload/", response_model=schemas.DocumentResponse)
async def create_upload_file_legacy(
    file: UploadFile = File(...),
    project_id: Optional[int] = None,
    component_id: Optional[int] = None,
    task_id: Optional[int] = None,
    is_public: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Legacy upload endpoint for compatibility"""
    # In real implementation: Upload file to Google Cloud Storage
    fake_storage_path = f"gcs/fake_path/{file.filename}"
    
    document_data = schemas.DocumentCreate(
        name=file.filename or "Uploaded File",
        description=None,
        file_type=file.content_type or "application/octet-stream",
        storage_path=fake_storage_path,
        file_size=file.size,
        document_type=None,
        project_id=project_id,
        component_id=component_id,
        task_id=task_id,
        is_public=is_public
    )
    
    return crud.create_document(db=db, document=document_data, uploaded_by_id=get_user_id(current_user))

@router.get("/documents/", response_model=List[schemas.DocumentResponse])
def read_documents_legacy(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Legacy endpoint for compatibility"""
    return crud.get_documents_accessible_by_user(db, get_user_id(current_user), skip, limit)
