import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getProjects, createProject, updateProject } from '../../api/projects'
import { getTeams } from '../../api/teams'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import Button from '../../components/common/Button'
import { FormField, Input, Select, Textarea } from '../../components/common/FormField'
import HealthBadge from '../../components/common/HealthBadge'
import type { Project, ProjectStatus, ProjectPriority, HealthIndicator, Team } from '../../types'

const STATUS_COLORS: Record<ProjectStatus, string> = {
  Draft: 'bg-gray-100 text-gray-600',
  Active: 'bg-green-100 text-green-700',
  OnHold: 'bg-amber-100 text-amber-700',
  Completed: 'bg-blue-100 text-blue-700',
  Cancelled: 'bg-red-100 text-red-600',
}

const PRIORITY_COLORS: Record<ProjectPriority, string> = {
  Low: 'text-gray-500',
  Medium: 'text-blue-600',
  High: 'text-amber-600',
  Critical: 'text-red-600 font-bold',
}

const STATUSES: ProjectStatus[] = ['Draft', 'Active', 'OnHold', 'Completed', 'Cancelled']
const PRIORITIES: ProjectPriority[] = ['Low', 'Medium', 'High', 'Critical']
const HEALTH_OPTS: HealthIndicator[] = ['Green', 'Amber', 'Red']

const EMPTY: Partial<Project> = {
  name: '', description: '', status: 'Active', priority: 'Medium',
  health_indicator: 'Green', start_date: '', end_date: '',
}

export default function ProjectsPage() {
  const navigate = useNavigate()
  const { isAdmin } = useRole()
  const [projects, setProjects] = useState<Project[]>([])
  const [teams, setTeams] = useState<Team[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [editing, setEditing] = useState<Project | null>(null)
  const [form, setForm] = useState<Partial<Project>>(EMPTY)
  const [error, setError] = useState('')

  const load = () => {
    setLoading(true)
    Promise.all([getProjects(), getTeams()])
      .then(([p, t]) => { setProjects(p); setTeams(t) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const openCreate = () => { setEditing(null); setForm(EMPTY); setError(''); setFormOpen(true) }
  const openEdit = (p: Project) => {
    setEditing(p)
    setForm({
      name: p.name, description: p.description, status: p.status,
      priority: p.priority, health_indicator: p.health_indicator,
      start_date: p.start_date || '', end_date: p.end_date || '',
      owner_team_id: p.owner_team_id,
    })
    setError('')
    setFormOpen(true)
  }

  const handleSave = async () => {
    if (!form.name?.trim()) { setError('Name is required'); return }
    setSaving(true)
    try {
      if (editing) await updateProject(editing.id, form)
      else await createProject(form)
      setFormOpen(false)
      load()
    } catch { setError('Save failed. Please try again.') }
    finally { setSaving(false) }
  }

  if (loading) return <div className="p-6 text-gray-500">Loading projects...</div>

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-bold text-gray-900">Projects ({projects.length})</h1>
        {isAdmin && <Button onClick={openCreate}>+ New Project</Button>}
      </div>

      <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-4 py-3 font-medium text-gray-600">Project</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Priority</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Health</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Squads</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Members</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">End Date</th>
             <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody>
            {projects.map(p => (
              <tr key={p.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="px-4 py-3">
                  <div className="font-medium text-gray-800">{p.name}</div>
                  {p.description && <div className="text-xs text-gray-400 line-clamp-1">{p.description}</div>}
                </td>
                <td className="px-4 py-3">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${STATUS_COLORS[p.status]}`}>{p.status}</span>
                </td>
                <td className={`px-4 py-3 text-xs font-semibold ${PRIORITY_COLORS[p.priority]}`}>{p.priority}</td>
                <td className="px-4 py-3"><HealthBadge value={p.health_indicator} /></td>
                <td className="px-4 py-3 text-gray-600">{p.squad_count}</td>
                <td className="px-4 py-3 text-gray-600">{p.employee_count}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{p.end_date || '—'}</td>
                <td className="px-4 py-3 text-right whitespace-nowrap">
                  {isAdmin && (
                    <button onClick={() => openEdit(p)} className="text-xs text-blue-600 hover:underline mr-3">Edit</button>
                  )}
                  <button onClick={() => navigate(`/projects/${p.id}/hub`)} className="text-xs text-indigo-600 hover:underline font-medium">Hub →</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal open={formOpen} title={editing ? 'Edit Project' : 'New Project'} onClose={() => setFormOpen(false)} width="max-w-2xl">
        <div className="grid grid-cols-2 gap-x-4">
          <div className="col-span-2">
            <FormField label="Name" required>
              <Input value={form.name || ''} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="Project name" error={!!error && !form.name?.trim()} />
            </FormField>
          </div>
          <div className="col-span-2">
            <FormField label="Description">
              <Textarea value={form.description || ''} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} placeholder="Brief description..." />
            </FormField>
          </div>
          <FormField label="Status">
            <Select value={form.status || 'Active'} onChange={e => setForm(f => ({ ...f, status: e.target.value as ProjectStatus }))}>
              {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
            </Select>
          </FormField>
          <FormField label="Priority">
            <Select value={form.priority || 'Medium'} onChange={e => setForm(f => ({ ...f, priority: e.target.value as ProjectPriority }))}>
              {PRIORITIES.map(p => <option key={p} value={p}>{p}</option>)}
            </Select>
          </FormField>
          <FormField label="Health">
            <Select value={form.health_indicator || 'Green'} onChange={e => setForm(f => ({ ...f, health_indicator: e.target.value as HealthIndicator }))}>
              {HEALTH_OPTS.map(h => <option key={h} value={h}>{h}</option>)}
            </Select>
          </FormField>
          <FormField label="Owner Team">
            <Select value={form.owner_team_id || ''} onChange={e => setForm(f => ({ ...f, owner_team_id: e.target.value ? Number(e.target.value) : undefined }))}>
              <option value="">No owner team</option>
              {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
            </Select>
          </FormField>
          <FormField label="Start Date">
            <Input type="date" value={form.start_date || ''} onChange={e => setForm(f => ({ ...f, start_date: e.target.value }))} />
          </FormField>
          <FormField label="End Date">
            <Input type="date" value={form.end_date || ''} onChange={e => setForm(f => ({ ...f, end_date: e.target.value }))} />
          </FormField>
        </div>
        {error && <p className="text-xs text-red-500 mb-3">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setFormOpen(false)}>Cancel</Button>
          <Button loading={saving} onClick={handleSave}>{editing ? 'Save Changes' : 'Create Project'}</Button>
        </div>
      </Modal>
    </div>
  )
}
