import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { ThemeProvider } from '@/components/theme-provider'

// Layouts
import DashboardLayout from '@/layouts/DashboardLayout'

// Pages
import Dashboard from '@/pages/Dashboard'
import Prendas from '@/pages/Prendas'
import NuevaPrenda from '@/pages/NuevaPrenda'
import DetallePrenda from '@/pages/DetallePrenda'
import Clientes from '@/pages/Clientes'
import NuevoCliente from '@/pages/NuevoCliente'
import DetalleCliente from '@/pages/DetalleCliente'
import Ventas from '@/pages/Ventas'
import NuevaVenta from '@/pages/NuevaVenta'
import DetalleVenta from '@/pages/DetalleVenta'
import Login from '@/pages/Login'
import { Categorias } from '@/pages/Categorias'
import NotFound from '@/pages/NotFound'
import AuthGuard from '@/components/AuthGuard'

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="san-pedrito-theme">
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<Login />} />
        
        {/* Rutas protegidas */}
        <Route path="/" element={<AuthGuard><DashboardLayout /></AuthGuard>}>
          <Route index element={<Dashboard />} />
          
          {/* Prendas */}
          <Route path="prendas" element={<Prendas />} />
          <Route path="prendas/nueva" element={<NuevaPrenda />} />
          <Route path="prendas/:id" element={<DetallePrenda />} />
          <Route path="prendas/editar/:id" element={<NuevaPrenda />} />
          
          {/* Clientes */}
          <Route path="clientes" element={<Clientes />} />
          <Route path="clientes/nuevo" element={<NuevoCliente />} />
          <Route path="clientes/:id" element={<DetalleCliente />} />
          
          {/* Ventas */}
          <Route path="ventas" element={<Ventas />} />
          <Route path="ventas/nueva" element={<NuevaVenta />} />
          <Route path="ventas/:id" element={<DetalleVenta />} />

          {/* Categorías */}
          <Route path="categorias" element={<Categorias />} />
        </Route>
        
        {/* Ruta 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
      
      <Toaster />
    </ThemeProvider>
  )
}

export default App