# Solution Architecture

## Overview

The Enterprise Capability & Delivery Governance Platform is a full-stack web application providing enterprise-grade visibility across teams, squads, employees, projects, capabilities, resource allocation, delivery performance, and authorization compliance.

## Component Architecture

```
Browser (React + TypeScript)
        │
        │  HTTP/REST + JWT Bearer
        ▼
FastAPI Backend (Python 3.11)
        │
        ├── Auth0 JWT Middleware ──────── Auth0 (JWKS Endpoint)
        │
        ├── API Routers (11 domains)
        │       ├── /api/v1/teams
        │       ├── /api/v1/squads
        │       ├── /api/v1/employees
        │       ├── /api/v1/skills
        │       ├── /api/v1/projects
        │       ├── /api/v1/authorizations
        │       ├── /api/v1/metrics
        │       ├── /api/v1/allocations
        │       ├── /api/v1/dashboard
        │       ├── /api/v1/ai  ─────────── IBM watsonx.ai (Granite)
        │       └── /demo (no auth)
        │
        ├── Service Layer (business logic)
        │
        └── SQLAlchemy ORM
                │
                ▼
        MySQL 8 Database (Docker volume)
```

## Technology Rationale

| Component | Choice | Why |
|---|---|---|
| FastAPI | Python framework | Auto-Swagger, async, Pydantic validation |
| SQLAlchemy + Alembic | ORM + migrations | Reproducible schema management |
| MySQL 8 | Database | Proven enterprise RDBMS |
| Auth0 | Identity | Zero-infrastructure RBAC with JWT |
| React + Vite | Frontend | Fast builds, TypeScript, modern ecosystem |
| Recharts | Charts | React-native, composable |
| IBM watsonx.ai | AI | Official IBM Granite model for governance intelligence |
| Docker Compose | Deployment | Single-host, fully reproducible |

## Data Flow

1. User authenticates via Auth0 → receives JWT
2. Frontend attaches JWT to all API requests
3. Backend verifies JWT signature against Auth0 JWKS
4. Roles extracted from custom namespace claims
5. Business logic queries MySQL via SQLAlchemy
6. AI endpoints call IBM watsonx.ai Granite via ibm-watsonx-ai SDK
7. Demo endpoints bypass auth for hackathon judging
