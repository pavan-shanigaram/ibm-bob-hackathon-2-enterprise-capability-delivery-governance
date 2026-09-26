from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.allocation import ResourceAllocationCreate, ResourceAllocationResponse, OverAllocationAlert
from app.services import allocation_service

router = APIRouter(prefix="/allocations", tags=["Resource Allocation"])


@router.get("", response_model=List[ResourceAllocationResponse])
def list_allocations(
    employee_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return allocation_service.get_allocations(db, employee_id=employee_id)


@router.post("", response_model=ResourceAllocationResponse, status_code=201)
def create_allocation(
    data: ResourceAllocationCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "team_lead"])),
):
    return allocation_service.create_allocation(db, data)


@router.get("/over-allocated")
def over_allocated(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return allocation_service.get_over_allocated(db)
