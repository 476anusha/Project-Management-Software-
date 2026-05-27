from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class AttachmentBase(BaseModel):
    file_url: str


class AttachmentCreate(AttachmentBase):
    issue_id: UUID


class AttachmentResponse(AttachmentBase):
    id: UUID
    issue_id: UUID
    uploader_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True
