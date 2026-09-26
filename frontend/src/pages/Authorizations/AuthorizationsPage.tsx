import React, { useEffect, useState } from 'react'
import { getAuthorizations, createAuthorization, updateAuthorization } from '../../api/dashboard'
import { getEmployees } from '../../api/employees'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import Button from '../../components/common/Button'
import { FormField, Input, Select } from '../../components/common/FormField'
import type { Authorization, ComplianceStatus, AuthorizedSystem, Employee } from '../../types'

const STATUS_COLORS: Record<ComplianceStatus, string> = {
  Compliant: 'bg-green-100 text-green-700',
  Expired: 'bg-red-100 text-red-700',
  PendingReview: 'bg-amber-100 text-amber-700',
  Revoked: 'bg-gray-100 text-gray-600',
}

const SYSTEMS: AuthorizedSystem[] = ['GitHub', 'AzureDevOps', 'SAP', 'Salesforce', 'Production']
const ACCESS_LEVELS = ['read', 'write', 'admin', 'deploy']
const STATUSES: ComplianceStatus[] = ['Compliant', 'PendingReview', 'Expired', 'Revoked']

interface AuthForm {
  employee_id: number | ''
  system: AuthorizedSystem | ''
  access_level: string
  compliance_status: ComplianceStatus
  expires_at: string
  is_active: boolean
}

const EMPTY: AuthForm = {
  employee_id: '',
  system: '',
  access_level: 'read',
  compliance_status: 'Compliant',
  expires_at: '',
  is_active: true,
}

export default function AuthorizationsPage() {
  const { isAdmin } = useRole()
  const [auths, setAuths] = useState<Authorization[]>([])
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [editing, setEditing] = useState<Authorization | null>(null)
  const [form, setForm] = useState<AuthForm>(EMPTY)
  const [filterStatus, setFilterStatus] = useState<ComplianceStatus | ''>('')
  const [error, setError] = useState('')

  const load = () => {
    setLoading(true)
    Promise.all([getAuthorizations(), getEmployees()])
      .then(([a, e]) => { setAuths(a); setEmployees(e) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const openCreate = () => { setEditing(null); setForm(EMPTY); setError(''); setFormOpen(true) }
  const openEdit = (a: Authorization) => {
    setEditing(a)
    setForm({
      employee_id: a.employee_id,
      system: a.system,
      access_level: a.access_level,
      compliance_status: a.compliance_status,
      expires_at: a.expires_at ? a.expires_at.slice(0, 10) : '',
      is_active: a.is_active,
    })
    setError('')
    setFormOpen(true)
  }

  const handleSave = async () => {
    if (!form.employee_id) { setError('Employee is required'); return }
    if (!form.system) { setError('System is required'); return }
    setSaving(true)
    try {
      const payload = { ...form, expires_at: form.expires_at || null }
      if (editing) await updateAuthorization(editing.id, payload)
      else await createAuthorization(payload)
      setFormOpen(false)
      load()
    } catch { setError('Save failed. Please try again.') }
    finally { setSaving(false) }
  }

  if (loading) return <div className="p-6 text-gray-500">Loading authorizations...</div>

  const filtered = filterStatus !== '' ? auths.filter(a => a.compliance_status === filterStatus) : auths

  const compliantCount = auths.filter(a => a.compliance_status === 'Compliant').length
  const expiredCount = auths.filter(a => a.compliance_status === 'Expired').length
  const pendingCount = auths.filter(a => a.compliance_status === 'PendingReview').length

  return (
    <div className="p-6">
      {/* Summary strip */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: 'Compliant', value: compliantCount, color: 'text-green-700 bg-green-50' },
          { label: 'Expired', value: expiredCount, color: 'text-red-700 bg-red-50' },
          { label: 'Pending Review', value: pendingCount, color: 'text-amber-700 bg-amber-50' },
        ].map(({ label, value, color }) => (
          <div key={label} className={`rounded-lg border border-gray-200 p-4 ${color}`}>
            <div className="text-2xl font-bold">{value}</div>
            <div className="text-sm">{label}</div>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-900">Authorization & Compliance ({filtered.length})</h1>
        <div className="flex items-center gap-3">
          <select
            value={filterStatus}
            onChange={e => setFilterStatus(e.target.value as ComplianceStatus | '')}
            className="border border-gray-200 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
          >
            <option value="">All Statuses</option>
            {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          {isAdmin && <Button onClick={openCreate}>+ Grant Access</Button>}
        </div>
      </div>

      <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-4 py-3 font-medium text-gray-600">Employee</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">System</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Access Level</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Expires</th>
              {isAdmin && <th className="px-4 py-3" />}
            </tr>
          </thead>
          <tbody>
            {filtered.map(a => (
              <tr key={a.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="px-4 py-3 font-medium text-gray-800">{a.employee_name}</td>
                <td className="px-4 py-3 text-gray-600">{a.system}</td>
                <td className="px-4 py-3 text-gray-600">{a.access_level}</td>
                <td className="px-4 py-3">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${STATUS_COLORS[a.compliance_status]}`}>
                    {a.compliance_status}
                  </span>
                </td>
                <td className="px-4 py-3 text-xs text-gray-500">
                  {a.expires_at ? new Date(a.expires_at).toLocaleDateString() : '—'}
                </td>
                {isAdmin && (
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => openEdit(a)} className="text-xs text-blue-600 hover:underline">Edit</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="text-center text-gray-400 py-8 text-sm">No authorizations found.</div>}
      </div>

      <Modal open={formOpen} title={editing ? 'Edit Authorization' : 'Grant Access'} onClose={() => setFormOpen(false)}>
        <FormField label="Employee" required>
          <Select
            value={form.employee_id}
            onChange={e => setForm(f => ({ ...f, employee_id: Number(e.target.value) }))}
            error={!!error && !form.employee_id}
            disabled={!!editing}
          >
            <option value="">Select employee…</option>
            {employees.map(e => <option key={e.id} value={e.id}>{e.name}</option>)}
          </Select>
        </FormField>
        <FormField label="System" required>
          <Select
            value={form.system}
            onChange={e => setForm(f => ({ ...f, system: e.target.value as AuthorizedSystem }))}
            error={!!error && !form.system}
          >
            <option value="">Select system…</option>
            {SYSTEMS.map(s => <option key={s} value={s}>{s}</option>)}
          </Select>
        </FormField>
        <FormField label="Access Level">
          <Select value={form.access_level} onChange={e => setForm(f => ({ ...f, access_level: e.target.value }))}>
            {ACCESS_LEVELS.map(l => <option key={l} value={l}>{l}</option>)}
          </Select>
        </FormField>
        <FormField label="Status">
          <Select value={form.compliance_status} onChange={e => setForm(f => ({ ...f, compliance_status: e.target.value as ComplianceStatus }))}>
            {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
          </Select>
        </FormField>
        <FormField label="Expiry Date">
          <Input type="date" value={form.expires_at || ''} onChange={e => setForm(f => ({ ...f, expires_at: e.target.value }))} />
        </FormField>
        <FormField label="Active">
          <Select value={form.is_active ? 'true' : 'false'} onChange={e => setForm(f => ({ ...f, is_active: e.target.value === 'true' }))}>
            <option value="true">Active</option>
            <option value="false">Revoked</option>
          </Select>
        </FormField>
        {error && <p className="text-xs text-red-500 mb-3">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setFormOpen(false)}>Cancel</Button>
          <Button loading={saving} onClick={handleSave}>{editing ? 'Save Changes' : 'Grant Access'}</Button>
        </div>
      </Modal>
    </div>
  )
}
