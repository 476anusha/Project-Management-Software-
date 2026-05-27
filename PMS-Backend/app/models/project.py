from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    key = Column(String(10), nullable=False)
    settings = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('workspace_id', 'key', name='uix_workspace_project_key'),
    )
    
    # Relationships
    workspace = relationship("Workspace", back_populates="projects")
    issues = relationship("Issue", back_populates="project")
    boards = relationship("Board", back_populates="project")
    members = relationship("ProjectMember", back_populates="project")
    sprints = relationship("Sprint", back_populates="project")
