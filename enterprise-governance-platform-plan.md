# Enterprise Capability & Delivery Governance Platform — Master Plan

## Top-Level Overview

**Goal:** Design and build an enterprise-grade platform that enables organizations to manage teams, squads, employees, projects, capabilities, resource allocation, authorization compliance, and delivery performance — all surfaced through an executive governance dashboard.

**Hackathon Scope:** Full-stack monorepo delivered as a runnable Docker Compose stack. No external CI/CD pipeline required. Dashboards built inside the React frontend using Recharts. Platform includes IBM watsonx.ai (Granite) AI intelligence layer and live demo endpoints for judging.

**Technology Stack:**
| Layer | Technology |
|---|---|
| Backend API | Python — FastAPI |
| Database | MySQL 8 |
| ORM | SQLAlchemy + Alembic |
| Authentication | Auth0 (JWT RBAC) |
| Frontend | React 18 + TypeScript + Vite |
| Charts | Recharts |
| Styling | Tailwind CSS |
| Containerisation | Docker Compose |
| API Documentation | Swagger UI (built into FastAPI) |
| AI Intelligence | IBM watsonx.ai — ibm/granite-3-3-8b-instruct via ibm-watsonx-ai Python SDK |

**Repository Structure (Monorepo):**
```
/
├── backend/
│   ├── app/
│   │   ├── api/           # Route handlers per domain
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── services/      # Business logic layer
│   │   ├── auth/          # Auth0 JWT verification + RBAC
│   │   ├── core/          # Config, database session, constants
│   │   └── main.py        # FastAPI app entry point
│   ├── alembic/           # DB migrations
│   ├── seed/              # Sample data scripts
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/           # Axios API client per domain
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Full page views
│   │   ├── hooks/         # Custom React hooks
│   │   ├── context/       # Auth context
│   │   ├── types/         # TypeScript interfaces
│   │   └── main.tsx       # App entry point
│   ├── package.json
│   └── Dockerfile
├── docs/
│   ├── architecture.md
│   ├── er-diagram.md
│   ├── api-spec.md
│   ├── rbac-model.md
│   └── dashboard-design.md
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Database ER Model (Entity Definitions)

### Core Entities

**teams** — top-level organizational unit
- id, name, description, lead_employee_id (FK→employees), created_at, updated_at

**squads** — scrum squads belonging to a team
- id, name, team_id (FK→teams), scrum_master_id (FK→employees), capacity_points, created_at, updated_at

**employees** — people across all teams
- id, name, email, job_title, role (enum), team_id (FK→teams), auth0_user_id, allocation_percentage, is_active, created_at, updated_at

**squad_members** — many-to-many: employees ↔ squads
- id, squad_id, employee_id, role_in_squad (enum), allocation_percentage

**skills** — canonical skill taxonomy
- id, name, category (e.g. Frontend, Backend, Cloud, Security), description

**employee_skills** — proficiency per employee per skill
- id, employee_id, skill_id, proficiency_level (enum: Beginner/Intermediate/Expert/Lead)

**projects** — project registry
- id, name, description, status (enum), priority (enum), start_date, end_date, owner_team_id, owner_squad_id, health_indicator (enum: Green/Amber/Red)

**project_squad_assignments** — squads assigned to projects
- id, project_id, squad_id, assigned_at

**project_employee_assignments** — individuals assigned to projects
- id, project_id, employee_id, allocation_percentage, role_on_project, assigned_at

**authorizations** — access control records per employee
- id, employee_id, system (enum: GitHub/AzureDevOps/SAP/Salesforce/Production), access_level, granted_at, expires_at, is_active, compliance_status (enum)

**delivery_metrics** — sprint-level performance data
- id, squad_id, project_id, sprint_name, sprint_start, sprint_end, velocity, story_points_planned, story_points_delivered, cycle_time_days, lead_time_days, defect_leakage_count, release_success (bool), delivery_score, recorded_at

**resource_allocations** — allocation tracking with over-allocation detection
- id, employee_id, project_id, squad_id, allocation_percentage, period_start, period_end, is_over_allocated (computed)

**capability_requirements** — skills required by a project
- id, project_id, skill_id, required_proficiency, headcount_needed

---

## RBAC Security Model

### Roles (Auth0 custom claims)
| Role | Permissions |
|---|---|
| `platform_admin` | Full CRUD on all entities, user management |
| `team_lead` | CRUD on own team's squads, employees, projects; read-only on others |
| `scrum_master` | CRUD on own squad's delivery metrics, sprint data; read members |
| `employee` | Read own profile, skills, assignments; update own skills |
| `executive` | Read-only on all dashboards and reports |
| `security_admin` | CRUD on authorizations and compliance records |

### JWT Claim Structure
```json
{
  "sub": "auth0|...",
  "email": "user@org.com",
  "https://governance/roles": ["team_lead"],
  "https://governance/team_id": 3
}
```

---

## API Design Summary

All endpoints are prefixed `/api/v1/`. Auth0 JWT Bearer token required on all routes.

### Domain Groups
| Router | Base Path | Key Operations |
|---|---|---|
| Teams | `/teams` | CRUD teams, team capacity, team leads |
| Squads | `/squads` | CRUD squads, squad members, capacity |
| Employees | `/employees` | CRUD employees, skills, utilization |
| Skills | `/skills` | Skill taxonomy CRUD |
| Projects | `/projects` | CRUD projects, squad/employee assignments |
| Authorizations | `/authorizations` | Access records, compliance reports |
| Delivery Metrics | `/metrics` | Sprint metrics CRUD, velocity trends |
| Resource Allocation | `/allocations` | Allocation records, over-allocation alerts |
| Dashboard | `/dashboard` | Aggregated read-only dashboard data |
| Reports | `/reports` | Skill gap, capacity risk, delivery bottlenecks |

---

## Sub-Tasks

---

### Sub-Task 1 — Repository Scaffold & Docker Compose Setup
**Status:** [ ] pending

**Intent:**
Establish the monorepo folder structure, Docker Compose orchestration, environment configuration, and base project files. This is the foundation every other sub-task builds on.

**Expected Outcomes:**
- `docker-compose.yml` runs MySQL, backend (FastAPI), and frontend (React/Vite) containers
- Backend container starts and serves `GET /health → 200 OK`
- Frontend container serves the Vite dev/build output
- `.env.example` documents all required environment variables
- `README.md` updated with setup instructions

**Todo List:**
1. Create `docker-compose.yml` with services: `db` (MySQL 8), `backend` (FastAPI), `frontend` (React Vite)
2. Create `backend/Dockerfile` — Python 3.11 slim, install requirements, uvicorn entrypoint
3. Create `backend/requirements.txt` — fastapi, uvicorn, sqlalchemy, alembic, pymysql, python-jose, pydantic[email], python-dotenv, httpx
4. Create `backend/app/core/config.py` — settings via pydantic-settings from env vars
5. Create `backend/app/core/database.py` — SQLAlchemy engine + SessionLocal + get_db dependency
6. Create `backend/app/main.py` — FastAPI app, CORS middleware, router registration, `/health` endpoint
7. Create `frontend/Dockerfile` — Node 20 alpine, npm install, vite build
8. Create `frontend/package.json` — React 18, TypeScript, Vite, Tailwind CSS, Recharts, Axios, React Router
9. Create `frontend/src/main.tsx` and `frontend/src/App.tsx` shell
10. Update root `README.md` with `docker compose up` quick-start instructions
11. Update `.env.example` with all required variables (DB creds, Auth0 domain/client, secret key)

**Relevant Context:**
- Target directory: `ibm-bob-hackathon-2-enterprise-capability-delivery-governance/`
- All new files go inside this repo directory

---

### Sub-Task 2 — Database Models & Alembic Migrations
**Status:** [ ] pending

**Intent:**
Define all SQLAlchemy ORM models for every entity and generate the initial Alembic migration. This creates the full schema in MySQL.

**Expected Outcomes:**
- All 14 ORM model files exist under `backend/app/models/`
- `alembic/versions/001_initial_schema.py` migration creates all tables
- Running `alembic upgrade head` inside the container produces a clean schema with no errors
- All foreign key relationships, indexes, and enum columns are correctly defined

**Todo List:**
1. Create `backend/app/models/__init__.py` — imports all models for Alembic auto-detection
2. Create `backend/app/models/team.py` — Team model
3. Create `backend/app/models/squad.py` — Squad model with FK to Team
4. Create `backend/app/models/employee.py` — Employee model with enums for role
5. Create `backend/app/models/squad_member.py` — Squad ↔ Employee junction
6. Create `backend/app/models/skill.py` — Skill taxonomy model
7. Create `backend/app/models/employee_skill.py` — Employee ↔ Skill with proficiency enum
8. Create `backend/app/models/project.py` — Project model with status/priority/health enums
9. Create `backend/app/models/project_assignment.py` — Squad and Employee project assignments
10. Create `backend/app/models/authorization.py` — Authorization records with system and compliance enums
11. Create `backend/app/models/delivery_metric.py` — Sprint-level metrics
12. Create `backend/app/models/resource_allocation.py` — Allocation records with computed over-allocation flag
13. Create `backend/app/models/capability_requirement.py` — Project skill requirements
14. Configure `alembic/env.py` to use the app's metadata and DB URL from config
15. Generate and review initial migration: `alembic revision --autogenerate -m "initial_schema"`

**Relevant Context:**
- Sub-Task 1 must be complete (database.py and config.py exist)
- Use SQLAlchemy declarative base from `backend/app/core/database.py`
- MySQL enum columns: use `sqlalchemy.Enum` with Python `enum.Enum` classes defined in each model file

---

### Sub-Task 3 — Auth0 Integration & RBAC Middleware
**Status:** [ ] pending

**Intent:**
Implement JWT verification against Auth0 and a role-based permission system that protects all API routes.

**Expected Outcomes:**
- `backend/app/auth/` module verifies Auth0 JWTs using JWKS
- Custom Auth0 namespace claims for `roles` and `team_id` are extracted
- FastAPI dependency `require_roles(["platform_admin"])` can be used on any route
- Unauthorized requests return `401`; forbidden role returns `403`

**Todo List:**
1. Create `backend/app/auth/auth0.py` — fetch JWKS from Auth0, verify JWT signature, decode claims
2. Create `backend/app/auth/dependencies.py` — `get_current_user` FastAPI dependency; `require_roles` factory
3. Create `backend/app/auth/models.py` — `TokenData` Pydantic model (sub, email, roles, team_id)
4. Add Auth0 env vars to `config.py`: `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, `AUTH0_NAMESPACE`
5. Add CORS middleware configuration to `main.py` using `FRONTEND_URL` env var
6. Write a test script `backend/tests/test_auth.py` that validates a mock JWT decode
7. Document Auth0 application setup steps in `docs/rbac-model.md`

