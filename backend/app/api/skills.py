from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.skill import SkillCreate, SkillResponse, CapabilityMatrixRow
from app.services import skill_service

router = APIRouter(prefix="/skills", tags=["Skills & Capabilities"])


@router.get("", response_model=List[SkillResponse])
def list_skills(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return skill_service.get_skills(db)


@router.post("", response_model=SkillResponse, status_code=201)
def create_skill(
    data: SkillCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin"])),
):
    return skill_service.create_skill(db, data)


@router.get("/matrix")
def capability_matrix(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return skill_service.get_capability_matrix(db)


@router.get("/gaps")
def skill_gap_report(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return skill_service.get_skill_gaps(db)
