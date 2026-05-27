from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    workspace_id: UUID


class TeamResponse(TeamBase):
    id: UUID
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