**Relevant Context:**
- Auth0 custom claims namespace: `https://governance/`
- Claims to extract: `roles` (list), `team_id` (int)
- python-jose library handles JWT decode; httpx fetches JWKS

---

### Sub-Task 4 — Team & Squad API Module
**Status:** [ ] pending

**Intent:**
Build the full CRUD API for Teams and Squads including capacity endpoints and squad member management.

**Expected Outcomes:**
- `GET /api/v1/teams` returns paginated list of teams with their lead and squad count
- `POST /api/v1/teams` creates a team (platform_admin only)
- `GET /api/v1/teams/{id}/squads` returns all squads for a team
- `POST /api/v1/squads/{id}/members` adds an employee to a squad with role and allocation
- All endpoints protected by Auth0 JWT and role guards

**Todo List:**
1. Create `backend/app/schemas/team.py` — TeamCreate, TeamUpdate, TeamResponse Pydantic schemas
2. Create `backend/app/schemas/squad.py` — SquadCreate, SquadUpdate, SquadResponse, SquadMemberAdd schemas
3. Create `backend/app/services/team_service.py` — business logic: create, list, get, update, delete, get_capacity
4. Create `backend/app/services/squad_service.py` — business logic: CRUD + member add/remove + capacity calc
5. Create `backend/app/api/teams.py` — FastAPI router with all team endpoints
6. Create `backend/app/api/squads.py` — FastAPI router with all squad endpoints
7. Register both routers in `main.py`
8. Add pagination support using `skip` and `limit` query params on all list endpoints

