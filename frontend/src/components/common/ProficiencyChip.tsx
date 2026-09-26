import React from 'react'
import type { ProficiencyLevel } from '../../types'

const COLOR: Record<ProficiencyLevel, string> = {
  Beginner: 'bg-gray-100 text-gray-600',
  Intermediate: 'bg-blue-100 text-blue-700',
  Expert: 'bg-green-100 text-green-700',
  Lead: 'bg-purple-100 text-purple-700',
}

export default function ProficiencyChip({ level }: { level: ProficiencyLevel }) {
  return (
    <span className={`inline-block px-2 py-0.5 text-xs font-medium rounded-full ${COLOR[level]}`}>
      {level}
    </span>
  )
}
