import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  ChartBarIcon,
  ClockIcon,
  CurrencyDollarIcon,
  ShoppingBagIcon,
  UserGroupIcon,
  TableCellsIcon,
} from '@heroicons/react/24/outline';
import { pedidoService } from '../services/pedidoService';

const Dashboard = () => {
  const [dateRange, setDateRange] = useState('today');

  // Query para estadísticas generales
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats', dateRange],
    queryFn: () => pedidoService.getEstadisticas(),
  });

  // Query para pedidos recientes
  const { data: recentOrders, isLoading: ordersLoading } = useQuery({
    queryKey: ['recent-orders'],
    queryFn: () => pedidoService.obtenerTodos({ limit: 5, ordering: '-fecha_creacion' }),
  });

  const statsCards = [
    {
      name: 'Pedidos Hoy',
      value: stats?.pedidos_hoy || 0,
      icon: ShoppingBagIcon,
      color: 'bg-blue-500',
    },
    {
      name: 'Ventas Hoy',
      value: `$${stats?.ventas_hoy?.toLocaleString() || 0}`,
      icon: CurrencyDollarIcon,
      color: 'bg-green-500',
    },
    {
      name: 'Clientes Activos',
      value: stats?.clientes_activos || 0,
      icon: UserGroupIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'Mesas Ocupadas',
      value: `${stats?.mesas_ocupadas || 0}/${stats?.total_mesas || 0}`,
      icon: TableCellsIcon,
      color: 'bg-orange-500',
    },
    {
      name: 'Tiempo Promedio',
      value: `${stats?.tiempo_promedio || 0} min`,
      icon: ClockIcon,
      color: 'bg-indigo-500',
    },
    {
      name: 'Pedidos Pendientes',
      value: stats?.pedidos_pendientes || 0,
      icon: ChartBarIcon,
      color: 'bg-red-500',
    },
  ];

  const getEstadoBadge = (estado) => {
    const badges = {
      'pendiente': 'bg-yellow-100 text-yellow-800',
      'confirmado': 'bg-blue-100 text-blue-800',
      'preparando': 'bg-orange-100 text-orange-800',
      'listo': 'bg-green-100 text-green-800',
      'entregado': 'bg-gray-100 text-gray-800',
      'cancelado': 'bg-red-100 text-red-800',
    };
    return badges[estado] || 'bg-gray-100 text-gray-800';
  };

  if (statsLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-2">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
          >
            <option value="today">Hoy</option>
            <option value="week">Esta Semana</option>
            <option value="month">Este Mes</option>
          </select>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {statsCards.map((stat) => (
          <div
            key={stat.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6"
          >
            <dt>
              <div className={`absolute rounded-md p-3 ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline">
              <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
            </dd>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pedidos Recientes */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
              Pedidos Recientes
            </h3>
            {ordersLoading ? (
              <div className="animate-pulse space-y-4">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="h-16 bg-gray-200 rounded"></div>
                ))}
              </div>
            ) : (
              <div className="flow-root">
                <ul className="-mb-8">
                  {recentOrders?.results?.map((pedido, idx) => (
                    <li key={pedido.id}>
                      <div className="relative pb-8">
                        {idx !== recentOrders.results.length - 1 && (
                          <span
                            className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                            aria-hidden="true"
                          />
                        )}
                        <div className="relative flex space-x-3">
                          <div>
                            <span className="h-8 w-8 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white">
                              <ShoppingBagIcon
                                className="h-5 w-5 text-white"
                                aria-hidden="true"
                              />
                            </span>
                          </div>
                          <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                            <div>
                              <p className="text-sm text-gray-500">
                                Pedido #{pedido.numero_pedido}{' '}
                                <span className="font-medium text-gray-900">
                                  Mesa {pedido.mesa?.numero || 'N/A'}
                                </span>
                              </p>
                              <span
                                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEstadoBadge(
                                  pedido.estado
                                )}`}
                              >
                                {pedido.estado}
                              </span>
                            </div>
                            <div className="whitespace-nowrap text-right text-sm text-gray-500">
                              <p>${pedido.total}</p>
                              <p>{new Date(pedido.fecha_creacion).toLocaleTimeString()}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* Gráfico de Ventas (placeholder) */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
              Ventas del Día
            </h3>
            <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
              <div className="text-center">
                <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">
                  Gráfico de Ventas
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  Próximamente disponible
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Estado de Cocina */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
            Estado de Cocina
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {stats?.pedidos_preparando || 0}
              </div>
              <div className="text-sm text-gray-500">Preparando</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {stats?.pedidos_listos || 0}
              </div>
              <div className="text-sm text-gray-500">Listos</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {stats?.tiempo_promedio_cocina || 0}min
              </div>
              <div className="text-sm text-gray-500">Tiempo Promedio</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
