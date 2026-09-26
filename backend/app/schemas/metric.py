from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


class DeliveryMetricCreate(BaseModel):
    squad_id: int
    project_id: Optional[int] = None
    sprint_name: str
    sprint_start: Optional[date] = None
    sprint_end: Optional[date] = None
    story_points_planned: int = 0
    story_points_delivered: int = 0
    cycle_time_days: Optional[float] = None
    lead_time_days: Optional[float] = None
    defect_leakage_count: int = 0
    release_success: bool = True


class DeliveryMetricResponse(BaseModel):
    id: int
    squad_id: int
    project_id: Optional[int]
    sprint_name: str
    sprint_start: Optional[date]
    sprint_end: Optional[date]
    velocity: float
    story_points_planned: int
    story_points_delivered: int
    cycle_time_days: Optional[float]
    lead_time_days: Optional[float]
    defect_leakage_count: int
    release_success: bool
    delivery_score: float
    recorded_at: datetime

    class Config:
        from_attributes = True


class VelocityTrendPoint(BaseModel):
    sprint_name: str
    velocity: float
    delivery_score: float
    story_points_delivered: int
