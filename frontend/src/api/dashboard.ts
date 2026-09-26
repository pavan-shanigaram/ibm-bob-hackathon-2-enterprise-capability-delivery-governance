import client, { demoClient } from './client'
import type { ExecutiveDashboard, SkillGapProject, CapacityRisk, AIInsight } from '../types'

export const getExecutiveDashboard = () =>
  client.get<ExecutiveDashboard>('/dashboard/executive').then(r => r.data)

export const getSkillGaps = () =>
  client.get<SkillGapProject[]>('/dashboard/reports/skill-gaps').then(r => r.data)

export const getCapacityRisk = () =>
  client.get<CapacityRisk[]>('/dashboard/reports/capacity-risk').then(r => r.data)

export const getDeliveryBottlenecks = () =>
  client.get('/dashboard/reports/delivery-bottlenecks').then(r => r.data)

// Demo endpoints (no auth)
export const getDemoSummary = () => demoClient.get('/summary').then(r => r.data)
export const getDemoDashboard = () => demoClient.get<ExecutiveDashboard>('/dashboard').then(r => r.data)
export const getDemoAIInsights = () => demoClient.get<AIInsight>('/ai-insights').then(r => r.data)

// Metrics
export const getMetrics = (params?: object) =>
  client.get('/metrics', { params }).then(r => r.data)

export const getVelocityTrend = (squadId: number, n = 10) =>
  client.get(`/metrics/squad/${squadId}/velocity-trend`, { params: { n } }).then(r => r.data)

// Authorizations
export const getAuthorizations = (employeeId?: number) =>
  client.get('/authorizations', { params: employeeId ? { employee_id: employeeId } : {} }).then(r => r.data)

export const createAuthorization = (data: object) =>
  client.post('/authorizations', data).then(r => r.data)

export const updateAuthorization = (id: number, data: object) =>
  client.put(`/authorizations/${id}`, data).then(r => r.data)

export const getComplianceReport = () =>
  client.get('/authorizations/compliance-report').then(r => r.data)

// Skills
export const getSkills = () => client.get('/skills').then(r => r.data)
export const createSkill = (data: object) => client.post('/skills', data).then(r => r.data)
export const getCapabilityMatrix = () => client.get('/skills/matrix').then(r => r.data)

// AI
export const getAIHealth = () => client.get('/ai/health').then(r => r.data)
export const getSkillGapNarrative = (projectId: number) =>
  client.post<AIInsight>('/ai/skill-gap-narrative', { project_id: projectId }).then(r => r.data)
export const getDeliveryCoach = (squadId: number) =>
  client.post<AIInsight>('/ai/delivery-coach', { squad_id: squadId }).then(r => r.data)
export const getRiskSummary = () =>
  client.post<AIInsight>('/ai/risk-summary').then(r => r.data)
