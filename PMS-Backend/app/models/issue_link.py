from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class IssueLink(Base):
    __tablename__ = "issue_links"
    
    source_issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="CASCADE"), primary_key=True)
    target_issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="CASCADE"), primary_key=True)
    link_type = Column(String(30), primary_key=True)  # blocks, duplicates, relates
    
    # Relationships
    source_issue = relationship("Issue", foreign_keys=[source_issue_id], back_populates="source_links")
    target_issue = relationship("Issue", foreign_keys=[target_issue_id], back_populates="target_links")
