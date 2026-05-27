from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


class PersonalizationRequest(BaseModel):
    persona: str
    work_style: str


class WorkspaceRequest(BaseModel):
    name: str
    description: Optional[str] = None


class TemplateRequest(BaseModel):
    template: str


class InviteRequest(BaseModel):
    emails: List[str]


@router.post("/personalization")
async def save_personalization(
    data: PersonalizationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save user personalization preferences"""
    # For now, just acknowledge the data
    return {"message": "Personalization saved", "data": data.dict()}


@router.post("/workspace")
async def create_workspace_stub(
    data: WorkspaceRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create initial workspace during onboarding"""
    # For now, just acknowledge the data
    return {"message": "Workspace created", "data": data.dict()}

@router.put("/complete")
async def complete_onboarding(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark onboarding as completed"""
    current_user.onboarding_completed = True
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return {"message": "Onboarding completed", "user": {"id": str(current_user.id), "onboarding_completed": True}}



@router.post("/template")
async def save_template(
    data: TemplateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save selected template"""
    # For now, just acknowledge the data
    return {"message": "Template saved", "data": data.dict()}


@router.post("/invite")
async def send_invites(
    data: InviteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send team invites"""
    # For now, just acknowledge the data
    return {"message": "Invites sent", "emails": data.emails}


@router.put("/complete")
async def complete_onboarding(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark onboarding as completed for the user"""
    try:
        # Update user in DB
        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(onboarding_completed=True)
        )
        await db.execute(stmt)
        await db.commit()
        
        return {"message": "Onboarding completed successfully", "onboarding_completed": True}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
