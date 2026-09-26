from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.team import Team
from app.models.squad import Squad
from app.models.employee import Employee
from app.models.project import Project, ProjectStatus, HealthIndicator
from app.models.delivery_metric import DeliveryMetric
from app.models.authorization import Authorization, ComplianceStatus
from app.models.resource_allocation import ResourceAllocation
from app.models.squad_member import SquadMember
from app.services import allocation_service, skill_service

# Simple in-memory TTL cache
_cache: dict = {}
_CACHE_TTL_SECONDS = 300


def get_executive_dashboard(db: Session) -> dict:
    now = datetime.utcnow()
    if "dashboard" in _cache and (now - _cache["dashboard"]["ts"]).seconds < _CACHE_TTL_SECONDS:
        return _cache["dashboard"]["data"]

    data = _build_dashboard(db)
    _cache["dashboard"] = {"ts": now, "data": data}
    return data


def _build_dashboard(db: Session) -> dict:
    # KPI counts
    total_teams = db.query(func.count(Team.id)).scalar() or 0
    total_squads = db.query(func.count(Squad.id)).scalar() or 0
    total_employees = db.query(func.count(Employee.id)).filter(Employee.is_active == True).scalar() or 0
    active_projects = db.query(func.count(Project.id)).filter(Project.status == ProjectStatus.Active).scalar() or 0

    # Project health counts
    green_count = db.query(func.count(Project.id)).filter(Project.health_indicator == HealthIndicator.Green, Project.status == ProjectStatus.Active).scalar() or 0
    amber_count = db.query(func.count(Project.id)).filter(Project.health_indicator == HealthIndicator.Amber, Project.status == ProjectStatus.Active).scalar() or 0
    red_count = db.query(func.count(Project.id)).filter(Project.health_indicator == HealthIndicator.Red, Project.status == ProjectStatus.Active).scalar() or 0

    # Avg delivery score
    avg_score_result = db.query(func.avg(DeliveryMetric.delivery_score)).scalar()
    avg_delivery_score = round(float(avg_score_result), 1) if avg_score_result else 0.0

    # Over-allocated employees
    over_allocated = allocation_service.get_over_allocated(db)

    # Team health rows
    teams = db.query(Team).all()
    team_health = []
    for team in teams:
        emp_count = db.query(func.count(Employee.id)).filter(Employee.team_id == team.id).scalar() or 0
        squad_count = db.query(func.count(Squad.id)).filter(Squad.team_id == team.id).scalar() or 0
        squad_ids = [s.id for s in db.query(Squad).filter(Squad.team_id == team.id).all()]
        avg_team_score = 0.0
        if squad_ids:
            res = db.query(func.avg(DeliveryMetric.delivery_score)).filter(
                DeliveryMetric.squad_id.in_(squad_ids)
            ).scalar()
            avg_team_score = round(float(res), 1) if res else 0.0
        team_health.append({
            "team_id": team.id,
            "team_name": team.name,
            "employee_count": emp_count,
            "squad_count": squad_count,
            "avg_delivery_score": avg_team_score,
        })

    # Expired authorizations
    expired_auths = db.query(func.count(Authorization.id)).filter(
        Authorization.compliance_status == ComplianceStatus.Expired
    ).scalar() or 0

    # Risk heatmap: teams x dimensions
    risk_dimensions = ["Resource", "Delivery", "Capability", "Compliance"]
    risk_heatmap = []
    for team in teams:
        team_emp_ids = [e.id for e in db.query(Employee).filter(Employee.team_id == team.id).all()]
        squad_ids = [s.id for s in db.query(Squad).filter(Squad.team_id == team.id).all()]

        # Resource risk: % over-allocated employees
        over_cnt = len([a for a in over_allocated if a["employee_id"] in team_emp_ids])
        resource_risk = min(5, 1 + int(over_cnt / max(len(team_emp_ids), 1) * 10))

        # Delivery risk: based on avg delivery score
        avg_score = 0.0
        if squad_ids:
            res = db.query(func.avg(DeliveryMetric.delivery_score)).filter(DeliveryMetric.squad_id.in_(squad_ids)).scalar()
            avg_score = float(res) if res else 0.0
        delivery_risk = 1 if avg_score >= 80 else (2 if avg_score >= 60 else (4 if avg_score >= 40 else 5))

        # Capability risk (static for now — would need gap analysis)
        capability_risk = 2

        # Compliance risk: expired auths for this team
        if team_emp_ids:
            expired_team = db.query(func.count(Authorization.id)).filter(
                Authorization.employee_id.in_(team_emp_ids),
                Authorization.compliance_status == ComplianceStatus.Expired
            ).scalar() or 0
        else:
            expired_team = 0
        compliance_risk = min(5, 1 + expired_team)

        risk_heatmap.append({
            "team_name": team.name,
            "Resource": resource_risk,
            "Delivery": delivery_risk,
            "Capability": capability_risk,
            "Compliance": compliance_risk,
        })

    # Alerts
    alerts = []
    if over_allocated:
        alerts.append({"type": "warning", "message": f"{len(over_allocated)} employees are over-allocated"})
    if expired_auths:
        alerts.append({"type": "error", "message": f"{expired_auths} expired system authorizations require attention"})
    low_score_squads = db.query(DeliveryMetric.squad_id).filter(DeliveryMetric.delivery_score < 60).distinct().count()
    if low_score_squads:
        alerts.append({"type": "warning", "message": f"{low_score_squads} squads have delivery score below 60"})

    return {
        "kpis": {
            "total_teams": total_teams,
            "total_squads": total_squads,
            "total_employees": total_employees,
            "active_projects": active_projects,
            "avg_delivery_score": avg_delivery_score,
            "over_allocated_count": len(over_allocated),
        },
        "project_health_counts": {
            "green": green_count,
            "amber": amber_count,
            "red": red_count,
        },
        "team_health": team_health,
        "risk_heatmap": risk_heatmap,
        "alerts": alerts,
        "generated_at": datetime.utcnow().isoformat(),
    }


def get_capacity_risk(db: Session) -> List[dict]:
    squads = db.query(Squad).all()
    result = []
    for squad in squads:
        members = db.query(SquadMember).filter(SquadMember.squad_id == squad.id).all()
        if not members:
            continue
        total_alloc = sum(float(m.allocation_percentage) for m in members)
        avg_alloc = total_alloc / len(members)
        if avg_alloc > 90:
            result.append({
                "squad_id": squad.id,
                "squad_name": squad.name,
                "avg_allocation": round(avg_alloc, 1),
                "member_count": len(members),
            })
    return result


def get_delivery_bottlenecks(db: Session) -> List[dict]:
    squads = db.query(Squad).all()
    result = []
    for squad in squads:
        metrics = db.query(DeliveryMetric).filter(
            DeliveryMetric.squad_id == squad.id
        ).order_by(DeliveryMetric.recorded_at.desc()).limit(3).all()
        if not metrics:
            continue
        avg_score = sum(float(m.delivery_score) for m in metrics) / len(metrics)
        if avg_score < 60:
            result.append({
                "squad_id": squad.id,
                "squad_name": squad.name,
                "avg_delivery_score": round(avg_score, 1),
                "sprint_count_analyzed": len(metrics),
            })
    return result
