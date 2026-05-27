# Import all models here for Alembic to detect them
from app.core.database import Base
from app.models.user import User
from app.models.session import Session
from app.models.workspace import Workspace
from app.models.role import Role
from app.models.workspace_member import WorkspaceMember
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.issue import Issue
from app.models.issue_assignment import IssueAssignment
from app.models.issue_link import IssueLink
from app.models.comment import Comment
from app.models.attachment import Attachment
from app.models.label import Label
from app.models.issue_label import IssueLabel
from app.models.workflow import Workflow
from app.models.board import Board
from app.models.notification import Notification
from app.models.activity_log import ActivityLog
from app.models.audit_log import AuditLog
from app.models.team import Team
from app.models.sprint import Sprint

__all__ = [
    "Base",
    "User",
    "Session",
    "Workspace",
    "Role",
    "WorkspaceMember",
    "Project",
    "ProjectMember",
    "Issue",
    "IssueAssignment",
    "IssueLink",
    "Comment",
    "Attachment",
    "Label",
    "IssueLabel",
    "Workflow",
    "Board",
    "Notification",
    "ActivityLog",
    "AuditLog",
    "Team",
    "Sprint",
]
