// Frontend/src/utils/lazyComponents.js
// Implementa tareas S3-24 y S3-25: Lazy loading y code splitting
import { lazy } from 'react';

// Componentes principales con lazy loading
export const Dashboard = lazy(() => 
    import('../pages/Dashboard/Dashboard').then(module => ({
        default: module.default
    }))
);

export const Pedidos = lazy(() => 
    import('../pages/Pedidos/Pedidos').then(module => ({
        default: module.default
    }))
);

export const Delivery = lazy(() => 
    import('../components/Delivery').then(module => ({
        default: module.default
    }))
);

export const Pagos = lazy(() => 
    import('../components/Pagos').then(module => ({
        default: module.default
    }))
);

export const Menus = lazy(() => 
    import('../pages/Menus/Menus').then(module => ({
        default: module.default
    }))
);

export const Ingredientes = lazy(() => 
    import('../pages/Ingredientes/Ingredientes').then(module => ({
        default: module.default
    }))
);

export const Clientes = lazy(() => 
    import('../pages/Clientes/Clientes').then(module => ({
        default: module.default
    }))
);

export const Mesas = lazy(() => 
    import('../pages/Mesas/Mesas').then(module => ({
        default: module.default
    }))
);

export const Cocina = lazy(() => 
    import('../pages/Cocina/Cocina').then(module => ({
        default: module.default
    }))
);

export const Reportes = lazy(() => 
    import('../pages/Reportes/Reportes').then(module => ({
        default: module.default
    }))
);

export const DashboardAnalytics = lazy(() => 
    import('../components/Analytics/DashboardAnalytics').then(module => ({
        default: module.default
    }))
);

// Componentes de formularios con lazy loading
export const CrearPedido = lazy(() => 
    import('../pages/Pedidos/CrearPedido').then(module => ({
        default: module.default
    }))
);

export const DetallePedido = lazy(() => 
    import('../pages/Pedidos/DetallePedido').then(module => ({
        default: module.default
    }))
);

// Componentes de administración
export const Usuarios = lazy(() => 
    import('../pages/Usuarios/Usuarios').then(module => ({
        default: module.default
    }))
);

// Hook personalizado para precargar componentes
export const usePreloadComponent = () => {
    const preloadComponent = (importFunction) => {
        const componentImport = importFunction();
        // Precargar el componente en el fondo
        return componentImport;
    };

    return { preloadComponent };
};

// Configuración de chunks personalizados para webpack
export const chunkNames = {
    dashboard: 'dashboard',
    pedidos: 'pedidos', 
    delivery: 'delivery',
    pagos: 'pagos',
    analytics: 'analytics',
    admin: 'admin',
    reportes: 'reportes'
};

// Utilidad para manejar errores de carga de chunks
export const handleChunkError = (error, errorInfo) => {
    console.error('Error cargando chunk:', error);
    
    // Intentar recargar la página si es un error de chunk
    if (error.name === 'ChunkLoadError') {
        window.location.reload();
    }
};

// Preloader de rutas críticas
export const preloadCriticalRoutes = () => {
    // Precargar Dashboard y Pedidos que son las rutas más utilizadas
    const criticalImports = [
        () => import('../pages/Dashboard/Dashboard'),
        () => import('../pages/Pedidos/Pedidos'),
        () => import('../components/Layout/Layout')
    ];

    // Ejecutar precarga después de que la página principal se haya cargado
    setTimeout(() => {
        criticalImports.forEach(importFn => {
            importFn().catch(err => 
                console.warn('Error precargando ruta crítica:', err)
            );
        });
    }, 2000);
};
