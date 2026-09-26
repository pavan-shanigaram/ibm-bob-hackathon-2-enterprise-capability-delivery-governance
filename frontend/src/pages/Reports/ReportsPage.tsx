import React, { useEffect, useState } from 'react'
import { getSkillGaps, getCapacityRisk, getDeliveryBottlenecks } from '../../api/dashboard'
import type { SkillGapProject, CapacityRisk } from '../../types'

export default function ReportsPage() {
  const [gaps, setGaps] = useState<SkillGapProject[]>([])
  const [capacityRisks, setCapacityRisks] = useState<CapacityRisk[]>([])
  const [bottlenecks, setBottlenecks] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getSkillGaps(), getCapacityRisk(), getDeliveryBottlenecks()])
      .then(([g, c, b]) => { setGaps(g); setCapacityRisks(c); setBottlenecks(b) })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-6 text-gray-500">Loading reports...</div>

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-xl font-bold text-gray-900">Governance Reports</h1>

      {/* Skill Gaps */}
      <section>
        <h2 className="text-base font-semibold text-gray-800 mb-3">Skill Gap Analysis ({gaps.length} projects affected)</h2>
        {gaps.length === 0 ? (
          <div className="text-sm text-green-600">No skill gaps identified. All projects are covered.</div>
        ) : (
          <div className="space-y-3">
            {gaps.map(p => (
              <div key={p.project_id} className="bg-white rounded-lg border border-amber-200 p-4">
                <div className="font-semibold text-gray-800 mb-2">{p.project_name}</div>
                <div className="space-y-1">
                  {p.gaps.map((g, i) => (
                    <div key={i} className="flex items-center gap-3 text-sm text-gray-600">
                      <span className="font-medium text-gray-800">{g.skill_name}</span>
                      <span className="text-amber-600">Need {g.headcount_needed}, have {g.headcount_available} — Gap: {g.gap}</span>
                      <span className="text-xs text-gray-400">({g.required_proficiency})</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Capacity Risk */}
      <section>
        <h2 className="text-base font-semibold text-gray-800 mb-3">Capacity Risk (&gt;90% utilized)</h2>
        {capacityRisks.length === 0 ? (
          <div className="text-sm text-green-600">No capacity risks detected.</div>
        ) : (
          <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Squad</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Avg Allocation</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Members</th>
                </tr>
              </thead>
              <tbody>
                {capacityRisks.map(r => (
                  <tr key={r.squad_id} className="border-b border-gray-100">
                    <td className="px-4 py-3 font-medium text-gray-800">{r.squad_name}</td>
                    <td className="px-4 py-3">
                      <span className="text-red-600 font-semibold">{r.avg_allocation}%</span>
                    </td>
                    <td className="px-4 py-3 text-gray-600">{r.member_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Delivery Bottlenecks */}
      <section>
        <h2 className="text-base font-semibold text-gray-800 mb-3">Delivery Bottlenecks (Score &lt;60)</h2>
        {bottlenecks.length === 0 ? (
          <div className="text-sm text-green-600">No delivery bottlenecks detected.</div>
        ) : (
          <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Squad</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Avg Delivery Score</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Sprints Analyzed</th>
                </tr>
              </thead>
              <tbody>
                {bottlenecks.map((b: any) => (
                  <tr key={b.squad_id} className="border-b border-gray-100">
                    <td className="px-4 py-3 font-medium text-gray-800">{b.squad_name}</td>
                    <td className="px-4 py-3 text-red-600 font-semibold">{b.avg_delivery_score}</td>
                    <td className="px-4 py-3 text-gray-600">{b.sprint_count_analyzed}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  )
}
