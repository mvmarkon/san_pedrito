import { Link, useNavigate } from 'react-router-dom'; // Added Link import

import { useTheme } from '@/components/theme-provider';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import api from '@/lib/api';

import { Bell, Menu, Moon, Sun, User } from 'lucide-react';

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const Header = ({ sidebarOpen, setSidebarOpen }: HeaderProps) => {
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    // Optionally, you might want to call a backend logout endpoint here
    api.post('/logout/');
    navigate('/login');
  };

  return (
    <header
      className="sticky top-0 z-30 bg-card shadow-sm"
    >
      {' '}
      {/* Changed background and added shadow */}
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 -mb-px">
          {/* Botón de menú para móvil - Keep for mobile responsiveness */}
          <div className="flex lg:hidden">
            <Button
              // variant="ghost"
              // size="icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-slate-500 hover:text-slate-600 lg:hidden"
            >
              <Menu className="w-6 h-6" />
              <span className="sr-only">Abrir menú</span>
            </Button>
          </div>

          {/* Logo y menú horizontal para desktop */}
          <div className="flex items-center space-x-4">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-color-primary">
                San Pedrito
              </span>{' '}
              {/* Apply primary color to logo */}
            </Link>
            {/* Aquí iría el menú horizontal si lo hubiera, por ahora solo el logo */}
          </div>

          {/* Buscador - oculto en móvil */}
          <div className="hidden md:flex md:grow">
            <form className="relative w-full max-w-md">
              <input
                className="w-full bg-gray-100 px-4 py-2 pl-9 rounded-md focus:outline-none focus:ring-2 focus:ring-color-primary border border-gray-200" // Updated styling
                type="search"
                placeholder="Buscar..."
              />
              <button
                type="submit"
                className="absolute inset-y-0 left-0 flex items-center pl-3"
              >
                <svg
                  className="w-4 h-4 fill-current text-slate-400"
                  viewBox="0 0 16 16"
                >
                  <path d="M7 14c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7zM7 2C4.243 2 2 4.243 2 7s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5z" />
                  <path d="M15.707 14.293L13.314 11.9a8.019 8.019 0 01-1.414 1.414l2.393 2.393a.997.997 0 001.414 0 .999.999 0 000-1.414z" />
                </svg>
              </button>
            </form>
          </div>

          {/* Acciones de usuario */}
          <div className="flex items-center space-x-3">
            {/* Botón de tema */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  // variant="ghost"
                  // size="icon"
                  className="rounded-full hover:bg-gray-100 transition-colors duration-300"
                >
                  {' '}
                  {/* Added hover effect */}
                  {theme === 'dark' ? (
                    <Sun className="h-5 w-5" />
                  ) : (
                    <Moon className="h-5 w-5" />
                  )}
                  <span className="sr-only">Cambiar tema</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setTheme('light')}>
                  <Sun className="mr-2 h-4 w-4" />
                  <span>Claro</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme('dark')}>
                  <Moon className="mr-2 h-4 w-4" />
                  <span>Oscuro</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Notificaciones */}
            <Button
              // variant="ghost"
              // size="icon"
              className="rounded-full hover:bg-gray-100 transition-colors duration-300"
            >
              {' '}
              {/* Added hover effect */}
              <Bell className="h-5 w-5" />
              <span className="sr-only">Notificaciones</span>
            </Button>

            {/* Menú de usuario */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  // variant="ghost"
                  // size="icon"
                  className="rounded-full hover:bg-gray-100 transition-colors duration-300"
                >
                  {' '}
                  {/* Added hover effect */}
                  <User className="h-5 w-5" />
                  <span className="sr-only">Menú de usuario</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>Perfil</DropdownMenuItem>
                <DropdownMenuItem>Configuración</DropdownMenuItem>
                <DropdownMenuItem onClick={handleLogout}>
                  Cerrar sesión
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Botón de CTA de ejemplo (si aplica) */}
            <Button
              className="bg-color-primary text-white rounded-md px-4 py-2 hover:opacity-90 transition-opacity duration-300"
              style={{ borderRadius: '6px', padding: '10px 24px' }}
            >
              {' '}
              {/* Example CTA Button */}
              Nuevo Item
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
