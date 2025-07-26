import { useEffect, useCallback, useRef } from 'react';
import auditService from '../services/auditService';

/**
 * Hook personalizado para integrar auditoría en componentes React
 * Proporciona funciones para logear acciones, errores y métricas de rendimiento
 */
export const useAudit = (componentName) => {
  const mountTimeRef = useRef(null);
  const renderCountRef = useRef(0);
  const interactionCountRef = useRef(0);

  useEffect(() => {
    mountTimeRef.current = performance.now();
    
    // Log del montaje del componente
    auditService.logAction('component_mount', {
      component: componentName,
      timestamp: new Date().toISOString()
    });

    // Cleanup al desmontaje
    return () => {
      const unmountTime = performance.now();
      const mountDuration = mountTime ? unmountTime - mountTimeRef.current : 0;
      
      auditService.logAction('component_unmount', {
        component: componentName,
        mountDuration,
        renderCount: renderCountRef.current,
        interactionCount: interactionCountRef.current,
        timestamp: new Date().toISOString()
      });
    };
  }, [componentName]);

  // Incrementar contador de renders
  useEffect(() => {
    renderCountRef.current += 1;
    
    if (renderCountRef.current > 1) {
      auditService.logAction('component_rerender', {
        component: componentName,
        renderCount: renderCountRef.current
      });
    }
  });

  /**
   * Logea una acción del usuario en el componente
   */
  const logUserAction = useCallback((action, details = {}) => {
    interactionCountRef.current += 1;
    
    auditService.logAction('user_interaction', {
      component: componentName,
      action,
      interactionCount: interactionCountRef.current,
      ...details
    });
  }, [componentName]);

  /**
   * Logea un error en el componente
   */
  const logError = useCallback((error, context = {}) => {
    auditService.logError('component_error', error, componentName);
    
    // Log adicional con contexto del componente
    auditService.logAction('component_error_context', {
      component: componentName,
      renderCount: renderCountRef.current,
      interactionCount: interactionCountRef.current,
      ...context
    });
  }, [componentName]);

  /**
   * Logea métricas de rendimiento del componente
   */
  const logPerformance = useCallback((metrics = {}) => {
    const currentTime = performance.now();
    const mountDuration = mountTimeRef.current ? currentTime - mountTimeRef.current : 0;
    
    auditService.logAction('component_performance', {
      component: componentName,
      mountDuration,
      renderCount: renderCountRef.current,
      interactionCount: interactionCountRef.current,
      ...metrics
    });
  }, [componentName]);

  /**
   * Logea el tiempo de una operación específica
   */
  const timeOperation = useCallback((operationName, operation) => {
    return async (...args) => {
      const startTime = performance.now();
      
      try {
        const result = await operation(...args);
        const duration = performance.now() - startTime;
        
        auditService.logAction('operation_completed', {
          component: componentName,
          operation: operationName,
          duration,
          success: true
        });
        
        return result;
      } catch (error) {
        const duration = performance.now() - startTime;
        
        auditService.logError('operation_failed', error, componentName);
        auditService.logAction('operation_completed', {
          component: componentName,
          operation: operationName,
          duration,
          success: false,
          error: error.message
        });
        
        throw error;
      }
    };
  }, [componentName]);

  /**
   * Wrapper para funciones que deben ser auditadas
   */
  const withAudit = useCallback((functionName, fn) => {
    return (...args) => {
      logUserAction(functionName, { 
        args: args.length,
        timestamp: new Date().toISOString()
      });
      
      try {
        return fn(...args);
      } catch (error) {
        logError(error, { 
          function: functionName,
          args: args.length 
        });
        throw error;
      }
    };
  }, [logUserAction, logError]);

  return {
    logUserAction,
    logError,
    logPerformance,
    timeOperation,
    withAudit,
    // Métricas actuales del componente
    metrics: {
      renderCount: renderCountRef.current,
      interactionCount: interactionCountRef.current,
      mountTime: mountTimeRef.current
    }
  };
};

/**
 * Hook para monitorear el rendimiento de formularios
 */
export const useFormAudit = (formName) => {
  const { logUserAction, logError, logPerformance } = useAudit(`Form_${formName}`);
  const fieldInteractions = useRef({});
  const formStartTime = useRef(null);

  const trackFieldInteraction = useCallback((fieldName, interactionType) => {
    if (!fieldInteractions.current[fieldName]) {
      fieldInteractions.current[fieldName] = [];
    }
    
    fieldInteractions.current[fieldName].push({
      type: interactionType,
      timestamp: new Date().toISOString()
    });
    
    logUserAction('field_interaction', {
      field: fieldName,
      interactionType,
      totalInteractions: fieldInteractions.current[fieldName].length
    });
  }, [logUserAction]);

  const startForm = useCallback(() => {
    formStartTime.current = performance.now();
    logUserAction('form_started');
  }, [logUserAction]);

  const submitForm = useCallback((data, isSuccess = true) => {
    const duration = formStartTime.current ? 
      performance.now() - formStartTime.current : 0;
    
    const totalInteractions = Object.values(fieldInteractions.current)
      .reduce((sum, interactions) => sum + interactions.length, 0);
    
    logUserAction('form_submitted', {
      duration,
      totalInteractions,
      fieldsInteracted: Object.keys(fieldInteractions.current).length,
      success: isSuccess,
      dataFields: Object.keys(data || {}).length
    });
    
    logPerformance({
      formCompletionTime: duration,
      fieldInteractions: totalInteractions
    });
  }, [logUserAction, logPerformance]);

  return {
    trackFieldInteraction,
    startForm,
    submitForm,
    logError
  };
};

/**
 * Hook para monitorear APIs
 */
export const useApiAudit = (apiName) => {
  const { logUserAction, logError, timeOperation } = useAudit(`API_${apiName}`);

  const trackApiCall = useCallback((endpoint, method = 'GET') => {
    return timeOperation(`${method}_${endpoint}`, async (data) => {
      logUserAction('api_call_initiated', {
        endpoint,
        method,
        hasData: !!data
      });
      
      // Aquí iría la llamada real a la API
      // Por ahora retornamos una promesa simulada
      return new Promise((resolve) => {
        setTimeout(() => resolve({ success: true }), 100);
      });
    });
  }, [timeOperation, logUserAction]);

  return {
    trackApiCall,
    logError
  };
};

/**
 * Hook para monitorear navegación
 */
export const useNavigationAudit = () => {
  const { logUserAction } = useAudit('Navigation');

  useEffect(() => {
    const handleRouteChange = () => {
      logUserAction('route_changed', {
        path: window.location.pathname,
        search: window.location.search,
        timestamp: new Date().toISOString()
      });
    };

    // Escuchar cambios de ruta
    window.addEventListener('popstate', handleRouteChange);
    
    // Log de ruta inicial
    handleRouteChange();

    return () => {
      window.removeEventListener('popstate', handleRouteChange);
    };
  }, [logUserAction]);

  const trackNavigation = useCallback((destination, method = 'click') => {
    logUserAction('navigation_initiated', {
      destination,
      method,
      from: window.location.pathname
    });
  }, [logUserAction]);

  return { trackNavigation };
};

export default useAudit;
