from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceUpdate(WorkspaceBase):
    pass

class WorkspaceResponse(WorkspaceBase):
    id: UUID
    slug: str
    owner_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True

class WorkspaceNameResponse(BaseModel):
    name: str
