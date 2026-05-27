from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.issue import Issue
from app.models.project import Project
from app.models.label import Label
from app.models.issue_label import IssueLabel
from app.schemas.issue import IssueCreate, IssueResponse, IssueUpdate

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    issue_in: IssueCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new issue in a project"""
    
    # Log incoming data for debugging
    print(f"Creating issue with data: {issue_in.model_dump()}")
    
    # Verify project exists
    result = await db.execute(
        select(Project).where(Project.id == issue_in.project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verify project belongs to workspace
    if str(project.workspace_id) != str(issue_in.workspace_id):
        raise HTTPException(
            status_code=400, 
            detail="Project does not belong to the specified workspace"
        )
    
    # Get next issue number for this project
    result = await db.execute(
        select(func.max(Issue.issue_number)).where(
            Issue.project_id == issue_in.project_id
        )
    )
    max_issue_number = result.scalar()
    next_issue_number = (max_issue_number or 0) + 1
    
    # Generate issue key (e.g., PROJ-1)
    issue_key = f"{project.key}-{next_issue_number}"
    
    # Create the issue
    new_issue = Issue(
        workspace_id=issue_in.workspace_id,
        project_id=issue_in.project_id,
        parent_issue_id=issue_in.parent_issue_id,
        issue_number=next_issue_number,
        issue_key=issue_key,
        title=issue_in.title,
        description=issue_in.description,
        type=issue_in.type,
        priority=issue_in.priority,
        status=issue_in.status,
        assignee_id=issue_in.assignee_id,
        reporter_id=current_user.id,
        sprint_id=issue_in.sprint_id,
        team_id=issue_in.team_id,
        story_points=issue_in.story_points,
        is_flagged=issue_in.is_flagged,
        start_date=issue_in.start_date,
        due_date=issue_in.due_date,
    )
    
    db.add(new_issue)
    await db.commit()
    await db.refresh(new_issue)
    
    print(f"Created issue: ID={new_issue.id}, Key={new_issue.issue_key}, Title={new_issue.title}")
    print(f"Issue details: sprint_id={new_issue.sprint_id}, team_id={new_issue.team_id}, story_points={new_issue.story_points}, is_flagged={new_issue.is_flagged}")
    
    # Add labels if provided
    if issue_in.label_ids:
        print(f"Adding {len(issue_in.label_ids)} labels to issue")
        for label_id in issue_in.label_ids:
            issue_label = IssueLabel(issue_id=new_issue.id, label_id=label_id)
            db.add(issue_label)
        await db.commit()
        print(f"Labels added successfully")
    
    return new_issue


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific issue by ID"""
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    issue = result.scalar_one_or_none()
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return issue


@router.get("", response_model=List[IssueResponse])
async def list_issues(
    project_id: str = None,
    workspace_id: str = None,
    status: str = None,
    assignee_id: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List issues with optional filters"""
    query = select(Issue)
    
    if project_id:
        query = query.where(Issue.project_id == project_id)
    
    if workspace_id:
        query = query.where(Issue.workspace_id == workspace_id)
    
    if status:
        query = query.where(Issue.status == status)
    
    if assignee_id:
        query = query.where(Issue.assignee_id == assignee_id)
    
    query = query.order_by(Issue.created_at.desc())
    
    result = await db.execute(query)
    issues = result.scalars().all()
    
    return issues


@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: str,
    issue_in: IssueUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing issue"""
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    issue = result.scalar_one_or_none()
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Update fields
    update_data = issue_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(issue, field, value)
    
    # Mark as completed if status changed to 'done'
    if issue_in.status == 'done' and issue.completed_at is None:
        issue.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(issue)
    
    return issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an issue (soft delete by setting deleted_at)"""
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    issue = result.scalar_one_or_none()
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Soft delete
    issue.deleted_at = datetime.utcnow()
    
    await db.commit()
    
    return None
