# Demo Script — Hackathon Judge Walkthrough

## Prerequisites
- Docker Desktop running
- Repository cloned
- `.env` file configured (copy `.env.example`)

## Step 1 — Start the Platform (2 minutes)

```bash
cd ibm-bob-hackathon-2-enterprise-capability-delivery-governance
cp .env.example .env
docker compose up --build -d
```

Wait ~60 seconds for MySQL to initialise and the seed to complete.

## Step 2 — Live Demo Endpoints (No Login Required)

Open a terminal and run:

```bash
# Platform overview
curl http://localhost:8000/demo/summary | python -m json.tool

# Full executive dashboard data
curl http://localhost:8000/demo/dashboard | python -m json.tool

# IBM watsonx.ai Granite AI insights
curl http://localhost:8000/demo/ai-insights | python -m json.tool

# 8 enterprise teams
curl http://localhost:8000/demo/teams | python -m json.tool
```

## Step 3 — Swagger API Explorer

Open: **http://localhost:8000/docs**

Highlight to judges:
- All 11 API router groups
- Live Demo section (no auth needed)
- IBM watsonx.ai AI section
- Schema definitions showing all 14 entities

## Step 4 — Frontend Application

Open: **http://localhost:5173**

### Dashboard Tab
- Show KPI cards: 8 teams, 24 squads, ~150 employees, 14 active projects
- Show Team Health bar chart (colour-coded by delivery score)
- Show Project Health donut (Green/Amber/Red)
- Show Enterprise Risk Heatmap (8 teams × 4 risk dimensions)
- Click "Refresh" on the AI Insights panel to show Granite generating governance narrative

### Teams Tab
- Show 8 enterprise teams as cards
- Show squad counts and employee counts per team

### Employees Tab
- Show searchable employee table with utilization bars
- Demonstrate search filtering
- Show over-allocated employees (red utilization bars)

### Projects Tab
- Show 14 projects with health badges
- Highlight Critical priority projects
- Show Active vs Completed vs OnHold distribution

### Capabilities Tab
- Show capability matrix (employees × skills)
- Demonstrate proficiency colour coding (Beginner/Intermediate/Expert/Lead)

### Delivery Metrics Tab
- Select a squad from dropdown
- Show velocity trend line chart across 3 sprints
- Show delivery score column coloured by threshold

### Reports Tab
- Show skill gap analysis (projects with unfilled capability requirements)
- Show capacity risk (squads at >90% utilization)
- Show delivery bottlenecks (squads with score <60)

### Authorizations Tab
- Show compliance status badges per employee system access
- Highlight expired/pending review records

## Step 5 — IBM watsonx.ai (If Credentials Available)

```bash
# Test AI health
curl http://localhost:8000/api/v1/ai/health

# Generate skill gap narrative for project 1
curl -X POST http://localhost:8000/api/v1/ai/skill-gap-narrative \
  -H "Content-Type: application/json" \
  -d '{"project_id": 1}'

# Generate delivery coaching for squad 1
curl -X POST http://localhost:8000/api/v1/ai/delivery-coach \
  -H "Content-Type: application/json" \
  -d '{"squad_id": 1}'
```

## Key Differentiators to Highlight

1. **Enterprise scope**: 9 domain modules, 14 DB tables, 50+ API endpoints
2. **IBM watsonx.ai**: Granite model for AI governance intelligence with graceful fallback
3. **Live demo endpoints**: Judges can explore without any login
4. **RBAC**: 6 roles with Auth0 JWT (platform_admin, team_lead, scrum_master, employee, executive, security_admin)
5. **Delivery scoring**: Formula-based composite score (velocity ratio + release success + defect penalty)
6. **Risk heatmap**: 8 teams × 4 risk dimensions (Resource, Delivery, Capability, Compliance)
7. **Full Docker Compose**: One command to run the entire platform
