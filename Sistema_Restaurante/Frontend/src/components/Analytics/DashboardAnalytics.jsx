// Frontend/src/components/Analytics/DashboardAnalytics.jsx
import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

const DashboardAnalytics = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('today');
  const [customDateRange, setCustomDateRange] = useState({
    startDate: '',
    endDate: ''
  });

  useEffect(() => {
    fetchDashboardData();
  }, [selectedPeriod, customDateRange]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      let url = `/api/analytics/dashboard?period=${selectedPeriod}`;
      
      if (selectedPeriod === 'custom' && customDateRange.startDate && customDateRange.endDate) {
        url += `&start_date=${customDateRange.startDate}&end_date=${customDateRange.endDate}`;
      }

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        console.error('Error fetching dashboard data');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePeriodChange = (period) => {
    setSelectedPeriod(period);
  };

  const handleDateRangeChange = (field, value) => {
    setCustomDateRange(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const exportReport = async (format) => {
    try {
      const exportConfig = {
        format: format,
        sections: ['sales', 'inventory', 'operational'],
        start_date: customDateRange.startDate || new Date(Date.now() - 30*24*60*60*1000).toISOString().split('T')[0],
        end_date: customDateRange.endDate || new Date().toISOString().split('T')[0],
        include_charts: true
      };

      const response = await fetch('/api/analytics/export-report', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(exportConfig)
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Reporte ${format} generado exitosamente: ${result.download_url}`);
      }
    } catch (error) {
      console.error('Error exporting report:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center p-8">
        <p className="text-gray-500">No hay datos disponibles</p>
      </div>
    );
  }

  const { ventas, inventario, operacional, clientes, menus_populares, tendencias } = dashboardData;

  // Datos para gráficos
  const ventasPorDiaData = ventas?.ventas_por_dia || [];
  const pedidosPorHoraData = operacional?.pedidos_por_hora || [];
  const metodospagoData = ventas?.metodos_pago_mas_usados || [];
  const menusPopularesData = menus_populares || [];

  // Colores para gráficos
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header con controles */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Dashboard Analítico</h1>
        
        {/* Selector de período */}
        <div className="flex flex-wrap gap-4 mb-4">
          <div className="flex gap-2">
            {['today', 'week', 'month', 'custom'].map(period => (
              <button
                key={period}
                onClick={() => handlePeriodChange(period)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedPeriod === period
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {period === 'today' ? 'Hoy' : 
                 period === 'week' ? 'Esta semana' :
                 period === 'month' ? 'Este mes' : 'Personalizado'}
              </button>
            ))}
          </div>

          {/* Selector de fechas personalizadas */}
          {selectedPeriod === 'custom' && (
            <div className="flex gap-2">
              <input
                type="date"
                value={customDateRange.startDate}
                onChange={(e) => handleDateRangeChange('startDate', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg"
              />
              <input
                type="date"
                value={customDateRange.endDate}
                onChange={(e) => handleDateRangeChange('endDate', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          )}

          {/* Botones de exportación */}
          <div className="flex gap-2">
            <button
              onClick={() => exportReport('pdf')}
              className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
            >
              Exportar PDF
            </button>
            <button
              onClick={() => exportReport('excel')}
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              Exportar Excel
            </button>
          </div>
        </div>
      </div>

      {/* KPIs Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Ventas */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Total Ventas</h3>
          <p className="text-3xl font-bold text-gray-900">${ventas?.total_ventas?.toLocaleString() || 0}</p>
          <p className="text-sm text-green-600 mt-1">
            {tendencias?.crecimiento_ventas > 0 ? '+' : ''}{tendencias?.crecimiento_ventas?.toFixed(1) || 0}% vs período anterior
          </p>
        </div>

        {/* Pedidos */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Total Pedidos</h3>
          <p className="text-3xl font-bold text-gray-900">{ventas?.total_pedidos || 0}</p>
          <p className="text-sm text-blue-600 mt-1">
            {tendencias?.crecimiento_pedidos > 0 ? '+' : ''}{tendencias?.crecimiento_pedidos?.toFixed(1) || 0}% vs período anterior
          </p>
        </div>

        {/* Ticket Promedio */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Ticket Promedio</h3>
          <p className="text-3xl font-bold text-gray-900">${ventas?.ticket_promedio?.toFixed(2) || 0}</p>
        </div>

        {/* Clientes Activos */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Clientes Activos</h3>
          <p className="text-3xl font-bold text-gray-900">{clientes?.clientes_activos || 0}</p>
          <p className="text-sm text-gray-500 mt-1">{clientes?.clientes_nuevos || 0} nuevos</p>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Ventas por día */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Ventas por Día</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={ventasPorDiaData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="fecha" />
              <YAxis />
              <Tooltip formatter={(value) => [`$${value}`, 'Ventas']} />
              <Line type="monotone" dataKey="total" stroke="#0088FE" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Pedidos por hora */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Pedidos por Hora</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={pedidosPorHoraData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hora" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cantidad" fill="#00C49F" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Métodos de pago */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Métodos de Pago Populares</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={metodospagoData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ medio_pago__nombre, percent }) => `${medio_pago__nombre} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="total_transacciones"
              >
                {metodospagoData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Menús populares */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Menús Más Populares</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={menusPopularesData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="nombre" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="total_pedidos" fill="#FFBB28" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tabla de inventario crítico */}
      {inventario?.ingredientes_criticos > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8">
          <h3 className="text-lg font-semibold text-red-600 mb-4">
            ⚠️ Ingredientes Críticos ({inventario.ingredientes_criticos})
          </h3>
          <p className="text-gray-600">
            Hay {inventario.ingredientes_criticos} ingredientes con stock por debajo del nivel crítico.
            <a href="/inventario" className="text-blue-500 hover:underline ml-2">
              Ver detalles →
            </a>
          </p>
        </div>
      )}

      {/* Información adicional */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Operaciones</h3>
          <div className="space-y-2">
            <p className="text-sm text-gray-600">
              Total Mesas: <span className="font-medium">{operacional?.total_mesas || 0}</span>
            </p>
            <p className="text-sm text-gray-600">
              Capacidad Total: <span className="font-medium">{operacional?.capacidad_total || 0}</span>
            </p>
            <p className="text-sm text-gray-600">
              Ocupación Promedio: <span className="font-medium">{operacional?.ocupacion_promedio_mesas?.toFixed(1) || 0}%</span>
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Inventario</h3>
          <div className="space-y-2">
            <p className="text-sm text-gray-600">
              Total Ingredientes: <span className="font-medium">{inventario?.total_ingredientes || 0}</span>
            </p>
            <p className="text-sm text-gray-600">
              Valor Total: <span className="font-medium">${inventario?.valor_total_inventario?.toLocaleString() || 0}</span>
            </p>
            <p className="text-sm text-red-600">
              Stock Crítico: <span className="font-medium">{inventario?.ingredientes_criticos || 0}</span>
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Clientes</h3>
          <div className="space-y-2">
            <p className="text-sm text-gray-600">
              Total Clientes: <span className="font-medium">{clientes?.total_clientes || 0}</span>
            </p>
            <p className="text-sm text-gray-600">
              Clientes Activos: <span className="font-medium">{clientes?.clientes_activos || 0}</span>
            </p>
            <p className="text-sm text-green-600">
              Nuevos: <span className="font-medium">{clientes?.clientes_nuevos || 0}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardAnalytics;
