import React, { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { Link, useLocation } from 'react-router-dom';
import { 
  XMarkIcon,
  HomeIcon,
  ShoppingBagIcon,
  ChefHatIcon,
  UsersIcon,
  TableCellsIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  ChartBarIcon,
  TruckIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  ClipboardDocumentListIcon
} from '@heroicons/react/24/outline';
import { useAudit } from '../../hooks/useAudit';

const navigation = [
  { 
    name: 'Dashboard', 
    href: '/dashboard', 
    icon: HomeIcon,
    description: 'Vista general del sistema'
  },
  { 
    name: 'Pedidos', 
    href: '/pedidos', 
    icon: ShoppingBagIcon,
    description: 'Gestionar pedidos'
  },
  { 
    name: 'Cocina', 
    href: '/cocina', 
    icon: ChefHatIcon,
    description: 'Vista de cocina'
  },
  { 
    name: 'Menús', 
    href: '/menus', 
    icon: DocumentTextIcon,
    description: 'Gestionar menús'
  },
  { 
    name: 'Mesas', 
    href: '/mesas', 
    icon: TableCellsIcon,
    description: 'Administrar mesas'
  },
  { 
    name: 'Clientes', 
    href: '/clientes', 
    icon: UsersIcon,
    description: 'Base de clientes'
  },
  { 
    name: 'Ingredientes', 
    href: '/ingredientes', 
    icon: Cog6ToothIcon,
    description: 'Inventario de ingredientes'
  },
  { 
    name: 'Delivery', 
    href: '/delivery', 
    icon: TruckIcon,
    description: 'Sistema de delivery'
  },
  { 
    name: 'Pagos', 
    href: '/pagos', 
    icon: CreditCardIcon,
    description: 'Gestión de pagos'
  },
  { 
    name: 'Reportes', 
    href: '/reportes', 
    icon: ChartBarIcon,
    description: 'Reportes y estadísticas'
  },
  { 
    name: 'Usuarios', 
    href: '/usuarios', 
    icon: UsersIcon,
    description: 'Administrar usuarios'
  },
];

const adminNavigation = [
  { 
    name: 'Auditoría', 
    href: '/audit', 
    icon: ShieldCheckIcon,
    description: 'Sistema de auditoría'
  },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

const Sidebar = ({ isOpen, onClose, onToggle }) => {
  const location = useLocation();
  const { logUserAction } = useAudit('Sidebar');

  const handleNavigationClick = (item) => {
    logUserAction('navigation_click', {
      destination: item.href,
      itemName: item.name
    });
    
    // Cerrar sidebar en móvil
    if (window.innerWidth < 1024) {
      onClose();
    }
  };

  const SidebarContent = ({ isMobile = false }) => (
    <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4">
      <div className="flex h-16 shrink-0 items-center justify-between">
        <div className="flex items-center">
          <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <ClipboardDocumentListIcon className="h-5 w-5 text-white" />
          </div>
          <span className="ml-2 text-xl font-bold text-gray-900">
            Sistema ER
          </span>
        </div>
        {!isMobile && (
          <button
            onClick={onToggle}
            className="lg:hidden p-1 text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        )}
      </div>
      
      <nav className="flex flex-1 flex-col">
        <ul className="flex flex-1 flex-col gap-y-7">
          <li>
            <div className="text-xs font-semibold leading-6 text-gray-400 mb-2">
              MENÚ PRINCIPAL
            </div>
            <ul className="-mx-2 space-y-1">
              {navigation.map((item) => (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    onClick={() => handleNavigationClick(item)}
                    className={classNames(
                      location.pathname === item.href
                        ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-blue-700',
                      'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-medium transition-colors'
                    )}
                  >
                    <item.icon
                      className={classNames(
                        location.pathname === item.href
                          ? 'text-blue-700'
                          : 'text-gray-400 group-hover:text-blue-700',
                        'h-6 w-6 shrink-0'
                      )}
                      aria-hidden="true"
                    />
                    <div className="flex flex-col">
                      <span>{item.name}</span>
                      <span className="text-xs text-gray-500">{item.description}</span>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          </li>
          
          {/* Sección de administración */}
          <li>
            <div className="text-xs font-semibold leading-6 text-gray-400 mb-2">
              ADMINISTRACIÓN
            </div>
            <ul className="-mx-2 space-y-1">
              {adminNavigation.map((item) => (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    onClick={() => handleNavigationClick(item)}
                    className={classNames(
                      location.pathname === item.href
                        ? 'bg-red-50 text-red-700 border-r-2 border-red-700'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-red-700',
                      'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-medium transition-colors'
                    )}
                  >
                    <item.icon
                      className={classNames(
                        location.pathname === item.href
                          ? 'text-red-700'
                          : 'text-gray-400 group-hover:text-red-700',
                        'h-6 w-6 shrink-0'
                      )}
                      aria-hidden="true"
                    />
                    <div className="flex flex-col">
                      <span>{item.name}</span>
                      <span className="text-xs text-gray-500">{item.description}</span>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          </li>
        </ul>
      </nav>
    </div>
  );

  return (
    <>
      {/* Sidebar móvil */}
      <Transition.Root show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-50 lg:hidden" onClose={onClose}>
          <Transition.Child
            as={Fragment}
            enter="transition-opacity ease-linear duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-linear duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-gray-900/80" />
          </Transition.Child>

          <div className="fixed inset-0 flex">
            <Transition.Child
              as={Fragment}
              enter="transition ease-in-out duration-300 transform"
              enterFrom="-translate-x-full"
              enterTo="translate-x-0"
              leave="transition ease-in-out duration-300 transform"
              leaveFrom="translate-x-0"
              leaveTo="-translate-x-full"
            >
              <Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
                <Transition.Child
                  as={Fragment}
                  enter="ease-in-out duration-300"
                  enterFrom="opacity-0"
                  enterTo="opacity-100"
                  leave="ease-in-out duration-300"
                  leaveFrom="opacity-100"
                  leaveTo="opacity-0"
                >
                  <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                    <button
                      type="button"
                      className="-m-2.5 p-2.5"
                      onClick={onClose}
                    >
                      <span className="sr-only">Cerrar sidebar</span>
                      <XMarkIcon className="h-6 w-6 text-white" aria-hidden="true" />
                    </button>
                  </div>
                </Transition.Child>
                
                <SidebarContent isMobile={true} />
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition.Root>

      {/* Sidebar desktop */}
      <div className={classNames(
        'hidden lg:fixed lg:inset-y-0 lg:flex lg:w-72 lg:flex-col transition-transform duration-300 z-30',
        isOpen ? 'lg:translate-x-0' : 'lg:-translate-x-72'
      )}>
        <div className="flex grow flex-col border-r border-gray-200 bg-white">
          <SidebarContent />
        </div>
      </div>
    </>
  );
};

export default Sidebar;
