import client from './client'
import type {
  ProjectHub,
  ProjectTeamPhase,
  ProjectTeamDependency,
} from '../types'

export const getProjectHub = (projectId: number): Promise<ProjectHub> =>
  client.get<ProjectHub>(`/projects/${projectId}/hub`).then(r => r.data)

export const getPhases = (projectId: number) =>
  client.get<ProjectTeamPhase[]>(`/projects/${projectId}/phases`).then(r => r.data)

export const createPhase = (projectId: number, data: Partial<ProjectTeamPhase>) =>
  client.post<ProjectTeamPhase>(`/projects/${projectId}/phases`, data).then(r => r.data)

export const updatePhase = (projectId: number, phaseId: number, data: Partial<ProjectTeamPhase>) =>
  client.put<ProjectTeamPhase>(`/projects/${projectId}/phases/${phaseId}`, data).then(r => r.data)

export const deletePhase = (projectId: number, phaseId: number) =>
  client.delete(`/projects/${projectId}/phases/${phaseId}`).then(r => r.data)

export const getDependencies = (projectId: number) =>
  client.get<ProjectTeamDependency[]>(`/projects/${projectId}/dependencies`).then(r => r.data)

export const createDependency = (projectId: number, data: Partial<ProjectTeamDependency>) =>
  client.post<ProjectTeamDependency>(`/projects/${projectId}/dependencies`, data).then(r => r.data)

export const updateDependency = (projectId: number, depId: number, data: Partial<ProjectTeamDependency>) =>
  client.put<ProjectTeamDependency>(`/projects/${projectId}/dependencies/${depId}`, data).then(r => r.data)

export const deleteDependency = (projectId: number, depId: number) =>
  client.delete(`/projects/${projectId}/dependencies/${depId}`).then(r => r.data)
