// Frontend/src/components/Delivery/DeliveryManager.jsx
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
  AlertDescription
} from '@/components/ui';
import { 
  Truck, 
  MapPin, 
  Clock, 
  Phone, 
  CheckCircle, 
  AlertCircle,
  Plus,
  RefreshCw
} from 'lucide-react';

const DeliveryManager = () => {
  // Estados principales
  const [pedidosPendientes, setPedidosPendientes] = useState([]);
  const [repartidoresDisponibles, setRepartidoresDisponibles] = useState([]);
  const [entregasEnCurso, setEntregasEnCurso] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Estados para crear nuevo pedido
  const [showNuevoPedido, setShowNuevoPedido] = useState(false);
  const [nuevoPedidoData, setNuevoPedidoData] = useState({
    cliente_rut: '',
    direccion_entrega: '',
    telefono_contacto: '',
    observaciones: '',
    total: 0
  });

  // Cargar datos iniciales
  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      await Promise.all([
        cargarPedidosPendientes(),
        cargarRepartidoresDisponibles(),
        cargarEntregasEnCurso()
      ]);
    } catch (err) {
      setError('Error al cargar datos de delivery');
    } finally {
      setLoading(false);
    }
  };

  const cargarPedidosPendientes = async () => {
    try {
      const response = await fetch('/api/delivery/pedidos-pendientes/');
      const data = await response.json();
      if (data.success) {
        setPedidosPendientes(data.data);
      }
    } catch (err) {
      console.error('Error al cargar pedidos pendientes:', err);
    }
  };

  const cargarRepartidoresDisponibles = async () => {
    try {
      const response = await fetch('/api/delivery/repartidores-disponibles/');
      const data = await response.json();
      if (data.success) {
        setRepartidoresDisponibles(data.data);
      }
    } catch (err) {
      console.error('Error al cargar repartidores:', err);
    }
  };

  const cargarEntregasEnCurso = async () => {
    try {
      // Simular entregas en curso - en producción vendría de la API
      setEntregasEnCurso([]);
    } catch (err) {
      console.error('Error al cargar entregas en curso:', err);
    }
  };

  const crearPedidoDelivery = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/delivery/crear-pedido-directo/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(nuevoPedidoData)
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Pedido delivery creado exitosamente');
        setShowNuevoPedido(false);
        setNuevoPedidoData({
          cliente_rut: '',
          direccion_entrega: '',
          telefono_contacto: '',
          observaciones: '',
          total: 0
        });
        await cargarPedidosPendientes();
      } else {
        setError(data.error || 'Error al crear pedido');
      }
    } catch (err) {
      setError('Error de conexión al crear pedido');
    } finally {
      setLoading(false);
    }
  };

  const asignarRepartidor = async (pedidoId, repartidorId) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/delivery/${pedidoId}/asignar-repartidor/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repartidor_id: repartidorId })
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Repartidor asignado exitosamente');
        await cargarDatos(); // Recargar todos los datos
      } else {
        setError(data.error || 'Error al asignar repartidor');
      }
    } catch (err) {
      setError('Error de conexión al asignar repartidor');
    } finally {
      setLoading(false);
    }
  };

  const completarEntrega = async (pedidoId, comentarios = '') => {
    setLoading(true);
    try {
      const response = await fetch(`/api/delivery/${pedidoId}/completar-entrega/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comentarios })
      });

      const data = await response.json();
      
      if (data.success) {
        setSuccess('Entrega completada exitosamente');
        await cargarDatos();
      } else {
        setError(data.error || 'Error al completar entrega');
      }
    } catch (err) {
      setError('Error de conexión al completar entrega');
    } finally {
      setLoading(false);
    }
  };

  const obtenerBadgeEstado = (estado) => {
    const colores = {
      'pendiente': 'bg-yellow-100 text-yellow-800',
      'asignado': 'bg-blue-100 text-blue-800',
      'en_ruta': 'bg-purple-100 text-purple-800',
      'entregado': 'bg-green-100 text-green-800'
    };
    return colores[estado] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gestión de Delivery</h1>
          <p className="text-gray-600">Administra pedidos de entrega y repartidores</p>
        </div>
        <div className="flex gap-4">
          <Button 
            onClick={() => setShowNuevoPedido(true)}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Nuevo Pedido Delivery
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

      {/* Modal para nuevo pedido */}
      {showNuevoPedido && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>Crear Nuevo Pedido Delivery</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input
                placeholder="RUT del cliente"
                value={nuevoPedidoData.cliente_rut}
                onChange={(e) => setNuevoPedidoData({
                  ...nuevoPedidoData,
                  cliente_rut: e.target.value
                })}
              />
              <Input
                placeholder="Dirección de entrega"
                value={nuevoPedidoData.direccion_entrega}
                onChange={(e) => setNuevoPedidoData({
                  ...nuevoPedidoData,
                  direccion_entrega: e.target.value
                })}
              />
              <Input
                placeholder="Teléfono de contacto"
                value={nuevoPedidoData.telefono_contacto}
                onChange={(e) => setNuevoPedidoData({
                  ...nuevoPedidoData,
                  telefono_contacto: e.target.value
                })}
              />
              <Input
                type="number"
                placeholder="Total del pedido"
                value={nuevoPedidoData.total}
                onChange={(e) => setNuevoPedidoData({
                  ...nuevoPedidoData,
                  total: parseFloat(e.target.value) || 0
                })}
              />
              <Input
                placeholder="Observaciones (opcional)"
                value={nuevoPedidoData.observaciones}
                onChange={(e) => setNuevoPedidoData({
                  ...nuevoPedidoData,
                  observaciones: e.target.value
                })}
              />
              <div className="flex gap-2">
                <Button 
                  onClick={crearPedidoDelivery}
                  className="flex-1"
                  disabled={loading}
                >
                  {loading ? 'Creando...' : 'Crear Pedido'}
                </Button>
                <Button 
                  onClick={() => setShowNuevoPedido(false)}
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

      {/* Grid de contenido */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Pedidos Pendientes de Asignación */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              Pedidos Pendientes ({pedidosPendientes.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {pedidosPendientes.map((pedido) => (
                <div key={pedido.id} className="border rounded-lg p-4 space-y-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-semibold">Pedido #{pedido.id}</h4>
                      <p className="text-sm text-gray-600">{pedido.cliente}</p>
                    </div>
                    <Badge className={`${obtenerBadgeEstado('pendiente')}`}>
                      Pendiente
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <MapPin className="w-4 h-4" />
                    {pedido.direccion}
                  </div>
                  
                  <div className="flex justify-between items-center text-sm">
                    <span className="font-medium">${pedido.total.toLocaleString()}</span>
                    <span className="text-gray-500">
                      {pedido.tiempo_estimado} min estimado
                    </span>
                  </div>

                  {pedido.app_externa && (
                    <Badge variant="outline" className="text-xs">
                      {pedido.app_externa}
                    </Badge>
                  )}

                  {/* Selector de repartidor */}
                  <div className="flex gap-2 mt-3">
                    <Select onValueChange={(value) => asignarRepartidor(pedido.id, value)}>
                      <SelectTrigger className="flex-1">
                        <SelectValue placeholder="Asignar repartidor" />
                      </SelectTrigger>
                      <SelectContent>
                        {repartidoresDisponibles.map((repartidor) => (
                          <SelectItem key={repartidor.id} value={repartidor.id.toString()}>
                            {repartidor.nombre} - {repartidor.vehiculo}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              ))}

              {pedidosPendientes.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  No hay pedidos pendientes de asignación
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Repartidores Disponibles */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Truck className="w-5 h-5" />
              Repartidores Disponibles ({repartidoresDisponibles.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {repartidoresDisponibles.map((repartidor) => (
                <div key={repartidor.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-semibold">{repartidor.nombre}</h4>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Phone className="w-4 h-4" />
                        {repartidor.telefono}
                      </div>
                    </div>
                    <Badge className="bg-green-100 text-green-800">
                      Disponible
                    </Badge>
                  </div>
                  
                  <div className="mt-2">
                    <span className="text-sm text-gray-600">
                      Vehículo: {repartidor.vehiculo}
                    </span>
                  </div>

                  {repartidor.ubicacion && (
                    <div className="flex items-center gap-2 text-sm text-gray-600 mt-1">
                      <MapPin className="w-4 h-4" />
                      Ubicación disponible
                    </div>
                  )}
                </div>
              ))}

              {repartidoresDisponibles.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  No hay repartidores disponibles
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Entregas en Curso (si las hay) */}
      {entregasEnCurso.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Truck className="w-5 h-5" />
              Entregas en Curso ({entregasEnCurso.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {entregasEnCurso.map((entrega) => (
                <div key={entrega.pedido_id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold">Pedido #{entrega.pedido_id}</h4>
                    <Badge className={`${obtenerBadgeEstado(entrega.estado)}`}>
                      {entrega.estado}
                    </Badge>
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <MapPin className="w-4 h-4" />
                      {entrega.direccion}
                    </div>
                    <div className="flex items-center gap-2">
                      <Truck className="w-4 h-4" />
                      {entrega.repartidor?.nombre}
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      {entrega.tiempo_restante_estimado} min restantes
                    </div>
                  </div>

                  <Button 
                    onClick={() => completarEntrega(entrega.pedido_id)}
                    className="w-full mt-3"
                    size="sm"
                  >
                    Marcar como Entregado
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DeliveryManager;
