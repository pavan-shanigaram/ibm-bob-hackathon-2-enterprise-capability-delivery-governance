import React, { useEffect, useState } from 'react'
import KPICard from '../../components/dashboard/KPICard'
import TeamHealthChart from '../../components/charts/TeamHealthChart'
import ProjectHealthDonut from '../../components/charts/ProjectHealthDonut'
import RiskHeatmap from '../../components/dashboard/RiskHeatmap'
import AIInsightsPanel from '../../components/dashboard/AIInsightsPanel'
import { getDemoDashboard, getDemoAIInsights } from '../../api/dashboard'
import type { ExecutiveDashboard, AIInsight } from '../../types'

export default function ExecutiveDashboardPage() {
  const [dashboard, setDashboard] = useState<ExecutiveDashboard | null>(null)
  const [aiInsight, setAiInsight] = useState<AIInsight | null>(null)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    try {
      const [db, ai] = await Promise.all([getDemoDashboard(), getDemoAIInsights()])
      setDashboard(db)
      setAiInsight(ai)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    const interval = setInterval(load, 60000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-gray-500">Loading dashboard...</div>
  }
  if (!dashboard) {
    return <div className="text-red-500 p-6">Failed to load dashboard. Is the backend running?</div>
  }

  const { kpis, project_health_counts, team_health, risk_heatmap, alerts } = dashboard

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">Executive Governance Dashboard</h1>
        <span className="text-xs text-gray-400">Auto-refreshes every 60s</span>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="space-y-2">
          {alerts.map((a, i) => (
            <div
              key={i}
              className={`px-4 py-2 rounded text-sm font-medium ${
                a.type === 'error' ? 'bg-red-50 text-red-700 border border-red-200'
                : 'bg-amber-50 text-amber-700 border border-amber-200'
              }`}
            >
              {a.message}
            </div>
          ))}
        </div>
      )}

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <KPICard label="Teams" value={kpis.total_teams} />
        <KPICard label="Squads" value={kpis.total_squads} />
        <KPICard label="Employees" value={kpis.total_employees} />
        <KPICard label="Active Projects" value={kpis.active_projects} color="text-green-700" />
        <KPICard label="Avg Delivery Score" value={`${kpis.avg_delivery_score}%`} color="text-blue-700" />
        <KPICard
          label="Over-Allocated"
          value={kpis.over_allocated_count}
          color={kpis.over_allocated_count > 0 ? 'text-red-600' : 'text-green-600'}
        />
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-gray-700 mb-3">Team Delivery Health</h2>
          <TeamHealthChart data={team_health} />
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-sm font-semibold text-gray-700 mb-3">Project Health</h2>
          <ProjectHealthDonut
            green={project_health_counts.green}
            amber={project_health_counts.amber}
            red={project_health_counts.red}
          />
        </div>
      </div>

      {/* Risk Heatmap */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Enterprise Risk Heatmap</h2>
        <RiskHeatmap data={risk_heatmap} />
      </div>

      {/* AI Insights */}
      <AIInsightsPanel initialInsight={aiInsight} />
    </div>
  )
}
