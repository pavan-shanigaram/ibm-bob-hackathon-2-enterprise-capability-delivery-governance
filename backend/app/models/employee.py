import enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Numeric, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum
from app.core.database import Base


class EmployeeRole(str, enum.Enum):
    Designer = "Designer"
    Developer = "Developer"
    BusinessAnalyst = "BusinessAnalyst"
    ScrumMaster = "ScrumMaster"
    PlatformEngineer = "PlatformEngineer"
    OperationsEngineer = "OperationsEngineer"
    QAEngineer = "QAEngineer"
    Architect = "Architect"


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    job_title: Mapped[str | None] = mapped_column(String(150))
    role: Mapped[EmployeeRole] = mapped_column(SAEnum(EmployeeRole), nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    auth0_user_id: Mapped[str | None] = mapped_column(String(200), unique=True, nullable=True)
    allocation_percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    team: Mapped["Team"] = relationship("Team", back_populates="employees", foreign_keys=[team_id])
    squad_memberships: Mapped[list["SquadMember"]] = relationship("SquadMember", back_populates="employee")
    skills: Mapped[list["EmployeeSkill"]] = relationship("EmployeeSkill", back_populates="employee")
    project_assignments: Mapped[list["ProjectEmployeeAssignment"]] = relationship("ProjectEmployeeAssignment", back_populates="employee")
    authorizations: Mapped[list["Authorization"]] = relationship("Authorization", back_populates="employee")
    resource_allocations: Mapped[list["ResourceAllocation"]] = relationship("ResourceAllocation", back_populates="employee")
