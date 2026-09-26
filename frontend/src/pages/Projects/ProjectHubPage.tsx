import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getProjectHub, createPhase, updatePhase, deletePhase, createDependency, updateDependency, deleteDependency } from '../../api/projectHub'
import { getTeams } from '../../api/teams'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import Button from '../../components/common/Button'
import { FormField, Input, Select, Textarea } from '../../components/common/FormField'
import HealthBadge from '../../components/common/HealthBadge'
import type {
  ProjectHub,
  ProjectTeamPhase,
  ProjectTeamDependency,
  PhaseStatus,
  DependencyType,
  DependencyStatus,
  Team,
} from '../../types'

// ── Status / type helpers ─────────────────────────────────────────────────────

const PHASE_STATUS_PILL: Record<PhaseStatus, string> = {
  NotStarted: 'bg-gray-100 text-gray-600',
  InProgress:  'bg-blue-100 text-blue-700',
  Done:        'bg-green-100 text-green-700',
  Blocked:     'bg-red-100 text-red-600',
}

const DEP_TYPE_PILL: Record<DependencyType, string> = {
  Blocker:    'bg-red-100 text-red-700',
  Parallel:   'bg-blue-100 text-blue-700',
  Sequential: 'bg-amber-100 text-amber-700',
}

const DEP_STATUS_PILL: Record<DependencyStatus, string> = {
  Pending:  'bg-orange-100 text-orange-700',
  Resolved: 'bg-green-100 text-green-700',
}

const STATUS_COLORS: Record<string, string> = {
  Draft:     'bg-gray-100 text-gray-600',
  Active:    'bg-green-100 text-green-700',
  OnHold:    'bg-amber-100 text-amber-700',
  Completed: 'bg-blue-100 text-blue-700',
  Cancelled: 'bg-red-100 text-red-600',
}

const PRIORITY_COLORS: Record<string, string> = {
  Low:      'text-gray-500',
  Medium:   'text-blue-600',
  High:     'text-amber-600',
  Critical: 'text-red-600 font-bold',
}

const PHASE_STATUSES: PhaseStatus[] = ['NotStarted', 'InProgress', 'Done', 'Blocked']
const DEP_TYPES: DependencyType[] = ['Blocker', 'Parallel', 'Sequential']
const DEP_STATUSES: DependencyStatus[] = ['Pending', 'Resolved']

// ── Default form values ───────────────────────────────────────────────────────

const EMPTY_PHASE: Partial<ProjectTeamPhase> = {
  team_id: undefined, phase_name: '', planned_start: '', planned_end: '',
  status: 'NotStarted', notes: '',
}

