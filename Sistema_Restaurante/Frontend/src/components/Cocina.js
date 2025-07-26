import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  FireIcon,
} from '@heroicons/react/24/outline';
import { pedidoService } from '../services/pedidoService';

const Cocina = () => {
  const [filter, setFilter] = useState('preparando');
  const queryClient = useQueryClient();

  // Query para obtener pedidos de cocina
  const { data: pedidos, isLoading } = useQuery({
    queryKey: ['pedidos-cocina', filter],
    queryFn: () => pedidoService.obtenerTodos({
      estado__in: filter === 'all' ? 'confirmado,preparando,listo' : filter,
      ordering: 'fecha_creacion',
    }),
    refetchInterval: 30000, // Refrescar cada 30 segundos
  });

  // Mutation para cambiar estado de pedido
  const changeStateMutation = useMutation({
    mutationFn: ({ id, estado }) => pedidoService.cambiarEstado(id, estado),
    onSuccess: () => {
      queryClient.invalidateQueries(['pedidos-cocina']);
    },
  });

  const handleStateChange = async (pedidoId, newState) => {
    try {
      await changeStateMutation.mutateAsync({ id: pedidoId, estado: newState });
    } catch (error) {
      console.error('Error al cambiar estado:', error);
    }
  };

  const getEstadoColor = (estado) => {
    switch (estado) {
      case 'confirmado':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'preparando':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'listo':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getPriorityColor = (tiempoTranscurrido) => {
    if (tiempoTranscurrido > 30) return 'text-red-600';
    if (tiempoTranscurrido > 20) return 'text-orange-600';
    return 'text-green-600';
  };

  const calculateTiempoTranscurrido = (fechaCreacion) => {
    const now = new Date();
    const created = new Date(fechaCreacion);
    const diffMinutes = Math.floor((now - created) / (1000 * 60));
    return diffMinutes;
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-orange-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Vista de Cocina</h1>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <FireIcon className="h-5 w-5 text-orange-500" />
            <span className="text-sm text-gray-600">Actualización automática</span>
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="block rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-orange-500 focus:outline-none focus:ring-orange-500"
          >
            <option value="confirmado">Por Preparar</option>
            <option value="preparando">En Preparación</option>
            <option value="listo">Listos</option>
            <option value="all">Todos</option>
          </select>
        </div>
      </div>

      {/* Estadísticas rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="flex items-center">
            <ClockIcon className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-blue-600">Por Preparar</p>
              <p className="text-2xl font-bold text-blue-900">
                {pedidos?.results?.filter(p => p.estado === 'confirmado').length || 0}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-orange-50 rounded-lg p-4">
          <div className="flex items-center">
            <FireIcon className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-orange-600">En Preparación</p>
              <p className="text-2xl font-bold text-orange-900">
                {pedidos?.results?.filter(p => p.estado === 'preparando').length || 0}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4">
          <div className="flex items-center">
            <CheckCircleIcon className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-green-600">Listos</p>
              <p className="text-2xl font-bold text-green-900">
                {pedidos?.results?.filter(p => p.estado === 'listo').length || 0}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <ClockIcon className="h-8 w-8 text-gray-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Tiempo Promedio</p>
              <p className="text-2xl font-bold text-gray-900">25 min</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tickets de Cocina */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {pedidos?.results?.map((pedido) => {
          const tiempoTranscurrido = calculateTiempoTranscurrido(pedido.fecha_creacion);
          
          return (
            <div
              key={pedido.id}
              className={`bg-white rounded-lg shadow-md border-l-4 ${
                pedido.estado === 'confirmado' ? 'border-blue-500' :
                pedido.estado === 'preparando' ? 'border-orange-500' :
                'border-green-500'
              } p-4 hover:shadow-lg transition-shadow`}
            >
              {/* Header del ticket */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-gray-900">
                    #{pedido.numero_pedido}
                  </span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium border ${getEstadoColor(
                      pedido.estado
                    )}`}
                  >
                    {pedido.estado}
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">Mesa</p>
                  <p className="text-lg font-bold text-gray-900">
                    {pedido.mesa?.numero || 'N/A'}
                  </p>
                </div>
              </div>

              {/* Tiempo transcurrido */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-1">
                  <ClockIcon className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-500">Tiempo:</span>
                </div>
                <span className={`text-sm font-medium ${getPriorityColor(tiempoTranscurrido)}`}>
                  {tiempoTranscurrido} min
                </span>
              </div>

              {/* Items del pedido */}
              <div className="space-y-2 mb-4">
                <h4 className="text-sm font-medium text-gray-700">Items:</h4>
                <div className="space-y-1">
                  {pedido.items?.map((item, index) => (
                    <div key={index} className="flex justify-between text-sm">
                      <span className="flex-1">
                        {item.cantidad}x {item.menu_nombre}
                      </span>
                      {item.observaciones && (
                        <span className="text-xs text-gray-500 italic ml-2">
                          {item.observaciones}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Observaciones */}
              {pedido.observaciones && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Observaciones:</h4>
                  <p className="text-sm text-gray-600 bg-yellow-50 p-2 rounded">
                    {pedido.observaciones}
                  </p>
                </div>
              )}

              {/* Botones de acción */}
              <div className="flex space-x-2">
                {pedido.estado === 'confirmado' && (
                  <button
                    onClick={() => handleStateChange(pedido.id, 'preparando')}
                    disabled={changeStateMutation.isLoading}
                    className="flex-1 bg-orange-600 hover:bg-orange-700 text-white text-sm font-medium py-2 px-3 rounded-md transition-colors disabled:opacity-50"
                  >
                    Iniciar Preparación
                  </button>
                )}
                
                {pedido.estado === 'preparando' && (
                  <button
                    onClick={() => handleStateChange(pedido.id, 'listo')}
                    disabled={changeStateMutation.isLoading}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white text-sm font-medium py-2 px-3 rounded-md transition-colors disabled:opacity-50"
                  >
                    Marcar Listo
                  </button>
                )}
                
                {pedido.estado === 'listo' && (
                  <div className="flex-1 bg-gray-100 text-gray-700 text-sm font-medium py-2 px-3 rounded-md text-center">
                    Esperando Entrega
                  </div>
                )}
                
                {/* Botón de cancelar (siempre disponible) */}
                <button
                  onClick={() => handleStateChange(pedido.id, 'cancelado')}
                  disabled={changeStateMutation.isLoading}
                  className="px-3 py-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md transition-colors"
                  title="Cancelar pedido"
                >
                  <XCircleIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Mensaje cuando no hay pedidos */}
      {(!pedidos?.results || pedidos.results.length === 0) && (
        <div className="text-center py-12">
          <FireIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No hay pedidos</h3>
          <p className="mt-1 text-sm text-gray-500">
            No hay pedidos en {filter === 'all' ? 'cocina' : `estado "${filter}"`} en este momento.
          </p>
        </div>
      )}
    </div>
  );
};

export default Cocina;
