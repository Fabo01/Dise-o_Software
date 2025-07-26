import React, { useState, useEffect } from 'react';
import { Outlet, useLocation, Link } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import { useAudit } from '../../hooks/useAudit';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { logUserAction, logPerformance } = useAudit('Layout');

  // Monitorear cambios de ruta
  useEffect(() => {
    logUserAction('route_change', {
      path: location.pathname,
      search: location.search
    });

    // Cerrar sidebar en móvil al cambiar de ruta
    if (sidebarOpen && window.innerWidth < 1024) {
      setSidebarOpen(false);
    }
  }, [location, logUserAction, sidebarOpen]);

  // Monitorear rendimiento de la navegación
  useEffect(() => {
    const navigationStart = performance.getEntriesByType('navigation')[0];
    if (navigationStart) {
      logPerformance({
        pageLoadTime: navigationStart.loadEventEnd - navigationStart.navigationStart,
        domContentLoaded: navigationStart.domContentLoadedEventEnd - navigationStart.navigationStart,
        firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime
      });
    }
  }, [location.pathname, logPerformance]);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
    logUserAction('sidebar_toggle', { open: !sidebarOpen });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)}
        onToggle={toggleSidebar}
      />
      
      {/* Overlay para móvil */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Contenido principal */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <Header 
          onToggleSidebar={toggleSidebar}
          sidebarOpen={sidebarOpen}
        />
        
        {/* Contenido de la página */}
        <main className="flex-1 overflow-auto p-4 lg:p-6">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
        
        {/* Footer opcional */}
        <footer className="bg-white border-t border-gray-200 px-4 lg:px-6 py-3">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center text-sm text-gray-500">
            <div className="flex items-center space-x-4">
              <span>© 2024 Sistema Restaurante</span>
              <span className="hidden sm:inline">|</span>
              <span className="text-xs">
                Versión 2.0.0
              </span>
            </div>
            <div className="flex items-center space-x-4 mt-2 sm:mt-0">
              <Link 
                to="/audit" 
                className="hover:text-blue-600 transition-colors"
                onClick={() => logUserAction('audit_access_attempt')}
              >
                Auditoría
              </Link>
              <span className="text-xs">
                {new Date().toLocaleString('es-CL')}
              </span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Layout;
