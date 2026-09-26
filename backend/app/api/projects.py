from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectSquadAssign, ProjectEmployeeAssign
from app.models.project import ProjectStatus, ProjectPriority
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=List[ProjectResponse])
def list_projects(
    status: Optional[ProjectStatus] = Query(None),
    priority: Optional[ProjectPriority] = Query(None),
    team_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return project_service.get_projects(db, status=status, priority=priority, team_id=team_id, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    p = project_service.get_project(db, project_id)
    return project_service._enrich(db, p)


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_service.create_project(db, data)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_service.update_project(db, project_id, data)


@router.put("/{project_id}/squads")
def assign_squads(
    project_id: int,
    data: ProjectSquadAssign,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return project_service.assign_squads(db, project_id, data)


@router.post("/{project_id}/employees")
def assign_employee(
    project_id: int,
    data: ProjectEmployeeAssign,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead", "scrum_master"])),
):
    return project_service.assign_employee(db, project_id, data)
