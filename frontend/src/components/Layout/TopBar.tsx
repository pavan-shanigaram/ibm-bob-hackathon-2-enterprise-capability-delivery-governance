import React from 'react'
import { LogOut, ShieldCheck } from 'lucide-react'
import { useRole, type AppRole } from '../../context/RoleContext'

const ROLES: AppRole[] = ['platform_admin', 'team_lead', 'scrum_master', 'employee', 'executive', 'security_admin']

const ROLE_COLORS: Record<AppRole, string> = {
  platform_admin:  'bg-blue-100 text-blue-700',
  team_lead:       'bg-purple-100 text-purple-700',
  scrum_master:    'bg-green-100 text-green-700',
  employee:        'bg-gray-100 text-gray-700',
  executive:       'bg-amber-100 text-amber-700',
  security_admin:  'bg-red-100 text-red-700',
}

export default function TopBar() {
  const { role, setRole, isAdmin } = useRole()

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div className="text-sm text-gray-500">
        Enterprise Capability &amp; Delivery Governance
      </div>

      <div className="flex items-center gap-3">
        {/* Role switcher — demo only */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400 hidden md:inline">Role:</span>
          <select
            value={role}
            onChange={e => setRole(e.target.value as AppRole)}
            className="text-xs border border-gray-200 rounded-lg px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
          >
            {ROLES.map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* Active role badge */}
        <span className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full ${ROLE_COLORS[role]}`}>
          <ShieldCheck size={11} />
          {isAdmin ? 'Admin' : role.replace(/_/g, ' ')}
        </span>

        <button
          className="text-gray-400 hover:text-gray-600 transition-colors"
          title="Logout"
          onClick={() => {
            localStorage.removeItem('access_token')
            localStorage.removeItem('app_role')
            window.location.href = '/login'
          }}
        >
          <LogOut size={18} />
        </button>
      </div>
    </header>
  )
}
