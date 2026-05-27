from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    key: Optional[str] = None

class ProjectCreate(ProjectBase):
    workspace_id: UUID

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    key: Optional[str] = None
    # For template selection
    template_id: Optional[str] = None 

class ProjectResponse(ProjectBase):
    id: UUID
    workspace_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class InviteMembers(BaseModel):
    emails: List[str]

class ProjectNameResponse(BaseModel):
    name: str
