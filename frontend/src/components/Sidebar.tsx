import { NavLink, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { X, Home, ShoppingBag, Users, ShoppingCart, BarChart4, Tag } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

interface SidebarProps {
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
}

const Sidebar = ({ sidebarOpen, setSidebarOpen }: SidebarProps) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 1024)

  // Cerrar sidebar al cambiar de ruta en móvil
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 1024)
      if (window.innerWidth >= 1024) {
        setSidebarOpen(false)
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <>
      {/* Overlay para móvil */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900 bg-opacity-30 transition-opacity lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        ></div>
      )}

      {/* Sidebar */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-64 flex-shrink-0 overflow-y-auto bg-background border-r transition-transform duration-200 ease-in-out lg:static lg:left-auto lg:top-auto lg:translate-x-0 lg:overflow-y-visible lg:w-20 xl:w-64",
          sidebarOpen ? "translate-x-0" : "-translate-x-64"
        )}
      >
        {/* Sidebar header */}
        <div className="flex items-center justify-between px-4 py-4 border-b lg:py-6">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <span className={cn("text-xl font-bold", !isMobile && "xl:block hidden")}>San Pedrito</span>
            <span className={cn("text-xl font-bold", !isMobile && "xl:hidden block")}>SP</span>
          </Link>

          {/* Botón cerrar para móvil */}
          {isMobile && (
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(false)}
              className="text-slate-500 hover:text-slate-600 lg:hidden"
            >
              <X className="w-6 h-6" />
              <span className="sr-only">Cerrar sidebar</span>
            </Button>
          )}
        </div>

        {/* Links */}
        <div className="space-y-8 px-4 py-6">
          {/* Sección principal */}
          <div>
            <h3 className={cn("text-xs font-semibold text-muted-foreground uppercase mb-3", !isMobile && "xl:block hidden")}>
              Principal
            </h3>
            <ul className="space-y-2">
              <li>
                <NavLink
                  to="/"
                  end
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted",
                      isActive ? "bg-muted text-primary" : "text-muted-foreground"
                    )
                  }
                >
                  <Home className="w-5 h-5" />
                  <span className={cn("text-sm font-medium", !isMobile && "xl:block hidden")}>Dashboard</span>
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/prendas"
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted",
                      isActive ? "bg-muted text-primary" : "text-muted-foreground"
                    )
                  }
                >
                  <ShoppingBag className="w-5 h-5" />
                  <span className={cn("text-sm font-medium", !isMobile && "xl:block hidden")}>Prendas</span>
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/clientes"
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted",
                      isActive ? "bg-muted text-primary" : "text-muted-foreground"
                    )
                  }
                >
                  <Users className="w-5 h-5" />
                  <span className={cn("text-sm font-medium", !isMobile && "xl:block hidden")}>Clientes</span>
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/ventas"
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted",
                      isActive ? "bg-muted text-primary" : "text-muted-foreground"
                    )
                  }
                >
                  <ShoppingCart className="w-5 h-5" />
                  <span className={cn("text-sm font-medium", !isMobile && "xl:block hidden")}>Ventas</span>
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/categorias"
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted",
                      isActive ? "bg-muted text-primary" : "text-muted-foreground"
                    )
                  }
                >
                  <Tag className="w-5 h-5" />
                  <span className={cn("text-sm font-medium", !isMobile && "xl:block hidden")}>Categorías</span>
                </NavLink>
              </li>
            </ul>
          </div>

          {/* Sección reportes */}
          <div>
            <h3 className={cn("text-xs font-semibold text-muted-foreground uppercase mb-3", !isMobile && "xl:block hidden")}>
              Reportes
            </h3>
            <ul className="space-y-2">
              <li>
                <NavLink
                  to="/reportes/ventas"
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted",
                      isActive ? "bg-muted text-primary" : "text-muted-foreground"
                    )
                  }
                >
                  <BarChart4 className="w-5 h-5" />
                  <span className={cn("text-sm font-medium", !isMobile && "xl:block hidden")}>Estadísticas</span>
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar