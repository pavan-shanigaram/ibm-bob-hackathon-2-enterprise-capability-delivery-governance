from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.project import Project, HealthIndicator
from app.models.project_assignment import ProjectSquadAssignment, ProjectEmployeeAssignment
from app.models.delivery_metric import DeliveryMetric
from app.models.employee import Employee
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectSquadAssign, ProjectEmployeeAssign


def get_projects(db: Session, status=None, priority=None, team_id=None, skip=0, limit=100) -> List[dict]:
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    if priority:
        query = query.filter(Project.priority == priority)
    if team_id:
        query = query.filter(Project.owner_team_id == team_id)
    projects = query.offset(skip).limit(limit).all()
    return [_enrich(db, p) for p in projects]


def get_project(db: Session, project_id: int) -> Project:
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p


def create_project(db: Session, data: ProjectCreate) -> dict:
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return _enrich(db, project)


def update_project(db: Session, project_id: int, data: ProjectUpdate) -> dict:
    project = get_project(db, project_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    # Recompute health
    project.health_indicator = _compute_health(db, project)
    db.commit()
    db.refresh(project)
    return _enrich(db, project)


def assign_squads(db: Session, project_id: int, data: ProjectSquadAssign) -> dict:
    get_project(db, project_id)
    for squad_id in data.squad_ids:
        existing = db.query(ProjectSquadAssignment).filter(
            ProjectSquadAssignment.project_id == project_id,
            ProjectSquadAssignment.squad_id == squad_id
        ).first()
        if not existing:
            db.add(ProjectSquadAssignment(project_id=project_id, squad_id=squad_id))
    db.commit()
    return {"project_id": project_id, "assigned_squads": data.squad_ids}


def assign_employee(db: Session, project_id: int, data: ProjectEmployeeAssign) -> dict:
    get_project(db, project_id)
    existing = db.query(ProjectEmployeeAssignment).filter(
        ProjectEmployeeAssignment.project_id == project_id,
        ProjectEmployeeAssignment.employee_id == data.employee_id
    ).first()
    if existing:
        existing.allocation_percentage = data.allocation_percentage
        existing.role_on_project = data.role_on_project
    else:
        db.add(ProjectEmployeeAssignment(
            project_id=project_id,
            employee_id=data.employee_id,
            allocation_percentage=data.allocation_percentage,
            role_on_project=data.role_on_project,
        ))
    db.commit()
    return {"project_id": project_id, "employee_id": data.employee_id}


def _compute_health(db: Session, project: Project) -> HealthIndicator:
    # Get latest delivery score
    latest_metric = db.query(DeliveryMetric).filter(
        DeliveryMetric.project_id == project.id
    ).order_by(DeliveryMetric.recorded_at.desc()).first()
    score = float(latest_metric.delivery_score) if latest_metric else 100.0
    # Check over-allocation
    assignments = db.query(ProjectEmployeeAssignment).filter(
        ProjectEmployeeAssignment.project_id == project.id
    ).all()
    over_alloc = 0
    for a in assignments:
        total = db.query(func.sum(ProjectEmployeeAssignment.allocation_percentage)).filter(
            ProjectEmployeeAssignment.employee_id == a.employee_id
        ).scalar() or 0
        if float(total) > 100:
            over_alloc += 1
    if score >= 80 and over_alloc == 0:
        return HealthIndicator.Green
    elif score >= 60 or over_alloc <= 1:
        return HealthIndicator.Amber
    return HealthIndicator.Red


def _enrich(db: Session, p: Project) -> dict:
    squad_count = db.query(func.count(ProjectSquadAssignment.id)).filter(
        ProjectSquadAssignment.project_id == p.id
    ).scalar() or 0
    emp_count = db.query(func.count(ProjectEmployeeAssignment.id)).filter(
        ProjectEmployeeAssignment.project_id == p.id
    ).scalar() or 0
    return {
        **p.__dict__,
        "squad_count": squad_count,
        "employee_count": emp_count,
    }
