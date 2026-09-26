from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.team import Team
from app.models.squad import Squad
from app.models.employee import Employee
from app.schemas.team import TeamCreate, TeamUpdate


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    teams = db.query(Team).offset(skip).limit(limit).all()
    result = []
    for team in teams:
        squad_count = db.query(func.count(Squad.id)).filter(Squad.team_id == team.id).scalar() or 0
        employee_count = db.query(func.count(Employee.id)).filter(Employee.team_id == team.id).scalar() or 0
        result.append({
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "lead_employee_id": team.lead_employee_id,
            "created_at": team.created_at,
            "updated_at": team.updated_at,
            "squad_count": squad_count,
            "employee_count": employee_count,
        })
    return result


def get_team(db: Session, team_id: int) -> Team:
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


def create_team(db: Session, data: TeamCreate) -> Team:
    existing = db.query(Team).filter(Team.name == data.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Team name already exists")
    team = Team(**data.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: Session, team_id: int, data: TeamUpdate) -> Team:
    team = get_team(db, team_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team_id: int) -> None:
    team = get_team(db, team_id)
    db.delete(team)
    db.commit()
