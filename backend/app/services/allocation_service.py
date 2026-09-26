from typing import List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.resource_allocation import ResourceAllocation
from app.models.employee import Employee
from app.schemas.allocation import ResourceAllocationCreate


def create_allocation(db: Session, data: ResourceAllocationCreate) -> dict:
    allocation = ResourceAllocation(**data.model_dump())
    # Check over-allocation
    total = db.query(func.sum(ResourceAllocation.allocation_percentage)).filter(
        ResourceAllocation.employee_id == data.employee_id,
        ResourceAllocation.period_start <= data.period_end,
        ResourceAllocation.period_end >= data.period_start,
    ).scalar() or 0
    allocation.is_over_allocated = (float(total) + data.allocation_percentage) > 100
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return _to_dict(allocation)


def get_allocations(db: Session, employee_id: int = None) -> List[dict]:
    query = db.query(ResourceAllocation)
    if employee_id:
        query = query.filter(ResourceAllocation.employee_id == employee_id)
    return [_to_dict(a) for a in query.all()]


def get_over_allocated(db: Session) -> List[dict]:
    """Return employees with total current allocation > 100%."""
    today = date.today()
    employees = db.query(Employee).filter(Employee.is_active == True).all()
    alerts = []
    for emp in employees:
        allocations = db.query(ResourceAllocation).filter(
            ResourceAllocation.employee_id == emp.id,
            ResourceAllocation.period_start <= today,
            ResourceAllocation.period_end >= today,
        ).all()
        total = sum(float(a.allocation_percentage) for a in allocations)
        if total > 100:
            alerts.append({
                "employee_id": emp.id,
                "employee_name": emp.name,
                "total_allocation": total,
                "allocations": [_to_dict(a) for a in allocations],
            })
    return alerts


def _to_dict(a: ResourceAllocation) -> dict:
    return {
        "id": a.id,
        "employee_id": a.employee_id,
        "project_id": a.project_id,
        "squad_id": a.squad_id,
        "allocation_percentage": float(a.allocation_percentage),
        "period_start": a.period_start,
        "period_end": a.period_end,
        "is_over_allocated": a.is_over_allocated,
    }
