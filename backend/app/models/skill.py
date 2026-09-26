from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    employee_skills: Mapped[list["EmployeeSkill"]] = relationship("EmployeeSkill", back_populates="skill")
    capability_requirements: Mapped[list["CapabilityRequirement"]] = relationship("CapabilityRequirement", back_populates="skill")
