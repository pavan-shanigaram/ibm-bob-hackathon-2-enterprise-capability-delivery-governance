# Project Hub — Team Assignment, Workflow Timeline & Dependency Tracker

## Top-Level Overview

Extend the platform with a dedicated **Project Hub** page that gives a full operational picture of any project:

1. **Team & Squad Breakdown** — which teams are assigned, which squads under each team, and who are the members in each squad
2. **Workflow Timeline** — per-team involvement phases (phase name, planned start/end, status: Not Started / In Progress / Done / Blocked) giving a Gantt-like view of when each team is needed
3. **Dependency Tracker** — inter-team dependencies on a project (Team A blocks/runs-parallel/is-sequential-to Team B), with type, description, status (Pending / Resolved), and optional due date; blockers are highlighted in red

The work is split into four independent sub-tasks processed in order:

1. DB model + migration for `project_team_phases` and `project_team_dependencies`
2. Backend API endpoints (service + router + schemas)
3. Frontend API client + TypeScript types
4. Frontend Project Hub page

---

## Sub-Task 1 — Database Models & Migration

**Intent**
Add two new tables to capture per-team workflow phases and inter-team dependencies for a project. No existing tables are modified.

**Expected Outcomes**
- `project_team_phases` table exists in the DB with correct columns and FKs
- `project_team_dependencies` table exists with correct columns and FKs
- Alembic migration `002_project_hub.py` runs cleanly via `alembic upgrade head`
- SQLAlchemy ORM models importable from `app.models`

**Todo List**
1. Create `backend/app/models/project_team_phase.py` with model `ProjectTeamPhase`:
   - `id`, `project_id` (FK projects), `team_id` (FK teams), `phase_name` (String 200),
     `planned_start` (Date nullable), `planned_end` (Date nullable),
     `status` (Enum: NotStarted/InProgress/Done/Blocked, default NotStarted),
     `notes` (Text nullable), `created_at`, `updated_at`
   - relationships: `project`, `team`
2. Create `backend/app/models/project_team_dependency.py` with model `ProjectTeamDependency`:
   - `id`, `project_id` (FK projects), `from_team_id` (FK teams, "this team is the dependency source"),
     `to_team_id` (FK teams, "this team is waiting / blocked"),
     `dependency_type` (Enum: Blocker/Parallel/Sequential),
     `description` (Text nullable), `status` (Enum: Pending/Resolved, default Pending),
     `due_date` (Date nullable), `created_at`, `updated_at`
   - relationships: `project`, `from_team`, `to_team`
3. Register both models in `backend/app/models/__init__.py` (or wherever models are imported to ensure Alembic sees them)
4. Create `backend/alembic/versions/002_project_hub.py`:
   - upgrade: CREATE TABLE project_team_phases, CREATE TABLE project_team_dependencies
   - downgrade: DROP both tables
5. Run migration inside the `governance_migrate` one-shot container to verify

**Relevant Context**
- Existing model pattern: `backend/app/models/project_assignment.py` (ProjectSquadAssignment)
- Existing migration pattern: `backend/alembic/versions/001_initial_schema.py`
- `backend/alembic/env.py` — ensure new models are imported so Alembic detects them
- Base class: `app.core.database.Base`

**Status** `[ ] pending`

---

## Sub-Task 2 — Backend API (Schemas, Service, Router)

**Intent**
Expose CRUD endpoints for project team phases and dependencies under `/api/v1/projects/{project_id}/phases` and `/api/v1/projects/{project_id}/dependencies`. Also add a single rich "hub" GET endpoint that returns everything needed for the Project Hub page in one call.

**Expected Outcomes**
- `GET /api/v1/projects/{id}/hub` returns: project detail, assigned teams with their squads and squad members, all phases, all dependencies (with blocker flag)
- `GET/POST/PUT/DELETE /api/v1/projects/{id}/phases` — full CRUD for team phases
- `GET/POST/PUT/DELETE /api/v1/projects/{id}/dependencies` — full CRUD for dependencies
- All endpoints follow the existing auth pattern (`Depends(get_current_user)` for reads, `require_roles(["platform_admin","team_lead"])` for writes)

**Todo List**
1. Create `backend/app/schemas/project_hub.py`:
   - `PhaseStatus` enum, `DependencyType` enum, `DependencyStatus` enum
   - `ProjectTeamPhaseCreate`, `ProjectTeamPhaseUpdate`, `ProjectTeamPhaseResponse`
   - `ProjectTeamDependencyCreate`, `ProjectTeamDependencyUpdate`, `ProjectTeamDependencyResponse`
   - `HubSquadMember` (employee_id, employee_name, role_in_squad, allocation_percentage)
   - `HubSquad` (squad id, name, member_count, members: list[HubSquadMember])
   - `HubTeam` (team id, name, squads: list[HubSquad], phases: list[PhaseResponse], is_blocked: bool)
   - `ProjectHubResponse` (project fields, teams: list[HubTeam], dependencies: list[DependencyResponse])
2. Create `backend/app/services/project_hub_service.py`:
   - `get_hub(db, project_id)` — assembles the full ProjectHubResponse:
     - Fetch project, fetch all ProjectSquadAssignments → unique team_ids
     - For each team: fetch squads assigned to this project that belong to this team, fetch SquadMembers for each squad
     - Fetch phases for the project, fetch dependencies for the project
     - Mark `is_blocked = True` on a team if any dependency where `to_team_id == team.id` has type=Blocker and status=Pending
   - `create_phase`, `update_phase`, `delete_phase`
   - `create_dependency`, `update_dependency`, `delete_dependency`
