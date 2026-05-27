from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID


class IssueBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    type: str = Field(..., pattern="^(epic|story|task|bug|subtask)$")
    priority: str = Field(default="medium", pattern="^(lowest|low|medium|high|highest)$")
    status: str
    assignee_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    team_id: Optional[UUID] = None
    story_points: Optional[int] = Field(None, ge=0, le=100)
    is_flagged: Optional[int] = Field(0, ge=0, le=1)
    start_date: Optional[date] = None
    due_date: Optional[date] = None


class IssueCreate(IssueBase):
    workspace_id: UUID
    project_id: UUID
    parent_issue_id: Optional[UUID] = None
    label_ids: Optional[List[UUID]] = []


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    type: Optional[str] = Field(None, pattern="^(epic|story|task|bug|subtask)$")
    priority: Optional[str] = Field(None, pattern="^(lowest|low|medium|high|highest)$")
    status: Optional[str] = None
    assignee_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    team_id: Optional[UUID] = None
    story_points: Optional[int] = Field(None, ge=0, le=100)
    is_flagged: Optional[int] = Field(None, ge=0, le=1)
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    parent_issue_id: Optional[UUID] = None


class IssueResponse(IssueBase):
    id: UUID
    workspace_id: UUID
    project_id: UUID
    parent_issue_id: Optional[UUID] = None
    issue_number: int
    issue_key: str
    reporter_id: Optional[UUID] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
