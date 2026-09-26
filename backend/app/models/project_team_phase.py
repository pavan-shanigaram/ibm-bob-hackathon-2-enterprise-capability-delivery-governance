import enum
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Enum as SAEnum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class PhaseStatus(str, enum.Enum):
    NotStarted = "NotStarted"
    InProgress = "InProgress"
    Done = "Done"
    Blocked = "Blocked"


class ProjectTeamPhase(Base):
    __tablename__ = "project_team_phases"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    phase_name: Mapped[str] = mapped_column(String(200), nullable=False)
    planned_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    planned_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[PhaseStatus] = mapped_column(
        SAEnum(PhaseStatus, name="phasestatus"),
        nullable=False,
        default=PhaseStatus.NotStarted,
        server_default=PhaseStatus.NotStarted.value,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project")
    team: Mapped["Team"] = relationship("Team")
