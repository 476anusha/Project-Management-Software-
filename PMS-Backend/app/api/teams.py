from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new team in a workspace"""
    new_team = Team(
        workspace_id=team_in.workspace_id,
        name=team_in.name,
        description=team_in.description,
    )
    
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)
    
    return new_team


@router.get("/workspace/{workspace_id}", response_model=List[TeamResponse])
async def get_workspace_teams(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all teams in a workspace"""
    result = await db.execute(
        select(Team).where(Team.workspace_id == workspace_id)
    )
    return result.scalars().all()


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific team by ID"""
    result = await db.execute(
        select(Team).where(Team.id == team_id)
    )
    team = result.scalar_one_or_none()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return team
