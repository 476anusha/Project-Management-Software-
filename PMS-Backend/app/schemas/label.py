from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class LabelBase(BaseModel):
    name: str
    color: Optional[str] = None


class LabelCreate(LabelBase):
    workspace_id: UUID


class LabelResponse(LabelBase):
    id: UUID
    workspace_id: UUID

    class Config:
        from_attributes = True
