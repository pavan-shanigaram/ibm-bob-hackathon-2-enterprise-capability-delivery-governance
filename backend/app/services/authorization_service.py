from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.authorization import Authorization, ComplianceStatus
from app.models.employee import Employee
from app.models.team import Team
from app.schemas.authorization import AuthorizationCreate, AuthorizationUpdate


def get_authorizations(db: Session, employee_id: int = None) -> List[dict]:
    query = db.query(Authorization)
    if employee_id:
        query = query.filter(Authorization.employee_id == employee_id)
    auths = query.all()
    return [_enrich(db, a) for a in auths]


def create_authorization(db: Session, data: AuthorizationCreate) -> dict:
    emp = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    auth = Authorization(**data.model_dump())
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return _enrich(db, auth)


def update_authorization(db: Session, auth_id: int, data: AuthorizationUpdate) -> dict:
    auth = db.query(Authorization).filter(Authorization.id == auth_id).first()
    if not auth:
        raise HTTPException(status_code=404, detail="Authorization not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(auth, field, value)
    db.commit()
    db.refresh(auth)
    return _enrich(db, auth)


def check_and_update_expiries(db: Session) -> int:
    """Mark expired authorizations and return count updated."""
    now = datetime.utcnow()
    expired = db.query(Authorization).filter(
        Authorization.expires_at <= now,
        Authorization.is_active == True
    ).all()
    for a in expired:
        a.is_active = False
        a.compliance_status = ComplianceStatus.Expired
    db.commit()
    return len(expired)


def get_compliance_report(db: Session) -> List[dict]:
    check_and_update_expiries(db)
    teams = db.query(Team).all()
    systems = ["GitHub", "AzureDevOps", "SAP", "Salesforce", "Production"]
    result = []
    for team in teams:
        emp_ids = [e.id for e in db.query(Employee).filter(Employee.team_id == team.id).all()]
        for sys in systems:
            auths = db.query(Authorization).filter(
                Authorization.employee_id.in_(emp_ids),
                Authorization.system == sys
            ).all() if emp_ids else []
            result.append({
                "system": sys,
                "team_name": team.name,
                "compliant_count": sum(1 for a in auths if a.compliance_status == "Compliant"),
                "expired_count": sum(1 for a in auths if a.compliance_status == "Expired"),
                "pending_count": sum(1 for a in auths if a.compliance_status == "PendingReview"),
                "revoked_count": sum(1 for a in auths if a.compliance_status == "Revoked"),
            })
    return result


def _enrich(db: Session, a: Authorization) -> dict:
    emp = db.query(Employee).filter(Employee.id == a.employee_id).first()
    return {
        "id": a.id,
        "employee_id": a.employee_id,
        "employee_name": emp.name if emp else "Unknown",
        "system": a.system,
        "access_level": a.access_level,
        "granted_at": a.granted_at,
        "expires_at": a.expires_at,
        "is_active": a.is_active,
        "compliance_status": a.compliance_status,
    }
