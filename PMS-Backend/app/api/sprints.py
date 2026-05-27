from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.sprint import Sprint
from app.schemas.sprint import SprintCreate, SprintResponse

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.post("", response_model=SprintResponse, status_code=status.HTTP_201_CREATED)
async def create_sprint(
    sprint_in: SprintCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new sprint in a project"""
    new_sprint = Sprint(
        project_id=sprint_in.project_id,
        name=sprint_in.name,
        goal=sprint_in.goal,
        start_date=sprint_in.start_date,
        end_date=sprint_in.end_date,
        status=sprint_in.status,
    )
    
    db.add(new_sprint)
    await db.commit()
    await db.refresh(new_sprint)
    
    return new_sprint


@router.get("/project/{project_id}", response_model=List[SprintResponse])
async def get_project_sprints(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all sprints in a project"""
    result = await db.execute(
        select(Sprint).where(Sprint.project_id == project_id)
    )
    return result.scalars().all()


@router.get("/{sprint_id}", response_model=SprintResponse)
async def get_sprint(
    sprint_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific sprint by ID"""
    result = await db.execute(
        select(Sprint).where(Sprint.id == sprint_id)
    )
    sprint = result.scalar_one_or_none()
    
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    return sprint
