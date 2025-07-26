// Frontend/src/components/Pagos/PagosManager.jsx
import React, { useState, useEffect } from 'react';
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardContent 
} from '@/components/ui/card';
import { 
  Button, 
  Input, 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue,
  Badge,
  Alert,
  AlertDescription,
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger
} from '@/components/ui';
import { 
  CreditCard, 
  DollarSign, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Plus,
  RefreshCw,
  Receipt,
  TrendingUp,
  Banknote
} from 'lucide-react';

const PagosManager = () => {
  // Estados principales
  const [mediosPago, setMediosPago] = useState([]);
  const [transaccionesPendientes, setTransaccionesPendientes] = useState([]);
  const [estadisticasDiarias, setEstadisticasDiarias] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Estados para procesar pago
  const [showProcesarPago, setShowProcesarPago] = useState(false);
  const [tipoPago, setTipoPago] = useState('unico'); // 'unico' o 'dividido'
  const [pagoData, setPagoData] = useState({
    pedido_id: '',
    medio_pago_id: '',
    monto: 0,
    pagos: [] // Para pago dividido
  });

  // Estados para historial
  const [historialPedido, setHistorialPedido] = useState(null);
  const [pedidoIdBuscar, setPedidoIdBuscar] = useState('');

  // Cargar datos iniciales
  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      await Promise.all([
        cargarMediosPago(),
        cargarTransaccionesPendientes(),
        cargarEstadisticasDiarias()
      ]);
    } catch (err) {
      setError('Error al cargar datos de pagos');
    } finally {
      setLoading(false);
    }
  };

  const cargarMediosPago = async () => {
    try {
      const response = await fetch('/api/pagos/medios-pago/');
      const data = await response.json();
      if (data.success) {
        setMediosPago(data.data);
      }
    } catch (err) {
      console.error('Error al cargar medios de pago:', err);
    }
  };

  const cargarTransaccionesPendientes = async () => {
    try {
      const response = await fetch('/api/pagos/transacciones-pendientes/');
      const data = await response.json();
      if (data.success) {
        setTransaccionesPendientes(data.data);
      }
    } catch (err) {
      console.error('Error al cargar transacciones pendientes:', err);
    }
  };

  const cargarEstadisticasDiarias = async () => {
    try {
      const response = await fetch('/api/pagos/estadisticas-diarias/');
      const data = await response.json();
      if (data.success) {
        setEstadisticasDiarias(data.data);
      }
    } catch (err) {
      console.error('Error al cargar estadísticas:', err);
    }
  };

  const procesarPagoUnico = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/pagos/procesar-pago-unico/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(pagoData)
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Pago procesado exitosamente');
        setShowProcesarPago(false);
        resetearFormulario();
        await cargarDatos();
      } else {
        setError(data.error || 'Error al procesar pago');
      }
    } catch (err) {
      setError('Error de conexión al procesar pago');
    } finally {
      setLoading(false);
    }
  };

  const procesarPagoDividido = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/pagos/procesar-pago-dividido/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pedido_id: pagoData.pedido_id,
          pagos: pagoData.pagos
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Pago dividido procesado exitosamente');
        setShowProcesarPago(false);
        resetearFormulario();
        await cargarDatos();
      } else {
        setError(data.error || 'Error al procesar pago dividido');
      }
    } catch (err) {
      setError('Error de conexión al procesar pago dividido');
    } finally {
      setLoading(false);
    }
  };

  const confirmarTransaccion = async (transaccionId) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/pagos/${transaccionId}/confirmar/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          codigo_autorizacion: `AUTO-${Date.now()}`
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Transacción confirmada exitosamente');
        await cargarTransaccionesPendientes();
      } else {
        setError(data.error || 'Error al confirmar transacción');
      }
    } catch (err) {
      setError('Error de conexión al confirmar transacción');
    } finally {
      setLoading(false);
    }
  };

  const rechazarTransaccion = async (transaccionId, motivo) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/pagos/${transaccionId}/rechazar/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ motivo })
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Transacción rechazada');
        await cargarTransaccionesPendientes();
      } else {
        setError(data.error || 'Error al rechazar transacción');
      }
    } catch (err) {
      setError('Error de conexión al rechazar transacción');
    } finally {
      setLoading(false);
    }
  };

  const buscarHistorialPedido = async () => {
    if (!pedidoIdBuscar) return;
    
    setLoading(true);
    try {
      const response = await fetch(`/api/pagos/historial-pedido/${pedidoIdBuscar}/`);
      const data = await response.json();
      
      if (data.success) {
        setHistorialPedido(data.data);
      } else {
        setError(data.error || 'Pedido no encontrado');
        setHistorialPedido(null);
      }
    } catch (err) {
      setError('Error al buscar historial de pedido');
    } finally {
      setLoading(false);
    }
  };

  const resetearFormulario = () => {
    setPagoData({
      pedido_id: '',
      medio_pago_id: '',
      monto: 0,
      pagos: []
    });
    setTipoPago('unico');
  };

  const agregarPagoDividido = () => {
    setPagoData({
      ...pagoData,
      pagos: [...pagoData.pagos, { medio_pago_id: '', monto: 0 }]
    });
  };

  const actualizarPagoDividido = (index, campo, valor) => {
    const nuevosPagos = [...pagoData.pagos];
    nuevosPagos[index][campo] = valor;
    setPagoData({ ...pagoData, pagos: nuevosPagos });
  };

  const eliminarPagoDividido = (index) => {
    const nuevosPagos = pagoData.pagos.filter((_, i) => i !== index);
    setPagoData({ ...pagoData, pagos: nuevosPagos });
  };

  const obtenerIconoMedioPago = (tipo) => {
    switch (tipo) {
      case 'efectivo':
        return <Banknote className="w-4 h-4" />;
      case 'tarjeta_credito':
      case 'tarjeta_debito':
        return <CreditCard className="w-4 h-4" />;
      default:
        return <DollarSign className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gestión de Pagos</h1>
          <p className="text-gray-600">Procesa y administra transacciones de pago</p>
        </div>
        <div className="flex gap-4">
          <Button 
            onClick={() => setShowProcesarPago(true)}
            className="bg-green-600 hover:bg-green-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Procesar Pago
          </Button>
          <Button 
            onClick={cargarDatos}
            variant="outline"
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Actualizar
          </Button>
        </div>
      </div>

      {/* Alertas */}
      {error && (
        <Alert className="border-red-200 bg-red-50">
          <AlertCircle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="border-green-200 bg-green-50">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}

      {/* Modal para procesar pago */}
      {showProcesarPago && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card className="w-full max-w-2xl max-h-[80vh] overflow-y-auto">
            <CardHeader>
              <CardTitle>Procesar Nuevo Pago</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Tipo de pago */}
              <div>
                <label className="block text-sm font-medium mb-2">Tipo de Pago</label>
                <Select value={tipoPago} onValueChange={setTipoPago}>
                  <SelectTrigger>
                    <SelectValue placeholder="Seleccionar tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="unico">Pago Único</SelectItem>
                    <SelectItem value="dividido">Pago Dividido</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* ID del pedido */}
              <Input
                placeholder="ID del pedido"
                type="number"
                value={pagoData.pedido_id}
                onChange={(e) => setPagoData({
                  ...pagoData,
                  pedido_id: e.target.value
                })}
              />

              {tipoPago === 'unico' ? (
                // Pago único
                <>
                  <Select 
                    value={pagoData.medio_pago_id} 
                    onValueChange={(value) => setPagoData({
                      ...pagoData,
                      medio_pago_id: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Seleccionar medio de pago" />
                    </SelectTrigger>
                    <SelectContent>
                      {mediosPago.map((medio) => (
                        <SelectItem key={medio.id} value={medio.id.toString()}>
                          <div className="flex items-center gap-2">
                            {obtenerIconoMedioPago(medio.tipo)}
                            {medio.nombre}
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Input
                    placeholder="Monto"
                    type="number"
                    step="0.01"
                    value={pagoData.monto}
                    onChange={(e) => setPagoData({
                      ...pagoData,
                      monto: parseFloat(e.target.value) || 0
                    })}
                  />
                </>
              ) : (
                // Pago dividido
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h4 className="font-medium">Pagos Divididos</h4>
                    <Button onClick={agregarPagoDividido} size="sm">
                      <Plus className="w-4 h-4 mr-1" />
                      Agregar Pago
                    </Button>
                  </div>

                  {pagoData.pagos.map((pago, index) => (
                    <div key={index} className="border rounded-lg p-4 space-y-2">
                      <div className="flex justify-between items-center">
                        <h5 className="font-medium">Pago {index + 1}</h5>
                        <Button 
                          onClick={() => eliminarPagoDividido(index)}
                          variant="outline"
                          size="sm"
                        >
                          Eliminar
                        </Button>
                      </div>
                      
                      <Select 
                        value={pago.medio_pago_id} 
                        onValueChange={(value) => actualizarPagoDividido(index, 'medio_pago_id', value)}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Medio de pago" />
                        </SelectTrigger>
                        <SelectContent>
                          {mediosPago.map((medio) => (
                            <SelectItem key={medio.id} value={medio.id.toString()}>
                              <div className="flex items-center gap-2">
                                {obtenerIconoMedioPago(medio.tipo)}
                                {medio.nombre}
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>

                      <Input
                        placeholder="Monto"
                        type="number"
                        step="0.01"
                        value={pago.monto}
                        onChange={(e) => actualizarPagoDividido(index, 'monto', parseFloat(e.target.value) || 0)}
                      />
                    </div>
                  ))}

                  {pagoData.pagos.length > 0 && (
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <p className="text-sm font-medium">
                        Total: ${pagoData.pagos.reduce((sum, pago) => sum + pago.monto, 0).toLocaleString()}
                      </p>
                    </div>
                  )}
                </div>
              )}

              <div className="flex gap-2">
                <Button 
                  onClick={tipoPago === 'unico' ? procesarPagoUnico : procesarPagoDividido}
                  className="flex-1"
                  disabled={loading}
                >
                  {loading ? 'Procesando...' : 'Procesar Pago'}
                </Button>
                <Button 
                  onClick={() => {
                    setShowProcesarPago(false);
                    resetearFormulario();
                  }}
                  variant="outline"
                  className="flex-1"
                >
                  Cancelar
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Contenido principal con tabs */}
      <Tabs defaultValue="resumen" className="space-y-4">
        <TabsList>
          <TabsTrigger value="resumen">Resumen Diario</TabsTrigger>
          <TabsTrigger value="pendientes">Transacciones Pendientes</TabsTrigger>
          <TabsTrigger value="medios">Medios de Pago</TabsTrigger>
          <TabsTrigger value="historial">Historial de Pedido</TabsTrigger>
        </TabsList>

        {/* Tab Resumen */}
        <TabsContent value="resumen" className="space-y-4">
          {estadisticasDiarias.resumen_ventas && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-green-100 rounded-lg">
                      <TrendingUp className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Total Ventas</p>
                      <p className="text-2xl font-bold">
                        ${estadisticasDiarias.resumen_ventas.total_ventas?.toLocaleString() || 0}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-blue-100 rounded-lg">
                      <Receipt className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Transacciones</p>
                      <p className="text-2xl font-bold">
                        {estadisticasDiarias.resumen_ventas.total_transacciones || 0}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-yellow-100 rounded-lg">
                      <Clock className="w-6 h-6 text-yellow-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Pendientes</p>
                      <p className="text-2xl font-bold">
                        {estadisticasDiarias.transacciones_pendientes || 0}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Detalle por medio de pago */}
          {estadisticasDiarias.detalle_por_medio_pago && (
            <Card>
              <CardHeader>
                <CardTitle>Ventas por Medio de Pago</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries(estadisticasDiarias.detalle_por_medio_pago).map(([medio, datos]) => (
                    <div key={medio} className="flex justify-between items-center p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        {obtenerIconoMedioPago(medio)}
                        <div>
                          <h4 className="font-medium">{medio}</h4>
                          <p className="text-sm text-gray-600">
                            {datos.cantidad_transacciones} transacciones
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">${datos.monto_total?.toLocaleString()}</p>
                        <p className="text-sm text-gray-600">
                          {datos.porcentaje_del_total?.toFixed(1)}% del total
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Tab Transacciones Pendientes */}
        <TabsContent value="pendientes" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Transacciones Pendientes de Confirmación</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {transaccionesPendientes.map((transaccion) => (
                  <div key={transaccion.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="font-semibold">
                          Transacción #{transaccion.codigo_referencia}
                        </h4>
                        <p className="text-sm text-gray-600">
                          Pedido #{transaccion.pedido_id}
                        </p>
                      </div>
                      <Badge className="bg-yellow-100 text-yellow-800">
                        Pendiente
                      </Badge>
                    </div>

                    <div className="flex justify-between items-center mb-4">
                      <div className="flex items-center gap-2">
                        {obtenerIconoMedioPago(transaccion.medio_pago)}
                        <span>{transaccion.medio_pago}</span>
                      </div>
                      <span className="font-bold">${transaccion.monto.toLocaleString()}</span>
                    </div>

                    <div className="text-sm text-gray-600 mb-4">
                      Esperando por {transaccion.tiempo_espera_minutos} minutos
                    </div>

                    <div className="flex gap-2">
                      <Button 
                        onClick={() => confirmarTransaccion(transaccion.id)}
                        size="sm"
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <CheckCircle className="w-4 h-4 mr-1" />
                        Confirmar
                      </Button>
                      <Button 
                        onClick={() => rechazarTransaccion(transaccion.id, 'Rechazado manualmente')}
                        size="sm"
                        variant="outline"
                      >
                        <AlertCircle className="w-4 h-4 mr-1" />
                        Rechazar
                      </Button>
                    </div>
                  </div>
                ))}

                {transaccionesPendientes.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    No hay transacciones pendientes
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab Medios de Pago */}
        <TabsContent value="medios" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Medios de Pago Disponibles</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {mediosPago.map((medio) => (
                  <div key={medio.id} className="border rounded-lg p-4">
                    <div className="flex items-center gap-3 mb-2">
                      {obtenerIconoMedioPago(medio.tipo)}
                      <div>
                        <h4 className="font-semibold">{medio.nombre}</h4>
                        <p className="text-sm text-gray-600 capitalize">{medio.tipo}</p>
                      </div>
                    </div>
                    
                    <div className="text-sm space-y-1">
                      <p>Comisión: {medio.comision_porcentaje}% + ${medio.comision_fija}</p>
                      {medio.requiere_validacion_externa && (
                        <p className="text-yellow-600">Requiere validación externa</p>
                      )}
                      {medio.descripcion && (
                        <p className="text-gray-600">{medio.descripcion}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tab Historial */}
        <TabsContent value="historial" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Buscar Historial de Pedido</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-4">
                <Input
                  placeholder="ID del pedido"
                  type="number"
                  value={pedidoIdBuscar}
                  onChange={(e) => setPedidoIdBuscar(e.target.value)}
                />
                <Button onClick={buscarHistorialPedido} disabled={loading}>
                  Buscar
                </Button>
              </div>

              {historialPedido && (
                <div className="space-y-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-semibold mb-2">Resumen del Pedido #{historialPedido.pedido_id}</h4>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>Total Pedido: ${historialPedido.total_pedido.toLocaleString()}</div>
                      <div>Total Pagado: ${historialPedido.total_pagado.toLocaleString()}</div>
                      <div>Saldo Pendiente: ${historialPedido.saldo_pendiente.toLocaleString()}</div>
                      <div>Total Comisiones: ${historialPedido.total_comisiones.toLocaleString()}</div>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <h5 className="font-medium">Transacciones</h5>
                    {historialPedido.transacciones.map((transaccion) => (
                      <div key={transaccion.id} className="border rounded-lg p-3">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h6 className="font-medium">#{transaccion.codigo_referencia}</h6>
                            <p className="text-sm text-gray-600">{transaccion.medio_pago}</p>
                          </div>
                          <Badge className={`${
                            transaccion.estado === 'completada' 
                              ? 'bg-green-100 text-green-800' 
                              : transaccion.estado === 'pendiente'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {transaccion.estado}
                          </Badge>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-2 text-sm">
                          <div>Monto: ${transaccion.monto.toLocaleString()}</div>
                          <div>Comisión: ${transaccion.comision.toLocaleString()}</div>
                          <div>Neto: ${transaccion.monto_neto.toLocaleString()}</div>
                        </div>
                        
                        <div className="text-xs text-gray-500 mt-2">
                          {new Date(transaccion.fecha_creacion).toLocaleString()}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default PagosManager;
