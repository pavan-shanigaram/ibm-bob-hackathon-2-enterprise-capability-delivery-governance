import React, { useState } from 'react'
import { Brain, RefreshCw } from 'lucide-react'
import type { AIInsight } from '../../types'
import { getRiskSummary } from '../../api/dashboard'

interface Props {
  initialInsight?: AIInsight | null
}

export default function AIInsightsPanel({ initialInsight }: Props) {
  const [insight, setInsight] = useState<AIInsight | null>(initialInsight || null)
  const [loading, setLoading] = useState(false)

  const refresh = async () => {
    setLoading(true)
    try {
      const data = await getRiskSummary()
      setInsight(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg border border-blue-200 p-5">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Brain size={16} className="text-blue-600" />
          <h3 className="font-semibold text-gray-800 text-sm">IBM watsonx.ai — Governance Insights</h3>
          {insight?.is_live_ai && (
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">Live AI</span>
          )}
        </div>
        <button
          onClick={refresh}
          disabled={loading}
          className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 disabled:opacity-50"
        >
          <RefreshCw size={12} className={loading ? 'animate-spin' : ''} />
          {loading ? 'Generating...' : 'Refresh'}
        </button>
      </div>
      {insight ? (
        <div className="text-sm text-gray-700 whitespace-pre-line leading-relaxed bg-blue-50 rounded p-3">
          {insight.narrative}
        </div>
      ) : (
        <div className="text-sm text-gray-400 italic">
          Click Refresh to generate AI governance insights using IBM Granite.
        </div>
      )}
      <div className="mt-2 text-xs text-gray-400">Model: {insight?.model || 'ibm/granite-3-3-8b-instruct'}</div>
    </div>
  )
}