**Relevant Context:**
- Team capacity = sum of all member allocation_percentage across the team's squads
- Squad capacity_points field is manually maintained by scrum master
- Role guard: team creation = platform_admin; team update = platform_admin or team_lead of that team

---

### Sub-Task 5 — Employee & Skills API Module
**Status:** [ ] pending

**Intent:**
Build the employee profile management API, skill taxonomy API, and proficiency assignment endpoints. This powers the capability matrix and skill gap analysis.

**Expected Outcomes:**
- `GET /api/v1/employees` lists employees with team, squad memberships, and utilization %
- `POST /api/v1/employees/{id}/skills` assigns a skill with proficiency level
- `GET /api/v1/skills/matrix` returns the full capability matrix (employees × skills)
- `GET /api/v1/reports/skill-gaps` returns projects with unfilled capability requirements
- Employee utilization = sum of all active project allocation percentages

**Todo List:**
1. Create `backend/app/schemas/employee.py` — EmployeeCreate, EmployeeUpdate, EmployeeResponse, UtilizationResponse schemas
2. Create `backend/app/schemas/skill.py` — SkillCreate, SkillResponse, EmployeeSkillAdd, CapabilityMatrixRow schemas
3. Create `backend/app/services/employee_service.py` — CRUD, utilization calc, squad memberships
4. Create `backend/app/services/skill_service.py` — skill CRUD, capability matrix builder, skill gap analyzer
5. Create `backend/app/api/employees.py` — employee router with profile, skills, utilization endpoints
6. Create `backend/app/api/skills.py` — skill taxonomy and matrix endpoints
7. Register routers in `main.py`
8. Utilization over-allocation threshold: flag employee if total allocation > 100%

**Relevant Context:**
- Skill gap = capability_requirements for active projects where no qualified employee (matching proficiency) is assigned
- Capability matrix query: JOIN employees → employee_skills → skills, pivot by skill category

---

### Sub-Task 6 — Project Management API Module
**Status:** [ ] pending

**Intent:**
Build the project registry with full lifecycle management, squad/employee assignment, and health tracking.

**Expected Outcomes:**
- `POST /api/v1/projects` creates a project with owner team/squad
- `PUT /api/v1/projects/{id}/squads` assigns squads to a project
- `PUT /api/v1/projects/{id}/employees` assigns employees with allocation %
- `GET /api/v1/projects/{id}/health` returns health_indicator, delivery score, resource coverage
- Project status transitions: Draft → Active → On Hold → Completed → Cancelled

