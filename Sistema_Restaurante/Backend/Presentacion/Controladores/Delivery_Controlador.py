# Backend/Presentacion/Controladores/Delivery_Controlador.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone

from Backend.Aplicacion.Servicios.Delivery_Servicio import DeliveryServicio

class DeliveryControlador(viewsets.ViewSet):
    """
    Controlador REST para gestión de delivery
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.delivery_servicio = DeliveryServicio()
    
    @action(detail=False, methods=['post'], url_path='crear-pedido-directo')
    def crear_pedido_directo(self, request):
        """
        POST /api/delivery/crear-pedido-directo/
        Crea un pedido delivery directo (no desde app externa)
        """
        try:
            datos_pedido = request.data
            resultado = self.delivery_servicio.crear_pedido_delivery_directo(datos_pedido)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Pedido delivery creado exitosamente'
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], url_path='crear-desde-app-externa')
    def crear_desde_app_externa(self, request):
        """
        POST /api/delivery/crear-desde-app-externa/
        Registra un pedido recibido desde una app externa
        """
        try:
            datos_pedido = request.data
            resultado = self.delivery_servicio.crear_pedido_desde_app_externa(datos_pedido)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Pedido desde app externa registrado exitosamente'
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'], url_path='asignar-repartidor')
    def asignar_repartidor(self, request, pk=None):
        """
        POST /api/delivery/{pedido_id}/asignar-repartidor/
        Asigna un repartidor a un pedido delivery
        """
        try:
            pedido_id = int(pk)
            repartidor_id = request.data.get('repartidor_id')
            
            if not repartidor_id:
                return Response({
                    'success': False,
                    'error': 'repartidor_id es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            resultado = self.delivery_servicio.asignar_repartidor(pedido_id, repartidor_id)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Repartidor asignado exitosamente'
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='repartidores-disponibles')
    def repartidores_disponibles(self, request):
        """
        GET /api/delivery/repartidores-disponibles/
        Obtiene lista de repartidores disponibles
        """
        try:
            repartidores = self.delivery_servicio.obtener_repartidores_disponibles()
            
            return Response({
                'success': True,
                'data': repartidores,
                'count': len(repartidores)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='pedidos-pendientes')
    def pedidos_pendientes(self, request):
        """
        GET /api/delivery/pedidos-pendientes/
        Obtiene pedidos pendientes de asignación
        """
        try:
            pedidos = self.delivery_servicio.obtener_pedidos_pendientes_asignacion()
            
            return Response({
                'success': True,
                'data': pedidos,
                'count': len(pedidos)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'], url_path='seguimiento')
    def seguimiento(self, request, pk=None):
        """
        GET /api/delivery/{pedido_id}/seguimiento/
        Obtiene el estado actual de una entrega
        """
        try:
            pedido_id = int(pk)
            estado = self.delivery_servicio.seguir_estado_entrega(pedido_id)
            
            return Response({
                'success': True,
                'data': estado
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'], url_path='completar-entrega')
    def completar_entrega(self, request, pk=None):
        """
        POST /api/delivery/{pedido_id}/completar-entrega/
        Marca un pedido como entregado
        """
        try:
            pedido_id = int(pk)
            datos_entrega = request.data
            
            resultado = self.delivery_servicio.completar_entrega(pedido_id, datos_entrega)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Entrega completada exitosamente'
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='estadisticas')
    def estadisticas(self, request):
        """
        GET /api/delivery/estadisticas/
        Obtiene estadísticas de delivery para un período
        """
        try:
            # Parámetros de fecha (por defecto últimos 30 días)
            fecha_fin = timezone.now()
            fecha_inicio = fecha_fin - timedelta(days=30)
            
            # Permitir override por parámetros
            if request.query_params.get('fecha_inicio'):
                fecha_inicio = datetime.fromisoformat(request.query_params['fecha_inicio'])
            if request.query_params.get('fecha_fin'):
                fecha_fin = datetime.fromisoformat(request.query_params['fecha_fin'])
            
            estadisticas = self.delivery_servicio.obtener_estadisticas_delivery(fecha_inicio, fecha_fin)
            
            return Response({
                'success': True,
                'data': estadisticas,
                'periodo': {
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat()
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
