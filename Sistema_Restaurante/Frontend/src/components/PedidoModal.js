import React, { useState, useEffect } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { XMarkIcon, PlusIcon, MinusIcon } from '@heroicons/react/24/outline';
import { pedidoService } from '../services/pedidoService';

const PedidoModal = ({ isOpen, onClose, pedido, mode }) => {
  const [formData, setFormData] = useState({
    cliente: null,
    mesa: null,
    items: [],
    observaciones: '',
    descuento: 0,
  });
  
  const queryClient = useQueryClient();

  // Query para obtener datos necesarios
  const { data: clientes } = useQuery({
    queryKey: ['clientes'],
    queryFn: () => fetch('/api/clientes/').then(res => res.json()),
    enabled: isOpen,
  });

  const { data: mesas } = useQuery({
    queryKey: ['mesas'],
    queryFn: () => fetch('/api/mesas/').then(res => res.json()),
    enabled: isOpen,
  });

  const { data: menus } = useQuery({
    queryKey: ['menus'],
    queryFn: () => fetch('/api/menus/').then(res => res.json()),
    enabled: isOpen,
  });

  // Mutations
  const createMutation = useMutation({
    mutationFn: pedidoService.crear,
    onSuccess: () => {
      queryClient.invalidateQueries(['pedidos']);
      onClose();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => pedidoService.actualizar(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['pedidos']);
      onClose();
    },
  });

  useEffect(() => {
    if (pedido && (mode === 'edit' || mode === 'view')) {
      setFormData({
        cliente: pedido.cliente?.id || null,
        mesa: pedido.mesa?.id || null,
        items: pedido.items || [],
        observaciones: pedido.observaciones || '',
        descuento: pedido.descuento || 0,
      });
    } else {
      setFormData({
        cliente: null,
        mesa: null,
        items: [],
        observaciones: '',
        descuento: 0,
      });
    }
  }, [pedido, mode]);

  const handleAddItem = (menu) => {
    const existingItem = formData.items.find(item => item.menu === menu.id);
    if (existingItem) {
      setFormData({
        ...formData,
        items: formData.items.map(item =>
          item.menu === menu.id
            ? { ...item, cantidad: item.cantidad + 1 }
            : item
        ),
      });
    } else {
      setFormData({
        ...formData,
        items: [...formData.items, {
          menu: menu.id,
          menu_nombre: menu.nombre,
          precio_unitario: menu.precio,
          cantidad: 1,
        }],
      });
    }
  };

  const handleRemoveItem = (menuId) => {
    setFormData({
      ...formData,
      items: formData.items.filter(item => item.menu !== menuId),
    });
  };

  const handleUpdateQuantity = (menuId, newQuantity) => {
    if (newQuantity <= 0) {
      handleRemoveItem(menuId);
      return;
    }
    
    setFormData({
      ...formData,
      items: formData.items.map(item =>
        item.menu === menuId
          ? { ...item, cantidad: newQuantity }
          : item
      ),
    });
  };

  const calculateSubtotal = () => {
    return formData.items.reduce((sum, item) => sum + (item.precio_unitario * item.cantidad), 0);
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    return subtotal - formData.descuento;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const submitData = {
      ...formData,
      total: calculateTotal(),
    };

    try {
      if (mode === 'create') {
        await createMutation.mutateAsync(submitData);
      } else if (mode === 'edit') {
        await updateMutation.mutateAsync({ id: pedido.id, data: submitData });
      }
    } catch (error) {
      console.error('Error al guardar pedido:', error);
    }
  };

  const isReadOnly = mode === 'view';

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-4xl sm:p-6">
                <div className="absolute right-0 top-0 hidden pr-4 pt-4 sm:block">
                  <button
                    type="button"
                    className="rounded-md bg-white text-gray-400 hover:text-gray-500"
                    onClick={onClose}
                  >
                    <span className="sr-only">Cerrar</span>
                    <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                  </button>
                </div>
                
                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
                    <Dialog.Title as="h3" className="text-lg font-semibold leading-6 text-gray-900">
                      {mode === 'create' && 'Nuevo Pedido'}
                      {mode === 'edit' && `Editar Pedido #${pedido?.numero_pedido}`}
                      {mode === 'view' && `Pedido #${pedido?.numero_pedido}`}
                    </Dialog.Title>
                    
                    <form onSubmit={handleSubmit} className="mt-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Información básica */}
                        <div className="space-y-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700">
                              Cliente
                            </label>
                            <select
                              value={formData.cliente || ''}
                              onChange={(e) => setFormData({ ...formData, cliente: e.target.value })}
                              disabled={isReadOnly}
                              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
                            >
                              <option value="">Seleccionar cliente</option>
                              {clientes?.map((cliente) => (
                                <option key={cliente.id} value={cliente.id}>
                                  {cliente.nombre} - {cliente.rut}
                                </option>
                              ))}
                            </select>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700">
                              Mesa
                            </label>
                            <select
                              value={formData.mesa || ''}
                              onChange={(e) => setFormData({ ...formData, mesa: e.target.value })}
                              disabled={isReadOnly}
                              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
                            >
                              <option value="">Seleccionar mesa</option>
                              {mesas?.filter(mesa => mesa.estado === 'disponible')?.map((mesa) => (
                                <option key={mesa.id} value={mesa.id}>
                                  Mesa {mesa.numero} - {mesa.capacidad} personas
                                </option>
                              ))}
                            </select>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700">
                              Observaciones
                            </label>
                            <textarea
                              value={formData.observaciones}
                              onChange={(e) => setFormData({ ...formData, observaciones: e.target.value })}
                              disabled={isReadOnly}
                              rows={3}
                              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
                              placeholder="Observaciones del pedido..."
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700">
                              Descuento ($)
                            </label>
                            <input
                              type="number"
                              value={formData.descuento}
                              onChange={(e) => setFormData({ ...formData, descuento: parseFloat(e.target.value) || 0 })}
                              disabled={isReadOnly}
                              min="0"
                              step="0.01"
                              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
                            />
                          </div>
                        </div>

                        {/* Items del pedido */}
                        <div>
                          <h4 className="text-lg font-medium text-gray-900 mb-4">Items del Pedido</h4>
                          
                          {/* Lista de items actuales */}
                          <div className="space-y-2 mb-4 max-h-60 overflow-y-auto">
                            {formData.items.map((item) => (
                              <div key={item.menu} className="flex items-center justify-between bg-gray-50 p-3 rounded-md">
                                <div className="flex-1">
                                  <p className="text-sm font-medium">{item.menu_nombre}</p>
                                  <p className="text-sm text-gray-500">${item.precio_unitario}</p>
                                </div>
                                <div className="flex items-center space-x-2">
                                  {!isReadOnly && (
                                    <button
                                      type="button"
                                      onClick={() => handleUpdateQuantity(item.menu, item.cantidad - 1)}
                                      className="p-1 text-gray-400 hover:text-gray-600"
                                    >
                                      <MinusIcon className="h-4 w-4" />
                                    </button>
                                  )}
                                  <span className="text-sm font-medium w-8 text-center">
                                    {item.cantidad}
                                  </span>
                                  {!isReadOnly && (
                                    <button
                                      type="button"
                                      onClick={() => handleUpdateQuantity(item.menu, item.cantidad + 1)}
                                      className="p-1 text-gray-400 hover:text-gray-600"
                                    >
                                      <PlusIcon className="h-4 w-4" />
                                    </button>
                                  )}
                                </div>
                                <div className="text-sm font-medium w-20 text-right">
                                  ${(item.precio_unitario * item.cantidad).toFixed(2)}
                                </div>
                              </div>
                            ))}
                          </div>

                          {/* Menú para agregar items */}
                          {!isReadOnly && (
                            <div>
                              <h5 className="text-sm font-medium text-gray-700 mb-2">Agregar Items</h5>
                              <div className="space-y-2 max-h-48 overflow-y-auto border rounded-md p-2">
                                {menus?.map((menu) => (
                                  <div key={menu.id} className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                                    <div className="flex-1">
                                      <p className="text-sm font-medium">{menu.nombre}</p>
                                      <p className="text-sm text-gray-500">{menu.descripcion}</p>
                                      <p className="text-sm font-medium text-green-600">${menu.precio}</p>
                                    </div>
                                    <button
                                      type="button"
                                      onClick={() => handleAddItem(menu)}
                                      className="p-1 text-indigo-600 hover:text-indigo-900"
                                    >
                                      <PlusIcon className="h-5 w-5" />
                                    </button>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Total */}
                          <div className="mt-4 pt-4 border-t">
                            <div className="flex justify-between text-sm">
                              <span>Subtotal:</span>
                              <span>${calculateSubtotal().toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span>Descuento:</span>
                              <span>-${formData.descuento.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-lg font-bold">
                              <span>Total:</span>
                              <span>${calculateTotal().toFixed(2)}</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Botones */}
                      <div className="mt-6 flex justify-end space-x-3">
                        <button
                          type="button"
                          onClick={onClose}
                          className="inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                        >
                          {isReadOnly ? 'Cerrar' : 'Cancelar'}
                        </button>
                        {!isReadOnly && (
                          <button
                            type="submit"
                            disabled={createMutation.isLoading || updateMutation.isLoading}
                            className="inline-flex justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 disabled:opacity-50"
                          >
                            {(createMutation.isLoading || updateMutation.isLoading) ? 'Guardando...' : 'Guardar'}
                          </button>
                        )}
                      </div>
                    </form>
                  </div>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
};

export default PedidoModal;
