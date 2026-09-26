import React from 'react'
import type { HealthIndicator } from '../../types'

const COLOR: Record<HealthIndicator, string> = {
  Green: 'bg-green-100 text-green-700 border-green-200',
  Amber: 'bg-amber-100 text-amber-700 border-amber-200',
  Red: 'bg-red-100 text-red-700 border-red-200',
}

export default function HealthBadge({ value }: { value: HealthIndicator }) {
  return (
    <span className={`inline-block px-2 py-0.5 text-xs font-semibold rounded border ${COLOR[value]}`}>
      {value}
    </span>
  )
}
