from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.squad import SquadCreate, SquadUpdate, SquadResponse, SquadMemberAdd, SquadMemberResponse
from app.services import squad_service

router = APIRouter(prefix="/squads", tags=["Squads"])


@router.get("", response_model=List[SquadResponse])
def list_squads(
    team_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return squad_service.get_squads(db, team_id=team_id, skip=skip, limit=limit)


@router.get("/{squad_id}", response_model=SquadResponse)
def get_squad(
    squad_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    squad = squad_service.get_squad(db, squad_id)
    from sqlalchemy import func
    from app.models.squad_member import SquadMember
    member_count = db.query(func.count(SquadMember.id)).filter(SquadMember.squad_id == squad_id).scalar() or 0
    return {**squad.__dict__, "member_count": member_count}


@router.post("", response_model=SquadResponse, status_code=201)
def create_squad(
    data: SquadCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    squad = squad_service.create_squad(db, data)
    return {**squad.__dict__, "member_count": 0}


@router.put("/{squad_id}", response_model=SquadResponse)
def update_squad(
    squad_id: int,
    data: SquadUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead", "scrum_master"])),
):
    squad = squad_service.update_squad(db, squad_id, data)
    from sqlalchemy import func
    from app.models.squad_member import SquadMember
    member_count = db.query(func.count(SquadMember.id)).filter(SquadMember.squad_id == squad_id).scalar() or 0
    return {**squad.__dict__, "member_count": member_count}


@router.delete("/{squad_id}", status_code=204)
def delete_squad(
    squad_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin"])),
):
    squad_service.delete_squad(db, squad_id)


@router.get("/{squad_id}/members", response_model=List[SquadMemberResponse])
def get_members(
    squad_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return squad_service.get_squad_members(db, squad_id)


@router.post("/{squad_id}/members", response_model=SquadMemberResponse, status_code=201)
def add_member(
    squad_id: int,
    data: SquadMemberAdd,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead", "scrum_master"])),
):
    return squad_service.add_member(db, squad_id, data)


@router.delete("/{squad_id}/members/{employee_id}", status_code=204)
def remove_member(
    squad_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead", "scrum_master"])),
):
    squad_service.remove_member(db, squad_id, employee_id)
