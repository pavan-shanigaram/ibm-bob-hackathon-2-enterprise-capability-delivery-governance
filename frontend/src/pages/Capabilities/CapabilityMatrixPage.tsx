import React, { useEffect, useState } from 'react'
import { getCapabilityMatrix, getSkills, createSkill } from '../../api/dashboard'
import { useRole } from '../../context/RoleContext'
import Modal from '../../components/common/Modal'
import Button from '../../components/common/Button'
import { FormField, Input, Textarea } from '../../components/common/FormField'
import ProficiencyChip from '../../components/common/ProficiencyChip'
import type { ProficiencyLevel, Skill } from '../../types'

interface MatrixRow {
  employee_id: number
  employee_name: string
  skills: Array<{
    skill_id: number
    skill_name: string
    skill_category: string
    proficiency_level: ProficiencyLevel | null
  }>
}

const EMPTY_SKILL: Partial<Skill> = { name: '', category: '', description: '' }

export default function CapabilityMatrixPage() {
  const { isAdmin } = useRole()
  const [matrix, setMatrix] = useState<MatrixRow[]>([])
  const [skills, setSkills] = useState<Skill[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [skillFormOpen, setSkillFormOpen] = useState(false)
  const [skillForm, setSkillForm] = useState<Partial<Skill>>(EMPTY_SKILL)
  const [skillError, setSkillError] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')

  const load = () => {
    setLoading(true)
    Promise.all([getCapabilityMatrix(), getSkills()])
      .then(([m, s]) => { setMatrix(m); setSkills(s) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const openSkillCreate = () => { setSkillForm(EMPTY_SKILL); setSkillError(''); setSkillFormOpen(true) }

  const handleSkillSave = async () => {
    if (!skillForm.name?.trim()) { setSkillError('Skill name is required'); return }
    if (!skillForm.category?.trim()) { setSkillError('Category is required'); return }
    setSaving(true)
    try {
      await createSkill(skillForm)
      setSkillFormOpen(false)
      load()
    } catch { setSkillError('Save failed. Please try again.') }
    finally { setSaving(false) }
  }

  if (loading) return <div className="p-6 text-gray-500">Loading capability matrix...</div>
  if (matrix.length === 0) return <div className="p-6 text-gray-400">No data available.</div>

  const allSkills = matrix[0]?.skills || []
  const categories = Array.from(new Set(allSkills.map(s => s.skill_category))).sort()
  const visibleSkills = categoryFilter ? allSkills.filter(s => s.skill_category === categoryFilter) : allSkills

  // Skill summary: how many employees have each skill
  const skillCoverage = allSkills.map(s => ({
    ...s,
    count: matrix.filter(row => row.skills.find(rs => rs.skill_id === s.skill_id && rs.proficiency_level)).length,
  }))

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Capability Matrix</h1>
          <p className="text-sm text-gray-500">Employee proficiency across all tracked skills</p>
        </div>
        {isAdmin && <Button onClick={openSkillCreate}>+ Add Skill</Button>}
      </div>

      {/* Skill summary row */}
      <div className="mt-4 mb-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {skillCoverage.slice(0, 8).map(s => (
          <div key={s.skill_id} className="bg-white border border-gray-200 rounded-lg p-3 text-xs">
            <div className="font-semibold text-gray-800 truncate">{s.skill_name}</div>
            <div className="text-gray-400 truncate">{s.skill_category}</div>
            <div className="mt-1 text-blue-600 font-bold">{s.count} / {matrix.length}</div>
          </div>
        ))}
      </div>

      {/* Filter */}
      <div className="flex items-center gap-3 mb-4">
        <span className="text-sm text-gray-600">Filter by category:</span>
        <select
          value={categoryFilter}
          onChange={e => setCategoryFilter(e.target.value)}
          className="border border-gray-200 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
        >
          <option value="">All Categories ({allSkills.length} skills)</option>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <span className="text-xs text-gray-400">Showing {visibleSkills.length} skills, first 50 employees</span>
      </div>

      <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
        <table className="text-xs w-full border-collapse">
          <thead>
            <tr>
              <th className="sticky left-0 bg-gray-50 px-3 py-2 border border-gray-200 font-medium text-gray-600 text-left whitespace-nowrap">Employee</th>
              {visibleSkills.map(s => (
                <th key={s.skill_id} className="px-2 py-2 border border-gray-200 font-medium text-gray-600 whitespace-nowrap" style={{ writingMode: 'vertical-rl', minWidth: 32 }}>
                  {s.skill_name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.slice(0, 50).map(row => (
              <tr key={row.employee_id} className="hover:bg-gray-50">
                <td className="sticky left-0 bg-white px-3 py-1.5 border border-gray-200 font-medium text-gray-700 whitespace-nowrap">{row.employee_name}</td>
                {visibleSkills.map(s => {
                  const match = row.skills.find(rs => rs.skill_id === s.skill_id)
                  return (
                    <td key={s.skill_id} className="px-1 py-1 border border-gray-200 text-center">
                      {match?.proficiency_level ? (
                        <ProficiencyChip level={match.proficiency_level} />
                      ) : (
                        <span className="text-gray-200">—</span>
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
        {matrix.length > 50 && (
          <div className="text-xs text-gray-400 text-center py-2">Showing first 50 of {matrix.length} employees</div>
        )}
      </div>

      {/* All Skills list */}
      <div className="mt-6">
        <h2 className="text-base font-semibold text-gray-900 mb-3">Skill Catalogue ({skills.length} skills)</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
          {skills.map(s => (
            <div key={s.id} className="bg-white border border-gray-200 rounded-lg px-3 py-2 text-xs">
              <div className="font-medium text-gray-800 truncate">{s.name}</div>
              <div className="text-gray-400 truncate">{s.category}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Add Skill Modal */}
      <Modal open={skillFormOpen} title="Add New Skill" onClose={() => setSkillFormOpen(false)} width="max-w-sm">
        <FormField label="Skill Name" required>
          <Input value={skillForm.name || ''} onChange={e => setSkillForm(f => ({ ...f, name: e.target.value }))} placeholder="e.g. Kubernetes" error={!!skillError && !skillForm.name?.trim()} />
        </FormField>
        <FormField label="Category" required>
          <Input value={skillForm.category || ''} onChange={e => setSkillForm(f => ({ ...f, category: e.target.value }))} placeholder="e.g. Cloud & Infrastructure" error={!!skillError && !skillForm.category?.trim()} />
        </FormField>
        <FormField label="Description">
          <Textarea value={skillForm.description || ''} onChange={e => setSkillForm(f => ({ ...f, description: e.target.value }))} />
        </FormField>
        {skillError && <p className="text-xs text-red-500 mb-3">{skillError}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" onClick={() => setSkillFormOpen(false)}>Cancel</Button>
          <Button loading={saving} onClick={handleSkillSave}>Add Skill</Button>
        </div>
      </Modal>
    </div>
  )
}
