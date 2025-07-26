import React, { useState, useEffect } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { useLocation } from 'react-router-dom';
import {
  Bars3Icon,
  BellIcon,
  UserCircleIcon,
  MagnifyingGlassIcon,
  SunIcon,
  MoonIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';
import { useAudit } from '../../hooks/useAudit';

const userNavigation = [
  { name: 'Tu Perfil', href: '#', icon: UserCircleIcon },
  { name: 'Configuración', href: '#', icon: Cog6ToothIcon },
  { name: 'Cerrar Sesión', href: '#', icon: ArrowRightOnRectangleIcon, action: 'logout' },
];

const pageNames = {
  '/dashboard': 'Dashboard',
  '/pedidos': 'Gestión de Pedidos',
  '/pedidos/crear': 'Crear Nuevo Pedido',
  '/cocina': 'Vista de Cocina',
  '/menus': 'Gestión de Menús',
  '/mesas': 'Administrar Mesas',
  '/clientes': 'Base de Clientes',
  '/ingredientes': 'Inventario de Ingredientes',
  '/delivery': 'Sistema de Delivery',
  '/pagos': 'Gestión de Pagos',
  '/reportes': 'Reportes y Estadísticas',
  '/usuarios': 'Administrar Usuarios',
  '/audit': 'Dashboard de Auditoría',
};

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

const Header = ({ onToggleSidebar, sidebarOpen }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const { logUserAction } = useAudit('Header');
  const [searchQuery, setSearchQuery] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [notifications] = useState([
    { id: 1, title: 'Nuevo pedido #123', time: '2 min' },
    { id: 2, title: 'Mesa 5 solicita atención', time: '5 min' },
    { id: 3, title: 'Inventario bajo: Tomates', time: '10 min' }
  ]);

  // Obtener el nombre de la página actual
  const getCurrentPageName = () => {
    return pageNames[location.pathname] || 'Sistema de Gestión';
  };

  useEffect(() => {
    // Log del cambio de página
    logUserAction('page_view', {
      path: location.pathname,
      pageName: getCurrentPageName()
    });
  }, [location.pathname, logUserAction]);

  const handleLogout = () => {
    logUserAction('logout_initiated');
    logout();
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      logUserAction('search_performed', {
        query: searchQuery,
        page: location.pathname
      });
      // Aquí iría la lógica de búsqueda
      console.log('Búsqueda:', searchQuery);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    logUserAction('theme_toggle', { darkMode: !darkMode });
  };

  const handleNotificationClick = () => {
    logUserAction('notifications_opened');
  };

  const handleUserMenuAction = (action, item) => {
    logUserAction('user_menu_action', {
      action: action || item.name,
      itemName: item.name
    });

    if (action === 'logout') {
      handleLogout();
    }
  };

  return (
    <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      {/* Botón de menú móvil */}
      <button
        type="button"
        className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
        onClick={() => {
          onToggleSidebar();
          logUserAction('mobile_menu_toggle', { open: !sidebarOpen });
        }}
      >
        <span className="sr-only">Abrir sidebar</span>
        <Bars3Icon className="h-6 w-6" aria-hidden="true" />
      </button>

      {/* Separador */}
      <div className="h-6 w-px bg-gray-200 lg:hidden" aria-hidden="true" />

      {/* Título y búsqueda */}
      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="flex flex-1 items-center">
          {/* Título de la página actual */}
          <div className="flex-1">
            <h1 className="text-lg font-semibold text-gray-900 sm:text-xl">
              {getCurrentPageName()}
            </h1>
            <p className="text-sm text-gray-500 hidden sm:block">
              {user?.email || 'Usuario no autenticado'}
            </p>
          </div>

          {/* Barra de búsqueda - Solo en desktop */}
          <form onSubmit={handleSearch} className="hidden lg:flex lg:items-center lg:w-96">
            <div className="relative w-full">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
              <input
                type="search"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Buscar pedidos, mesas, clientes..."
                className="block w-full rounded-md border-0 py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
              />
            </div>
          </form>
        </div>

        {/* Acciones del usuario */}
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          {/* Alternar tema */}
          <button
            type="button"
            className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500"
            onClick={toggleDarkMode}
          >
            <span className="sr-only">Alternar tema</span>
            {darkMode ? (
              <SunIcon className="h-6 w-6" aria-hidden="true" />
            ) : (
              <MoonIcon className="h-6 w-6" aria-hidden="true" />
            )}
          </button>

          {/* Notificaciones */}
          <Menu as="div" className="relative">
            <Menu.Button 
              className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500"
              onClick={handleNotificationClick}
            >
              <span className="sr-only">Ver notificaciones</span>
              <div className="relative">
                <BellIcon className="h-6 w-6" aria-hidden="true" />
                {notifications.length > 0 && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {notifications.length}
                  </span>
                )}
              </div>
            </Menu.Button>
            
            <Transition
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 z-10 mt-2.5 w-80 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                <div className="px-4 py-2 border-b border-gray-100">
                  <h3 className="font-medium text-gray-900">Notificaciones</h3>
                </div>
                {notifications.length === 0 ? (
                  <div className="px-4 py-3 text-sm text-gray-500">
                    No hay notificaciones nuevas
                  </div>
                ) : (
                  notifications.map((notification) => (
                    <Menu.Item key={notification.id}>
                      {({ active }) => (
                        <div
                          className={classNames(
                            active ? 'bg-gray-50' : '',
                            'px-4 py-3 text-sm cursor-pointer border-b border-gray-100 last:border-b-0'
                          )}
                        >
                          <p className="text-gray-900">{notification.title}</p>
                          <p className="text-gray-500 text-xs">{notification.time} ago</p>
                        </div>
                      )}
                    </Menu.Item>
                  ))
                )}
              </Menu.Items>
            </Transition>
          </Menu>

          {/* Separador */}
          <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-200" aria-hidden="true" />

          {/* Perfil del usuario */}
          <Menu as="div" className="relative">
            <Menu.Button className="-m-1.5 flex items-center p-1.5">
              <span className="sr-only">Abrir menú de usuario</span>
              <div className="flex items-center gap-x-3">
                {user?.avatar ? (
                  <img
                    className="h-8 w-8 rounded-full bg-gray-50"
                    src={user.avatar}
                    alt={user.name || 'Usuario'}
                  />
                ) : (
                  <UserCircleIcon className="h-8 w-8 text-gray-400" />
                )}
                <span className="hidden lg:flex lg:items-center">
                  <span className="ml-2 text-sm font-semibold leading-6 text-gray-900" aria-hidden="true">
                    {user?.name || user?.email || 'Usuario'}
                  </span>
                </span>
              </div>
            </Menu.Button>
            
            <Transition
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 z-10 mt-2.5 w-56 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                {userNavigation.map((item) => (
                  <Menu.Item key={item.name}>
                    {({ active }) => (
                      <button
                        onClick={() => handleUserMenuAction(item.action, item)}
                        className={classNames(
                          active ? 'bg-gray-50' : '',
                          'flex w-full items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-50'
                        )}
                      >
                        <item.icon className="mr-3 h-5 w-5 text-gray-400" aria-hidden="true" />
                        {item.name}
                      </button>
                    )}
                  </Menu.Item>
                ))}
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </div>
  );
};

export default Header;
