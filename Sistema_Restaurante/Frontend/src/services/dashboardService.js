import axios from 'axios';

// Configuración base de axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const dashboardService = {
  // Obtener estadísticas principales del dashboard
  async getStats() {
    try {
      const response = await api.get('/dashboard/stats/');
      return response.data;
    } catch (error) {
      console.error('Error getting dashboard stats:', error);
      // Datos de fallback para desarrollo
      return {
        todayOrders: 45,
        ordersChangePercent: 12,
        todayRevenue: 2850,
        revenueChangePercent: 8,
        occupiedTables: 8,
        totalTables: 15,
        averageServiceTime: 23,
        serviceTimeChange: -2
      };
    }
  },

  // Obtener pedidos recientes
  async getRecentOrders() {
    try {
      const response = await api.get('/dashboard/recent-orders/');
      return response.data;
    } catch (error) {
      console.error('Error getting recent orders:', error);
      // Datos de fallback
      return [
        {
          id: 1,
          mesa: 5,
          items: ['Pizza Margherita', 'Coca Cola'],
          total: 15500,
          estado: 'preparando',
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          mesa: 3,
          items: ['Hamburguesa Clásica', 'Papas Fritas'],
          total: 12000,
          estado: 'entregado',
          timestamp: new Date(Date.now() - 300000).toISOString()
        }
      ];
    }
  },

  // Obtener estado de las mesas
  async getTableStatuses() {
    try {
      const response = await api.get('/dashboard/table-statuses/');
      return response.data;
    } catch (error) {
      console.error('Error getting table statuses:', error);
      // Datos de fallback
      return Array.from({ length: 15 }, (_, i) => ({
        id: i + 1,
        numero: i + 1,
        estado: ['libre', 'ocupada', 'reservada'][Math.floor(Math.random() * 3)],
        comensales: Math.floor(Math.random() * 6) + 1,
        tiempoOcupacion: Math.floor(Math.random() * 120) + 10
      }));
    }
  },

  // Obtener datos para gráfico de pedidos
  async getOrdersChartData(period = '7d') {
    try {
      const response = await api.get(`/dashboard/orders-chart/?period=${period}`);
      return response.data;
    } catch (error) {
      console.error('Error getting orders chart data:', error);
      // Datos de fallback
      const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
      return {
        labels: days,
        datasets: [
          {
            label: 'Pedidos',
            data: days.map(() => Math.floor(Math.random() * 50) + 10),
            borderColor: 'rgb(249, 115, 22)',
            backgroundColor: 'rgba(249, 115, 22, 0.1)',
            tension: 0.4
          }
        ]
      };
    }
  },

  // Obtener datos para gráfico de ingresos
  async getRevenueChartData(period = '7d') {
    try {
      const response = await api.get(`/dashboard/revenue-chart/?period=${period}`);
      return response.data;
    } catch (error) {
      console.error('Error getting revenue chart data:', error);
      // Datos de fallback
      const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
      return {
        labels: days,
        datasets: [
          {
            label: 'Ingresos',
            data: days.map(() => Math.floor(Math.random() * 50000) + 20000),
            borderColor: 'rgb(34, 197, 94)',
            backgroundColor: 'rgba(34, 197, 94, 0.1)',
            tension: 0.4
          }
        ]
      };
    }
  },

  // Obtener alertas del sistema
  async getSystemAlerts() {
    try {
      const response = await api.get('/dashboard/alerts/');
      return response.data;
    } catch (error) {
      console.error('Error getting system alerts:', error);
      return [];
    }
  },

  // Obtener métricas de rendimiento
  async getPerformanceMetrics() {
    try {
      const response = await api.get('/dashboard/performance/');
      return response.data;
    } catch (error) {
      console.error('Error getting performance metrics:', error);
      return {
        responseTime: 145,
        throughput: 98.5,
        errorRate: 0.2,
        uptime: 99.9
      };
    }
  }
};

export default dashboardService;
