from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.project import Project
from app.models.team import Team
from app.models.squad import Squad
from app.models.squad_member import SquadMember
from app.models.employee import Employee
from app.models.project_assignment import ProjectSquadAssignment
from app.models.project_team_phase import ProjectTeamPhase, PhaseStatus
from app.models.project_team_dependency import ProjectTeamDependency, DependencyType, DependencyStatus
from app.schemas.project_hub import (
    ProjectTeamPhaseCreate,
    ProjectTeamPhaseUpdate,
    ProjectTeamPhaseResponse,
    ProjectTeamDependencyCreate,
    ProjectTeamDependencyUpdate,
    ProjectTeamDependencyResponse,
    HubSquadMember,
    HubSquad,
    HubTeam,
    ProjectHubResponse,
)


# ---------------------------------------------------------------------------
# Hub assembly
# ---------------------------------------------------------------------------

def get_hub(db: Session, project_id: int) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Collect unique team_ids from two sources
    assignment_team_ids = {
        row.team_id
        for row in db.query(Squad.team_id).join(
            ProjectSquadAssignment, ProjectSquadAssignment.squad_id == Squad.id
        ).filter(ProjectSquadAssignment.project_id == project_id).all()
    }
    phase_team_ids = {
        row.team_id
        for row in db.query(ProjectTeamPhase.team_id).filter(
            ProjectTeamPhase.project_id == project_id
        ).all()
    }
    team_ids = assignment_team_ids | phase_team_ids

    # Fetch all dependencies once for is_blocked computation
    all_deps = db.query(ProjectTeamDependency).filter(
        ProjectTeamDependency.project_id == project_id
    ).all()

    blocker_to_team_ids = {
        d.to_team_id
        for d in all_deps
        if d.dependency_type == DependencyType.Blocker and d.status == DependencyStatus.Pending
    }

    teams_out: List[dict] = []
    for team_id in sorted(team_ids):
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            continue

        # Squads for this team that are assigned to this project
        squads = (
            db.query(Squad)
            .join(ProjectSquadAssignment, ProjectSquadAssignment.squad_id == Squad.id)
            .filter(
                ProjectSquadAssignment.project_id == project_id,
                Squad.team_id == team_id,
            )
            .all()
        )

        squads_out: List[dict] = []
        for squad in squads:
            members = (
                db.query(SquadMember)
                .filter(SquadMember.squad_id == squad.id)
                .all()
            )
            members_out = []
            for m in members:
                emp = db.query(Employee).filter(Employee.id == m.employee_id).first()
                members_out.append({
                    "employee_id": m.employee_id,
                    "employee_name": emp.name if emp else "",
                    "role_in_squad": m.role_in_squad.value if hasattr(m.role_in_squad, "value") else m.role_in_squad,
                    "allocation_percentage": float(m.allocation_percentage),
                })
            squads_out.append({
                "id": squad.id,
                "name": squad.name,
                "member_count": len(members_out),
                "members": members_out,
            })

        # Phases for this team on this project
        phases = db.query(ProjectTeamPhase).filter(
            ProjectTeamPhase.project_id == project_id,
            ProjectTeamPhase.team_id == team_id,
        ).all()
        phases_out = [_phase_response(db, ph) for ph in phases]

        teams_out.append({
            "team_id": team.id,
            "team_name": team.name,
            "squads": squads_out,
            "phases": phases_out,
            "is_blocked": team_id in blocker_to_team_ids,
        })

    deps_out = [_dep_response(db, d) for d in all_deps]

    return {
        "project_id": project.id,
        "project_name": project.name,
        "project_status": project.status,
        "project_priority": project.priority,
        "health_indicator": project.health_indicator,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "teams": teams_out,
        "dependencies": deps_out,
    }


# ---------------------------------------------------------------------------
# Phase CRUD
# ---------------------------------------------------------------------------

