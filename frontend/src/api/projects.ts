import client from './client'
import type { Project } from '../types'

export const getProjects = (params?: object) =>
  client.get<Project[]>('/projects', { params }).then(r => r.data)

export const getProject = (id: number) =>
  client.get<Project>(`/projects/${id}`).then(r => r.data)

export const createProject = (data: Partial<Project>) =>
  client.post<Project>('/projects', data).then(r => r.data)

export const updateProject = (id: number, data: Partial<Project>) =>
  client.put<Project>(`/projects/${id}`, data).then(r => r.data)

export const assignSquads = (projectId: number, squadIds: number[]) =>
  client.put(`/projects/${projectId}/squads`, { squad_ids: squadIds }).then(r => r.data)

export const assignEmployee = (projectId: number, data: object) =>
  client.post(`/projects/${projectId}/employees`, data).then(r => r.data)
