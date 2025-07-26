import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  PlusIcon,
  MagnifyingGlassIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  PrinterIcon,
} from '@heroicons/react/24/outline';
import { pedidoService } from '../services/pedidoService';
import PedidoModal from './PedidoModal';

const PedidosList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [showModal, setShowModal] = useState(false);
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [modalMode, setModalMode] = useState('create'); // 'create', 'view', 'edit'
  
  const queryClient = useQueryClient();

  // Query para obtener pedidos
  const { data: pedidos, isLoading, error } = useQuery({
    queryKey: ['pedidos', currentPage, searchTerm, statusFilter],
    queryFn: () => pedidoService.obtenerTodos({
      page: currentPage,
      search: searchTerm,
      estado: statusFilter,
      page_size: 10,
    }),
    keepPreviousData: true,
  });

  // Mutation para eliminar pedido
  const deleteMutation = useMutation({
    mutationFn: pedidoService.eliminar,
    onSuccess: () => {
      queryClient.invalidateQueries(['pedidos']);
    },
  });

  // Mutation para cambiar estado
  const changeStateMutation = useMutation({
    mutationFn: ({ id, estado }) => pedidoService.cambiarEstado(id, estado),
    onSuccess: () => {
      queryClient.invalidateQueries(['pedidos']);
    },
  });

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

  const handleCreate = () => {
    setSelectedPedido(null);
    setModalMode('create');
    setShowModal(true);
  };

  const handleView = (pedido) => {
    setSelectedPedido(pedido);
    setModalMode('view');
    setShowModal(true);
  };

  const handleEdit = (pedido) => {
    setSelectedPedido(pedido);
    setModalMode('edit');
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este pedido?')) {
      try {
        await deleteMutation.mutateAsync(id);
      } catch (error) {
        console.error('Error al eliminar pedido:', error);
      }
    }
  };

  const handleChangeState = async (id, newState) => {
    try {
      await changeStateMutation.mutateAsync({ id, estado: newState });
    } catch (error) {
      console.error('Error al cambiar estado:', error);
    }
  };

  const handlePrint = (pedido) => {
    // Implementar impresión de ticket
    window.print();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center">
        <div className="text-red-600">Error al cargar los pedidos</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Gestión de Pedidos</h1>
        <button
          onClick={handleCreate}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Nuevo Pedido
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Buscar
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Buscar por número de pedido, cliente..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Estado
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="">Todos los estados</option>
              <option value="pendiente">Pendiente</option>
              <option value="confirmado">Confirmado</option>
              <option value="preparando">Preparando</option>
              <option value="listo">Listo</option>
              <option value="entregado">Entregado</option>
              <option value="cancelado">Cancelado</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('');
                setCurrentPage(1);
              }}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Limpiar Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Lista de Pedidos */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {pedidos?.results?.map((pedido) => (
            <li key={pedido.id}>
              <div className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center space-x-3">
                        <p className="text-sm font-medium text-indigo-600 truncate">
                          Pedido #{pedido.numero_pedido}
                        </p>
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEstadoBadge(
                            pedido.estado
                          )}`}
                        >
                          {pedido.estado}
                        </span>
                      </div>
                      <div className="mt-2 flex items-center text-sm text-gray-500">
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
                          <div>
                            <span className="font-medium">Cliente:</span>{' '}
                            {pedido.cliente?.nombre || 'N/A'}
                          </div>
                          <div>
                            <span className="font-medium">Mesa:</span>{' '}
                            {pedido.mesa?.numero || 'N/A'}
                          </div>
                          <div>
                            <span className="font-medium">Total:</span> ${pedido.total}
                          </div>
                          <div>
                            <span className="font-medium">Fecha:</span>{' '}
                            {new Date(pedido.fecha_creacion).toLocaleDateString()}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {/* Cambio de estado rápido */}
                    {pedido.estado === 'pendiente' && (
                      <button
                        onClick={() => handleChangeState(pedido.id, 'confirmado')}
                        className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-blue-600 hover:bg-blue-700"
                      >
                        Confirmar
                      </button>
                    )}
                    {pedido.estado === 'confirmado' && (
                      <button
                        onClick={() => handleChangeState(pedido.id, 'preparando')}
                        className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-orange-600 hover:bg-orange-700"
                      >
                        Preparar
                      </button>
                    )}
                    {pedido.estado === 'preparando' && (
                      <button
                        onClick={() => handleChangeState(pedido.id, 'listo')}
                        className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-green-600 hover:bg-green-700"
                      >
                        Marcar Listo
                      </button>
                    )}
                    {pedido.estado === 'listo' && (
                      <button
                        onClick={() => handleChangeState(pedido.id, 'entregado')}
                        className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-gray-600 hover:bg-gray-700"
                      >
                        Entregar
                      </button>
                    )}
                    
                    {/* Botones de acción */}
                    <button
                      onClick={() => handleView(pedido)}
                      className="p-1 text-gray-400 hover:text-gray-500"
                      title="Ver detalles"
                    >
                      <EyeIcon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleEdit(pedido)}
                      className="p-1 text-indigo-600 hover:text-indigo-900"
                      title="Editar"
                    >
                      <PencilIcon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handlePrint(pedido)}
                      className="p-1 text-green-600 hover:text-green-900"
                      title="Imprimir"
                    >
                      <PrinterIcon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(pedido.id)}
                      className="p-1 text-red-600 hover:text-red-900"
                      title="Eliminar"
                    >
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Paginación */}
      {pedidos?.count > 10 && (
        <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
          <div className="flex-1 flex justify-between sm:hidden">
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={!pedidos.previous}
              className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Anterior
            </button>
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={!pedidos.next}
              className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Siguiente
            </button>
          </div>
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Mostrando{' '}
                <span className="font-medium">
                  {(currentPage - 1) * 10 + 1}
                </span>{' '}
                a{' '}
                <span className="font-medium">
                  {Math.min(currentPage * 10, pedidos.count)}
                </span>{' '}
                de <span className="font-medium">{pedidos.count}</span> resultados
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  onClick={() => setCurrentPage(currentPage - 1)}
                  disabled={!pedidos.previous}
                  className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  Anterior
                </button>
                <button
                  onClick={() => setCurrentPage(currentPage + 1)}
                  disabled={!pedidos.next}
                  className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  Siguiente
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <PedidoModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          pedido={selectedPedido}
          mode={modalMode}
        />
      )}
    </div>
  );
};

export default PedidosList;
