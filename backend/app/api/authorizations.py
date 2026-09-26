from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import TokenData
from app.schemas.authorization import AuthorizationCreate, AuthorizationUpdate, AuthorizationResponse, ComplianceReportRow
from app.services import authorization_service

router = APIRouter(prefix="/authorizations", tags=["Authorizations & Compliance"])


@router.get("", response_model=List[AuthorizationResponse])
def list_authorizations(
    employee_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return authorization_service.get_authorizations(db, employee_id=employee_id)


@router.post("", response_model=AuthorizationResponse, status_code=201)
def create_authorization(
    data: AuthorizationCreate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "security_admin"])),
):
    return authorization_service.create_authorization(db, data)


@router.put("/{auth_id}", response_model=AuthorizationResponse)
def update_authorization(
    auth_id: int,
    data: AuthorizationUpdate,
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "security_admin"])),
):
    return authorization_service.update_authorization(db, auth_id, data)


@router.get("/compliance-report")
def compliance_report(
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_user),
):
    return authorization_service.get_compliance_report(db)


@router.post("/check-expiries")
def check_expiries(
    db: Session = Depends(get_db),
    _: TokenData = Depends(require_roles(["platform_admin", "security_admin"])),
):
    count = authorization_service.check_and_update_expiries(db)
    return {"updated": count, "message": f"{count} authorizations marked as expired"}
