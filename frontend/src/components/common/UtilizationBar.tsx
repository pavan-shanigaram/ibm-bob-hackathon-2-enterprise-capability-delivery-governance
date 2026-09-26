import React from 'react'

interface Props {
  value: number
  max?: number
  label?: string
}

export default function UtilizationBar({ value, max = 100, label }: Props) {
  const pct = Math.min((value / max) * 100, 100)
  const color =
    value >= 100 ? 'bg-red-500'
    : value >= 80 ? 'bg-amber-400'
    : 'bg-green-500'
  return (
    <div className="w-full">
      {label && <div className="text-xs text-gray-500 mb-0.5">{label}</div>}
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div className={`${color} h-2 rounded-full transition-all`} style={{ width: `${pct}%` }} />
      </div>
      <div className="text-xs text-gray-500 mt-0.5 text-right">{Math.round(value)}%</div>
    </div>
  )
}
