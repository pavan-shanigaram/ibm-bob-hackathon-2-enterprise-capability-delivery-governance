import enum
from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Squad(Base):
    __tablename__ = "squads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    scrum_master_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", use_alter=True, name="fk_squad_scrum_master"), nullable=True)
    capacity_points: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    team: Mapped["Team"] = relationship("Team", back_populates="squads", foreign_keys=[team_id])
    members: Mapped[list["SquadMember"]] = relationship("SquadMember", back_populates="squad")
    project_assignments: Mapped[list["ProjectSquadAssignment"]] = relationship("ProjectSquadAssignment", back_populates="squad")
    delivery_metrics: Mapped[list["DeliveryMetric"]] = relationship("DeliveryMetric", back_populates="squad")
