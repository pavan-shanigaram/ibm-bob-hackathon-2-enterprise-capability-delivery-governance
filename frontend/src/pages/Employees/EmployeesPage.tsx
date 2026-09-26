import React, { useEffect, useState } from 'react'
import { getEmployees, createEmployee, updateEmployee, deleteEmployee } from '../../api/employees'
import { getTeams } from '../../api/teams'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import ConfirmDialog from '../../components/common/ConfirmDialog'
import Button from '../../components/common/Button'
import { FormField, Input, Select } from '../../components/common/FormField'
import UtilizationBar from '../../components/common/UtilizationBar'
import type { Employee, Team, EmployeeRole } from '../../types'

const ROLES: EmployeeRole[] = ['Designer', 'Developer', 'BusinessAnalyst', 'ScrumMaster', 'PlatformEngineer', 'OperationsEngineer', 'QAEngineer', 'Architect']
const EMPTY: Partial<Employee> = { name: '', email: '', role: 'Developer', job_title: '', is_active: true, allocation_percentage: 100 }

export default function EmployeesPage() {
  const { isAdmin } = useRole()
  const [employees, setEmployees] = useState<Employee[]>([])
  const [teams, setTeams] = useState<Team[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [editing, setEditing] = useState<Employee | null>(null)
  const [form, setForm] = useState<Partial<Employee>>(EMPTY)
  const [deleteTarget, setDeleteTarget] = useState<Employee | null>(null)
  const [error, setError] = useState('')

  const load = () => {
    setLoading(true)
    Promise.all([getEmployees(), getTeams()])
      .then(([e, t]) => { setEmployees(e); setTeams(t) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const teamMap = Object.fromEntries(teams.map(t => [t.id, t.name]))
  const filtered = employees.filter(e =>
    e.name.toLowerCase().includes(search.toLowerCase()) ||
    e.email.toLowerCase().includes(search.toLowerCase()) ||
    e.role.toLowerCase().includes(search.toLowerCase())
  )

  const openCreate = () => { setEditing(null); setForm(EMPTY); setError(''); setFormOpen(true) }
  const openEdit = (emp: Employee) => {
    setEditing(emp)
    setForm({ name: emp.name, email: emp.email, role: emp.role, job_title: emp.job_title, team_id: emp.team_id, is_active: emp.is_active, allocation_percentage: emp.allocation_percentage })
    setError('')
    setFormOpen(true)
  }

  const handleSave = async () => {
    if (!form.name?.trim()) { setError('Name is required'); return }
    if (!form.email?.trim()) { setError('Email is required'); return }
    if (!form.role) { setError('Role is required'); return }
    setSaving(true)
    try {
      if (editing) await updateEmployee(editing.id, form)
      else await createEmployee(form)
      setFormOpen(false)
      load()
    } catch { setError('Save failed. Please try again.') }
    finally { setSaving(false) }
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    try { await deleteEmployee(deleteTarget.id); load() }
    catch { /* ignore */ }
    finally { setDeleteTarget(null) }
  }

  if (loading) return <div className="p-6 text-gray-500">Loading employees...</div>

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-900">Employees ({employees.length})</h1>
        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Search by name, email, role..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="border border-gray-200 rounded px-3 py-1.5 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
          {isAdmin && <Button onClick={openCreate}>+ New Employee</Button>}
        </div>
      </div>

      <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Role</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Team</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Squads</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600 w-40">Utilization</th>
              {isAdmin && <th className="px-4 py-3" />}
            </tr>
          </thead>
          <tbody>
            {filtered.map(emp => (
              <tr key={emp.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="px-4 py-3">
                  <div className="font-medium text-gray-800">{emp.name}</div>
                  <div className="text-xs text-gray-400">{emp.email}</div>
                </td>
                <td className="px-4 py-3 text-gray-600">{emp.role}</td>
                <td className="px-4 py-3 text-gray-600">{teamMap[emp.team_id || 0] || '—'}</td>
                <td className="px-4 py-3 text-gray-600">{emp.squad_count}</td>
                <td className="px-4 py-3"><UtilizationBar value={emp.utilization_percentage} /></td>
                {isAdmin && (
                  <td className="px-4 py-3 text-right whitespace-nowrap">
                    <button onClick={() => openEdit(emp)} className="text-xs text-blue-600 hover:underline mr-2">Edit</button>
                    <button onClick={() => setDeleteTarget(emp)} className="text-xs text-red-500 hover:underline">Delete</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="text-center text-gray-400 py-8 text-sm">No employees match your search.</div>}
      </div>

      {/* Create / Edit Modal */}
      <Modal open={formOpen} title={editing ? 'Edit Employee' : 'New Employee'} onClose={() => setFormOpen(false)}>
        <div className="grid grid-cols-2 gap-x-4">
          <div className="col-span-2">
            <FormField label="Full Name" required>
              <Input value={form.name || ''} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="Jane Smith" error={!!error && !form.name?.trim()} />
            </FormField>
          </div>
          <div className="col-span-2">
            <FormField label="Email" required>
              <Input type="email" value={form.email || ''} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} placeholder="jane.smith@example.com" error={!!error && !form.email?.trim()} />
            </FormField>
          </div>
          <FormField label="Role" required>
            <Select value={form.role || ''} onChange={e => setForm(f => ({ ...f, role: e.target.value as EmployeeRole }))}>
              {ROLES.map(r => <option key={r} value={r}>{r}</option>)}
            </Select>
          </FormField>
          <FormField label="Job Title">
            <Input value={form.job_title || ''} onChange={e => setForm(f => ({ ...f, job_title: e.target.value }))} placeholder="Senior Developer" />
          </FormField>
          <FormField label="Team">
            <Select value={form.team_id || ''} onChange={e => setForm(f => ({ ...f, team_id: e.target.value ? Number(e.target.value) : undefined }))}>
              <option value="">No team</option>
              {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
            </Select>
          </FormField>
          <FormField label="Allocation %">
            <Input type="number" min={0} max={100} value={form.allocation_percentage ?? 100} onChange={e => setForm(f => ({ ...f, allocation_percentage: Number(e.target.value) }))} />
          </FormField>
          <FormField label="Status">
            <Select value={form.is_active ? 'true' : 'false'} onChange={e => setForm(f => ({ ...f, is_active: e.target.value === 'true' }))}>
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </Select>
          </FormField>
        </div>
        {error && <p className="text-xs text-red-500 mb-3">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setFormOpen(false)}>Cancel</Button>
          <Button loading={saving} onClick={handleSave}>{editing ? 'Save Changes' : 'Create Employee'}</Button>
        </div>
      </Modal>

      {/* Delete Confirm */}
      <ConfirmDialog
        open={!!deleteTarget}
        title="Delete Employee"
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This cannot be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
