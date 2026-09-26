from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum
from app.core.database import Base
from app.models.employee_skill import ProficiencyLevel


class CapabilityRequirement(Base):
    __tablename__ = "capability_requirements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    required_proficiency: Mapped[ProficiencyLevel] = mapped_column(SAEnum(ProficiencyLevel), nullable=False)
    headcount_needed: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="capability_requirements")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="capability_requirements")
