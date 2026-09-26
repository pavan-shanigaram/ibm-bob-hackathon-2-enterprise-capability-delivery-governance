from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.squad_member import SquadRoleEnum


class SquadBase(BaseModel):
    name: str
    team_id: int
    scrum_master_id: Optional[int] = None
    capacity_points: int = 0
    description: Optional[str] = None


class SquadCreate(SquadBase):
    pass


class SquadUpdate(BaseModel):
    name: Optional[str] = None
    scrum_master_id: Optional[int] = None
    capacity_points: Optional[int] = None
    description: Optional[str] = None


class SquadMemberAdd(BaseModel):
    employee_id: int
    role_in_squad: SquadRoleEnum
    allocation_percentage: float = 100.0


class SquadMemberResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    role_in_squad: SquadRoleEnum
    allocation_percentage: float

    class Config:
        from_attributes = True


class SquadResponse(SquadBase):
    id: int
    created_at: datetime
    updated_at: datetime
    member_count: int = 0

    class Config:
        from_attributes = True
