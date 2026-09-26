import client from './client'
import type { Squad, SquadMember } from '../types'

export const getSquads = (teamId?: number) =>
  client.get<Squad[]>('/squads', { params: teamId ? { team_id: teamId } : {} }).then(r => r.data)

export const getSquad = (id: number) => client.get<Squad>(`/squads/${id}`).then(r => r.data)

export const createSquad = (data: Partial<Squad>) =>
  client.post<Squad>('/squads', data).then(r => r.data)

export const updateSquad = (id: number, data: Partial<Squad>) =>
  client.put<Squad>(`/squads/${id}`, data).then(r => r.data)

export const getSquadMembers = (squadId: number) =>
  client.get<SquadMember[]>(`/squads/${squadId}/members`).then(r => r.data)

export const addSquadMember = (squadId: number, data: object) =>
  client.post<SquadMember>(`/squads/${squadId}/members`, data).then(r => r.data)
