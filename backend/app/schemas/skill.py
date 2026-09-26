from typing import Optional, List
from pydantic import BaseModel
from app.models.employee_skill import ProficiencyLevel


class SkillBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True


class CapabilityMatrixRow(BaseModel):
    employee_id: int
    employee_name: str
    skills: List[dict]  # [{skill_id, skill_name, proficiency_level}]
