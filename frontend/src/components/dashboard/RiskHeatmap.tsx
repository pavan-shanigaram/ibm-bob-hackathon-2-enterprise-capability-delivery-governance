import React from 'react'
import type { RiskHeatmapRow } from '../../types'

const riskColor = (v: number) =>
  v <= 1 ? '#22c55e'
  : v <= 2 ? '#86efac'
  : v === 3 ? '#f59e0b'
  : v === 4 ? '#f97316'
  : '#ef4444'

const DIMS = ['Resource', 'Delivery', 'Capability', 'Compliance'] as const

export default function RiskHeatmap({ data }: { data: RiskHeatmapRow[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="text-xs w-full border-collapse">
        <thead>
          <tr>
            <th className="text-left px-3 py-2 bg-gray-50 border border-gray-200 font-medium text-gray-600">Team</th>
            {DIMS.map(d => (
              <th key={d} className="px-3 py-2 bg-gray-50 border border-gray-200 font-medium text-gray-600 text-center">{d}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td className="px-3 py-2 border border-gray-200 font-medium text-gray-700 whitespace-nowrap">{row.team_name}</td>
              {DIMS.map(d => {
                const val = row[d] as number
                return (
                  <td
                    key={d}
                    className="px-3 py-2 border border-gray-200 text-center font-bold"
                    style={{ backgroundColor: riskColor(val), color: val >= 4 ? '#fff' : '#1f2328' }}
                  >
                    {val}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex gap-3 mt-2 text-xs text-gray-500">
        <span className="flex items-center gap-1"><span style={{ background: '#22c55e' }} className="w-3 h-3 rounded inline-block" /> Low (1)</span>
        <span className="flex items-center gap-1"><span style={{ background: '#f59e0b' }} className="w-3 h-3 rounded inline-block" /> Medium (3)</span>
        <span className="flex items-center gap-1"><span style={{ background: '#ef4444' }} className="w-3 h-3 rounded inline-block" /> High (5)</span>
      </div>
    </div>
  )
}