const EMPTY_DEP: Partial<ProjectTeamDependency> = {
  from_team_id: undefined, to_team_id: undefined,
  dependency_type: 'Blocker', description: '', status: 'Pending', due_date: '',
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function ProjectHubPage() {
  const { id } = useParams<{ id: string }>()
  const projectId = Number(id)
  const navigate = useNavigate()
  const { isAdmin } = useRole()

  const [hub, setHub] = useState<ProjectHub | null>(null)
  const [teams, setTeams] = useState<Team[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // expanded squads: key = squad id
  const [expandedSquads, setExpandedSquads] = useState<Set<number>>(new Set())

  // Phase modal
  const [phaseModalOpen, setPhaseModalOpen] = useState(false)
  const [editingPhase, setEditingPhase] = useState<ProjectTeamPhase | null>(null)
  const [phaseForm, setPhaseForm] = useState<Partial<ProjectTeamPhase>>(EMPTY_PHASE)
  const [phaseSaving, setPhaseSaving] = useState(false)
  const [phaseError, setPhaseError] = useState('')

  // Dependency modal
  const [depModalOpen, setDepModalOpen] = useState(false)
  const [editingDep, setEditingDep] = useState<ProjectTeamDependency | null>(null)
  const [depForm, setDepForm] = useState<Partial<ProjectTeamDependency>>(EMPTY_DEP)
  const [depSaving, setDepSaving] = useState(false)
  const [depError, setDepError] = useState('')

  const reload = () => {
    setLoading(true)
    setError('')
    Promise.all([getProjectHub(projectId), getTeams()])
      .then(([h, t]) => { setHub(h); setTeams(t) })
      .catch(() => setError('Failed to load project hub.'))
      .finally(() => setLoading(false))
  }

  useEffect(reload, [projectId])

  // ── Squad expand toggle ──────────────────────────────────────────────────────
  const toggleSquad = (squadId: number) => {
    setExpandedSquads(prev => {
      const next = new Set(prev)
      if (next.has(squadId)) next.delete(squadId)
      else next.add(squadId)
      return next
    })
  }

  // ── Phase handlers ───────────────────────────────────────────────────────────
  const openAddPhase = () => {
    setEditingPhase(null)
    setPhaseForm(EMPTY_PHASE)
    setPhaseError('')
    setPhaseModalOpen(true)
  }

  const openEditPhase = (ph: ProjectTeamPhase) => {
    setEditingPhase(ph)
    setPhaseForm({
      team_id: ph.team_id,
      phase_name: ph.phase_name,
      planned_start: ph.planned_start || '',
      planned_end: ph.planned_end || '',
      status: ph.status,
      notes: ph.notes || '',
    })
    setPhaseError('')
    setPhaseModalOpen(true)
  }

  const handleSavePhase = async () => {
    if (!phaseForm.phase_name?.trim()) { setPhaseError('Phase name is required'); return }
    if (!phaseForm.team_id) { setPhaseError('Team is required'); return }
    setPhaseSaving(true)
    try {
      if (editingPhase) await updatePhase(projectId, editingPhase.id, phaseForm)
      else await createPhase(projectId, phaseForm)
      setPhaseModalOpen(false)
      reload()
    } catch { setPhaseError('Save failed. Please try again.') }
    finally { setPhaseSaving(false) }
  }

  const handleDeletePhase = async (ph: ProjectTeamPhase) => {
    if (!window.confirm(`Delete phase "${ph.phase_name}"?`)) return
    await deletePhase(projectId, ph.id)
    reload()
  }

  // ── Dependency handlers ──────────────────────────────────────────────────────
  const openAddDep = () => {
    setEditingDep(null)
    setDepForm(EMPTY_DEP)
    setDepError('')
    setDepModalOpen(true)
  }

  const openEditDep = (dep: ProjectTeamDependency) => {
    setEditingDep(dep)
    setDepForm({
      from_team_id: dep.from_team_id,
      to_team_id: dep.to_team_id,
      dependency_type: dep.dependency_type,
      description: dep.description || '',
      status: dep.status,
      due_date: dep.due_date || '',
    })
    setDepError('')
    setDepModalOpen(true)
  }

  const handleSaveDep = async () => {
    if (!depForm.from_team_id) { setDepError('Blocking / Source Team is required'); return }
    if (!depForm.to_team_id)   { setDepError('Waiting Team is required'); return }
    setDepSaving(true)
    try {
      if (editingDep) await updateDependency(projectId, editingDep.id, depForm)
      else await createDependency(projectId, depForm)
      setDepModalOpen(false)
      reload()
    } catch { setDepError('Save failed. Please try again.') }
    finally { setDepSaving(false) }
  }

  const handleDeleteDep = async (dep: ProjectTeamDependency) => {
    if (!window.confirm('Delete this dependency?')) return
    await deleteDependency(projectId, dep.id)
    reload()
  }

  // ── Collect all phases across teams ─────────────────────────────────────────
  const allPhases: ProjectTeamPhase[] = hub ? hub.teams.flatMap(t => t.phases) : []

  // ── Render ───────────────────────────────────────────────────────────────────
  if (loading) return <div className="p-6 text-gray-500">Loading project hub...</div>
  if (error)   return <div className="p-6 text-red-500">{error}</div>
  if (!hub)    return null

  return (
    <div className="p-6 space-y-8">

      {/* Back nav */}
      <button
        onClick={() => navigate('/projects')}
        className="text-sm text-blue-600 hover:underline flex items-center gap-1"
      >
        ← Back to Projects
      </button>

      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-bold text-gray-900">{hub.project_name}</h1>
        <span className={`text-xs px-2 py-0.5 rounded font-medium ${STATUS_COLORS[hub.project_status]}`}>
          {hub.project_status}
        </span>
        <span className={`text-xs font-semibold ${PRIORITY_COLORS[hub.project_priority]}`}>
          {hub.project_priority}
        </span>
        <HealthBadge value={hub.health_indicator} />
      </div>

      {/* ══════════════════════════════════════════════════════════════════════
          Section 1 — Team & Squad Breakdown
      ══════════════════════════════════════════════════════════════════════ */}
      <section>
        <h2 className="text-base font-semibold text-gray-800 mb-4">Team &amp; Squad Breakdown</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {hub.teams.map(team => (
            <div key={team.team_id} className="bg-white rounded-lg border border-gray-200 p-4">
              {/* Team header */}
              <div className="flex items-center gap-2 mb-3">
                <span className="font-semibold text-gray-800">{team.team_name}</span>
                {team.is_blocked && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-600 text-white">BLOCKED</span>
                )}
              </div>

              {/* Squads */}
              {team.squads.length === 0 ? (
                <p className="text-xs text-gray-400 italic">No squads assigned</p>
              ) : (
                <ul className="space-y-2">
                  {team.squads.map(squad => (
                    <li key={squad.id} className="border border-gray-100 rounded-md overflow-hidden">
                      {/* Squad row — clickable header */}
                      <button
                        className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-gray-50 transition-colors"
                        onClick={() => toggleSquad(squad.id)}
                      >
                        <span className="text-sm font-medium text-gray-700">{squad.name}</span>
                        <span className="text-xs text-gray-400">{squad.member_count} member{squad.member_count !== 1 ? 's' : ''}</span>
                      </button>

                      {/* Expanded member list */}
                      {expandedSquads.has(squad.id) && (
                        <div className="border-t border-gray-100 bg-gray-50 px-3 py-2 space-y-1">
                          {squad.members.length === 0 ? (
                            <p className="text-xs text-gray-400 italic">No members</p>
                          ) : (
                            squad.members.map(m => (
                              <div key={m.employee_id} className="flex items-center justify-between text-xs">
                                <span className="text-gray-700">{m.employee_name}</span>
                                <span className="text-gray-400">{m.role_in_squad}</span>
                              </div>
                            ))
                          )}
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          Section 2 — Workflow Timeline
      ══════════════════════════════════════════════════════════════════════ */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-gray-800">Workflow Timeline</h2>
          {isAdmin && <Button size="sm" onClick={openAddPhase}>+ Add Phase</Button>}
        </div>

        <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left px-4 py-3 font-medium text-gray-600">Team</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Phase</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Start</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">End</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                {isAdmin && <th className="px-4 py-3" />}
              </tr>
            </thead>
            <tbody>
              {allPhases.length === 0 ? (
                <tr>
                  <td colSpan={isAdmin ? 6 : 5} className="px-4 py-6 text-center text-gray-400 italic">
                    No phases defined yet
                  </td>
                </tr>
              ) : (
                allPhases.map(ph => (
                  <tr key={ph.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">{ph.team_name}</td>
                    <td className="px-4 py-3 font-medium text-gray-800">{ph.phase_name}</td>
                    <td className="px-4 py-3 text-gray-500 text-xs">{ph.planned_start || '—'}</td>
                    <td className="px-4 py-3 text-gray-500 text-xs">{ph.planned_end || '—'}</td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-0.5 rounded font-medium ${PHASE_STATUS_PILL[ph.status]}`}>
                        {ph.status}
                      </span>
                    </td>
                    {isAdmin && (
                      <td className="px-4 py-3 text-right whitespace-nowrap">
                        <button onClick={() => openEditPhase(ph)} className="text-xs text-blue-600 hover:underline mr-3">Edit</button>
                        <button onClick={() => handleDeletePhase(ph)} className="text-xs text-red-500 hover:underline">Delete</button>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          Section 3 — Dependency Tracker
      ══════════════════════════════════════════════════════════════════════ */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-gray-800">Dependency Tracker</h2>
          {isAdmin && <Button size="sm" onClick={openAddDep}>+ Add Dependency</Button>}
        </div>

        <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left px-4 py-3 font-medium text-gray-600">From Team</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Type</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">To Team (waiting)</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Description</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                <th className="text-left px-4 py-3 font-medium text-gray-600">Due Date</th>
                {isAdmin && <th className="px-4 py-3" />}
              </tr>
            </thead>
            <tbody>
              {hub.dependencies.length === 0 ? (
                <tr>
                  <td colSpan={isAdmin ? 7 : 6} className="px-4 py-6 text-center text-gray-400 italic">
                    No dependencies defined
                  </td>
                </tr>
              ) : (
                hub.dependencies.map(dep => (
                  <tr
                    key={dep.id}
                    className={`border-b border-gray-100 ${dep.is_blocker ? 'border-l-4 border-red-500 bg-red-50' : 'hover:bg-gray-50'}`}
                  >
                    <td className="px-4 py-3 text-gray-700">{dep.from_team_name}</td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-0.5 rounded font-medium ${DEP_TYPE_PILL[dep.dependency_type]}`}>
                        {dep.dependency_type}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-700">{dep.to_team_name}</td>
                    <td className="px-4 py-3 text-gray-500 text-xs max-w-xs truncate">{dep.description || '—'}</td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-0.5 rounded font-medium ${DEP_STATUS_PILL[dep.status]}`}>
                        {dep.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-500 text-xs">{dep.due_date || '—'}</td>
                    {isAdmin && (
                      <td className="px-4 py-3 text-right whitespace-nowrap">
                        <button onClick={() => openEditDep(dep)} className="text-xs text-blue-600 hover:underline mr-3">Edit</button>
                        <button onClick={() => handleDeleteDep(dep)} className="text-xs text-red-500 hover:underline">Delete</button>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          Add / Edit Phase Modal
      ══════════════════════════════════════════════════════════════════════ */}
      <Modal
        open={phaseModalOpen}
        title={editingPhase ? 'Edit Phase' : 'Add Phase'}
        onClose={() => setPhaseModalOpen(false)}
      >
        <FormField label="Team" required>
          <Select
            value={phaseForm.team_id ?? ''}
            onChange={e => setPhaseForm(f => ({ ...f, team_id: e.target.value ? Number(e.target.value) : undefined }))}
            error={!!phaseError && !phaseForm.team_id}
          >
            <option value="">Select team…</option>
            {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
          </Select>
        </FormField>

        <FormField label="Phase Name" required>
          <Input
            value={phaseForm.phase_name || ''}
            onChange={e => setPhaseForm(f => ({ ...f, phase_name: e.target.value }))}
            placeholder="e.g. Discovery"
            error={!!phaseError && !phaseForm.phase_name?.trim()}
          />
        </FormField>

        <div className="grid grid-cols-2 gap-x-4">
          <FormField label="Start Date">
            <Input
              type="date"
              value={phaseForm.planned_start || ''}
              onChange={e => setPhaseForm(f => ({ ...f, planned_start: e.target.value }))}
            />
          </FormField>
          <FormField label="End Date">
            <Input
              type="date"
              value={phaseForm.planned_end || ''}
              onChange={e => setPhaseForm(f => ({ ...f, planned_end: e.target.value }))}
            />
          </FormField>
        </div>

        <FormField label="Status">
          <Select
            value={phaseForm.status || 'NotStarted'}
            onChange={e => setPhaseForm(f => ({ ...f, status: e.target.value as PhaseStatus }))}
          >
            {PHASE_STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
          </Select>
        </FormField>

        <FormField label="Notes">
          <Textarea
            value={phaseForm.notes || ''}
            onChange={e => setPhaseForm(f => ({ ...f, notes: e.target.value }))}
            placeholder="Optional notes…"
          />
        </FormField>

        {phaseError && <p className="text-xs text-red-500 mb-3">{phaseError}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setPhaseModalOpen(false)}>Cancel</Button>
          <Button loading={phaseSaving} onClick={handleSavePhase}>
            {editingPhase ? 'Save Changes' : 'Add Phase'}
          </Button>
        </div>
      </Modal>

      {/* ══════════════════════════════════════════════════════════════════════
          Add / Edit Dependency Modal
      ══════════════════════════════════════════════════════════════════════ */}
      <Modal
        open={depModalOpen}
        title={editingDep ? 'Edit Dependency' : 'Add Dependency'}
        onClose={() => setDepModalOpen(false)}
      >
        <FormField label="Blocking / Source Team" required>
          <Select
            value={depForm.from_team_id ?? ''}
            onChange={e => setDepForm(f => ({ ...f, from_team_id: e.target.value ? Number(e.target.value) : undefined }))}
            error={!!depError && !depForm.from_team_id}
          >
            <option value="">Select team…</option>
            {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
          </Select>
        </FormField>

        <FormField label="Waiting Team" required>
          <Select
            value={depForm.to_team_id ?? ''}
            onChange={e => setDepForm(f => ({ ...f, to_team_id: e.target.value ? Number(e.target.value) : undefined }))}
            error={!!depError && !depForm.to_team_id}
          >
            <option value="">Select team…</option>
            {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
          </Select>
        </FormField>

        <FormField label="Type">
          <Select
            value={depForm.dependency_type || 'Blocker'}
            onChange={e => setDepForm(f => ({ ...f, dependency_type: e.target.value as DependencyType }))}
          >
            {DEP_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </Select>
        </FormField>

        <FormField label="Description">
          <Textarea
            value={depForm.description || ''}
            onChange={e => setDepForm(f => ({ ...f, description: e.target.value }))}
            placeholder="What is being blocked or coordinated…"
          />
        </FormField>

        <div className="grid grid-cols-2 gap-x-4">
          <FormField label="Status">
            <Select
              value={depForm.status || 'Pending'}
              onChange={e => setDepForm(f => ({ ...f, status: e.target.value as DependencyStatus }))}
            >
              {DEP_STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
            </Select>
          </FormField>
          <FormField label="Due Date">
            <Input
              type="date"
              value={depForm.due_date || ''}
              onChange={e => setDepForm(f => ({ ...f, due_date: e.target.value }))}
            />
          </FormField>
        </div>

        {depError && <p className="text-xs text-red-500 mb-3">{depError}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setDepModalOpen(false)}>Cancel</Button>
          <Button loading={depSaving} onClick={handleSaveDep}>
            {editingDep ? 'Save Changes' : 'Add Dependency'}
          </Button>
        </div>
      </Modal>

    </div>
  )
}