3. Create `backend/app/api/project_hub.py` router with prefix `/projects`:
   - `GET /{project_id}/hub`
   - `GET /{project_id}/phases`, `POST /{project_id}/phases`
   - `PUT /{project_id}/phases/{phase_id}`, `DELETE /{project_id}/phases/{phase_id}`
   - `GET /{project_id}/dependencies`, `POST /{project_id}/dependencies`
   - `PUT /{project_id}/dependencies/{dep_id}`, `DELETE /{project_id}/dependencies/{dep_id}`
4. Register the new router in `backend/app/main.py` (add `include_router`)
5. Test `GET /api/v1/projects/1/hub` returns valid JSON with teams, squads, members, phases, dependencies

**Relevant Context**
- Existing router registration pattern: `backend/app/main.py`
- Existing service pattern: `backend/app/services/project_service.py`
- `ProjectSquadAssignment` links projects to squads — use `squad.team_id` to infer which teams are involved
- `SquadMember` in `backend/app/models/squad_member.py` — has `employee_id`, `role_in_squad`, `allocation_percentage`
- Employee name comes from joining `Employee` model on `SquadMember.employee_id`

**Status** `[ ] pending`

---

## Sub-Task 3 — Frontend Types & API Client

**Intent**
Add TypeScript interfaces for the new data shapes and API functions to call the new endpoints. No UI yet — just the data layer.

**Expected Outcomes**
- All new types exported from `frontend/src/types/index.ts`
- New API functions in `frontend/src/api/projectHub.ts`

**Todo List**
1. Add to `frontend/src/types/index.ts`:
   - `PhaseStatus`: `'NotStarted' | 'InProgress' | 'Done' | 'Blocked'`
   - `DependencyType`: `'Blocker' | 'Parallel' | 'Sequential'`
   - `DependencyStatus`: `'Pending' | 'Resolved'`
   - `ProjectTeamPhase` interface
   - `ProjectTeamDependency` interface
   - `HubSquadMember`, `HubSquad`, `HubTeam`, `ProjectHub` interfaces matching backend response shapes
2. Create `frontend/src/api/projectHub.ts`:
   - `getProjectHub(projectId)` → `GET /projects/{id}/hub`
   - `getPhases(projectId)`, `createPhase(projectId, data)`, `updatePhase(projectId, phaseId, data)`, `deletePhase(projectId, phaseId)`
   - `getDependencies(projectId)`, `createDependency(projectId, data)`, `updateDependency(projectId, depId, data)`, `deleteDependency(projectId, depId)`

**Relevant Context**
- Existing API client base: `frontend/src/api/client.ts` — use `client` (axios instance with `/api/v1` base)
- Existing type pattern: `frontend/src/types/index.ts`
- Existing API function pattern: `frontend/src/api/projects.ts`

**Status** `[ ] pending`

---

## Sub-Task 4 — Frontend Project Hub Page

**Intent**
Build the `ProjectHubPage` React component and wire it into the app router. The page has three sections:
1. **Team & Squad Breakdown** — accordion per team, shows squads, member chips per squad, blocker badge if team is blocked
2. **Workflow Timeline** — table of team phases (team, phase, planned start/end, status pill), admin can add/edit/delete phases
3. **Dependency Tracker** — table of dependencies (from team → to team, type badge, description, status, due date), blocked dependencies highlighted red, admin can add/edit/delete

**Expected Outcomes**
- `/projects/:id/hub` route renders the Project Hub page
- Projects list page has a "Hub →" link per row to navigate to the hub
- All three sections load real data from the API
- Blockers are visually highlighted (red border / badge)
- Admins can add/edit/delete phases and dependencies via modals

**Todo List**
1. Create `frontend/src/pages/Projects/ProjectHubPage.tsx`:
   - Use `useParams` to get `projectId`, call `getProjectHub` on mount
   - Section 1: render a card per `HubTeam`; inside each card list squads as collapsible rows showing member chips; show red "BLOCKED" badge if `is_blocked`
   - Section 2: render phases as a table with status-coloured pills (NotStarted=gray, InProgress=blue, Done=green, Blocked=red); "+ Add Phase" button opens modal (team selector, phase name, start/end date, status)
   - Section 3: render dependencies as a table; rows where `dependency_type === 'Blocker'` and `status === 'Pending'` get a red left-border highlight; "+ Add Dependency" button opens modal (from-team, to-team, type, description, status, due date)
   - Edit/delete actions on each row for admin users
2. Add route in `frontend/src/App.tsx` (or wherever routes are defined): `<Route path="/projects/:id/hub" element={<ProjectHubPage />} />`
3. In `frontend/src/pages/Projects/ProjectsPage.tsx` add a "Hub →" link per project row that navigates to `/projects/:id/hub`
4. Reuse existing components: `Modal`, `Button`, `FormField`, `Input`, `Select`, `Textarea`, `HealthBadge` from `frontend/src/components/common/`

**Relevant Context**
- Routing pattern: check `frontend/src/App.tsx` for how existing routes are registered
- Existing page pattern: `frontend/src/pages/Teams/TeamsPage.tsx` (modal + CRUD pattern to reuse)
- Common components live in `frontend/src/components/common/`
- `useRole` from `frontend/src/context/RoleContext.tsx` provides `isAdmin`

**Status** `[ ] pending`

---

## Implementation Notes

- Sub-tasks must be done in order: 1 → 2 → 3 → 4 (each depends on the previous)
- After Sub-task 1: run `docker compose exec backend alembic upgrade head` to apply migration
- After Sub-task 4: rebuild the frontend container with `docker compose up -d --build frontend`
- The `project_team_phases` table uses `team_id` directly — a team can be added to phases even if no squad from that team has been formally assigned to the project yet (intentional: allows planning before squad assignment)
- For the hub endpoint, teams are inferred from `ProjectSquadAssignment → Squad.team_id`; additionally any team that has a phase record for the project is included
