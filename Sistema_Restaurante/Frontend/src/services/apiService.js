import axios from 'axios';
import auditService from './auditService';
import { AUDIT_CONFIG } from '../config/auditConfig';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: AUDIT_CONFIG.api.baseURL,
      timeout: AUDIT_CONFIG.api.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  setupInterceptors() {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        auditService.logError('api_request_failed', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        if (error.response?.status === 401) {
          this.handleUnauthorized();
        }
        auditService.logError('api_response_failed', error);
        return Promise.reject(error);
      }
    );
  }

  getAuthToken() {
    return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
  }

  handleUnauthorized() {
    localStorage.removeItem('authToken');
    sessionStorage.removeItem('authToken');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  // ========== MÉTODOS GENÉRICOS ==========
  async get(endpoint, params = {}) {
    try {
      const response = await this.api.get(endpoint, { params });
      auditService.logAction('api_get_success', { endpoint, params });
      return response.data;
    } catch (error) {
      auditService.logError('api_get_error', error, `GET ${endpoint}`);
      throw error;
    }
  }

  async post(endpoint, data = {}) {
    try {
      const response = await this.api.post(endpoint, data);
      auditService.logAction('api_post_success', { endpoint, dataKeys: Object.keys(data) });
      return response.data;
    } catch (error) {
      auditService.logError('api_post_error', error, `POST ${endpoint}`);
      throw error;
    }
  }

  async put(endpoint, data = {}) {
    try {
      const response = await this.api.put(endpoint, data);
      auditService.logAction('api_put_success', { endpoint, dataKeys: Object.keys(data) });
      return response.data;
    } catch (error) {
      auditService.logError('api_put_error', error, `PUT ${endpoint}`);
      throw error;
    }
  }

  async patch(endpoint, data = {}) {
    try {
      const response = await this.api.patch(endpoint, data);
      auditService.logAction('api_patch_success', { endpoint, dataKeys: Object.keys(data) });
      return response.data;
    } catch (error) {
      auditService.logError('api_patch_error', error, `PATCH ${endpoint}`);
      throw error;
    }
  }

  async delete(endpoint) {
    try {
      const response = await this.api.delete(endpoint);
      auditService.logAction('api_delete_success', { endpoint });
      return response.data;
    } catch (error) {
      auditService.logError('api_delete_error', error, `DELETE ${endpoint}`);
      throw error;
    }
  }

  // ========== AUTENTICACIÓN ==========
  async login(credentials) {
    const response = await this.post('/auth/login/', credentials);
    if (response.token) {
      localStorage.setItem('authToken', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      auditService.logAction('LOGIN_SUCCESS', { userId: response.user.id });
    }
    return response;
  }

  async logout() {
    try {
      await this.post('/auth/logout/');
    } catch (error) {
      console.warn('Logout request failed, but proceeding with local cleanup');
    }
    
    localStorage.removeItem('authToken');
    sessionStorage.removeItem('authToken');
    localStorage.removeItem('user');
    auditService.logAction('LOGOUT', {});
  }

  async register(userData) {
    return await this.post('/auth/register/', userData);
  }

  async refreshToken() {
    const response = await this.post('/auth/refresh/');
    if (response.token) {
      localStorage.setItem('authToken', response.token);
    }
    return response;
  }

  // ========== CLIENTES ==========
  async getClientes(params = {}) {
    return await this.get('/clientes/', params);
  }

  async getCliente(id) {
    return await this.get(`/clientes/${id}/`);
  }

  async createCliente(clienteData) {
    auditService.logAction('CLIENTE_CREATE_ATTEMPT', { rut: clienteData.rut });
    return await this.post('/clientes/', clienteData);
  }

  async updateCliente(id, clienteData) {
    auditService.logAction('CLIENTE_UPDATE_ATTEMPT', { id });
    return await this.put(`/clientes/${id}/`, clienteData);
  }

  async deleteCliente(id) {
    auditService.logAction('CLIENTE_DELETE_ATTEMPT', { id });
    return await this.delete(`/clientes/${id}/`);
  }

  // ========== PEDIDOS ==========
  async getPedidos(params = {}) {
    return await this.get('/pedidos/', params);
  }

  async getPedido(id) {
    return await this.get(`/pedidos/${id}/`);
  }

  async createPedido(pedidoData) {
    auditService.logAction('PEDIDO_CREATE_ATTEMPT', { 
      clienteId: pedidoData.cliente_id,
      total: pedidoData.total 
    });
    return await this.post('/pedidos/', pedidoData);
  }

  async updatePedido(id, pedidoData) {
    auditService.logAction('PEDIDO_UPDATE_ATTEMPT', { id });
    return await this.put(`/pedidos/${id}/`, pedidoData);
  }

  async updateEstadoPedido(id, estado) {
    auditService.logAction('PEDIDO_ESTADO_CHANGE', { id, estado });
    return await this.patch(`/pedidos/${id}/`, { estado });
  }

  async deletePedido(id) {
    auditService.logAction('PEDIDO_DELETE_ATTEMPT', { id });
    return await this.delete(`/pedidos/${id}/`);
  }

  // ========== MESAS ==========
  async getMesas(params = {}) {
    return await this.get('/mesas/', params);
  }

  async getMesa(id) {
    return await this.get(`/mesas/${id}/`);
  }

  async createMesa(mesaData) {
    auditService.logAction('MESA_CREATE_ATTEMPT', { numero: mesaData.numero });
    return await this.post('/mesas/', mesaData);
  }

  async updateMesa(id, mesaData) {
    auditService.logAction('MESA_UPDATE_ATTEMPT', { id });
    return await this.put(`/mesas/${id}/`, mesaData);
  }

  async updateEstadoMesa(id, estado) {
    auditService.logAction('MESA_ESTADO_CHANGE', { id, estado });
    return await this.patch(`/mesas/${id}/`, { estado });
  }

  async deleteMesa(id) {
    auditService.logAction('MESA_DELETE_ATTEMPT', { id });
    return await this.delete(`/mesas/${id}/`);
  }

  // ========== MENÚS ==========
  async getMenus(params = {}) {
    return await this.get('/menus/', params);
  }

  async getMenu(id) {
    return await this.get(`/menus/${id}/`);
  }

  async createMenu(menuData) {
    auditService.logAction('MENU_CREATE_ATTEMPT', { nombre: menuData.nombre });
    return await this.post('/menus/', menuData);
  }

  async updateMenu(id, menuData) {
    auditService.logAction('MENU_UPDATE_ATTEMPT', { id });
    return await this.put(`/menus/${id}/`, menuData);
  }

  async deleteMenu(id) {
    auditService.logAction('MENU_DELETE_ATTEMPT', { id });
    return await this.delete(`/menus/${id}/`);
  }

  // ========== INGREDIENTES ==========
  async getIngredientes(params = {}) {
    return await this.get('/ingredientes/', params);
  }

  async getIngrediente(id) {
    return await this.get(`/ingredientes/${id}/`);
  }

  async createIngrediente(ingredienteData) {
    auditService.logAction('INGREDIENTE_CREATE_ATTEMPT', { nombre: ingredienteData.nombre });
    return await this.post('/ingredientes/', ingredienteData);
  }

  async updateIngrediente(id, ingredienteData) {
    auditService.logAction('INGREDIENTE_UPDATE_ATTEMPT', { id });
    return await this.put(`/ingredientes/${id}/`, ingredienteData);
  }

  async deleteIngrediente(id) {
    auditService.logAction('INGREDIENTE_DELETE_ATTEMPT', { id });
    return await this.delete(`/ingredientes/${id}/`);
  }

  // ========== USUARIOS ==========
  async getUsuarios(params = {}) {
    return await this.get('/usuarios/', params);
  }

  async getUsuario(rut) {
    return await this.get(`/usuarios/${rut}/`);
  }

  async createUsuario(usuarioData) {
    auditService.logAction('USUARIO_CREATE_ATTEMPT', { 
      rut: usuarioData.rut,
      rol: usuarioData.rol 
    });
    return await this.post('/usuarios/', usuarioData);
  }

  async updateUsuario(rut, usuarioData) {
    auditService.logAction('USUARIO_UPDATE_ATTEMPT', { rut });
    return await this.put(`/usuarios/${rut}/`, usuarioData);
  }

  async deleteUsuario(rut) {
    auditService.logAction('USUARIO_DELETE_ATTEMPT', { rut });
    return await this.delete(`/usuarios/${rut}/`);
  }

  // ========== REPORTES ==========
  async getReporteVentas(params = {}) {
    auditService.logAction('REPORTE_VENTAS_REQUEST', params);
    return await this.get('/reportes/ventas/', params);
  }

  async getReporteInventario(params = {}) {
    auditService.logAction('REPORTE_INVENTARIO_REQUEST', params);
    return await this.get('/reportes/inventario/', params);
  }

  async getReporteMesas(params = {}) {
    auditService.logAction('REPORTE_MESAS_REQUEST', params);
    return await this.get('/reportes/mesas/', params);
  }

  async getReporteClientes(params = {}) {
    auditService.logAction('REPORTE_CLIENTES_REQUEST', params);
    return await this.get('/reportes/clientes/', params);
  }

  // ========== DELIVERY ==========
  async createPedidoDelivery(pedidoData) {
    auditService.logAction('DELIVERY_ORDER_CREATE', { 
      plataforma: pedidoData.plataforma,
      total: pedidoData.total 
    });
    return await this.post('/delivery/pedidos/', pedidoData);
  }

  async updateEstadoDelivery(id, estado) {
    auditService.logAction('DELIVERY_ORDER_STATUS_UPDATE', { id, estado });
    return await this.patch(`/delivery/pedidos/${id}/`, { estado });
  }

  // ========== PAGOS ==========
  async procesarPago(pagoData) {
    auditService.logAction('PAYMENT_PROCESS_ATTEMPT', { 
      pedidoId: pagoData.pedido_id,
      metodo: pagoData.metodo_pago,
      monto: pagoData.monto 
    });
    return await this.post('/pagos/', pagoData);
  }

  async getHistorialPagos(params = {}) {
    return await this.get('/pagos/', params);
  }

  // ========== DASHBOARD Y MÉTRICAS ==========
  async getDashboardData() {
    return await this.get('/dashboard/');
  }

  async getMetricasRealTime() {
    return await this.get('/metricas/realtime/');
  }

  // ========== HEALTH CHECK ==========
  async healthCheck() {
    try {
      const response = await this.get('/health/');
      auditService.logAction('HEALTH_CHECK_SUCCESS', response);
      return response;
    } catch (error) {
      auditService.logError('HEALTH_CHECK_FAILED', error);
      throw error;
    }
  }

  // ========== WEBSOCKET CONNECTION ==========
  connectWebSocket(onMessage, onError) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/restaurant/`;
    
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      auditService.logAction('WEBSOCKET_CONNECTED', { url: wsUrl });
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      auditService.logAction('WEBSOCKET_MESSAGE_RECEIVED', { type: data.type });
      if (onMessage) onMessage(data);
    };
    
    ws.onerror = (error) => {
      auditService.logError('WEBSOCKET_ERROR', error);
      if (onError) onError(error);
    };
    
    ws.onclose = () => {
      auditService.logAction('WEBSOCKET_DISCONNECTED', {});
    };
    
    return ws;
  }
}

// Instancia singleton
const apiService = new ApiService();
export default apiService;
