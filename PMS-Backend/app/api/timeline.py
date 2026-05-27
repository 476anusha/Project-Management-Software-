from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.issue import Issue
from app.models.project import Project

router = APIRouter(prefix="/projects", tags=["timeline"])


@router.get("/{project_id}/timeline")
async def get_project_timeline(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get timeline data for a project, grouped by epics.
    Returns epics with their child issues that have start_date or due_date.
    """
    
    # Verify project exists
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all epics for this project
    epics_result = await db.execute(
        select(Issue).where(
            Issue.project_id == project_id,
            Issue.type == "epic"
        ).order_by(Issue.created_at)
    )
    epics = epics_result.scalars().all()
    
    timeline_data = {
        "epics": []
    }
    
    for epic in epics:
        # Get all issues that belong to this epic and have dates
        issues_result = await db.execute(
            select(Issue).where(
                Issue.project_id == project_id,
                Issue.parent_issue_id == epic.id
            ).order_by(Issue.start_date.nullsfirst(), Issue.due_date.nullsfirst())
        )
        issues = issues_result.scalars().all()
        
        # Filter issues that have at least start_date or due_date
        dated_issues = [
            issue for issue in issues 
            if issue.start_date is not None or issue.due_date is not None
        ]
        
        # Only include epic if it has dated issues
        if dated_issues:
            epic_data = {
                "id": str(epic.id),
                "title": epic.title,
                "key": epic.issue_key,
                "issues": [
                    {
                        "id": str(issue.id),
                        "title": issue.title,
                        "key": issue.issue_key,
                        "type": issue.type,
                        "status": issue.status,
                        "priority": issue.priority,
                        "start_date": issue.start_date.isoformat() if issue.start_date else None,
                        "end_date": issue.due_date.isoformat() if issue.due_date else None,
                        "due_date": issue.due_date.isoformat() if issue.due_date else None,
                        "assignee_id": str(issue.assignee_id) if issue.assignee_id else None,
                        "story_points": issue.story_points,
                    }
                    for issue in dated_issues
                ]
            }
            timeline_data["epics"].append(epic_data)
    
    return timeline_data
