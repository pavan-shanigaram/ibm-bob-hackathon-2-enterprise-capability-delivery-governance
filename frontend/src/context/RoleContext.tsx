/**
 * Role context — in DEMO_MODE the backend returns platform_admin for all requests.
 * We store the simulated role in localStorage so the UI can show/hide admin controls.
 * In a real Auth0 setup this would read from the decoded JWT.
 */
import React, { createContext, useContext, useState } from 'react'

export type AppRole = 'platform_admin' | 'team_lead' | 'scrum_master' | 'employee' | 'executive' | 'security_admin'

interface RoleContextValue {
  role: AppRole
  setRole: (r: AppRole) => void
  isAdmin: boolean
}

const RoleContext = createContext<RoleContextValue>({
  role: 'platform_admin',
  setRole: () => {},
  isAdmin: true,
})

export function RoleProvider({ children }: { children: React.ReactNode }) {
  const [role, setRoleState] = useState<AppRole>(
    () => (localStorage.getItem('app_role') as AppRole) || 'platform_admin'
  )

  const setRole = (r: AppRole) => {
    localStorage.setItem('app_role', r)
    setRoleState(r)
  }

  return (
    <RoleContext.Provider value={{ role, setRole, isAdmin: role === 'platform_admin' }}>
      {children}
    </RoleContext.Provider>
  )
}

export const useRole = () => useContext(RoleContext)
