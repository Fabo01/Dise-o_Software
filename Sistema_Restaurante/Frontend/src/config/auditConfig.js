// Configuración de auditoría avanzada para el sistema de restaurante
export const AUDIT_CONFIG = {
  // Configuración de logging
  logging: {
    level: process.env.NODE_ENV === 'production' ? 'warn' : 'debug',
    maxLogs: 1000,
    enablePerformanceMetrics: true,
    enableUserActions: true,
    enableAPIRequests: true,
    enableErrors: true,
    enableSecurityEvents: true
  },
  
  // Configuración de API
  api: {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
    timeout: 30000,
    retries: 3,
    enableRequestInterception: true,
    enableResponseInterception: true
  },
  
  // Configuración de performance
  performance: {
    enableWebVitals: true,
    enableResourceTiming: true,
    enableNavigationTiming: true,
    thresholds: {
      LCP: 2500, // Largest Contentful Paint
      FID: 100,  // First Input Delay
      CLS: 0.1,  // Cumulative Layout Shift
      FCP: 1800, // First Contentful Paint
      TTFB: 600  // Time to First Byte
    }
  },
  
  // Configuración de seguridad
  security: {
    enableCSPReporting: true,
    enableXSSDetection: true,
    maxFailedLoginAttempts: 5,
    sessionTimeout: 30 * 60 * 1000, // 30 minutos
    enableTokenValidation: true
  },
  
  // Configuración de monitoreo de componentes
  components: {
    enableRenderTracking: true,
    enableStateChanges: true,
    enableErrorBoundaries: true,
    maxRenderTime: 16, // 60fps
    enableMemoryTracking: true
  },
  
  // Configuración de testing
  testing: {
    enableE2E: true,
    enableUnitTests: true,
    enableIntegrationTests: true,
    enableVisualRegression: false,
    enableAccessibilityTests: true
  },

  // Roles de usuario para auditoría
  userRoles: {
    JEFE_LOCAL: 'jefe_local',
    JEFE_TURNO: 'jefe_turno', 
    MESERO: 'mesero',
    COCINA: 'cocina'
  },

  // Eventos de auditoría críticos
  criticalEvents: [
    'LOGIN_ATTEMPT',
    'LOGIN_SUCCESS',
    'LOGIN_FAILURE',
    'LOGOUT',
    'PASSWORD_CHANGE',
    'PERMISSION_DENIED',
    'DATA_EXPORT',
    'DATA_DELETE',
    'SYSTEM_ERROR',
    'PAYMENT_PROCESSED',
    'ORDER_CANCELLED',
    'INVENTORY_CRITICAL'
  ]
};

export default AUDIT_CONFIG;
