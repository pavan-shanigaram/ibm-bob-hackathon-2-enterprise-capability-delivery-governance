import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { RoleProvider } from './context/RoleContext'
import Sidebar from './components/Layout/Sidebar'
import TopBar from './components/Layout/TopBar'
import ExecutiveDashboardPage from './pages/Dashboard/ExecutiveDashboard'
import TeamsPage from './pages/Teams/TeamsPage'
import SquadsPage from './pages/Squads/SquadsPage'
import EmployeesPage from './pages/Employees/EmployeesPage'
import ProjectsPage from './pages/Projects/ProjectsPage'
import ProjectHubPage from './pages/Projects/ProjectHubPage'
import CapabilityMatrixPage from './pages/Capabilities/CapabilityMatrixPage'
import AuthorizationsPage from './pages/Authorizations/AuthorizationsPage'
import DeliveryMetricsPage from './pages/Metrics/DeliveryMetricsPage'
import ReportsPage from './pages/Reports/ReportsPage'

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <RoleProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<ExecutiveDashboardPage />} />
            <Route path="/teams" element={<TeamsPage />} />
            <Route path="/squads" element={<SquadsPage />} />
            <Route path="/employees" element={<EmployeesPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/projects/:id/hub" element={<ProjectHubPage />} />
            <Route path="/capabilities" element={<CapabilityMatrixPage />} />
            <Route path="/authorizations" element={<AuthorizationsPage />} />
            <Route path="/metrics" element={<DeliveryMetricsPage />} />
            <Route path="/reports/skill-gaps" element={<ReportsPage />} />
            <Route path="/reports/capacity" element={<ReportsPage />} />
            <Route path="/reports/bottlenecks" element={<ReportsPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </RoleProvider>
  )
}
