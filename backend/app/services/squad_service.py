from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.squad import Squad
from app.models.squad_member import SquadMember
from app.models.employee import Employee
from app.schemas.squad import SquadCreate, SquadUpdate, SquadMemberAdd


def get_squads(db: Session, team_id: int = None, skip: int = 0, limit: int = 100) -> List[dict]:
    query = db.query(Squad)
    if team_id:
        query = query.filter(Squad.team_id == team_id)
    squads = query.offset(skip).limit(limit).all()
    result = []
    for squad in squads:
        member_count = db.query(func.count(SquadMember.id)).filter(SquadMember.squad_id == squad.id).scalar() or 0
        result.append({
            "id": squad.id,
            "name": squad.name,
            "team_id": squad.team_id,
            "scrum_master_id": squad.scrum_master_id,
            "capacity_points": squad.capacity_points,
            "description": squad.description,
            "created_at": squad.created_at,
            "updated_at": squad.updated_at,
            "member_count": member_count,
        })
    return result


def get_squad(db: Session, squad_id: int) -> Squad:
    squad = db.query(Squad).filter(Squad.id == squad_id).first()
    if not squad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Squad not found")
    return squad


def create_squad(db: Session, data: SquadCreate) -> Squad:
    squad = Squad(**data.model_dump())
    db.add(squad)
    db.commit()
    db.refresh(squad)
    return squad


def update_squad(db: Session, squad_id: int, data: SquadUpdate) -> Squad:
    squad = get_squad(db, squad_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(squad, field, value)
    db.commit()
    db.refresh(squad)
    return squad


def delete_squad(db: Session, squad_id: int) -> None:
    squad = get_squad(db, squad_id)
    db.delete(squad)
    db.commit()


def add_member(db: Session, squad_id: int, data: SquadMemberAdd) -> dict:
    squad = get_squad(db, squad_id)
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Check if already a member
    existing = db.query(SquadMember).filter(
        SquadMember.squad_id == squad_id,
        SquadMember.employee_id == data.employee_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Employee already in squad")
    member = SquadMember(
        squad_id=squad_id,
        employee_id=data.employee_id,
        role_in_squad=data.role_in_squad,
        allocation_percentage=data.allocation_percentage,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return {
        "id": member.id,
        "employee_id": member.employee_id,
        "employee_name": employee.name,
        "role_in_squad": member.role_in_squad,
        "allocation_percentage": float(member.allocation_percentage),
    }


def remove_member(db: Session, squad_id: int, employee_id: int) -> None:
    member = db.query(SquadMember).filter(
        SquadMember.squad_id == squad_id,
        SquadMember.employee_id == employee_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in squad")
    db.delete(member)
    db.commit()


def get_squad_members(db: Session, squad_id: int) -> List[dict]:
    members = db.query(SquadMember).filter(SquadMember.squad_id == squad_id).all()
    result = []
    for m in members:
        emp = db.query(Employee).filter(Employee.id == m.employee_id).first()
        result.append({
            "id": m.id,
            "employee_id": m.employee_id,
            "employee_name": emp.name if emp else "Unknown",
            "role_in_squad": m.role_in_squad,
            "allocation_percentage": float(m.allocation_percentage),
        })
    return result