**Todo List:**
1. Create `backend/app/schemas/project.py` — ProjectCreate, ProjectUpdate, ProjectResponse, ProjectHealthResponse schemas
2. Create `backend/app/services/project_service.py` — CRUD, squad assignment, employee assignment, health calculation
3. Create `backend/app/api/projects.py` — project router
4. Health indicator logic: Green if delivery_score ≥ 80 and no over-allocated employees; Amber if score 60–79 or 1 over-allocated; Red otherwise
5. Add `GET /api/v1/projects` with filters: status, priority, team, date range
6. Register router in `main.py`

**Relevant Context:**
- Project ownership is at team level (owner_team_id) and optionally squad level
- Multiple squads can be assigned to one project (cross-team collaboration)
- health_indicator is auto-computed by the service, not manually set

---

### Sub-Task 7 — Authorization & Compliance API Module
**Status:** [ ] pending

**Intent:**
Track system access grants (GitHub, Azure DevOps, SAP, Salesforce, Production) per employee and generate compliance reports.

**Expected Outcomes:**
- `POST /api/v1/authorizations` records a new access grant
- `GET /api/v1/authorizations/compliance-report` returns employees with expired or non-compliant access
- `GET /api/v1/authorizations/employee/{id}` returns all system access for an employee
- Expired authorizations are flagged automatically

**Todo List:**
1. Create `backend/app/schemas/authorization.py` — AuthorizationCreate, AuthorizationResponse, ComplianceReportRow schemas
2. Create `backend/app/services/authorization_service.py` — CRUD, expiry check, compliance report aggregation
3. Create `backend/app/api/authorizations.py` — authorization router
4. Expiry logic: `expires_at < NOW()` → set `is_active = False`, `compliance_status = "Expired"`
5. Compliance report: group by system, show count of active/expired/non-compliant per team
6. Register router in `main.py`

**Relevant Context:**
- Authorized systems enum: GitHub, AzureDevOps, SAP, Salesforce, Production
- compliance_status enum: Compliant, Expired, PendingReview, Revoked
- security_admin role required for CRUD; all roles can read own authorizations

---

### Sub-Task 8 — Delivery Metrics & Resource Allocation API Module
**Status:** [ ] pending

**Intent:**
Build the sprint performance tracking API and resource allocation management with over-allocation detection.

**Expected Outcomes:**
- `POST /api/v1/metrics` records sprint metrics for a squad/project
- `GET /api/v1/metrics/squad/{id}/velocity-trend` returns velocity over last N sprints
- `GET /api/v1/allocations/over-allocated` returns employees with total allocation > 100%
- Delivery score formula is consistently applied: weighted composite of velocity ratio, defect leakage, and release success

**Todo List:**
1. Create `backend/app/schemas/metric.py` — DeliveryMetricCreate, DeliveryMetricResponse, VelocityTrendResponse schemas
2. Create `backend/app/schemas/allocation.py` — ResourceAllocationCreate, AllocationResponse, OverAllocationAlert schemas
3. Create `backend/app/services/metric_service.py` — CRUD, delivery score calculation, trend queries
4. Create `backend/app/services/allocation_service.py` — CRUD, over-allocation detection, capacity forecast
5. Create `backend/app/api/metrics.py` — delivery metrics router
6. Create `backend/app/api/allocations.py` — resource allocation router
7. Delivery score formula: `(story_points_delivered / story_points_planned * 50) + (release_success * 30) + ((1 - defect_leakage_count / max(story_points_delivered,1)) * 20)`, capped 0–100
8. Register both routers in `main.py`

**Relevant Context:**
- Over-allocation: SUM of resource_allocations.allocation_percentage per employee where period overlaps today > 100
- Capacity forecast: aggregate team capacity vs sum of project demands for next quarter

---

### Sub-Task 9 — Dashboard & Reports API Module
**Status:** [ ] pending

**Intent:**
Build the aggregated read-only dashboard endpoint that powers the Executive Dashboard in the frontend, plus the reports endpoints for skill gaps, capacity risks, and delivery bottlenecks.

**Expected Outcomes:**
- `GET /api/v1/dashboard/executive` returns a single JSON payload with: team health, resource utilization, project health counts, delivery health, capability coverage %, risk heatmap data
- `GET /api/v1/reports/skill-gaps` returns unfilled capability requirements per project
- `GET /api/v1/reports/capacity-risk` returns teams/squads at > 90% utilization
- `GET /api/v1/reports/delivery-bottlenecks` returns squads with declining velocity or score < 60

**Todo List:**
1. Create `backend/app/schemas/dashboard.py` — ExecutiveDashboard, TeamHealthRow, ResourceUtilizationSummary, RiskHeatmapItem schemas
2. Create `backend/app/services/dashboard_service.py` — aggregate all dashboard data in a single service call
3. Create `backend/app/api/dashboard.py` — dashboard and reports router
4. Executive dashboard payload structure: `{ team_health[], project_health_counts{}, resource_utilization{}, delivery_health{}, capability_coverage_pct, risk_heatmap[], alerts[] }`
5. Risk heatmap: matrix of teams (rows) vs risk dimensions: resource, delivery, capability, compliance (columns), value = risk score 1–5
6. Register router in `main.py`

