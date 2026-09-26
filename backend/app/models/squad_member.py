import enum
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum, String
from app.core.database import Base


class SquadRoleEnum(str, enum.Enum):
    Designer = "Designer"
    Developer = "Developer"
    BusinessAnalyst = "BusinessAnalyst"
    ScrumMaster = "ScrumMaster"
    PlatformEngineer = "PlatformEngineer"
    OperationsEngineer = "OperationsEngineer"
    QAEngineer = "QAEngineer"
    Architect = "Architect"
    Lead = "Lead"


class SquadMember(Base):
    __tablename__ = "squad_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squads.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    role_in_squad: Mapped[SquadRoleEnum] = mapped_column(SAEnum(SquadRoleEnum), nullable=False)
    allocation_percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    squad: Mapped["Squad"] = relationship("Squad", back_populates="members")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="squad_memberships")
