from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class IssueAssignment(Base):
    __tablename__ = "issue_assignments"
    
    issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(30))
    
    # Relationships
    issue = relationship("Issue", back_populates="issue_assignments")
    user = relationship("User", back_populates="issue_assignments")
