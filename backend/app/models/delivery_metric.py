from datetime import datetime, date
from sqlalchemy import String, ForeignKey, DateTime, Date, Numeric, Boolean, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class DeliveryMetric(Base):
    __tablename__ = "delivery_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squads.id"), nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    sprint_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sprint_start: Mapped[date | None] = mapped_column(Date)
    sprint_end: Mapped[date | None] = mapped_column(Date)
    velocity: Mapped[float] = mapped_column(Numeric(8, 2), default=0)
    story_points_planned: Mapped[int] = mapped_column(Integer, default=0)
    story_points_delivered: Mapped[int] = mapped_column(Integer, default=0)
    cycle_time_days: Mapped[float | None] = mapped_column(Numeric(6, 2))
    lead_time_days: Mapped[float | None] = mapped_column(Numeric(6, 2))
    defect_leakage_count: Mapped[int] = mapped_column(Integer, default=0)
    release_success: Mapped[bool] = mapped_column(Boolean, default=True)
    delivery_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    squad: Mapped["Squad"] = relationship("Squad", back_populates="delivery_metrics")
    project: Mapped["Project"] = relationship("Project", back_populates="delivery_metrics")
