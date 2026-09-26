from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, computed_field

from app.models.project_team_phase import PhaseStatus
from app.models.project_team_dependency import DependencyType, DependencyStatus
from app.models.project import ProjectStatus, ProjectPriority, HealthIndicator

# Re-export enums so callers can import them from this schema module
__all__ = [
    "PhaseStatus",
    "DependencyType",
    "DependencyStatus",
    "ProjectTeamPhaseCreate",
    "ProjectTeamPhaseUpdate",
    "ProjectTeamPhaseResponse",
    "ProjectTeamDependencyCreate",
    "ProjectTeamDependencyUpdate",
    "ProjectTeamDependencyResponse",
    "HubSquadMember",
    "HubSquad",
    "HubTeam",
    "ProjectHubResponse",
]


# ---------------------------------------------------------------------------
# Phase schemas
# ---------------------------------------------------------------------------

class ProjectTeamPhaseCreate(BaseModel):
    project_id: int
    team_id: int
    phase_name: str
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    status: PhaseStatus = PhaseStatus.NotStarted
    notes: Optional[str] = None


class ProjectTeamPhaseUpdate(BaseModel):
    team_id: Optional[int] = None
    phase_name: Optional[str] = None
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    status: Optional[PhaseStatus] = None
    notes: Optional[str] = None


class ProjectTeamPhaseResponse(BaseModel):
    id: int
    project_id: int
    team_id: int
    team_name: str
    phase_name: str
    planned_start: Optional[date] = None
    planned_end: Optional[date] = None
    status: PhaseStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Dependency schemas
# ---------------------------------------------------------------------------

class ProjectTeamDependencyCreate(BaseModel):
    project_id: int
    from_team_id: int
    to_team_id: int
    dependency_type: DependencyType
    description: Optional[str] = None
    status: DependencyStatus = DependencyStatus.Pending
    due_date: Optional[date] = None


class ProjectTeamDependencyUpdate(BaseModel):
    from_team_id: Optional[int] = None
    to_team_id: Optional[int] = None
    dependency_type: Optional[DependencyType] = None
    description: Optional[str] = None
    status: Optional[DependencyStatus] = None
    due_date: Optional[date] = None


class ProjectTeamDependencyResponse(BaseModel):
    id: int
    project_id: int
    from_team_id: int
    from_team_name: str
    to_team_id: int
    to_team_name: str
    dependency_type: DependencyType
    description: Optional[str] = None
    status: DependencyStatus
    due_date: Optional[date] = None
    is_blocker: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Hub composite schemas
# ---------------------------------------------------------------------------

class HubSquadMember(BaseModel):
    employee_id: int
    employee_name: str
    role_in_squad: str
    allocation_percentage: float


class HubSquad(BaseModel):
    id: int
    name: str
    member_count: int
    members: List[HubSquadMember]


class HubTeam(BaseModel):
    team_id: int
    team_name: str
    squads: List[HubSquad]
    phases: List[ProjectTeamPhaseResponse]
    is_blocked: bool


class ProjectHubResponse(BaseModel):
    project_id: int
    project_name: str
    project_status: ProjectStatus
    project_priority: ProjectPriority
    health_indicator: HealthIndicator
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    teams: List[HubTeam]
    dependencies: List[ProjectTeamDependencyResponse]
