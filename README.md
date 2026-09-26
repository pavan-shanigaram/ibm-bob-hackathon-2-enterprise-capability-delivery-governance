# Enterprise Capability & Delivery Governance Platform

**IBM Bob Hackathon Submission** — A full-stack enterprise platform for managing teams, squads, employees, projects, resource allocation, capability management, delivery performance, and governance dashboards — powered by IBM watsonx.ai (Granite).

---

## 🏗️ Architecture

| Layer | Technology |
|---|---|
| Backend API | Python 3.11 — FastAPI |
| Database | MySQL 8 |
| ORM | SQLAlchemy + Alembic |
| Authentication | Auth0 (JWT RBAC) |
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Charts | Recharts |
| AI Intelligence | IBM watsonx.ai — `ibm/granite-3-3-8b-instruct` |
| Containerisation | Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (with Compose v2)
- Git

### 1. Clone and configure

```bash
git clone https://github.com/pavan-shanigaram/ibm-bob-hackathon-2-enterprise-capability-delivery-governance.git
cd ibm-bob-hackathon-2-enterprise-capability-delivery-governance
cp .env.example .env
# Edit .env — fill in Auth0 and optionally watsonx credentials
```

### 2. Start the platform

```bash
docker compose up --build -d
# or: make up
```

This starts:
- **MySQL** on port `3306`
- **FastAPI backend** on port `8000`
- **React frontend** on port `5173`
- Runs DB migrations automatically
- Seeds 150+ employees, 8 teams, 24 squads, 12 projects

### 3. Access the platform

| Service | URL |
|---|---|
| Frontend UI | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## 🎯 Live Demo Endpoints (No Auth Required)

Judges can test the platform immediately without any login:

```bash
# Platform KPI snapshot
curl http://localhost:8000/demo/summary

# Full executive dashboard payload
curl http://localhost:8000/demo/dashboard

# IBM watsonx.ai Granite AI insights
curl http://localhost:8000/demo/ai-insights

# All 8 teams with squads
curl http://localhost:8000/demo/teams
```

---

## 🤖 IBM watsonx.ai Integration

Add your IBM Cloud credentials to `.env`:

```
WATSONX_API_KEY=your-ibm-cloud-api-key
WATSONX_PROJECT_ID=your-watsonx-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
```

AI-powered endpoints:
- `POST /api/v1/ai/skill-gap-narrative` — hiring recommendations for skill gaps
- `POST /api/v1/ai/delivery-coach` — sprint improvement suggestions
- `POST /api/v1/ai/risk-summary` — board-ready risk narrative
- `GET /api/v1/ai/health` — watsonx connectivity check

> **Without credentials:** The platform runs fully — AI endpoints return clearly labelled mock responses.

---

## 📋 Core Modules

| Module | Description |
|---|---|
| Team Management | 8 enterprise teams with leads and capacity |
| Squad Management | 24 scrum squads, members, and sprint planning |
| Employee Management | ~150 employees with skills, utilization, and assignments |
| Capability Management | Skill inventory, proficiency matrix, gap analysis |
| Project Management | 12+ projects with health indicators and assignments |
| Authorization & Compliance | GitHub, Azure DevOps, SAP, Salesforce, Production access |
| Resource Allocation | Utilization tracking with over-allocation alerts |
| Delivery Performance | Velocity, story points, cycle time, delivery score |
| Executive Dashboard | KPIs, charts, risk heatmap, AI insights |

---

## 🔒 RBAC Roles

| Role | Access |
|---|---|
| `platform_admin` | Full CRUD on all entities |
| `team_lead` | Own team management |
| `scrum_master` | Own squad metrics |
| `employee` | Own profile and skills |
| `executive` | Read-only dashboards |
| `security_admin` | Authorization records |

---

## 📁 Repository Structure

```
├── backend/           FastAPI application
│   ├── app/
│   │   ├── api/       Route handlers per domain
│   │   ├── models/    SQLAlchemy ORM models
│   │   ├── schemas/   Pydantic schemas
│   │   ├── services/  Business logic
│   │   └── auth/      Auth0 JWT + RBAC
│   ├── alembic/       DB migrations
│   └── seed/          Sample data scripts
├── frontend/          React + TypeScript + Vite
│   └── src/
│       ├── api/       Axios API clients
│       ├── pages/     Full page views
│       └── components/ Reusable UI components
├── docs/              Architecture, ER diagram, API spec
├── docker-compose.yml
└── Makefile
```

---

## 🛠️ Development Commands

```bash
make up              # Start all services
make down            # Stop all services
make seed            # Re-run seed data
make logs            # Follow backend logs
make shell-backend   # Shell into backend container
make migrate         # Run Alembic migrations
```

---

## 📖 Documentation

- [Architecture](docs/architecture.md)
- [ER Diagram](docs/er-diagram.md)
- [API Specification](docs/api-spec.md)
- [RBAC Model](docs/rbac-model.md)
- [Dashboard Design](docs/dashboard-design.md)
- [watsonx.ai Integration](docs/watsonx-integration.md)
- [Demo Script](docs/demo-script.md)
