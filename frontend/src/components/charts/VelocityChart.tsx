import React from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import type { VelocityTrend } from '../../types'

export default function VelocityChart({ data }: { data: VelocityTrend[] }) {
  return (
    <ResponsiveContainer width="100%" height={240}>
      <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="sprint_name" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="velocity" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} name="Velocity" />
        <Line type="monotone" dataKey="delivery_score" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} name="Delivery Score" />
      </LineChart>
    </ResponsiveContainer>
  )
}
