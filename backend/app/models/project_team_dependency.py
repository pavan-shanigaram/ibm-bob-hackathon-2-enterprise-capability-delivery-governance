import enum
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Enum as SAEnum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class DependencyType(str, enum.Enum):
    Blocker = "Blocker"
    Parallel = "Parallel"
    Sequential = "Sequential"


class DependencyStatus(str, enum.Enum):
    Pending = "Pending"
    Resolved = "Resolved"


class ProjectTeamDependency(Base):
    __tablename__ = "project_team_dependencies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    from_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    to_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    dependency_type: Mapped[DependencyType] = mapped_column(
        SAEnum(DependencyType, name="dependencytype"),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[DependencyStatus] = mapped_column(
        SAEnum(DependencyStatus, name="dependencystatus"),
        nullable=False,
        default=DependencyStatus.Pending,
        server_default=DependencyStatus.Pending.value,
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project")
    from_team: Mapped["Team"] = relationship("Team", foreign_keys=[from_team_id])
    to_team: Mapped["Team"] = relationship("Team", foreign_keys=[to_team_id])
