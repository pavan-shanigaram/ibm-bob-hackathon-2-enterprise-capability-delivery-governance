import enum
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum
from app.core.database import Base


class AuthorizedSystem(str, enum.Enum):
    GitHub = "GitHub"
    AzureDevOps = "AzureDevOps"
    SAP = "SAP"
    Salesforce = "Salesforce"
    Production = "Production"


class ComplianceStatus(str, enum.Enum):
    Compliant = "Compliant"
    Expired = "Expired"
    PendingReview = "PendingReview"
    Revoked = "Revoked"


class Authorization(Base):
    __tablename__ = "authorizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    system: Mapped[AuthorizedSystem] = mapped_column(SAEnum(AuthorizedSystem), nullable=False)
    access_level: Mapped[str] = mapped_column(String(100), default="ReadOnly")
    granted_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    compliance_status: Mapped[ComplianceStatus] = mapped_column(SAEnum(ComplianceStatus), default=ComplianceStatus.Compliant)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="authorizations")