**Relevant Context:**
- Dashboard endpoint is cached for 5 minutes using a simple in-memory TTL dict (no Redis needed for hackathon)
- `executive` and `platform_admin` roles can access; team_lead sees only their team's data

---

### Sub-Task 10 — Sample Data Seed Script
**Status:** [ ] pending

**Intent:**
Populate the database with realistic sample data covering all 8 teams, multiple squads, employees, projects, metrics, and authorizations so the platform is demonstrable immediately after startup.

**Expected Outcomes:**
- Running `python seed/seed_data.py` populates all tables
- Data includes: 8 teams, 3 squads per team (24 squads), 5–8 employees per squad
- At least 12 active projects with squad/employee assignments
- 3 sprints of delivery metrics per squad
- Authorization records for all employees covering all 5 systems
- Skill assignments covering all proficiency levels

**Todo List:**
1. Create `backend/seed/seed_data.py` — master seed orchestrator
2. Create `backend/seed/data/teams.json` — 8 teams with names and descriptions
3. Create `backend/seed/data/employees.json` — ~150 employees across teams with roles
4. Create `backend/seed/data/skills.json` — 30+ skills across Frontend, Backend, Cloud, Security, SAP, Salesforce, Integration, Data categories
5. Create `backend/seed/data/projects.json` — 12+ projects with statuses, priorities, dates
6. Create `backend/seed/data/metrics.json` — 3 sprints × 24 squads of delivery data
7. Wire seed script into Docker Compose as a one-shot `seed` service that runs after `backend` is healthy
8. Add `make seed` convenience target to root Makefile

**Relevant Context:**
- Teams: Enterprise UI, SAP, Salesforce, Platform, Integration, Security, Network, BAU
- Employee roles enum: Designer, Developer, BusinessAnalyst, ScrumMaster, PlatformEngineer, OperationsEngineer, QAEngineer, Architect

---

### Sub-Task 11 — React Frontend Shell & Navigation
**Status:** [ ] pending

**Intent:**
Build the React + TypeScript frontend application shell including routing, Auth0 login integration, sidebar navigation, layout, and Axios API client setup.

**Expected Outcomes:**
- Application launches and shows a login page
- After Auth0 login, user sees the main layout with sidebar
- Sidebar has navigation links to all major modules
- Axios client automatically attaches JWT Bearer token
- TypeScript interfaces match all backend response schemas

**Todo List:**
1. Create `frontend/src/context/AuthContext.tsx` — Auth0Provider wrapper, `useAuth` hook
2. Create `frontend/src/api/client.ts` — Axios instance with `baseURL`, JWT interceptor
3. Create `frontend/src/api/teams.ts`, `squads.ts`, `employees.ts`, `projects.ts`, `metrics.ts`, `dashboard.ts` — typed API functions
4. Create `frontend/src/types/index.ts` — all TypeScript interfaces mirroring backend schemas
5. Create `frontend/src/components/Layout/Sidebar.tsx` — nav links: Dashboard, Teams, Squads, Employees, Projects, Capabilities, Authorizations, Delivery Metrics, Reports
6. Create `frontend/src/components/Layout/TopBar.tsx` — user avatar, role badge, logout
7. Create `frontend/src/App.tsx` — React Router routes, protected route wrapper
8. Create `frontend/src/pages/Login.tsx` — Auth0 redirect login page
9. Configure Tailwind CSS in `tailwind.config.ts` and `src/index.css`

**Relevant Context:**
- Use `@auth0/auth0-react` SDK
- Protected route: if not authenticated, redirect to `/login`
- API base URL comes from `VITE_API_URL` env var

---

### Sub-Task 12 — Team, Squad & Employee UI Pages
**Status:** [ ] pending

**Intent:**
Build the CRUD UI pages for Teams, Squads, and Employees with data tables, modals for create/edit, and drill-down detail views.

**Expected Outcomes:**
- `/teams` page: table of teams with squad count, lead, capacity bar; Create/Edit modal
- `/squads` page: grouped by team; shows members, scrum master, capacity
- `/employees` page: searchable table with role, team, utilization badge; profile detail drawer
- `/employees/{id}` page: full profile — skills with proficiency chips, current projects, squad memberships

**Todo List:**
1. Create `frontend/src/components/common/DataTable.tsx` — reusable sortable, filterable table
2. Create `frontend/src/components/common/Modal.tsx` — reusable modal wrapper
3. Create `frontend/src/components/common/UtilizationBar.tsx` — colored progress bar (green/amber/red)
4. Create `frontend/src/pages/Teams/TeamsPage.tsx` — teams list with Create/Edit/Delete
5. Create `frontend/src/pages/Teams/TeamDetailPage.tsx` — team detail: squads, members, capacity
6. Create `frontend/src/pages/Squads/SquadsPage.tsx` — squads list grouped by team
7. Create `frontend/src/pages/Employees/EmployeesPage.tsx` — searchable employee list
8. Create `frontend/src/pages/Employees/EmployeeDetailPage.tsx` — employee profile with skills, projects

