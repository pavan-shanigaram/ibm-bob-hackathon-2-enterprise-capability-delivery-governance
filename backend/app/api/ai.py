from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import TokenData
from app.services import watsonx_service, skill_service, metric_service

router = APIRouter(prefix="/ai", tags=["IBM watsonx.ai"])


@router.get("/health")
def ai_health():
    return watsonx_service.get_health()


@router.post("/skill-gap-narrative")
def skill_gap_narrative(
    project_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    gaps = skill_service.get_skill_gaps(db)
    project_gaps = next((g for g in gaps if g["project_id"] == project_id), None)
    if not project_gaps:
        prompt_data = f"No skill gaps found for project {project_id}"
    else:
        prompt_data = str(project_gaps)
    prompt = (
        f"You are an enterprise capability advisor. Given this project skill gap data: {prompt_data}, "
        "provide 3 specific hiring or training recommendations in bullet points."
    )
    return {"narrative": watsonx_service.generate(prompt), "project_id": project_id}


@router.post("/delivery-coach")
def delivery_coach(
    squad_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    from app.models.squad import Squad
    squad = db.query(Squad).filter(Squad.id == squad_id).first()
    squad_name = squad.name if squad else f"Squad {squad_id}"
    metrics = metric_service.get_velocity_trend(db, squad_id=squad_id, n=5)
    prompt = (
        f"You are an agile delivery coach. Given these sprint metrics for squad '{squad_name}': "
        f"{metrics}, identify the top 2 delivery risks and suggest concrete improvements."
    )
    return {"narrative": watsonx_service.generate(prompt), "squad_id": squad_id}


@router.post("/risk-summary")
def risk_summary(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    from app.services import dashboard_service
    dashboard = dashboard_service.get_executive_dashboard(db)
    heatmap = dashboard.get("risk_heatmap", [])
    prompt = (
        "You are a CTO advisor. Summarize the following enterprise risk heatmap data: "
        f"{heatmap} in 3 sentences suitable for a board presentation."
    )
    return {"narrative": watsonx_service.generate(prompt)}
