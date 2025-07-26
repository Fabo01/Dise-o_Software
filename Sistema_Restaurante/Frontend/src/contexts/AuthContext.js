import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '../services/apiService';
import auditService from '../services/auditService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        // Configurar el token en el servicio API
        apiService.setAuthToken(token);
        
        // Verificar el token con el backend
        const userData = await apiService.get('/auth/me/');
        setUser(userData);
        setIsAuthenticated(true);
        
        // Log del usuario autenticado
        auditService.logAction('user_authenticated', {
          userId: userData.id,
          email: userData.email,
          timestamp: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('Error verificando autenticación:', error);
      localStorage.removeItem('auth_token');
      apiService.setAuthToken(null);
      
      auditService.logError('auth_verification_failed', error, 'AuthContext');
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      
      // Intentar login con el backend
      const response = await apiService.post('/auth/login/', credentials);
      const { access, refresh, user: userData } = response;
      
      // Guardar tokens
      localStorage.setItem('auth_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // Configurar el token en el servicio API
      apiService.setAuthToken(access);
      
      // Actualizar estado
      setUser(userData);
      setIsAuthenticated(true);
      
      // Log del login exitoso
      auditService.logAction('user_login_success', {
        userId: userData.id,
        email: userData.email,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
      });
      
      return { success: true, user: userData };
    } catch (error) {
      // Log del error de login
      auditService.logError('user_login_failed', error, 'AuthContext');
      auditService.logAction('user_login_attempt', {
        email: credentials.email,
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      });
      
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Error de autenticación' 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Log del logout
      auditService.logAction('user_logout', {
        userId: user?.id,
        email: user?.email,
        timestamp: new Date().toISOString()
      });
      
      // Intentar logout en el backend
      try {
        await apiService.post('/auth/logout/');
      } catch (error) {
        // No es crítico si el logout del backend falla
        console.warn('Error en logout del backend:', error);
      }
      
      // Limpiar estado local
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      apiService.setAuthToken(null);
      
      setUser(null);
      setIsAuthenticated(false);
      
    } catch (error) {
      auditService.logError('logout_error', error, 'AuthContext');
    }
  };

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) {
        throw new Error('No refresh token available');
      }
      
      const response = await apiService.post('/auth/refresh/', { refresh });
      const { access } = response;
      
      localStorage.setItem('auth_token', access);
      apiService.setAuthToken(access);
      
      auditService.logAction('token_refreshed', {
        userId: user?.id,
        timestamp: new Date().toISOString()
      });
      
      return access;
    } catch (error) {
      auditService.logError('token_refresh_failed', error, 'AuthContext');
      // Si falla el refresh, hacer logout
      logout();
      throw error;
    }
  };

  const updateUser = (updatedUserData) => {
    setUser(updatedUserData);
    auditService.logAction('user_profile_updated', {
      userId: updatedUserData.id,
      timestamp: new Date().toISOString()
    });
  };

  // Verificar permisos del usuario
  const hasPermission = (permission) => {
    if (!user || !user.permissions) return false;
    return user.permissions.includes(permission) || user.is_superuser;
  };

  const hasRole = (role) => {
    if (!user || !user.roles) return false;
    return user.roles.includes(role) || user.is_superuser;
  };

  // Función de login simulado para desarrollo
  const loginDemo = () => {
    const demoUser = {
      id: 1,
      email: 'admin@restaurante.com',
      name: 'Administrador',
      is_superuser: true,
      permissions: ['all'],
      roles: ['admin']
    };
    
    setUser(demoUser);
    setIsAuthenticated(true);
    
    auditService.logAction('demo_login', {
      userId: demoUser.id,
      email: demoUser.email,
      timestamp: new Date().toISOString()
    });
    
    return { success: true, user: demoUser };
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    refreshToken,
    updateUser,
    hasPermission,
    hasRole,
    checkAuthStatus,
    loginDemo
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
