import enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    lead_employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", use_alter=True, name="fk_team_lead"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    squads: Mapped[list["Squad"]] = relationship("Squad", back_populates="team", foreign_keys="Squad.team_id")
    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="team", foreign_keys="Employee.team_id")
