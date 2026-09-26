import React from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from 'recharts'
import type { TeamHealth } from '../../types'

export default function TeamHealthChart({ data }: { data: TeamHealth[] }) {
  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="team_name" tick={{ fontSize: 10 }} angle={-30} textAnchor="end" />
        <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
        <Tooltip formatter={(v: number) => [`${v}`, 'Avg Delivery Score']} />
        <Bar dataKey="avg_delivery_score" name="Delivery Score" radius={[4, 4, 0, 0]}>
          {data.map((entry, index) => (
            <Cell
              key={index}
              fill={entry.avg_delivery_score >= 80 ? '#22c55e' : entry.avg_delivery_score >= 60 ? '#f59e0b' : '#ef4444'}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
