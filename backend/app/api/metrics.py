from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.metric import DeliveryMetricCreate, DeliveryMetricResponse, VelocityTrendPoint
from app.services import metric_service

router = APIRouter(prefix="/metrics", tags=["Delivery Metrics"])


@router.get("", response_model=List[DeliveryMetricResponse])
def list_metrics(
    squad_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return metric_service.get_metrics(db, squad_id=squad_id, project_id=project_id, limit=limit)


@router.post("", response_model=DeliveryMetricResponse, status_code=201)
def create_metric(
    data: DeliveryMetricCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "scrum_master", "team_lead"])),
):
    return metric_service.create_metric(db, data)


@router.get("/squad/{squad_id}/velocity-trend", response_model=List[VelocityTrendPoint])
def velocity_trend(
    squad_id: int,
    n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return metric_service.get_velocity_trend(db, squad_id=squad_id, n=n)
