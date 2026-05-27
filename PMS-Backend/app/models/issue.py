from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    parent_issue_id = Column(UUID(as_uuid=True), ForeignKey("issues.id", ondelete="SET NULL"))
    issue_number = Column(Integer, nullable=False)
    issue_key = Column(String(30), nullable=False, unique=True, index=True)
    type = Column(String(20), nullable=False)  # epic, story, task, bug, subtask
    title = Column(String(255), nullable=False)
    description = Column(String)
    status = Column(String(50), nullable=False)
    priority = Column(String(20), default='medium')
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    sprint_id = Column(UUID(as_uuid=True), ForeignKey("sprints.id", ondelete="SET NULL"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="SET NULL"))
    story_points = Column(Integer)
    is_flagged = Column(Integer, default=0)  # 0 = not flagged, 1 = flagged/impediment
    start_date = Column(Date)
    due_date = Column(Date)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    __table_args__ = (
        UniqueConstraint('project_id', 'issue_number', name='uix_project_issue_number'),
        Index('ix_issues_project_id', 'project_id'),
        Index('ix_issues_assignee_id', 'assignee_id'),
        Index('ix_issues_parent_issue_id', 'parent_issue_id'),
    )
    
    # Relationships
    project = relationship("Project", back_populates="issues")
    assignee = relationship("User", back_populates="assigned_issues", foreign_keys=[assignee_id])
    reporter = relationship("User", back_populates="reported_issues", foreign_keys=[reporter_id])
    parent_issue = relationship("Issue", remote_side=[id], backref="sub_issues")
    sprint = relationship("Sprint", back_populates="issues")
    team = relationship("Team", back_populates="issues")
    comments = relationship("Comment", back_populates="issue")
    attachments = relationship("Attachment", back_populates="issue")
    issue_assignments = relationship("IssueAssignment", back_populates="issue")
    labels = relationship("IssueLabel", back_populates="issue")
    source_links = relationship("IssueLink", foreign_keys="IssueLink.source_issue_id", back_populates="source_issue")
    target_links = relationship("IssueLink", foreign_keys="IssueLink.target_issue_id", back_populates="target_issue")
