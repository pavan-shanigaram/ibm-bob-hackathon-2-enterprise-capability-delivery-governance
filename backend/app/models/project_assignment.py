from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ProjectSquadAssignment(Base):
    __tablename__ = "project_squad_assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squads.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="squad_assignments")
    squad: Mapped["Squad"] = relationship("Squad", back_populates="project_assignments")


class ProjectEmployeeAssignment(Base):
    __tablename__ = "project_employee_assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    allocation_percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=100.0)
    role_on_project: Mapped[str | None] = mapped_column(String(100))
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="employee_assignments")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="project_assignments")
