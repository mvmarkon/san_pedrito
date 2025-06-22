import { Outlet, Route, Routes } from 'react-router-dom';

import AuthGuard from '@/components/AuthGuard';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from '@/components/ui/toaster';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// Layouts
import DashboardLayout from '@/layouts/DashboardLayout';
import { Categorias } from '@/pages/Categorias';
import Clientes from '@/pages/Clientes';
// Pages
import Dashboard from '@/pages/Dashboard';
import DetalleCliente from '@/pages/DetalleCliente';
import DetallePrenda from '@/pages/DetallePrenda';
import DetalleVenta from '@/pages/DetalleVenta';
import Login from '@/pages/Login';
import NotFound from '@/pages/NotFound';
import NuevaPrenda from '@/pages/NuevaPrenda';
import NuevaVenta from '@/pages/NuevaVenta';
import NuevoCliente from '@/pages/NuevoCliente';
import Prendas from '@/pages/Prendas';
import Ventas from '@/pages/Ventas';

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="san-pedrito-theme">
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<Login />} />

        {/* Rutas protegidas */}
        <Route
          path="/"
          element={
            <AuthGuard>
              <DashboardLayout />
            </AuthGuard>
          }
        >
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
      <ToastContainer position="bottom-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
    </ThemeProvider>
  );
}

export default App;
