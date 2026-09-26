import client from './client'
import type { Employee, EmployeeSkill } from '../types'

export const getEmployees = (teamId?: number) =>
  client.get<Employee[]>('/employees', { params: teamId ? { team_id: teamId } : {} }).then(r => r.data)

export const getEmployee = (id: number) =>
  client.get<Employee>(`/employees/${id}`).then(r => r.data)

export const createEmployee = (data: Partial<Employee>) =>
  client.post<Employee>('/employees', data).then(r => r.data)

export const updateEmployee = (id: number, data: Partial<Employee>) =>
  client.put<Employee>(`/employees/${id}`, data).then(r => r.data)

export const getEmployeeSkills = (id: number) =>
  client.get<EmployeeSkill[]>(`/employees/${id}/skills`).then(r => r.data)

export const deleteEmployee = (id: number) =>
  client.delete(`/employees/${id}`)

export const addEmployeeSkill = (id: number, data: object) =>
  client.post<EmployeeSkill>(`/employees/${id}/skills`, data).then(r => r.data)
