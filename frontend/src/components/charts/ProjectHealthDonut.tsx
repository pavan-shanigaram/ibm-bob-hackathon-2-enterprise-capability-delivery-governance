import React from 'react'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface Props {
  green: number
  amber: number
  red: number
}

const COLORS = ['#22c55e', '#f59e0b', '#ef4444']

export default function ProjectHealthDonut({ green, amber, red }: Props) {
  const data = [
    { name: 'Green', value: green },
    { name: 'Amber', value: amber },
    { name: 'Red', value: red },
  ]
  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%" innerRadius={55} outerRadius={85} dataKey="value" label>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}
