from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.delivery_metric import DeliveryMetric
from app.schemas.metric import DeliveryMetricCreate


def _delivery_score(planned: int, delivered: int, release_success: bool, defect_leakage: int) -> float:
    if planned == 0:
        return 0.0
    velocity_ratio = min(delivered / planned, 1.0)
    defect_penalty = max(0, 1 - defect_leakage / max(delivered, 1))
    score = (velocity_ratio * 50) + (float(release_success) * 30) + (defect_penalty * 20)
    return round(min(max(score, 0), 100), 2)


def create_metric(db: Session, data: DeliveryMetricCreate) -> dict:
    score = _delivery_score(
        data.story_points_planned,
        data.story_points_delivered,
        data.release_success,
        data.defect_leakage_count,
    )
    velocity = float(data.story_points_delivered)
    metric = DeliveryMetric(
        **data.model_dump(),
        velocity=velocity,
        delivery_score=score,
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return _to_dict(metric)


def get_metrics(db: Session, squad_id: int = None, project_id: int = None, limit: int = 50) -> List[dict]:
    query = db.query(DeliveryMetric)
    if squad_id:
        query = query.filter(DeliveryMetric.squad_id == squad_id)
    if project_id:
        query = query.filter(DeliveryMetric.project_id == project_id)
    metrics = query.order_by(DeliveryMetric.recorded_at.desc()).limit(limit).all()
    return [_to_dict(m) for m in metrics]


def get_velocity_trend(db: Session, squad_id: int, n: int = 10) -> List[dict]:
    metrics = (
        db.query(DeliveryMetric)
        .filter(DeliveryMetric.squad_id == squad_id)
        .order_by(DeliveryMetric.sprint_start.asc())
        .limit(n)
        .all()
    )
    return [
        {
            "sprint_name": m.sprint_name,
            "velocity": float(m.velocity),
            "delivery_score": float(m.delivery_score),
            "story_points_delivered": m.story_points_delivered,
        }
        for m in metrics
    ]


def _to_dict(m: DeliveryMetric) -> dict:
    return {
        "id": m.id,
        "squad_id": m.squad_id,
        "project_id": m.project_id,
        "sprint_name": m.sprint_name,
        "sprint_start": m.sprint_start,
        "sprint_end": m.sprint_end,
        "velocity": float(m.velocity),
        "story_points_planned": m.story_points_planned,
        "story_points_delivered": m.story_points_delivered,
        "cycle_time_days": float(m.cycle_time_days) if m.cycle_time_days else None,
        "lead_time_days": float(m.lead_time_days) if m.lead_time_days else None,
        "defect_leakage_count": m.defect_leakage_count,
        "release_success": m.release_success,
        "delivery_score": float(m.delivery_score),
        "recorded_at": m.recorded_at,
    }
