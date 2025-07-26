// Frontend/src/components/Pagos.js
import React, { useState, useEffect } from 'react';

const Pagos = () => {
    const [pedidosPendientes, setPedidosPendientes] = useState([]);
    const [transacciones, setTransacciones] = useState([]);
    const [mediosPago, setMediosPago] = useState([]);
    const [pedidoSeleccionado, setPedidoSeleccionado] = useState(null);
    const [pagoEnProceso, setPagoEnProceso] = useState(false);
    const [pagoActual, setPagoActual] = useState({
        medio_pago_id: '',
        monto: '',
        referencia: '',
        dividir_pago: false,
        pagos_parciales: []
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        cargarDatos();
    }, []);

    const cargarDatos = async () => {
        try {
            setLoading(true);
            const [pedidosResponse, transaccionesResponse, mediosResponse] = await Promise.all([
                fetch('/api/pedidos/?estado=listo'),
                fetch('/api/pagos/transacciones/'),
                fetch('/api/pagos/medios-pago/')
            ]);

            if (!pedidosResponse.ok || !transaccionesResponse.ok || !mediosResponse.ok) {
                throw new Error('Error al cargar datos de pagos');
            }

            const pedidos = await pedidosResponse.json();
            const transaccionesData = await transaccionesResponse.json();
            const medios = await mediosResponse.json();

            setPedidosPendientes(pedidos.filter(p => p.estado === 'listo'));
            setTransacciones(transaccionesData);
            setMediosPago(medios.filter(m => m.activo));
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const iniciarPago = (pedido) => {
        setPedidoSeleccionado(pedido);
        setPagoActual({
            medio_pago_id: '',
            monto: pedido.total.toString(),
            referencia: '',
            dividir_pago: false,
            pagos_parciales: []
        });
        setPagoEnProceso(true);
    };

    const procesarPago = async () => {
        try {
            if (!pagoActual.medio_pago_id) {
                setError('Debe seleccionar un medio de pago');
                return;
            }

            const datosPago = {
                pedido_id: pedidoSeleccionado.id,
                medio_pago_id: pagoActual.medio_pago_id,
                monto: parseFloat(pagoActual.monto),
                referencia: pagoActual.referencia
            };

            const response = await fetch('/api/pagos/procesar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(datosPago)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al procesar el pago');
            }

            const resultado = await response.json();
            
            // Actualizar datos y cerrar modal
            await cargarDatos();
            cerrarPago();
            
            alert(`Pago procesado exitosamente. ID de transacción: ${resultado.id}`);
        } catch (err) {
            setError(err.message);
        }
    };

    const agregarPagoParcial = () => {
        if (!pagoActual.medio_pago_id || !pagoActual.monto) {
            setError('Complete los datos del pago parcial');
            return;
        }

        const nuevoPago = {
            medio_pago_id: pagoActual.medio_pago_id,
            monto: parseFloat(pagoActual.monto),
            referencia: pagoActual.referencia,
            medio_pago_nombre: mediosPago.find(m => m.id == pagoActual.medio_pago_id)?.nombre || 'N/A'
        };

        const totalActual = pagoActual.pagos_parciales.reduce((sum, pago) => sum + pago.monto, 0);
        const nuevoTotal = totalActual + nuevoPago.monto;

        if (nuevoTotal > pedidoSeleccionado.total) {
            setError('El total de los pagos no puede exceder el monto del pedido');
            return;
        }

        setPagoActual({
            ...pagoActual,
            pagos_parciales: [...pagoActual.pagos_parciales, nuevoPago],
            medio_pago_id: '',
            monto: (pedidoSeleccionado.total - nuevoTotal).toString(),
            referencia: ''
        });
    };

    const procesarPagoDividido = async () => {
        try {
            const totalPagos = pagoActual.pagos_parciales.reduce((sum, pago) => sum + pago.monto, 0);
            
            if (totalPagos !== pedidoSeleccionado.total) {
                setError('El total de los pagos debe ser igual al monto del pedido');
                return;
            }

            const datosPago = {
                pedido_id: pedidoSeleccionado.id,
                pagos_multiples: pagoActual.pagos_parciales.map(pago => ({
                    medio_pago_id: pago.medio_pago_id,
                    monto: pago.monto,
                    referencia: pago.referencia
                }))
            };

            const response = await fetch('/api/pagos/procesar-multiple/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(datosPago)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al procesar los pagos');
            }

            await cargarDatos();
            cerrarPago();
            
            alert('Pagos procesados exitosamente');
        } catch (err) {
            setError(err.message);
        }
    };

    const cerrarPago = () => {
        setPedidoSeleccionado(null);
        setPagoEnProceso(false);
        setPagoActual({
            medio_pago_id: '',
            monto: '',
            referencia: '',
            dividir_pago: false,
            pagos_parciales: []
        });
        setError(null);
    };

    const generarComprobante = async (transaccionId) => {
        try {
            const response = await fetch(`/api/pagos/comprobante/${transaccionId}/`, {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Error al generar comprobante');
            }

            // Descargar el PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `comprobante_${transaccionId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (err) {
            setError(err.message);
        }
    };

    const getEstadoColor = (estado) => {
        const colores = {
            'exitosa': 'bg-green-100 text-green-800',
            'pendiente': 'bg-yellow-100 text-yellow-800',
            'fallida': 'bg-red-100 text-red-800',
            'cancelada': 'bg-gray-100 text-gray-800'
        };
        return colores[estado] || 'bg-gray-100 text-gray-800';
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Gestión de Pagos</h1>
                
                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                {/* Estadísticas */}
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
                                            Pedidos Pendientes de Pago
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {pedidosPendientes.length}
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
                                        <span className="text-white font-bold">$</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            Ventas Hoy
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            ${transacciones
                                                .filter(t => t.estado === 'exitosa' && 
                                                    new Date(t.fecha_creacion).toDateString() === new Date().toDateString())
                                                .reduce((sum, t) => sum + t.monto, 0)
                                                .toLocaleString()}
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
                                        <span className="text-white font-bold">T</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            Transacciones Hoy
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {transacciones.filter(t => 
                                                new Date(t.fecha_creacion).toDateString() === new Date().toDateString()).length}
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
                                        <span className="text-white font-bold">M</span>
                                    </div>
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">
                                            Medios de Pago Activos
                                        </dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {mediosPago.length}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Pedidos pendientes de pago */}
            <div className="bg-white shadow overflow-hidden sm:rounded-md mb-8">
                <div className="px-4 py-5 sm:px-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                        Pedidos Listos para Pagar
                    </h3>
                    <p className="mt-1 max-w-2xl text-sm text-gray-500">
                        Pedidos que han sido entregados y están pendientes de pago
                    </p>
                </div>
                <ul className="divide-y divide-gray-200">
                    {pedidosPendientes.length === 0 ? (
                        <li className="p-6 text-center text-gray-500">
                            No hay pedidos pendientes de pago
                        </li>
                    ) : (
                        pedidosPendientes.map((pedido) => (
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
                                                    Mesa: {pedido.mesa_numero || 'N/A'}
                                                </p>
                                            </div>
                                            <div className="flex flex-col items-end">
                                                <p className="text-lg font-bold text-gray-900">
                                                    ${pedido.total}
                                                </p>
                                                <button
                                                    onClick={() => iniciarPago(pedido)}
                                                    className="mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                                                >
                                                    Procesar Pago
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        ))
                    )}
                </ul>
            </div>

            {/* Transacciones recientes */}
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <div className="px-4 py-5 sm:px-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                        Transacciones Recientes
                    </h3>
                </div>
                <ul className="divide-y divide-gray-200">
                    {transacciones.slice(0, 10).map((transaccion) => (
                        <li key={transaccion.id} className="p-6 hover:bg-gray-50">
                            <div className="flex items-center justify-between">
                                <div className="flex-1">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-sm font-medium text-indigo-600 truncate">
                                                Transacción #{transaccion.id}
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                Pedido #{transaccion.pedido_id}
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                Método: {transaccion.medio_pago_nombre}
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                {new Date(transaccion.fecha_creacion).toLocaleString()}
                                            </p>
                                        </div>
                                        <div className="flex flex-col items-end">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getEstadoColor(transaccion.estado)}`}>
                                                {transaccion.estado.toUpperCase()}
                                            </span>
                                            <p className="text-lg font-bold text-gray-900 mt-1">
                                                ${transaccion.monto}
                                            </p>
                                            {transaccion.comision > 0 && (
                                                <p className="text-sm text-gray-500">
                                                    Comisión: ${transaccion.comision}
                                                </p>
                                            )}
                                            {transaccion.estado === 'exitosa' && (
                                                <button
                                                    onClick={() => generarComprobante(transaccion.id)}
                                                    className="mt-2 text-sm bg-blue-500 hover:bg-blue-700 text-white px-3 py-1 rounded"
                                                >
                                                    Descargar Comprobante
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Modal de procesamiento de pago */}
            {pagoEnProceso && (
                <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
                    <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
                        <div className="mt-3">
                            <h3 className="text-lg font-medium text-gray-900 mb-4">
                                Procesar Pago - Pedido #{pedidoSeleccionado?.id}
                            </h3>
                            
                            <div className="mb-4 p-3 bg-gray-100 rounded">
                                <p><strong>Cliente:</strong> {pedidoSeleccionado?.cliente_nombre}</p>
                                <p><strong>Total:</strong> ${pedidoSeleccionado?.total}</p>
                            </div>

                            {/* Opción de dividir pago */}
                            <div className="mb-4">
                                <label className="flex items-center">
                                    <input
                                        type="checkbox"
                                        checked={pagoActual.dividir_pago}
                                        onChange={(e) => setPagoActual({...pagoActual, dividir_pago: e.target.checked})}
                                        className="mr-2"
                                    />
                                    Dividir pago en múltiples métodos
                                </label>
                            </div>

                            {/* Pagos parciales */}
                            {pagoActual.dividir_pago && pagoActual.pagos_parciales.length > 0 && (
                                <div className="mb-4">
                                    <h4 className="font-medium mb-2">Pagos agregados:</h4>
                                    {pagoActual.pagos_parciales.map((pago, index) => (
                                        <div key={index} className="flex justify-between items-center p-2 bg-green-50 rounded mb-1">
                                            <span>{pago.medio_pago_nombre}: ${pago.monto}</span>
                                            <button
                                                onClick={() => {
                                                    const nuevosPagos = pagoActual.pagos_parciales.filter((_, i) => i !== index);
                                                    const totalRestante = pedidoSeleccionado.total - nuevosPagos.reduce((sum, p) => sum + p.monto, 0);
                                                    setPagoActual({
                                                        ...pagoActual,
                                                        pagos_parciales: nuevosPagos,
                                                        monto: totalRestante.toString()
                                                    });
                                                }}
                                                className="text-red-500 hover:text-red-700"
                                            >
                                                Eliminar
                                            </button>
                                        </div>
                                    ))}
                                    <p className="text-sm text-gray-600">
                                        Total pagado: ${pagoActual.pagos_parciales.reduce((sum, pago) => sum + pago.monto, 0)}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        Restante: ${pedidoSeleccionado.total - pagoActual.pagos_parciales.reduce((sum, pago) => sum + pago.monto, 0)}
                                    </p>
                                </div>
                            )}

                            {/* Formulario de pago */}
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Medio de Pago
                                    </label>
                                    <select
                                        value={pagoActual.medio_pago_id}
                                        onChange={(e) => setPagoActual({...pagoActual, medio_pago_id: e.target.value})}
                                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                                    >
                                        <option value="">Seleccionar medio de pago...</option>
                                        {mediosPago.map(medio => (
                                            <option key={medio.id} value={medio.id}>
                                                {medio.nombre} {medio.comision_porcentaje > 0 && `(${medio.comision_porcentaje}% comisión)`}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Monto
                                    </label>
                                    <input
                                        type="number"
                                        step="0.01"
                                        value={pagoActual.monto}
                                        onChange={(e) => setPagoActual({...pagoActual, monto: e.target.value})}
                                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                                        readOnly={!pagoActual.dividir_pago}
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Referencia (opcional)
                                    </label>
                                    <input
                                        type="text"
                                        value={pagoActual.referencia}
                                        onChange={(e) => setPagoActual({...pagoActual, referencia: e.target.value})}
                                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                                        placeholder="Número de transacción, aprobación, etc."
                                    />
                                </div>
                            </div>

                            {/* Botones */}
                            <div className="flex justify-end space-x-3 mt-6">
                                <button
                                    onClick={cerrarPago}
                                    className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                                >
                                    Cancelar
                                </button>
                                
                                {pagoActual.dividir_pago ? (
                                    <>
                                        <button
                                            onClick={agregarPagoParcial}
                                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                                        >
                                            Agregar Pago
                                        </button>
                                        {pagoActual.pagos_parciales.reduce((sum, pago) => sum + pago.monto, 0) === pedidoSeleccionado?.total && (
                                            <button
                                                onClick={procesarPagoDividido}
                                                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                                            >
                                                Finalizar Pagos
                                            </button>
                                        )}
                                    </>
                                ) : (
                                    <button
                                        onClick={procesarPago}
                                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                                    >
                                        Procesar Pago
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Pagos;
