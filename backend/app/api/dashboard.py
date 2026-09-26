from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import TokenData
from app.services import dashboard_service, skill_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Reports"])


@router.get("/executive")
def executive_dashboard(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return dashboard_service.get_executive_dashboard(db)


@router.get("/reports/skill-gaps")
def skill_gaps(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return skill_service.get_skill_gaps(db)


@router.get("/reports/capacity-risk")
def capacity_risk(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return dashboard_service.get_capacity_risk(db)


@router.get("/reports/delivery-bottlenecks")
def delivery_bottlenecks(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return dashboard_service.get_delivery_bottlenecks(db)
