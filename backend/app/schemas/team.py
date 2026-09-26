from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    lead_employee_id: Optional[int] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    lead_employee_id: Optional[int] = None


class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    squad_count: int = 0
    employee_count: int = 0

    class Config:
        from_attributes = True