**Relevant Context:**
- Utilization color thresholds: < 80% = green, 80–99% = amber, ≥ 100% = red
- Skill proficiency chips: Beginner (grey), Intermediate (blue), Expert (green), Lead (purple)

---

### Sub-Task 13 — Project Management & Authorization UI Pages
**Status:** [ ] pending

**Intent:**
Build the project registry UI with health indicators and the authorization/compliance tracking UI.

**Expected Outcomes:**
- `/projects` page: card and table views, filters by status/priority/team; health indicator badge
- `/projects/{id}` page: project detail — assigned squads, employees, capability requirements, delivery score
- `/authorizations` page: table of access records per employee; compliance status badges
- `/authorizations/compliance-report` page: compliance summary by system and team

**Todo List:**
1. Create `frontend/src/components/common/HealthBadge.tsx` — Green/Amber/Red badge component
2. Create `frontend/src/components/common/StatusChip.tsx` — project status chip
3. Create `frontend/src/pages/Projects/ProjectsPage.tsx` — project list with health indicators
4. Create `frontend/src/pages/Projects/ProjectDetailPage.tsx` — project detail view
5. Create `frontend/src/pages/Authorizations/AuthorizationsPage.tsx` — access records table
6. Create `frontend/src/pages/Authorizations/ComplianceReportPage.tsx` — compliance summary

**Relevant Context:**
- Project health badge is sourced from the backend `health_indicator` field (auto-computed)
- Compliance status colors: Compliant = green, Expired = red, PendingReview = amber, Revoked = grey

---

### Sub-Task 14 — Delivery Metrics UI & Capability Matrix Page
**Status:** [ ] pending

**Intent:**
Build the sprint performance tracking UI with velocity charts and the capability matrix / skill gap analysis page.

**Expected Outcomes:**
- `/metrics` page: squad selector → velocity trend line chart, delivery score gauge, sprint table
- `/capabilities` page: capability matrix heatmap (employees as rows, skills as columns, color by proficiency)
- `/reports/skill-gaps` page: table of projects with missing skill coverage

**Todo List:**
1. Create `frontend/src/pages/Metrics/DeliveryMetricsPage.tsx` — velocity trend chart using Recharts LineChart
2. Create `frontend/src/pages/Metrics/SprintDetailPage.tsx` — sprint-level breakdown table
3. Create `frontend/src/components/charts/VelocityChart.tsx` — Recharts LineChart component
4. Create `frontend/src/components/charts/DeliveryScoreGauge.tsx` — Recharts RadialBarChart gauge
5. Create `frontend/src/pages/Capabilities/CapabilityMatrixPage.tsx` — heatmap grid with color coding
6. Create `frontend/src/pages/Reports/SkillGapReportPage.tsx` — skill gap table
7. Create `frontend/src/pages/Reports/CapacityRiskPage.tsx` — capacity risk table

**Relevant Context:**
- Capability matrix: use CSS grid, not a chart library — better for tabular proficiency data
- Velocity chart: Recharts `<LineChart>` with sprint_name on X-axis, velocity on Y-axis, one line per squad

---

### Sub-Task 15 — Executive Dashboard UI
**Status:** [ ] pending

**Intent:**
Build the primary executive governance dashboard that aggregates all platform data into a single command-center view using Recharts visualizations.

**Expected Outcomes:**
- `/dashboard` page renders all KPI cards, charts, and risk heatmap from the `/api/v1/dashboard/executive` endpoint
- KPI cards: Total Teams, Active Projects, Total Employees, Avg Delivery Score, Over-Allocated Employees
- Charts: Team Health BarChart, Resource Utilization PieChart, Project Health Donut, Delivery Trend LineChart
- Risk Heatmap table: teams × risk dimensions with color-coded cells
- Alerts panel: over-allocation warnings, expired authorizations, low delivery score squads

**Todo List:**
1. Create `frontend/src/pages/Dashboard/ExecutiveDashboard.tsx` — main dashboard page
2. Create `frontend/src/components/dashboard/KPICard.tsx` — metric card with value, label, trend arrow
3. Create `frontend/src/components/charts/TeamHealthChart.tsx` — Recharts BarChart: teams vs health score
4. Create `frontend/src/components/charts/ResourceUtilizationChart.tsx` — Recharts PieChart
5. Create `frontend/src/components/charts/ProjectHealthDonut.tsx` — Recharts PieChart: Green/Amber/Red project counts
6. Create `frontend/src/components/charts/DeliveryTrendChart.tsx` — Recharts LineChart: avg delivery score trend
7. Create `frontend/src/components/dashboard/RiskHeatmap.tsx` — CSS grid heatmap component
8. Create `frontend/src/components/dashboard/AlertsPanel.tsx` — scrollable alerts list

