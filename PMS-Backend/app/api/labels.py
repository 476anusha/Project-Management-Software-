from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.label import Label
from app.schemas.label import LabelCreate, LabelResponse, LabelBase

router = APIRouter(prefix="/labels", tags=["labels"])


@router.post("", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
async def create_label(
    label_in: LabelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new label in a workspace"""
    new_label = Label(
        workspace_id=label_in.workspace_id,
        name=label_in.name,
        color=label_in.color,
    )
    
    db.add(new_label)
    await db.commit()
    await db.refresh(new_label)
    
    return new_label


@router.get("/workspace/{workspace_id}", response_model=List[LabelResponse])
async def get_workspace_labels(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all labels in a workspace"""
    result = await db.execute(
        select(Label).where(Label.workspace_id == workspace_id)
    )
    return result.scalars().all()


@router.post("/workspace/{workspace_id}/find-or-create", response_model=LabelResponse)
async def find_or_create_label(
    workspace_id: str,
    label_in: LabelBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Find existing label by name or create new one"""
    # Try to find existing label
    result = await db.execute(
        select(Label).where(
            Label.workspace_id == workspace_id,
            Label.name == label_in.name
        )
    )
    existing_label = result.scalar_one_or_none()
    
    if existing_label:
        return existing_label
    
    # Create new label
    new_label = Label(
        workspace_id=workspace_id,
        name=label_in.name,
        color=label_in.color or '#808080',
    )
    
    db.add(new_label)
    await db.commit()
    await db.refresh(new_label)
    
    return new_label


@router.get("/{label_id}", response_model=LabelResponse)
async def get_label(
    label_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific label by ID"""
    result = await db.execute(
        select(Label).where(Label.id == label_id)
    )
    label = result.scalar_one_or_none()
    
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    
    return label
