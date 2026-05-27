from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    permissions = Column(JSONB, nullable=False)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="roles")
    workspace_members = relationship("WorkspaceMember", back_populates="role")
    project_members = relationship("ProjectMember", back_populates="role")
