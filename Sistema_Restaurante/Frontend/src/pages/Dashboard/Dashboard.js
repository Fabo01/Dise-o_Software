import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  UsersIcon, 
  ShoppingBagIcon, 
  CurrencyDollarIcon,
  TruckIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';
import { useAudit } from '../../hooks/useAudit';

const Dashboard = () => {
  const { user, loginDemo } = useAuth();
  const { logUserAction, logPerformance } = useAudit('Dashboard');
  const [stats, setStats] = useState({
    pedidosHoy: 0,
    ventasHoy: 0,
    clientesActivos: 0,
    mesasOcupadas: 0,
    pedidosPendientes: 0,
    deliveryEnCurso: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const startTime = performance.now();
    
    // Si no hay usuario autenticado, hacer login demo
    if (!user) {
      loginDemo();
    }
    
    // Simular carga de datos del dashboard
    const loadDashboardData = async () => {
      try {
        logUserAction('dashboard_data_load_start');
        
        // Simular llamada a API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Datos simulados
        setStats({
          pedidosHoy: 47,
          ventasHoy: 2840000,
          clientesActivos: 156,
          mesasOcupadas: 12,
          pedidosPendientes: 8,
          deliveryEnCurso: 5
        });
        
        logUserAction('dashboard_data_loaded', {
          loadTime: performance.now() - startTime
        });
        
      } catch (error) {
        logUserAction('dashboard_data_load_error', {
          error: error.message
        });
      } finally {
        setLoading(false);
        
        logPerformance({
          dashboardLoadTime: performance.now() - startTime
        });
      }
    };

    loadDashboardData();
  }, [user, loginDemo, logUserAction, logPerformance]);

  const statsCards = [
    {
      title: 'Pedidos de Hoy',
      value: stats.pedidosHoy,
      icon: ShoppingBagIcon,
      color: 'blue',
      change: '+12%',
      changeType: 'positive'
    },
    {
      title: 'Ventas de Hoy',
      value: `$${stats.ventasHoy.toLocaleString()}`,
      icon: CurrencyDollarIcon,
      color: 'green',
      change: '+8%',
      changeType: 'positive'
    },
    {
      title: 'Clientes Activos',
      value: stats.clientesActivos,
      icon: UsersIcon,
      color: 'purple',
      change: '+24%',
      changeType: 'positive'
    },
    {
      title: 'Mesas Ocupadas',
      value: `${stats.mesasOcupadas}/20`,
      icon: ChartBarIcon,
      color: 'orange',
      change: '60%',
      changeType: 'neutral'
    },
    {
      title: 'Pedidos Pendientes',
      value: stats.pedidosPendientes,
      icon: ClockIcon,
      color: 'red',
      change: '-3',
      changeType: 'negative'
    },
    {
      title: 'Delivery en Curso',
      value: stats.deliveryEnCurso,
      icon: TruckIcon,
      color: 'indigo',
      change: '+2',
      changeType: 'positive'
    }
  ];

  const recentActivities = [
    { id: 1, type: 'pedido', message: 'Nuevo pedido #1234 - Mesa 5', time: '2 min ago', status: 'new' },
    { id: 2, type: 'pago', message: 'Pago completado - Mesa 3 ($45.000)', time: '5 min ago', status: 'success' },
    { id: 3, type: 'delivery', message: 'Delivery #567 entregado', time: '8 min ago', status: 'success' },
    { id: 4, type: 'alerta', message: 'Stock bajo: Ingrediente Tomates', time: '15 min ago', status: 'warning' },
    { id: 5, type: 'usuario', message: 'Nuevo cliente registrado: María García', time: '20 min ago', status: 'info' }
  ];

  const handleCardClick = (card) => {
    logUserAction('dashboard_card_click', {
      cardTitle: card.title,
      cardValue: card.value
    });
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-50 text-blue-700 border-blue-200',
      green: 'bg-green-50 text-green-700 border-green-200',
      purple: 'bg-purple-50 text-purple-700 border-purple-200',
      orange: 'bg-orange-50 text-orange-700 border-orange-200',
      red: 'bg-red-50 text-red-700 border-red-200',
      indigo: 'bg-indigo-50 text-indigo-700 border-indigo-200'
    };
    return colors[color] || colors.blue;
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'warning':
        return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      case 'new':
        return <ClockIcon className="h-5 w-5 text-blue-500" />;
      default:
        return <ChartBarIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header del Dashboard */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">
          Bienvenido de vuelta, {user?.name || 'Usuario'}. Aquí tienes un resumen de hoy.
        </p>
      </div>

      {/* Tarjetas de Estadísticas */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {statsCards.map((card, index) => (
          <div
            key={index}
            onClick={() => handleCardClick(card)}
            className={`relative overflow-hidden rounded-lg border p-6 cursor-pointer transition-all duration-200 hover:shadow-lg hover:scale-105 ${getColorClasses(card.color)}`}
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <card.icon className="h-8 w-8" aria-hidden="true" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium truncate opacity-75">
                    {card.title}
                  </dt>
                  <dd className="text-3xl font-bold">
                    {card.value}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="absolute bottom-4 right-4">
              <span className={`text-sm font-medium ${
                card.changeType === 'positive' ? 'text-green-600' :
                card.changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
              }`}>
                {card.change}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Sección de Actividad Reciente */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Actividad Reciente</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {recentActivities.map((activity) => (
            <div key={activity.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(activity.status)}
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {activity.message}
                    </p>
                    <p className="text-sm text-gray-500">
                      {activity.time}
                    </p>
                  </div>
                </div>
                <div className="flex-shrink-0">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    activity.status === 'success' ? 'bg-green-100 text-green-800' :
                    activity.status === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                    activity.status === 'new' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {activity.type}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Acciones Rápidas */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Acciones Rápidas</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { name: 'Nuevo Pedido', href: '/pedidos/crear', color: 'blue' },
            { name: 'Ver Cocina', href: '/cocina', color: 'green' },
            { name: 'Gestionar Mesas', href: '/mesas', color: 'purple' },
            { name: 'Ver Reportes', href: '/reportes', color: 'orange' }
          ].map((action) => (
            <button
              key={action.name}
              onClick={() => {
                logUserAction('quick_action_click', { action: action.name });
                // Aquí iría la navegación
              }}
              className={`relative group p-4 border border-gray-300 rounded-lg hover:border-blue-500 hover:shadow-md transition-all duration-200`}
            >
              <div className="text-center">
                <h4 className="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                  {action.name}
                </h4>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
