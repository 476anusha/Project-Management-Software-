from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Label(Base):
    __tablename__ = "labels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    color = Column(String(7))
    
    __table_args__ = (
        UniqueConstraint('workspace_id', 'name', name='uix_workspace_label_name'),
    )
    
    # Relationships
    workspace = relationship("Workspace", back_populates="labels")
    issues = relationship("IssueLabel", back_populates="label")
