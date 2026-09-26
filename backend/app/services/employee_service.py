from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.employee import Employee
from app.models.squad_member import SquadMember
from app.models.employee_skill import EmployeeSkill
from app.models.skill import Skill
from app.models.project_assignment import ProjectEmployeeAssignment
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeSkillAdd


def get_employees(db: Session, team_id: int = None, skip: int = 0, limit: int = 100) -> List[dict]:
    query = db.query(Employee)
    if team_id:
        query = query.filter(Employee.team_id == team_id)
    employees = query.filter(Employee.is_active == True).offset(skip).limit(limit).all()
    result = []
    for emp in employees:
        utilization = _calc_utilization(db, emp.id)
        squad_count = db.query(func.count(SquadMember.id)).filter(SquadMember.employee_id == emp.id).scalar() or 0
        result.append({**emp.__dict__, "utilization_percentage": utilization, "squad_count": squad_count})
    return result


def get_employee(db: Session, employee_id: int) -> Employee:
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp


def create_employee(db: Session, data: EmployeeCreate) -> dict:
    existing = db.query(Employee).filter(Employee.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    emp = Employee(**data.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return {**emp.__dict__, "utilization_percentage": 0.0, "squad_count": 0}


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> dict:
    emp = get_employee(db, employee_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    utilization = _calc_utilization(db, emp.id)
    squad_count = db.query(func.count(SquadMember.id)).filter(SquadMember.employee_id == emp.id).scalar() or 0
    return {**emp.__dict__, "utilization_percentage": utilization, "squad_count": squad_count}


def delete_employee(db: Session, employee_id: int) -> None:
    emp = get_employee(db, employee_id)
    emp.is_active = False
    db.commit()


def add_skill(db: Session, employee_id: int, data: EmployeeSkillAdd) -> dict:
    get_employee(db, employee_id)
    skill = db.query(Skill).filter(Skill.id == data.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    existing = db.query(EmployeeSkill).filter(
        EmployeeSkill.employee_id == employee_id,
        EmployeeSkill.skill_id == data.skill_id
    ).first()
    if existing:
        existing.proficiency_level = data.proficiency_level
        db.commit()
        db.refresh(existing)
        es = existing
    else:
        es = EmployeeSkill(employee_id=employee_id, skill_id=data.skill_id, proficiency_level=data.proficiency_level)
        db.add(es)
        db.commit()
        db.refresh(es)
    return {
        "id": es.id,
        "skill_id": es.skill_id,
        "skill_name": skill.name,
        "skill_category": skill.category,
        "proficiency_level": es.proficiency_level,
    }


def get_employee_skills(db: Session, employee_id: int) -> List[dict]:
    skills = db.query(EmployeeSkill).filter(EmployeeSkill.employee_id == employee_id).all()
    result = []
    for es in skills:
        skill = db.query(Skill).filter(Skill.id == es.skill_id).first()
        result.append({
            "id": es.id,
            "skill_id": es.skill_id,
            "skill_name": skill.name if skill else "Unknown",
            "skill_category": skill.category if skill else "Unknown",
            "proficiency_level": es.proficiency_level,
        })
    return result


def _calc_utilization(db: Session, employee_id: int) -> float:
    total = db.query(func.sum(ProjectEmployeeAssignment.allocation_percentage)).filter(
        ProjectEmployeeAssignment.employee_id == employee_id
    ).scalar() or 0
    return float(total)
