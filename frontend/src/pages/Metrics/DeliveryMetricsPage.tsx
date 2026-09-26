import React, { useEffect, useState } from 'react'
import { getSquads } from '../../api/squads'
import { getVelocityTrend } from '../../api/dashboard'
import VelocityChart from '../../components/charts/VelocityChart'
import type { Squad, VelocityTrend } from '../../types'

export default function DeliveryMetricsPage() {
  const [squads, setSquads] = useState<Squad[]>([])
  const [selectedSquad, setSelectedSquad] = useState<number | null>(null)
  const [trend, setTrend] = useState<VelocityTrend[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getSquads().then(s => {
      setSquads(s)
      if (s.length > 0) setSelectedSquad(s[0].id)
    })
  }, [])

  useEffect(() => {
    if (!selectedSquad) return
    setLoading(true)
    getVelocityTrend(selectedSquad).then(setTrend).finally(() => setLoading(false))
  }, [selectedSquad])

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-bold text-gray-900">Delivery Metrics</h1>
        <select
          value={selectedSquad ?? ''}
          onChange={e => setSelectedSquad(Number(e.target.value))}
          className="border border-gray-200 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
        >
          {squads.map(s => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="text-gray-500">Loading metrics...</div>
      ) : trend.length === 0 ? (
        <div className="text-gray-400 italic">No sprint data available for this squad.</div>
      ) : (
        <div className="space-y-6">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h2 className="text-sm font-semibold text-gray-700 mb-3">Velocity & Delivery Score Trend</h2>
            <VelocityChart data={trend} />
          </div>
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Sprint</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Velocity</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Story Points Delivered</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Delivery Score</th>
                </tr>
              </thead>
              <tbody>
                {trend.map((t, i) => (
                  <tr key={i} className="border-b border-gray-100">
                    <td className="px-4 py-3 font-medium">{t.sprint_name}</td>
                    <td className="px-4 py-3 text-gray-600">{t.velocity}</td>
                    <td className="px-4 py-3 text-gray-600">{t.story_points_delivered}</td>
                    <td className="px-4 py-3">
                      <span className={`font-semibold ${t.delivery_score >= 80 ? 'text-green-600' : t.delivery_score >= 60 ? 'text-amber-500' : 'text-red-500'}`}>
                        {t.delivery_score}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
