import apiClient from './apiClient';

class PedidoService {
  // Obtener todos los pedidos con filtros
  async obtenerPedidos(filtros = {}) {
    const params = new URLSearchParams();
    
    Object.entries(filtros).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });
    
    const query = params.toString();
    return await apiClient.get(`/pedidos/${query ? `?${query}` : ''}`);
  }

  // Obtener pedido por ID
  async obtenerPedidoPorId(id) {
    return await apiClient.get(`/pedidos/${id}/`);
  }

  // Crear nuevo pedido
  async crearPedido(pedidoData) {
    return await apiClient.post('/pedidos/', pedidoData);
  }

  // Actualizar pedido
  async actualizarPedido(id, pedidoData) {
    return await apiClient.put(`/pedidos/${id}/`, pedidoData);
  }

  // Cambiar estado del pedido
  async cambiarEstadoPedido(id, nuevoEstado, datos = {}) {
    return await apiClient.patch(`/pedidos/${id}/cambiar_estado/`, {
      nuevo_estado: nuevoEstado,
      ...datos
    });
  }

  // Eliminar pedido
  async eliminarPedido(id) {
    return await apiClient.delete(`/pedidos/${id}/`);
  }

  // Obtener pedidos activos
  async obtenerPedidosActivos() {
    return await apiClient.get('/pedidos/activos/');
  }

  // Obtener pedidos para cocina
  async obtenerPedidosCocina() {
    return await apiClient.get('/pedidos/cocina/');
  }

  // Obtener estadísticas de pedidos
  async obtenerEstadisticas(fechaInicio, fechaFin) {
    const params = new URLSearchParams();
    if (fechaInicio) params.append('fecha_inicio', fechaInicio);
    if (fechaFin) params.append('fecha_fin', fechaFin);
    
    return await apiClient.get(`/pedidos/estadisticas/?${params.toString()}`);
  }

  // Obtener historial de cliente
  async obtenerHistorialCliente(clienteId, limite) {
    const params = new URLSearchParams();
    params.append('cliente_id', clienteId);
    if (limite) params.append('limite', limite);
    
    return await apiClient.get(`/pedidos/cliente/?${params.toString()}`);
  }

  // Validar pedido antes de crear
  async validarPedido(pedidoData) {
    return await apiClient.post('/pedidos/validar/', pedidoData);
  }
}

export default new PedidoService();
