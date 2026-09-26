from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel


class ResourceAllocationCreate(BaseModel):
    employee_id: int
    project_id: Optional[int] = None
    squad_id: Optional[int] = None
    allocation_percentage: float
    period_start: date
    period_end: date


class ResourceAllocationResponse(BaseModel):
    id: int
    employee_id: int
    project_id: Optional[int]
    squad_id: Optional[int]
    allocation_percentage: float
    period_start: date
    period_end: date
    is_over_allocated: bool

    class Config:
        from_attributes = True


class OverAllocationAlert(BaseModel):
    employee_id: int
    employee_name: str
    total_allocation: float
    allocations: list
