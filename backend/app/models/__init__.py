# Import all models here so Alembic can detect them via Base.metadata
from app.models.team import Team  # noqa: F401
from app.models.employee import Employee, EmployeeRole  # noqa: F401
from app.models.squad import Squad  # noqa: F401
from app.models.squad_member import SquadMember, SquadRoleEnum  # noqa: F401
from app.models.skill import Skill  # noqa: F401
from app.models.employee_skill import EmployeeSkill, ProficiencyLevel  # noqa: F401
from app.models.project import Project, ProjectStatus, ProjectPriority, HealthIndicator  # noqa: F401
from app.models.project_assignment import ProjectSquadAssignment, ProjectEmployeeAssignment  # noqa: F401
from app.models.authorization import Authorization, AuthorizedSystem, ComplianceStatus  # noqa: F401
from app.models.delivery_metric import DeliveryMetric  # noqa: F401
from app.models.resource_allocation import ResourceAllocation  # noqa: F401
from app.models.capability_requirement import CapabilityRequirement  # noqa: F401
from app.models.project_team_phase import ProjectTeamPhase, PhaseStatus  # noqa: F401
from app.models.project_team_dependency import ProjectTeamDependency, DependencyType, DependencyStatus  # noqa: F401
