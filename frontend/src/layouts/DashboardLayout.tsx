import { Outlet } from 'react-router-dom'
import React, { useState, ReactNode } from 'react'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

interface DashboardLayoutProps {
  children?: ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      {/* Contenido principal */}
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        {/* Header */}
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Contenido de la página */}
        <main className="flex-grow p-4 sm:p-6 md:p-8">
          {children}
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout