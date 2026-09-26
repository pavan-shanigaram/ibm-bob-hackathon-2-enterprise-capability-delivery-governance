from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.project_hub import (
    ProjectTeamPhaseCreate,
    ProjectTeamPhaseUpdate,
    ProjectTeamPhaseResponse,
    ProjectTeamDependencyCreate,
    ProjectTeamDependencyUpdate,
    ProjectTeamDependencyResponse,
    ProjectHubResponse,
)
from app.services import project_hub_service

router = APIRouter(prefix="/projects", tags=["Project Hub"])


# ---------------------------------------------------------------------------
# Hub
# ---------------------------------------------------------------------------

@router.get("/{project_id}/hub", response_model=ProjectHubResponse)
def get_project_hub(
    project_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return project_hub_service.get_hub(db, project_id)


# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------

@router.get("/{project_id}/phases", response_model=List[ProjectTeamPhaseResponse])
def list_phases(
    project_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return project_hub_service.get_phases(db, project_id)


@router.post("/{project_id}/phases", response_model=ProjectTeamPhaseResponse, status_code=201)
def create_phase(
    project_id: int,
    data: ProjectTeamPhaseCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_hub_service.create_phase(db, project_id, data)


@router.put("/{project_id}/phases/{phase_id}", response_model=ProjectTeamPhaseResponse)
def update_phase(
    project_id: int,
    phase_id: int,
    data: ProjectTeamPhaseUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_hub_service.update_phase(db, project_id, phase_id, data)


@router.delete("/{project_id}/phases/{phase_id}", status_code=204)
def delete_phase(
    project_id: int,
    phase_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    project_hub_service.delete_phase(db, project_id, phase_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

@router.get("/{project_id}/dependencies", response_model=List[ProjectTeamDependencyResponse])
def list_dependencies(
    project_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return project_hub_service.get_dependencies(db, project_id)


@router.post("/{project_id}/dependencies", response_model=ProjectTeamDependencyResponse, status_code=201)
def create_dependency(
    project_id: int,
    data: ProjectTeamDependencyCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_hub_service.create_dependency(db, project_id, data)


@router.put("/{project_id}/dependencies/{dep_id}", response_model=ProjectTeamDependencyResponse)
def update_dependency(
    project_id: int,
    dep_id: int,
    data: ProjectTeamDependencyUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_hub_service.update_dependency(db, project_id, dep_id, data)


@router.delete("/{project_id}/dependencies/{dep_id}", status_code=204)
def delete_dependency(
    project_id: int,
    dep_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    project_hub_service.delete_dependency(db, project_id, dep_id)
    return Response(status_code=204)
