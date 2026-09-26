// All TypeScript interfaces mirroring backend schemas

export type EmployeeRole =
  | 'Designer' | 'Developer' | 'BusinessAnalyst' | 'ScrumMaster'
  | 'PlatformEngineer' | 'OperationsEngineer' | 'QAEngineer' | 'Architect'

export type ProficiencyLevel = 'Beginner' | 'Intermediate' | 'Expert' | 'Lead'
export type ProjectStatus = 'Draft' | 'Active' | 'OnHold' | 'Completed' | 'Cancelled'
export type ProjectPriority = 'Low' | 'Medium' | 'High' | 'Critical'
export type HealthIndicator = 'Green' | 'Amber' | 'Red'
export type AuthorizedSystem = 'GitHub' | 'AzureDevOps' | 'SAP' | 'Salesforce' | 'Production'
export type ComplianceStatus = 'Compliant' | 'Expired' | 'PendingReview' | 'Revoked'

export interface Team {
  id: number
  name: string
  description?: string
  lead_employee_id?: number
  squad_count: number
  employee_count: number
  created_at: string
  updated_at: string
}

export interface Squad {
  id: number
  name: string
  team_id: number
  scrum_master_id?: number
  capacity_points: number
  description?: string
  member_count: number
  created_at: string
  updated_at: string
}

export interface SquadMember {
  id: number
  employee_id: number
  employee_name: string
  role_in_squad: string
  allocation_percentage: number
}

export interface Employee {
  id: number
  name: string
  email: string
  job_title?: string
  role: EmployeeRole
  team_id?: number
  allocation_percentage: number
  is_active: boolean
  utilization_percentage: number
  squad_count: number
  created_at: string
  updated_at: string
}

export interface EmployeeSkill {
  id: number
  skill_id: number
  skill_name: string
  skill_category: string
  proficiency_level: ProficiencyLevel
}

export interface Skill {
  id: number
  name: string
  category: string
  description?: string
}

export interface Project {
  id: number
  name: string
  description?: string
  status: ProjectStatus
  priority: ProjectPriority
  start_date?: string
  end_date?: string
  owner_team_id?: number
  health_indicator: HealthIndicator
  squad_count: number
  employee_count: number
  created_at: string
  updated_at: string
}

export interface Authorization {
  id: number
  employee_id: number
  employee_name: string
  system: AuthorizedSystem
  access_level: string
  granted_at: string
  expires_at?: string
  is_active: boolean
  compliance_status: ComplianceStatus
}

export interface DeliveryMetric {
  id: number
  squad_id: number
  project_id?: number
  sprint_name: string
  sprint_start?: string
  sprint_end?: string
  velocity: number
  story_points_planned: number
  story_points_delivered: number
  cycle_time_days?: number
  lead_time_days?: number
  defect_leakage_count: number
  release_success: boolean
  delivery_score: number
  recorded_at: string
}

export interface VelocityTrend {
  sprint_name: string
  velocity: number
  delivery_score: number
  story_points_delivered: number
}

export interface ResourceAllocation {
  id: number
  employee_id: number
  project_id?: number
  squad_id?: number
  allocation_percentage: number
  period_start: string
  period_end: string
  is_over_allocated: boolean
}

export interface DashboardKPIs {
  total_teams: number
  total_squads: number
  total_employees: number
  active_projects: number
  avg_delivery_score: number
  over_allocated_count: number
}

export interface TeamHealth {
  team_id: number
  team_name: string
  employee_count: number
  squad_count: number
  avg_delivery_score: number
}

export interface RiskHeatmapRow {
  team_name: string
  Resource: number
  Delivery: number
  Capability: number
  Compliance: number
}

export interface DashboardAlert {
  type: 'warning' | 'error' | 'info'
  message: string
}

export interface ExecutiveDashboard {
  kpis: DashboardKPIs
  project_health_counts: { green: number; amber: number; red: number }
  team_health: TeamHealth[]
  risk_heatmap: RiskHeatmapRow[]
  alerts: DashboardAlert[]
  generated_at: string
}

export interface SkillGapProject {
  project_id: number
  project_name: string
  gaps: Array<{
    skill_id: number
    skill_name: string
    required_proficiency: ProficiencyLevel
    headcount_needed: number
    headcount_available: number
    gap: number
  }>
}

export interface CapacityRisk {
  squad_id: number
  squad_name: string
  avg_allocation: number
  member_count: number
}

export interface AIInsight {
  narrative: string
  model?: string
  is_live_ai?: boolean
}

export type PhaseStatus = 'NotStarted' | 'InProgress' | 'Done' | 'Blocked'
export type DependencyType = 'Blocker' | 'Parallel' | 'Sequential'
export type DependencyStatus = 'Pending' | 'Resolved'

export interface ProjectTeamPhase {
  id: number
  project_id: number
  team_id: number
  team_name: string
  phase_name: string
  planned_start?: string
  planned_end?: string
  status: PhaseStatus
  notes?: string
  created_at: string
  updated_at: string
}

export interface ProjectTeamDependency {
  id: number
  project_id: number
  from_team_id: number
  to_team_id: number
  from_team_name: string
  to_team_name: string
  dependency_type: DependencyType
  description?: string
  status: DependencyStatus
  due_date?: string
  is_blocker: boolean
  created_at: string
  updated_at: string
}

export interface HubSquadMember {
  employee_id: number
  employee_name: string
  role_in_squad: string
  allocation_percentage: number
}

export interface HubSquad {
  id: number
  name: string
  member_count: number
  members: HubSquadMember[]
}

export interface HubTeam {
  team_id: number
  team_name: string
  squads: HubSquad[]
  phases: ProjectTeamPhase[]
  is_blocked: boolean
}

export interface ProjectHub {
  project_id: number
  project_name: string
  project_status: ProjectStatus
  project_priority: ProjectPriority
  health_indicator: HealthIndicator
  start_date?: string
  end_date?: string
  teams: HubTeam[]
  dependencies: ProjectTeamDependency[]
}
