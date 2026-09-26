import enum
from datetime import date, datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum
from app.core.database import Base


class ProjectStatus(str, enum.Enum):
    Draft = "Draft"
    Active = "Active"
    OnHold = "OnHold"
    Completed = "Completed"
    Cancelled = "Cancelled"


class ProjectPriority(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"


class HealthIndicator(str, enum.Enum):
    Green = "Green"
    Amber = "Amber"
    Red = "Red"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(SAEnum(ProjectStatus), default=ProjectStatus.Draft)
    priority: Mapped[ProjectPriority] = mapped_column(SAEnum(ProjectPriority), default=ProjectPriority.Medium)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    owner_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    owner_squad_id: Mapped[int | None] = mapped_column(ForeignKey("squads.id"), nullable=True)
    health_indicator: Mapped[HealthIndicator] = mapped_column(SAEnum(HealthIndicator), default=HealthIndicator.Green)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    owner_team: Mapped["Team"] = relationship("Team", foreign_keys=[owner_team_id])
    squad_assignments: Mapped[list["ProjectSquadAssignment"]] = relationship("ProjectSquadAssignment", back_populates="project")
    employee_assignments: Mapped[list["ProjectEmployeeAssignment"]] = relationship("ProjectEmployeeAssignment", back_populates="project")
    delivery_metrics: Mapped[list["DeliveryMetric"]] = relationship("DeliveryMetric", back_populates="project")
    capability_requirements: Mapped[list["CapabilityRequirement"]] = relationship("CapabilityRequirement", back_populates="project")
    resource_allocations: Mapped[list["ResourceAllocation"]] = relationship("ResourceAllocation", back_populates="project")
