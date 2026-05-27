from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import re

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User as UserModel
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.workspace import Workspace
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, InviteMembers, ProjectNameResponse
from app.schemas.user import User

router = APIRouter(prefix="/projects", tags=["projects"])

def generate_key(name: str) -> str:
    # Simple key generation: "My Project" -> "MP" or "MYPROJ"
    # Take first 3 chars upper
    clean = re.sub(r'[^a-zA-Z0-9]', '', name).upper()
    if len(clean) >= 3:
        return clean[:3]
    return (clean + "PRJ")[:3]

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify workspace membership
    # In a real app, check if user has permission to create projects in this workspace
    
    # Check if key exists in workspace
    base_key = project_in.key if project_in.key else generate_key(project_in.name)
    key = base_key
    counter = 1
    
    while True:
        result = await db.execute(
            select(Project).where(
                Project.workspace_id == project_in.workspace_id,
                Project.key == key
            )
        )
        if not result.scalar_one_or_none():
            break
        key = f"{base_key}{counter}"
        counter += 1

    new_project = Project(
        name=project_in.name,
        key=key,
        workspace_id=project_in.workspace_id,
        settings={"description": project_in.description} if project_in.description else {}
    )
    
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    if project_in.name:
        project.name = project_in.name
    
    # If template_id is provided, store it in settings (assuming template logic is part of settings for now)
    if project_in.template_id:
        if project.settings is None:
            project.settings = {}
        # Ensure settings is a copy if it's a dict to modify it
        settings = dict(project.settings)
        settings["template_id"] = project_in.template_id
        project.settings = settings

    await db.commit()
    await db.refresh(project)
    return project

@router.post("/{project_id}/invites")
async def invite_members(
    project_id: str,
    invite_in: InviteMembers,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Placeholder for actual email invitation logic
    # In a real app, this would send emails and create pending invitations
    return {"message": f"Invited {len(invite_in.emails)} members"}

@router.get("/{project_id}/members", response_model=List[User])
async def get_project_members(
    project_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all members of a project"""
    try:
        # Check if project exists first
        project_result = await db.execute(select(Project).where(Project.id == project_id))
        if not project_result.scalar_one_or_none():
             raise HTTPException(status_code=404, detail="Project not found")

        # Get members
        result = await db.execute(
            select(UserModel)
            .join(ProjectMember, UserModel.id == ProjectMember.user_id)
            .where(ProjectMember.project_id == project_id)
        )
        return result.scalars().all()
    except Exception as e:
         # If invalid UUID
         raise HTTPException(status_code=400, detail=str(e))


@router.get("/workspace/{workspace_id}", response_model=List[ProjectResponse])
async def get_projects_by_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.workspace_id == workspace_id)
    )
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_by_id(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.get("/workspace/{workspace_id}", response_model=List[ProjectResponse])
async def get_projects_by_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.workspace_id == workspace_id)
    )
    return result.scalars().all()
