from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class IssueLinkBase(BaseModel):
    link_type: str  # blocks, is_blocked_by, clones, is_cloned_by, duplicates, is_duplicated_by, relates_to


class IssueLinkCreate(IssueLinkBase):
    source_issue_id: UUID
    target_issue_id: UUID


class IssueLinkResponse(IssueLinkBase):
    source_issue_id: UUID
    target_issue_id: UUID

    class Config:
        from_attributes = True
