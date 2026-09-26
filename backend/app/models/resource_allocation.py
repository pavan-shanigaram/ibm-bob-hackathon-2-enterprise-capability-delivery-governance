from datetime import datetime, date
from sqlalchemy import ForeignKey, DateTime, Date, Numeric, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    squad_id: Mapped[int | None] = mapped_column(ForeignKey("squads.id"), nullable=True)
    allocation_percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    is_over_allocated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="resource_allocations")
    project: Mapped["Project"] = relationship("Project", back_populates="resource_allocations")
