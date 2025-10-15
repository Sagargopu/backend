from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# ===============================
# DOCUMENT SCHEMAS
# ===============================

class DocumentBase(BaseModel):
    name: str = Field(..., description="Document name")
    description: Optional[str] = Field(None, description="Document description")
    document_type: Optional[str] = Field(None, description="Type of document (blueprint, contract, report, etc.)")
    is_public: bool = Field(False, description="Whether document is publicly accessible to all users")

class DocumentCreate(DocumentBase):
    storage_path: str = Field(..., description="Storage path in cloud")
    file_type: str = Field(..., description="MIME type of the file")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    project_id: Optional[int] = Field(None, description="Associated project ID")
    component_id: Optional[int] = Field(None, description="Associated component ID")
    task_id: Optional[int] = Field(None, description="Associated task ID")

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    document_type: Optional[str] = None
    is_public: Optional[bool] = None

class DocumentResponse(DocumentBase):
    id: int
    storage_path: str
    file_type: str
    file_size: Optional[int]
    project_id: Optional[int]
    component_id: Optional[int]
    task_id: Optional[int]
    uploaded_by_id: int
    uploader_name: Optional[str] = None
    project_name: Optional[str] = None
    component_name: Optional[str] = None
    task_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Access control info
    can_edit: bool = False
    can_share: bool = False
    access_level: Optional[str] = None

    class Config:
        from_attributes = True

# ===============================
# DOCUMENT ACCESS SCHEMAS
# ===============================

class DocumentAccessBase(BaseModel):
    access_level: str = Field("view", description="Access level: view, edit, admin")
    access_notes: Optional[str] = Field(None, description="Notes about the access")

class DocumentAccessCreate(DocumentAccessBase):
    document_id: int
    user_id: int

class DocumentAccessResponse(DocumentAccessBase):
    id: int
    document_id: int
    user_id: int
    granted_by_id: int
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    granted_by_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ===============================
# DOCUMENT SHARING SCHEMAS
# ===============================

class DocumentShareBase(BaseModel):
    share_message: Optional[str] = Field(None, description="Message to include with share")
    share_type: str = Field("direct", description="Type of share: direct, project_wide, component_wide")
    is_temporary: bool = Field(False, description="Whether share is temporary")
    expires_at: Optional[datetime] = Field(None, description="When temporary share expires")

class DocumentShareCreate(DocumentShareBase):
    document_id: int
    shared_with_id: int

class DocumentShareMultiple(BaseModel):
    document_id: int
    user_ids: List[int] = Field(..., description="List of user IDs to share with")
    access_level: str = Field("view", description="Access level to grant")
    share_message: Optional[str] = None
    share_type: str = Field("direct")

class DocumentShareResponse(DocumentShareBase):
    id: int
    document_id: int
    shared_by_id: int
    shared_with_id: int
    document_name: Optional[str] = None
    shared_by_name: Optional[str] = None
    shared_with_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ===============================
# USER SEARCH SCHEMAS
# ===============================

class UserSearchResult(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    department: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class UserSearchResponse(BaseModel):
    users: List[UserSearchResult]
    total: int
    page: int
    per_page: int

# ===============================
# DOCUMENT HIERARCHY SCHEMAS
# ===============================

class DocumentHierarchy(BaseModel):
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    component_id: Optional[int] = None
    component_name: Optional[str] = None
    task_id: Optional[int] = None
    task_name: Optional[str] = None

class DocumentWithHierarchy(DocumentResponse):
    hierarchy: DocumentHierarchy

# ===============================
# BULK OPERATIONS SCHEMAS
# ===============================

class BulkDocumentShareResult(BaseModel):
    successful_shares: List[int] = Field(description="User IDs successfully shared with")
    failed_shares: List[dict] = Field(description="Failed shares with error details")
    total_attempted: int
    total_successful: int

class DocumentPermissionsSummary(BaseModel):
    document_id: int
    document_name: str
    is_public: bool
    total_users_with_access: int
    access_levels: dict = Field(description="Count of users by access level")
    recent_shares: List[DocumentShareResponse] = Field(description="Recent sharing activity")
