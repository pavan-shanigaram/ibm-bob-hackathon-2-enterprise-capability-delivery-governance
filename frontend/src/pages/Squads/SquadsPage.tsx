import React, { useEffect, useState } from 'react'
import { getSquads, createSquad, updateSquad } from '../../api/squads'
import { getTeams } from '../../api/teams'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import Button from '../../components/common/Button'
import { FormField, Input, Select, Textarea } from '../../components/common/FormField'
import type { Squad, Team } from '../../types'

const EMPTY: Partial<Squad> = { name: '', team_id: 0, capacity_points: 80, description: '' }

export default function SquadsPage() {
  const { isAdmin } = useRole()
  const [squads, setSquads] = useState<Squad[]>([])
  const [teams, setTeams] = useState<Team[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [editing, setEditing] = useState<Squad | null>(null)
  const [form, setForm] = useState<Partial<Squad>>(EMPTY)
  const [filter, setFilter] = useState<number | ''>('')
  const [error, setError] = useState('')

  const load = () => {
    setLoading(true)
    Promise.all([getSquads(), getTeams()])
      .then(([s, t]) => { setSquads(s); setTeams(t) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const teamMap = Object.fromEntries(teams.map(t => [t.id, t.name]))

  const openCreate = () => {
    setEditing(null)
    setForm({ ...EMPTY, team_id: typeof filter === 'number' ? filter : 0 })
    setError('')
    setFormOpen(true)
  }
  const openEdit = (sq: Squad) => {
    setEditing(sq)
    setForm({ name: sq.name, team_id: sq.team_id, capacity_points: sq.capacity_points, description: sq.description })
    setError('')
    setFormOpen(true)
  }

  const handleSave = async () => {
    if (!form.name?.trim()) { setError('Name is required'); return }
    if (!form.team_id) { setError('Team is required'); return }
    setSaving(true)
    try {
      if (editing) await updateSquad(editing.id, form)
      else await createSquad(form)
      setFormOpen(false)
      load()
    } catch { setError('Save failed. Please try again.') }
    finally { setSaving(false) }
  }

  if (loading) return <div className="p-6 text-gray-500">Loading squads...</div>

  const filtered = filter !== '' ? squads.filter(s => s.team_id === filter) : squads

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-900">Squads ({filtered.length})</h1>
        <div className="flex items-center gap-3">
          <select
            value={filter}
            onChange={e => setFilter(e.target.value ? Number(e.target.value) : '')}
            className="border border-gray-200 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
          >
            <option value="">All Teams</option>
            {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
          </select>
          {isAdmin && <Button onClick={openCreate}>+ New Squad</Button>}
        </div>
      </div>

      <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-4 py-3 font-medium text-gray-600">Squad</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Team</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Members</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Capacity Points</th>
              {isAdmin && <th className="px-4 py-3" />}
            </tr>
          </thead>
          <tbody>
            {filtered.map(sq => (
              <tr key={sq.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="px-4 py-3">
                  <div className="font-medium text-gray-800">{sq.name}</div>
                  {sq.description && <div className="text-xs text-gray-400 line-clamp-1">{sq.description}</div>}
                </td>
                <td className="px-4 py-3 text-gray-600">{teamMap[sq.team_id] || '—'}</td>
                <td className="px-4 py-3 text-gray-600">{sq.member_count}</td>
                <td className="px-4 py-3 text-gray-600">{sq.capacity_points}</td>
                {isAdmin && (
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => openEdit(sq)} className="text-xs text-blue-600 hover:underline">Edit</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="text-center text-gray-400 py-8 text-sm">No squads found.</div>}
      </div>

      <Modal open={formOpen} title={editing ? 'Edit Squad' : 'New Squad'} onClose={() => setFormOpen(false)}>
        <FormField label="Name" required>
          <Input
            value={form.name || ''}
            onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            placeholder="e.g. Platform Squad Alpha"
            error={!!error && !form.name?.trim()}
          />
        </FormField>
        <FormField label="Team" required>
          <Select
            value={form.team_id || ''}
            onChange={e => setForm(f => ({ ...f, team_id: Number(e.target.value) }))}
            error={!!error && !form.team_id}
          >
            <option value="">Select team…</option>
            {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
          </Select>
        </FormField>
        <FormField label="Capacity Points">
          <Input
            type="number"
            min={0}
            value={form.capacity_points ?? 80}
            onChange={e => setForm(f => ({ ...f, capacity_points: Number(e.target.value) }))}
          />
        </FormField>
        <FormField label="Description">
          <Textarea value={form.description || ''} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} />
        </FormField>
        {error && <p className="text-xs text-red-500 mb-3">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setFormOpen(false)}>Cancel</Button>
          <Button loading={saving} onClick={handleSave}>{editing ? 'Save Changes' : 'Create Squad'}</Button>
        </div>
      </Modal>
    </div>
  )
}
