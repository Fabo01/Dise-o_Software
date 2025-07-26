// Frontend/src/components/Delivery.js
import React, { useState, useEffect } from 'react';

const Delivery = () => {
    const [pedidosDelivery, setPedidosDelivery] = useState([]);
    const [repartidores, setRepartidores] = useState([]);
    const [filtroEstado, setFiltroEstado] = useState('todos');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const estadosDelivery = [
        { valor: 'todos', etiqueta: 'Todos los Estados' },
        { valor: 'pendiente', etiqueta: 'Pendiente' },
        { valor: 'asignado', etiqueta: 'Asignado' },
        { valor: 'en_preparacion', etiqueta: 'En Preparación' },
        { valor: 'listo', etiqueta: 'Listo para Envío' },
        { valor: 'en_ruta', etiqueta: 'En Ruta' },
        { valor: 'entregado', etiqueta: 'Entregado' },
        { valor: 'fallido', etiqueta: 'Fallido' }
    ];

    useEffect(() => {
        cargarDatos();
    }, [filtroEstado]);

    const cargarDatos = async () => {
        try {
            setLoading(true);
            const [pedidosResponse, repartidoresResponse] = await Promise.all([
                fetch(`/api/delivery/pedidos/?estado=${filtroEstado}`),
                fetch('/api/delivery/repartidores/')
            ]);

            if (!pedidosResponse.ok || !repartidoresResponse.ok) {
                throw new Error('Error al cargar datos de delivery');
            }

            const pedidos = await pedidosResponse.json();
            const repartidoresData = await repartidoresResponse.json();

            setPedidosDelivery(pedidos);
            setRepartidores(repartidoresData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const asignarRepartidor = async (pedidoId, repartidorId) => {
        try {
            const response = await fetch(`/api/delivery/pedidos/${pedidoId}/asignar/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ repartidor_id: repartidorId })
            });

            if (!response.ok) {
                throw new Error('Error al asignar repartidor');
            }

            // Actualizar estado local
            cargarDatos();
        } catch (err) {
            setError(err.message);
        }
    };

    const actualizarEstadoPedido = async (pedidoId, nuevoEstado) => {
        try {
            const response = await fetch(`/api/delivery/pedidos/${pedidoId}/estado/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ estado: nuevoEstado })
            });

            if (!response.ok) {
                throw new Error('Error al actualizar estado');
            }

            cargarDatos();
        } catch (err) {
            setError(err.message);
        }
    };

    const getEstadoColor = (estado) => {
        const colores = {
            'pendiente': 'bg-yellow-100 text-yellow-800',
            'asignado': 'bg-blue-100 text-blue-800',
            'en_preparacion': 'bg-orange-100 text-orange-800',
            'listo': 'bg-green-100 text-green-800',
            'en_ruta': 'bg-purple-100 text-purple-800',
            'entregado': 'bg-gray-100 text-gray-800',
            'fallido': 'bg-red-100 text-red-800'
        };
        return colores[estado] || 'bg-gray-100 text-gray-800';
    };

    const formatearTiempo = (minutos) => {
        if (minutos < 60) {
            return `${minutos} min`;
        }
        const horas = Math.floor(minutos / 60);
        const mins = minutos % 60;
        return `${horas}h ${mins}min`;
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                Error: {error}
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Gestión de Delivery</h1>
                
                {/* Filtros */}
                <div className="flex flex-wrap gap-4 mb-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Estado
                        </label>
                        <select
                            value={filtroEstado}
                            onChange={(e) => setFiltroEstado(e.target.value)}
                            className="border border-gray-300 rounded-md px-3 py-2 bg-white"
                        >
                            {estadosDelivery.map(estado => (
                                <option key={estado.valor} value={estado.valor}>
                                    {estado.etiqueta}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="flex-1"></div>
                    <button
                        onClick={cargarDatos}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Actualizar
                    </button>
                </div>

                {/* Estadísticas rápidas */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                                        <span className="text-white font-bold">P</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            Pendientes
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {pedidosDelivery.filter(p => p.estado === 'pendiente').length}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                                        <span className="text-white font-bold">R</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            En Ruta
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {pedidosDelivery.filter(p => p.estado === 'en_ruta').length}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                                        <span className="text-white font-bold">E</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            Entregados Hoy
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {pedidosDelivery.filter(p => p.estado === 'entregado' && 
                                                new Date(p.fecha_creacion).toDateString() === new Date().toDateString()).length}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                                        <span className="text-white font-bold">A</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            Repartidores Activos
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {repartidores.filter(r => r.activo).length}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Lista de pedidos */}
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                    {pedidosDelivery.length === 0 ? (
                        <li className="p-6 text-center text-gray-500">
                            No hay pedidos de delivery para mostrar
                        </li>
                    ) : (
                        pedidosDelivery.map((pedido) => (
                            <li key={pedido.id} className="p-6 hover:bg-gray-50">
                                <div className="flex items-center justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="text-sm font-medium text-indigo-600 truncate">
                                                    Pedido #{pedido.id}
                                                </p>
                                                <p className="text-sm text-gray-500">
                                                    Cliente: {pedido.cliente_nombre}
                                                </p>
                                                <p className="text-sm text-gray-500">
                                                    Dirección: {pedido.direccion_entrega}
                                                </p>
                                                <p className="text-sm text-gray-500">
                                                    Teléfono: {pedido.telefono_contacto}
                                                </p>
                                            </div>
                                            <div className="flex flex-col items-end">
                                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getEstadoColor(pedido.estado)}`}>
                                                    {pedido.estado.replace('_', ' ').toUpperCase()}
                                                </span>
                                                <p className="text-sm text-gray-500 mt-1">
                                                    Tiempo estimado: {formatearTiempo(pedido.tiempo_estimado_minutos)}
                                                </p>
                                                <p className="text-sm font-medium text-gray-900 mt-1">
                                                    Total: ${pedido.total}
                                                </p>
                                            </div>
                                        </div>
                                        
                                        {/* Información del repartidor */}
                                        {pedido.repartidor && (
                                            <div className="mt-3 p-3 bg-blue-50 rounded-md">
                                                <p className="text-sm text-blue-700">
                                                    <strong>Repartidor:</strong> {pedido.repartidor.nombre}
                                                </p>
                                                <p className="text-sm text-blue-600">
                                                    Teléfono: {pedido.repartidor.telefono}
                                                </p>
                                            </div>
                                        )}

                                        {/* Acciones */}
                                        <div className="mt-4 flex flex-wrap gap-2">
                                            {/* Asignar repartidor */}
                                            {pedido.estado === 'pendiente' && (
                                                <div className="flex items-center gap-2">
                                                    <select
                                                        onChange={(e) => {
                                                            if (e.target.value) {
                                                                asignarRepartidor(pedido.id, e.target.value);
                                                            }
                                                        }}
                                                        className="text-sm border border-gray-300 rounded px-2 py-1"
                                                        defaultValue=""
                                                    >
                                                        <option value="">Asignar repartidor...</option>
                                                        {repartidores.filter(r => r.activo && r.esta_disponible).map(repartidor => (
                                                            <option key={repartidor.id} value={repartidor.id}>
                                                                {repartidor.nombre}
                                                            </option>
                                                        ))}
                                                    </select>
                                                </div>
                                            )}

                                            {/* Cambiar estado */}
                                            {pedido.estado === 'asignado' && (
                                                <button
                                                    onClick={() => actualizarEstadoPedido(pedido.id, 'en_preparacion')}
                                                    className="text-sm bg-orange-500 hover:bg-orange-700 text-white px-3 py-1 rounded"
                                                >
                                                    Marcar en Preparación
                                                </button>
                                            )}

                                            {pedido.estado === 'en_preparacion' && (
                                                <button
                                                    onClick={() => actualizarEstadoPedido(pedido.id, 'listo')}
                                                    className="text-sm bg-green-500 hover:bg-green-700 text-white px-3 py-1 rounded"
                                                >
                                                    Marcar Listo
                                                </button>
                                            )}

                                            {pedido.estado === 'listo' && (
                                                <button
                                                    onClick={() => actualizarEstadoPedido(pedido.id, 'en_ruta')}
                                                    className="text-sm bg-purple-500 hover:bg-purple-700 text-white px-3 py-1 rounded"
                                                >
                                                    Marcar En Ruta
                                                </button>
                                            )}

                                            {pedido.estado === 'en_ruta' && (
                                                <button
                                                    onClick={() => actualizarEstadoPedido(pedido.id, 'entregado')}
                                                    className="text-sm bg-gray-500 hover:bg-gray-700 text-white px-3 py-1 rounded"
                                                >
                                                    Marcar Entregado
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </li>
                        ))
                    )}
                </ul>
            </div>
        </div>
    );
};

export default Delivery;
