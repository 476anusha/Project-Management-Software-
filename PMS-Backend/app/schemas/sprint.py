from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from uuid import UUID


class SprintBase(BaseModel):
    name: str
    goal: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = 'planned'  # planned, active, completed


class SprintCreate(SprintBase):
    project_id: UUID


class SprintResponse(SprintBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
