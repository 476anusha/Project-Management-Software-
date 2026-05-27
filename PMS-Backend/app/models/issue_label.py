from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class IssueLabel(Base):
    __tablename__ = "issue_labels"
    
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="CASCADE"), primary_key=True)
    label_id = Column(UUID(as_uuid=True), ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    issue = relationship("Issue", back_populates="labels")
    label = relationship("Label", back_populates="issues")