def create_phase(db: Session, project_id: int, data: ProjectTeamPhaseCreate) -> dict:
    if data.project_id != project_id:
        data = data.model_copy(update={"project_id": project_id})
    phase = ProjectTeamPhase(**data.model_dump())
    db.add(phase)
    db.commit()
    db.refresh(phase)
    return _phase_response(db, phase)


def update_phase(db: Session, project_id: int, phase_id: int, data: ProjectTeamPhaseUpdate) -> dict:
    phase = _get_phase(db, project_id, phase_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(phase, field, value)
    db.commit()
    db.refresh(phase)
    return _phase_response(db, phase)


def delete_phase(db: Session, project_id: int, phase_id: int) -> None:
    phase = _get_phase(db, project_id, phase_id)
    db.delete(phase)
    db.commit()


def get_phases(db: Session, project_id: int) -> list:
    phases = db.query(ProjectTeamPhase).filter(
        ProjectTeamPhase.project_id == project_id
    ).all()
    return [_phase_response(db, ph) for ph in phases]


# ---------------------------------------------------------------------------
# Dependency CRUD
# ---------------------------------------------------------------------------

def create_dependency(db: Session, project_id: int, data: ProjectTeamDependencyCreate) -> dict:
    if data.project_id != project_id:
        data = data.model_copy(update={"project_id": project_id})
    dep = ProjectTeamDependency(**data.model_dump())
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return _dep_response(db, dep)


def update_dependency(db: Session, project_id: int, dep_id: int, data: ProjectTeamDependencyUpdate) -> dict:
    dep = _get_dep(db, project_id, dep_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(dep, field, value)
    db.commit()
    db.refresh(dep)
    return _dep_response(db, dep)


def delete_dependency(db: Session, project_id: int, dep_id: int) -> None:
    dep = _get_dep(db, project_id, dep_id)
    db.delete(dep)
    db.commit()


def get_dependencies(db: Session, project_id: int) -> list:
    deps = db.query(ProjectTeamDependency).filter(
        ProjectTeamDependency.project_id == project_id
    ).all()
    return [_dep_response(db, d) for d in deps]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_phase(db: Session, project_id: int, phase_id: int) -> ProjectTeamPhase:
    phase = db.query(ProjectTeamPhase).filter(
        ProjectTeamPhase.id == phase_id,
        ProjectTeamPhase.project_id == project_id,
    ).first()
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    return phase


def _get_dep(db: Session, project_id: int, dep_id: int) -> ProjectTeamDependency:
    dep = db.query(ProjectTeamDependency).filter(
        ProjectTeamDependency.id == dep_id,
        ProjectTeamDependency.project_id == project_id,
    ).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Dependency not found")
    return dep


def _phase_response(db: Session, phase: ProjectTeamPhase) -> dict:
    team = db.query(Team).filter(Team.id == phase.team_id).first()
    return {
        "id": phase.id,
        "project_id": phase.project_id,
        "team_id": phase.team_id,
        "team_name": team.name if team else "",
        "phase_name": phase.phase_name,
        "planned_start": phase.planned_start,
        "planned_end": phase.planned_end,
        "status": phase.status,
        "notes": phase.notes,
        "created_at": phase.created_at,
        "updated_at": phase.updated_at,
    }


def _dep_response(db: Session, dep: ProjectTeamDependency) -> dict:
    from_team = db.query(Team).filter(Team.id == dep.from_team_id).first()
    to_team = db.query(Team).filter(Team.id == dep.to_team_id).first()
    is_blocker = (dep.dependency_type == DependencyType.Blocker and dep.status == DependencyStatus.Pending)
    return {
        "id": dep.id,
        "project_id": dep.project_id,
        "from_team_id": dep.from_team_id,
        "from_team_name": from_team.name if from_team else "",
        "to_team_id": dep.to_team_id,
        "to_team_name": to_team.name if to_team else "",
        "dependency_type": dep.dependency_type,
        "description": dep.description,
        "status": dep.status,
        "due_date": dep.due_date,
        "is_blocker": is_blocker,
        "created_at": dep.created_at,
        "updated_at": dep.updated_at,
    }