**Relevant Context:**
- Dashboard is polled every 60 seconds using `setInterval` + React `useEffect`
- Color scale for risk heatmap: 1 = green (#22c55e), 2–3 = amber (#f59e0b), 4–5 = red (#ef4444)

---

### Sub-Task 16 — Documentation & Final Integration
**Status:** [ ] pending

**Intent:**
Write all technical documentation, wire everything together, verify end-to-end flow, and prepare the hackathon submission.

**Expected Outcomes:**
- `docs/architecture.md` — solution architecture narrative
- `docs/er-diagram.md` — entity relationship diagram in text/Mermaid
- `docs/api-spec.md` — full REST API endpoint catalogue
- `docs/rbac-model.md` — Auth0 setup guide + role matrix
- `docs/dashboard-design.md` — dashboard wireframe descriptions
- `README.md` updated with full setup, seed, and demo instructions
- Docker Compose `docker compose up` brings up the full platform end-to-end

**Todo List:**
1. Write `docs/architecture.md` — component diagram, data flow, technology rationale
2. Write `docs/er-diagram.md` — ER diagram using Mermaid `erDiagram` syntax
3. Write `docs/api-spec.md` — all endpoints with method, path, request body, response shape
4. Write `docs/rbac-model.md` — Auth0 app creation steps, role assignments, claim rules
5. Write `docs/dashboard-design.md` — describe each dashboard panel, chart type, data source
6. Update root `README.md` — prerequisites, `docker compose up --build`, seed command, login, demo walkthrough
7. Final integration check: verify all frontend API calls resolve correctly against backend routes
8. Verify all Docker Compose health checks pass

---

### Sub-Task 17 — IBM watsonx.ai Intelligence Layer
**Status:** [ ] pending

**Intent:**
Integrate IBM watsonx.ai (Granite) into the platform to provide AI-powered governance intelligence. This differentiates the hackathon submission by adding generative AI insights directly into the governance workflow using the official `ibm-watsonx-ai` Python SDK and the `ibm/granite-3-3-8b-instruct` model.

**Expected Outcomes:**
- `backend/app/services/watsonx_service.py` — SDK-based service that calls `ModelInference.generate_text()`
- `POST /api/v1/ai/skill-gap-narrative` — given a project's skill gap data, returns a natural-language summary and hiring recommendations
- `POST /api/v1/ai/delivery-coach` — given squad delivery metrics history, returns actionable coaching recommendations
- `POST /api/v1/ai/risk-summary` — given the executive dashboard risk heatmap, returns a boardroom-ready risk narrative
- `GET /api/v1/ai/health` — confirms watsonx connectivity; returns model id and status
- Frontend: AI Insights panel on Executive Dashboard showing generated narratives with a "Refresh AI Insights" button

**Todo List:**
1. Add `ibm-watsonx-ai` to `backend/requirements.txt`
2. Add watsonx env vars to `config.py` and `.env.example`: `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL` (e.g. `https://us-south.ml.cloud.ibm.com`), `WATSONX_MODEL_ID` (default `ibm/granite-3-3-8b-instruct`)
3. Create `backend/app/services/watsonx_service.py`:
   - Instantiate `ModelInference` using `ibm_watsonx_ai.foundation_models.ModelInference` with `credentials={"apikey": WATSONX_API_KEY, "url": WATSONX_URL}` and `project_id=WATSONX_PROJECT_ID`
   - Expose `generate(prompt: str) -> str` wrapper that calls `model.generate_text(prompt=prompt)`
   - Graceful fallback: if `WATSONX_API_KEY` is not set, return a mock/placeholder response so the platform still runs without credentials
4. Create `backend/app/api/ai.py` — AI router with 4 endpoints:
   - `POST /ai/skill-gap-narrative` — accepts `{project_id}`, fetches skill gap data, builds structured prompt, calls watsonx_service
   - `POST /ai/delivery-coach` — accepts `{squad_id}`, fetches last 5 sprints of metrics, builds coaching prompt, calls watsonx_service
   - `POST /ai/risk-summary` — accepts dashboard risk heatmap JSON, builds executive summary prompt, calls watsonx_service
   - `GET /ai/health` — calls `ModelInference.get_details()` to verify connectivity
5. Design prompt templates for each endpoint (structured, concise, role-specific):
   - Skill gap prompt: `"You are an enterprise capability advisor. Given this project skill gap data: {data}, provide 3 specific hiring or training recommendations in bullet points."`
   - Delivery coach prompt: `"You are an agile delivery coach. Given these sprint metrics for squad {name}: {metrics}, identify the top 2 delivery risks and suggest concrete improvements."`
   - Risk summary prompt: `"You are a CTO advisor. Summarize the following enterprise risk heatmap data: {heatmap} in 3 sentences suitable for a board presentation."`
6. Register AI router in `main.py`
7. Create `frontend/src/api/ai.ts` — typed API functions for all AI endpoints
8. Create `frontend/src/components/dashboard/AIInsightsPanel.tsx` — displays AI narratives with loading state and "Refresh" button
9. Add `AIInsightsPanel` to the Executive Dashboard page (Sub-Task 15 output)
10. Document watsonx setup in `docs/watsonx-integration.md`: how to get IBM Cloud API key, create watsonx project, set env vars

**Relevant Context:**
- SDK authentication pattern (from IBM docs): `ModelInference(model_id="ibm/granite-3-3-8b-instruct", credentials={"apikey": key, "url": url}, project_id=project_id)`
- Text generation call: `model.generate_text(prompt=prompt)`
- `WATSONX_URL` for US South region: `https://us-south.ml.cloud.ibm.com`
- If `WATSONX_API_KEY` is absent from env, service returns a clearly labelled mock response — platform remains fully functional without credentials
- `ibm_watsonx_ai` package available on PyPI

---

### Sub-Task 18 — Live Demo Endpoints & Hackathon Submission Package
**Status:** [ ] pending

**Intent:**
Add a dedicated set of zero-auth live demo endpoints that judges can hit without needing to log in, and assemble the final hackathon submission package with a polished README, demo script, and recorded demo walkthrough guide.

**Expected Outcomes:**
- `GET /demo/summary` — returns a pre-built platform overview: team count, squad count, employee count, active project count, avg delivery score, top skill gaps, risk heatmap snapshot — no auth required
- `GET /demo/dashboard` — returns the full executive dashboard payload from seed data — no auth required
- `GET /demo/ai-insights` — returns a pre-generated watsonx AI narrative (from seed data context) — no auth required
- `GET /demo/teams` — returns the 8 seeded teams with squads summary — no auth required
- All demo endpoints are clearly marked in Swagger UI under a `demo` tag
- Root `README.md` includes a "Live Demo" section with curl examples for each demo endpoint
- `docs/demo-script.md` — step-by-step judge walkthrough (what to open, what to click, what to highlight)

**Todo List:**
1. Create `backend/app/api/demo.py` — demo router, no Auth0 dependency, uses `get_db` only
2. Implement `GET /demo/summary` — single aggregated query across all seed data tables
3. Implement `GET /demo/dashboard` — calls `dashboard_service.get_executive_dashboard()` directly
4. Implement `GET /demo/ai-insights` — calls watsonx_service with a fixed representative prompt (or returns a cached seed narrative if no API key)
5. Implement `GET /demo/teams` — returns teams list with squad and member counts
6. Add `demo` APIRouter to `main.py` with prefix `/demo` and tag `"Live Demo"`
7. Add `DEMO_MODE=true` env var that, when set, pre-caches the demo responses at startup for instant response
8. Create `docs/demo-script.md` — judge walkthrough: startup, Swagger demo endpoints, login flow, dashboard tour, AI insights, compliance report
9. Update root `README.md` — add "Live Demo Endpoints" section with full curl examples:
   ```
   curl http://localhost:8000/demo/summary
   curl http://localhost:8000/demo/dashboard
   curl http://localhost:8000/demo/ai-insights
   ```
10. Create `docs/watsonx-integration.md` — IBM Cloud account → create watsonx project → generate API key → set env vars → restart stack

**Relevant Context:**
- Demo endpoints bypass Auth0 JWT verification entirely — they read from the seeded database only
- These endpoints exist purely for hackathon judging convenience and are gated by `DEMO_MODE=true` in production scenarios
- Sub-Task 10 (seed data) must be complete before demo endpoints return meaningful data
- Sub-Task 17 (watsonx) should be complete before `GET /demo/ai-insights` returns real AI content

---

## Implementation Phases

### Phase 1 — Foundation (Sub-Tasks 1–3)
Infrastructure, database, authentication. Nothing visible yet, but platform is runnable.

### Phase 2 — Core APIs (Sub-Tasks 4–9)
All backend modules. Swagger UI fully usable for demonstration at this point.

### Phase 3 — Data (Sub-Task 10)
Seed data makes the platform demonstrable with realistic content.

### Phase 4 — Frontend (Sub-Tasks 11–15)
Full React UI. Platform is visually complete and demo-ready.

### Phase 5 — AI + Demo (Sub-Tasks 17–18)
IBM watsonx.ai intelligence layer and live demo endpoints for hackathon judging.

### Phase 6 — Polish (Sub-Task 16)
Documentation, final wiring, submission readiness.

---

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | FastAPI | Async, auto-Swagger, Pydantic validation — ideal for rapid hackathon dev |
| ORM | SQLAlchemy + Alembic | Industry standard; Alembic migrations are reproducible |
| Auth | Auth0 | Zero-infrastructure SSO + RBAC; free tier sufficient |
| Frontend | React + Vite + Tailwind | Fast build, small bundle, utility-first CSS |
| Charts | Recharts | React-native, composable, no license issues |
| Container | Docker Compose | Single-host, reproducible, no cloud account needed |
| Reporting | In-app dashboards | Eliminates Power BI licensing complexity for hackathon |
| Monorepo | Single repo | Simpler for hackathon review and submission |
| AI Layer | IBM watsonx.ai Granite | Official IBM SDK, ibm/granite-3-3-8b-instruct, graceful fallback if no key |
| Demo Access | Zero-auth /demo/* endpoints | Judges can explore data immediately without Auth0 setup |
