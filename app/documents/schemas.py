from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    name: str
    file_type: str
    component_id: Optional[int] = None
    task_id: Optional[int] = None

class DocumentCreate(DocumentBase):
    storage_path: str
    uploaded_by_id: int

class Document(DocumentBase):
    id: int
    storage_path: str
    uploaded_by_id: int
    created_at: datetime

    class Config:
        orm_mode = True
