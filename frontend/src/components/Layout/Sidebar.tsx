import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Users, Shield, Briefcase, BarChart2,
  Cpu, AlertTriangle, Network, Activity, FileText
} from 'lucide-react'

const nav = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/teams', icon: Network, label: 'Teams' },
  { to: '/squads', icon: Users, label: 'Squads' },
  { to: '/employees', icon: Users, label: 'Employees' },
  { to: '/projects', icon: Briefcase, label: 'Projects' },
  { to: '/capabilities', icon: Cpu, label: 'Capabilities' },
  { to: '/authorizations', icon: Shield, label: 'Authorizations' },
  { to: '/metrics', icon: BarChart2, label: 'Delivery Metrics' },
  { to: '/reports/skill-gaps', icon: AlertTriangle, label: 'Skill Gaps' },
  { to: '/reports/capacity', icon: Activity, label: 'Capacity Risk' },
  { to: '/reports/bottlenecks', icon: FileText, label: 'Bottlenecks' },
]

export default function Sidebar() {
  return (
    <aside className="w-60 min-h-screen bg-blue-900 text-white flex flex-col">
      <div className="px-6 py-5 border-b border-blue-800">
        <p className="text-xs font-semibold uppercase tracking-widest text-blue-300">IBM Bob Hackathon</p>
        <h1 className="text-sm font-bold mt-1 leading-tight">Enterprise Governance Platform</h1>
      </div>
      <nav className="flex-1 py-4 overflow-y-auto">
        {nav.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-5 py-2.5 text-sm transition-colors ${
                isActive
                  ? 'bg-blue-700 text-white font-semibold'
                  : 'text-blue-200 hover:bg-blue-800 hover:text-white'
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="px-5 py-4 border-t border-blue-800 text-xs text-blue-400">
        Powered by IBM watsonx.ai
      </div>
    </aside>
  )
}
