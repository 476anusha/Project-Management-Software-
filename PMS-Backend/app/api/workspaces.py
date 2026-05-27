from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import re

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.role import Role
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate, WorkspaceNameResponse

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

def generate_slug(name: str) -> str:
    # Simple slug generation
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    return slug

@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_in: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if slug exists
    base_slug = generate_slug(workspace_in.name)
    slug = base_slug
    counter = 1
    
    while True:
        result = await db.execute(select(Workspace).where(Workspace.slug == slug))
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    new_workspace = Workspace(
        name=workspace_in.name,
        slug=slug,
        owner_id=current_user.id,
        # description=workspace_in.description # Model doesn't have description in the provided file content, checking...
    )
    # Double check Workspace model content I read earlier.
    # It had: name, slug, owner_id, settings, created_at. No description.
    # But schema has description. I will ignore description for now or store in settings?
    # I'll store it in settings for now since the model table definition is fixed.
    
    if workspace_in.description:
        new_workspace.settings = {"description": workspace_in.description}

    db.add(new_workspace)
    await db.commit()
    await db.refresh(new_workspace)

    # Add owner as member with Admin role
    # Need to find or create Admin role first? 
    # Usually roles are per workspace.
    
    # 1. Create default roles for this workspace
    admin_role = Role(name="Admin", workspace_id=new_workspace.id, permissions={"all": True})
    member_role = Role(name="Member", workspace_id=new_workspace.id, permissions={"read": True, "write": True})
    
    db.add(admin_role)
    db.add(member_role)
    await db.commit()
    await db.refresh(admin_role)

    # 2. Add user to workspace
    member = WorkspaceMember(
        workspace_id=new_workspace.id,
        user_id=current_user.id,
        role_id=admin_role.id
    )
    db.add(member)
    await db.commit()

    return new_workspace

@router.get("", response_model=List[WorkspaceResponse])
async def get_workspaces(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Workspace)
        .join(WorkspaceMember)
        .where(WorkspaceMember.user_id == current_user.id)
    )
    return result.scalars().all()

# add
@router.get("/{workspace_id}", response_model=WorkspaceNameResponse)
async def get_workspace_by_id(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Workspace.name)
        .join(WorkspaceMember)
        .where(
            Workspace.id == workspace_id,
            WorkspaceMember.user_id == current_user.id
        )
    )
    name = result.scalar_one_or_none()

    if not name:
        raise HTTPException(status_code=404, detail="Workspace not found")

    return {"name": name}
