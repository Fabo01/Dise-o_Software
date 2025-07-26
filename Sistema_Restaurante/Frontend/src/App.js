import React, { useEffect } from 'react';
import { Routes, Route, Navigate, BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import Pedidos from './pages/Pedidos/Pedidos';
import CrearPedido from './pages/Pedidos/CrearPedido';
import DetallePedido from './pages/Pedidos/DetallePedido';
import Cocina from './pages/Cocina/Cocina';
import Menus from './pages/Menus/Menus';
import Mesas from './pages/Mesas/Mesas';
import Clientes from './pages/Clientes/Clientes';
import Usuarios from './pages/Usuarios/Usuarios';
import Ingredientes from './pages/Ingredientes/Ingredientes';
import Reportes from './pages/Reportes/Reportes';
import AuditDashboard from './components/Audit/AuditDashboard';
import Delivery from './components/Delivery';
import Pagos from './components/Pagos';
import { AuthProvider } from './contexts/AuthContext';
import { useNavigationAudit } from './hooks/useAudit';
import auditService from './services/auditService';

// Configurar React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
    mutations: {
      retry: 1,
    },
  },
});

// Componente interno que usa los hooks
function AppRoutes() {
  const { trackNavigation } = useNavigationAudit();

  useEffect(() => {
    // Inicializar servicio de auditoría
    auditService.initialize();
    
    // Log del inicio de la aplicación
    auditService.logAction('app_initialized', {
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      url: window.location.href
    });

    // Log de errores no capturadas
    const handleUnhandledError = (event) => {
      auditService.logError('unhandled_error', new Error(event.error?.message || 'Unknown error'), 'App');
    };

    const handleUnhandledRejection = (event) => {
      auditService.logError('unhandled_promise_rejection', new Error(event.reason?.message || 'Promise rejection'), 'App');
    };

    window.addEventListener('error', handleUnhandledError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleUnhandledError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  return (
    <Routes>
        <Route path="/" element={<Layout />}>
          {/* Página principal redirige al dashboard */}
          <Route index element={<Navigate to="/dashboard" replace />} />
          
          {/* Dashboard principal */}
          <Route path="dashboard" element={<Dashboard />} />
          
          {/* Gestión de Pedidos */}
          <Route path="pedidos" element={<Pedidos />} />
          <Route path="pedidos/crear" element={<CrearPedido />} />
          <Route path="pedidos/:id" element={<DetallePedido />} />
          
          {/* Vista de Cocina */}
          <Route path="cocina" element={<Cocina />} />
          
          {/* Gestión de Menús */}
          <Route path="menus" element={<Menus />} />
          
          {/* Gestión de Mesas */}
          <Route path="mesas" element={<Mesas />} />
          
          {/* Gestión de Clientes */}
          <Route path="clientes" element={<Clientes />} />
          
          {/* Gestión de Usuarios */}
          <Route path="usuarios" element={<Usuarios />} />
          
          {/* Gestión de Ingredientes */}
          <Route path="ingredientes" element={<Ingredientes />} />
          
          {/* Sistema de Delivery */}
          <Route path="delivery" element={<Delivery />} />
          
          {/* Sistema de Pagos */}
          <Route path="pagos" element={<Pagos />} />
          
          {/* Reportes y Estadísticas */}
          <Route path="reportes" element={<Reportes />} />
          
          {/* Dashboard de Auditoría - Solo para administradores */}
          <Route path="audit" element={<AuditDashboard />} />
          
          {/* Ruta 404 - Página no encontrada */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <AppRoutes />
          {/* React Query DevTools - Solo en desarrollo */}
          {process.env.NODE_ENV === 'development' && <ReactQueryDevtools initialIsOpen={false} />}
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
