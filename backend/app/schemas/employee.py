from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.employee import EmployeeRole
from app.models.employee_skill import ProficiencyLevel


class EmployeeBase(BaseModel):
    name: str
    email: str
    job_title: Optional[str] = None
    role: EmployeeRole
    team_id: Optional[int] = None
    allocation_percentage: float = 0.0
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    auth0_user_id: Optional[str] = None


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    job_title: Optional[str] = None
    role: Optional[EmployeeRole] = None
    team_id: Optional[int] = None
    is_active: Optional[bool] = None


class EmployeeSkillAdd(BaseModel):
    skill_id: int
    proficiency_level: ProficiencyLevel


class EmployeeSkillResponse(BaseModel):
    id: int
    skill_id: int
    skill_name: str
    skill_category: str
    proficiency_level: ProficiencyLevel

    class Config:
        from_attributes = True


class EmployeeResponse(EmployeeBase):
    id: int
    auth0_user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    utilization_percentage: float = 0.0
    squad_count: int = 0

    class Config:
        from_attributes = True
