from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.services import team_service

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("", response_model=List[TeamResponse])
def list_teams(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return team_service.get_teams(db, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    team = team_service.get_team(db, team_id)
    from sqlalchemy import func
    from app.models.squad import Squad
    from app.models.employee import Employee
    squad_count = db.query(func.count(Squad.id)).filter(Squad.team_id == team_id).scalar() or 0
    employee_count = db.query(func.count(Employee.id)).filter(Employee.team_id == team_id).scalar() or 0
    return {
        **team.__dict__,
        "squad_count": squad_count,
        "employee_count": employee_count,
    }


@router.post("", response_model=TeamResponse, status_code=201)
def create_team(
    data: TeamCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin"])),
):
    team = team_service.create_team(db, data)
    return {**team.__dict__, "squad_count": 0, "employee_count": 0}


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    data: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    # platform_admin can update any; team_lead can update own team
    if "platform_admin" not in current_user.roles:
        if "team_lead" not in current_user.roles or current_user.team_id != team_id:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    team = team_service.update_team(db, team_id, data)
    from sqlalchemy import func
    from app.models.squad import Squad
    from app.models.employee import Employee
    squad_count = db.query(func.count(Squad.id)).filter(Squad.team_id == team_id).scalar() or 0
    employee_count = db.query(func.count(Employee.id)).filter(Employee.team_id == team_id).scalar() or 0
    return {**team.__dict__, "squad_count": squad_count, "employee_count": employee_count}


@router.delete("/{team_id}", status_code=204)
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin"])),
):
    team_service.delete_team(db, team_id)
