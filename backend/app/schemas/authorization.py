from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.authorization import AuthorizedSystem, ComplianceStatus


class AuthorizationCreate(BaseModel):
    employee_id: int
    system: AuthorizedSystem
    access_level: str = "ReadOnly"
    expires_at: Optional[datetime] = None


class AuthorizationUpdate(BaseModel):
    access_level: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    compliance_status: Optional[ComplianceStatus] = None


class AuthorizationResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    system: AuthorizedSystem
    access_level: str
    granted_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    compliance_status: ComplianceStatus

    class Config:
        from_attributes = True


class ComplianceReportRow(BaseModel):
    system: AuthorizedSystem
    team_name: str
    compliant_count: int
    expired_count: int
    pending_count: int
    revoked_count: int
