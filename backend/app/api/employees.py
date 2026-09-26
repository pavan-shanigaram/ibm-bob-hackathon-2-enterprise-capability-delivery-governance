from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeSkillAdd, EmployeeSkillResponse
from app.services import employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=List[EmployeeResponse])
def list_employees(
    team_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return employee_service.get_employees(db, team_id=team_id, skip=skip, limit=limit)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    emp = employee_service.get_employee(db, employee_id)
    from sqlalchemy import func
    from app.models.squad_member import SquadMember
    utilization = employee_service._calc_utilization(db, employee_id)
    squad_count = db.query(func.count(SquadMember.id)).filter(SquadMember.employee_id == employee_id).scalar() or 0
    return {**emp.__dict__, "utilization_percentage": utilization, "squad_count": squad_count}


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return employee_service.create_employee(db, data)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return employee_service.update_employee(db, employee_id, data)


@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin"])),
):
    employee_service.delete_employee(db, employee_id)


@router.get("/{employee_id}/skills", response_model=List[EmployeeSkillResponse])
def get_skills(
    employee_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return employee_service.get_employee_skills(db, employee_id)


@router.post("/{employee_id}/skills", response_model=EmployeeSkillResponse, status_code=201)
def add_skill(
    employee_id: int,
    data: EmployeeSkillAdd,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return employee_service.add_skill(db, employee_id, data)
