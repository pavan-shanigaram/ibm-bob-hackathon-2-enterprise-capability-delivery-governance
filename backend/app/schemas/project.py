from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel
from app.models.project import ProjectStatus, ProjectPriority, HealthIndicator


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.Draft
    priority: ProjectPriority = ProjectPriority.Medium
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    owner_team_id: Optional[int] = None
    owner_squad_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    owner_team_id: Optional[int] = None
    health_indicator: Optional[HealthIndicator] = None


class ProjectSquadAssign(BaseModel):
    squad_ids: List[int]


class ProjectEmployeeAssign(BaseModel):
    employee_id: int
    allocation_percentage: float = 100.0
    role_on_project: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    health_indicator: HealthIndicator
    created_at: datetime
    updated_at: datetime
    squad_count: int = 0
    employee_count: int = 0

    class Config:
        from_attributes = True
