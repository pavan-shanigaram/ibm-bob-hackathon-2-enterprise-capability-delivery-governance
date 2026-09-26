import React from 'react'

interface KPICardProps {
  label: string
  value: string | number
  sub?: string
  color?: string
}

export default function KPICard({ label, value, sub, color = 'text-blue-700' }: KPICardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-5 flex flex-col gap-1">
      <div className="text-xs text-gray-500 uppercase tracking-wide font-medium">{label}</div>
      <div className={`text-3xl font-bold ${color}`}>{value}</div>
      {sub && <div className="text-xs text-gray-400">{sub}</div>}
    </div>
  )
}
