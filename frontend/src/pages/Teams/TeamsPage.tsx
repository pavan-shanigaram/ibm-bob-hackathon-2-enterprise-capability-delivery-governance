import React, { useEffect, useState } from 'react'
import { getTeams, createTeam, updateTeam, deleteTeam } from '../../api/teams'
import { getSquads } from '../../api/squads'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import ConfirmDialog from '../../components/common/ConfirmDialog'
import Button from '../../components/common/Button'
import { FormField, Input, Textarea } from '../../components/common/FormField'
import type { Team, Squad } from '../../types'

const EMPTY: Partial<Team> = { name: '', description: '' }

export default function TeamsPage() {
  const { isAdmin } = useRole()
  const [teams, setTeams] = useState<Team[]>([])
  const [squads, setSquads] = useState<Squad[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [editing, setEditing] = useState<Team | null>(null)
  const [form, setForm] = useState<Partial<Team>>(EMPTY)
  const [deleteTarget, setDeleteTarget] = useState<Team | null>(null)
  const [error, setError] = useState('')

  const load = () => {
    setLoading(true)
    Promise.all([getTeams(), getSquads()])
      .then(([t, s]) => { setTeams(t); setSquads(s) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const openCreate = () => { setEditing(null); setForm(EMPTY); setError(''); setFormOpen(true) }
  const openEdit = (t: Team) => { setEditing(t); setForm({ name: t.name, description: t.description }); setError(''); setFormOpen(true) }

  const handleSave = async () => {
    if (!form.name?.trim()) { setError('Name is required'); return }
    setSaving(true)
    try {
      if (editing) await updateTeam(editing.id, form)
      else await createTeam(form)
      setFormOpen(false)
      load()
    } catch { setError('Save failed. Please try again.') }
    finally { setSaving(false) }
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    try { await deleteTeam(deleteTarget.id); load() }
    catch { /* ignore */ }
    finally { setDeleteTarget(null) }
  }

  if (loading) return <div className="p-6 text-gray-500">Loading teams...</div>

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-bold text-gray-900">Teams ({teams.length})</h1>
        {isAdmin && <Button onClick={openCreate}>+ New Team</Button>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {teams.map(team => {
          const teamSquads = squads.filter(s => s.team_id === team.id)
          return (
            <div key={team.id} className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-1">
                <div className="font-semibold text-gray-900 text-sm">{team.name}</div>
                {isAdmin && (
                  <div className="flex gap-1 ml-2 shrink-0">
                    <button onClick={() => openEdit(team)} className="text-xs text-blue-600 hover:underline">Edit</button>
                    <span className="text-gray-300">|</span>
                    <button onClick={() => setDeleteTarget(team)} className="text-xs text-red-500 hover:underline">Delete</button>
                  </div>
                )}
              </div>
              <div className="text-xs text-gray-500 mb-3 line-clamp-2">{team.description}</div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="bg-blue-50 rounded p-2 text-center">
                  <div className="font-bold text-blue-700 text-lg">{team.squad_count}</div>
                  <div className="text-blue-500">Squads</div>
                </div>
                <div className="bg-green-50 rounded p-2 text-center">
                  <div className="font-bold text-green-700 text-lg">{team.employee_count}</div>
                  <div className="text-green-500">Members</div>
                </div>
              </div>
              <div className="mt-3 space-y-1">
                {teamSquads.slice(0, 3).map(sq => (
                  <div key={sq.id} className="text-xs text-gray-600 flex justify-between bg-gray-50 rounded px-2 py-1">
                    <span className="truncate">{sq.name.split('—')[1]?.trim() || sq.name}</span>
                    <span className="text-gray-400 ml-2">{sq.member_count} members</span>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* Create / Edit Modal */}
      <Modal open={formOpen} title={editing ? 'Edit Team' : 'New Team'} onClose={() => setFormOpen(false)}>
        <FormField label="Name" required>
          <Input value={form.name || ''} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="e.g. Platform Engineering" error={!!error && !form.name?.trim()} />
        </FormField>
        <FormField label="Description">
          <Textarea value={form.description || ''} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} placeholder="What does this team own?" />
        </FormField>
        {error && <p className="text-xs text-red-500 mb-3">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setFormOpen(false)}>Cancel</Button>
          <Button loading={saving} onClick={handleSave}>{editing ? 'Save Changes' : 'Create Team'}</Button>
        </div>
      </Modal>

      {/* Delete Confirm */}
      <ConfirmDialog
        open={!!deleteTarget}
        title="Delete Team"
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This cannot be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
