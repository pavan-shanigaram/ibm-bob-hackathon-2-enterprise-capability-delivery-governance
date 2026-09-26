"""
Live Demo Endpoints — No authentication required.
These endpoints exist purely for hackathon judging convenience.
They are gated by DEMO_MODE=true in the environment.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.services import dashboard_service, watsonx_service
from app.models.team import Team
from app.models.squad import Squad
from app.models.employee import Employee
from app.models.squad_member import SquadMember
from sqlalchemy import func

router = APIRouter(prefix="/demo", tags=["Live Demo"])


def _check_demo_mode():
    if not settings.DEMO_MODE:
        raise HTTPException(status_code=403, detail="Demo mode is disabled. Set DEMO_MODE=true.")


@router.get("/summary")
def demo_summary(db: Session = Depends(get_db)):
    """Platform KPI snapshot — no auth required."""
    _check_demo_mode()
    from app.models.project import Project, ProjectStatus
    from app.models.delivery_metric import DeliveryMetric
    total_teams = db.query(func.count(Team.id)).scalar() or 0
    total_squads = db.query(func.count(Squad.id)).scalar() or 0
    total_employees = db.query(func.count(Employee.id)).filter(Employee.is_active == True).scalar() or 0
    active_projects = db.query(func.count(Project.id)).filter(Project.status == ProjectStatus.Active).scalar() or 0
    avg_score = db.query(func.avg(DeliveryMetric.delivery_score)).scalar()
    return {
        "platform": settings.APP_NAME,
        "total_teams": total_teams,
        "total_squads": total_squads,
        "total_employees": total_employees,
        "active_projects": active_projects,
        "avg_delivery_score": round(float(avg_score), 1) if avg_score else 0.0,
        "message": "Live demo data — populated by seed script",
    }


@router.get("/dashboard")
def demo_dashboard(db: Session = Depends(get_db)):
    """Full executive dashboard payload — no auth required."""
    _check_demo_mode()
    return dashboard_service.get_executive_dashboard(db)


@router.get("/teams")
def demo_teams(db: Session = Depends(get_db)):
    """All 8 teams with squad and member counts — no auth required."""
    _check_demo_mode()
    teams = db.query(Team).all()
    result = []
    for team in teams:
        squad_count = db.query(func.count(Squad.id)).filter(Squad.team_id == team.id).scalar() or 0
        employee_count = db.query(func.count(Employee.id)).filter(Employee.team_id == team.id).scalar() or 0
        result.append({
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "squad_count": squad_count,
            "employee_count": employee_count,
        })
    return result


@router.get("/ai-insights")
def demo_ai_insights(db: Session = Depends(get_db)):
    """IBM watsonx.ai Granite AI insights — no auth required."""
    _check_demo_mode()
    from app.services import dashboard_service
    dashboard = dashboard_service.get_executive_dashboard(db)
    heatmap = dashboard.get("risk_heatmap", [])
    prompt = (
        "You are a CTO advisor for a large enterprise. Summarize the following risk heatmap "
        f"data across all technology teams: {heatmap} in 3 concise sentences suitable for "
        "a board presentation. Highlight the top 2 areas of concern."
    )
    narrative = watsonx_service.generate(prompt)
    return {
        "narrative": narrative,
        "model": settings.WATSONX_MODEL_ID,
        "is_live_ai": bool(settings.WATSONX_API_KEY),
    }
