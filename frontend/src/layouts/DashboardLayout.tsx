import React, { useState, ReactNode } from 'react';
import { Outlet } from 'react-router-dom';

import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';

interface DashboardLayoutProps {
  children?: ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }: DashboardLayoutProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      {/* Contenido principal */}
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        {/* Header */}
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Contenido de la página */}
        <main className="flex-grow p-6 md:p-8 lg:p-10">
          <div className="flex h-full">
            {/* Columna Central */}
            <div className="flex-1 overflow-y-auto">
              {children}
              <Outlet />
            </div>
            {/* Columna Derecha Opcional */}
            {/* <aside className="w-80 bg-white p-4 shadow-lg rounded-lg ml-4"> */}
            {/*   Contenido del panel derecho */}
            {/* </aside> */}
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
