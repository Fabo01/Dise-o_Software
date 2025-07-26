# Backend/Presentacion/Controladores/Pagos_Controlador.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone

from Backend.Aplicacion.Servicios.Pagos_Servicio import PagosServicio

class PagosControlador(viewsets.ViewSet):
    """
    Controlador REST para gestión de pagos y transacciones
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pagos_servicio = PagosServicio()
    
    @action(detail=False, methods=['post'], url_path='procesar-pago-unico')
    def procesar_pago_unico(self, request):
        """
        POST /api/pagos/procesar-pago-unico/
        Procesa un pago único completo de un pedido
        """
        try:
            datos_pago = request.data
            
            # Validar campos requeridos
            campos_requeridos = ['pedido_id', 'medio_pago_id', 'monto']
            for campo in campos_requeridos:
                if campo not in datos_pago:
                    return Response({
                        'success': False,
                        'error': f'Campo requerido: {campo}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            resultado = self.pagos_servicio.procesar_pago_unico(datos_pago)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Pago procesado exitosamente'
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
    
    @action(detail=False, methods=['post'], url_path='procesar-pago-dividido')
    def procesar_pago_dividido(self, request):
        """
        POST /api/pagos/procesar-pago-dividido/
        Procesa un pago dividido en múltiples medios de pago
        """
        try:
            datos_pago = request.data
            
            # Validar campos requeridos
            if 'pedido_id' not in datos_pago:
                return Response({
                    'success': False,
                    'error': 'Campo requerido: pedido_id'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if 'pagos' not in datos_pago or not isinstance(datos_pago['pagos'], list):
                return Response({
                    'success': False,
                    'error': 'Campo requerido: pagos (debe ser una lista)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            resultado = self.pagos_servicio.procesar_pago_dividido(datos_pago)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Pago dividido procesado exitosamente'
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
    
    @action(detail=True, methods=['post'], url_path='confirmar')
    def confirmar_pago(self, request, pk=None):
        """
        POST /api/pagos/{transaccion_id}/confirmar/
        Confirma un pago que estaba pendiente de validación externa
        """
        try:
            transaccion_id = int(pk)
            datos_confirmacion = request.data
            
            resultado = self.pagos_servicio.confirmar_pago_pendiente(transaccion_id, datos_confirmacion)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Pago confirmado exitosamente'
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
    
    @action(detail=True, methods=['post'], url_path='rechazar')
    def rechazar_pago(self, request, pk=None):
        """
        POST /api/pagos/{transaccion_id}/rechazar/
        Rechaza un pago que estaba pendiente de validación
        """
        try:
            transaccion_id = int(pk)
            motivo = request.data.get('motivo', 'No especificado')
            
            resultado = self.pagos_servicio.rechazar_pago_pendiente(transaccion_id, motivo)
            
            return Response({
                'success': True,
                'data': resultado,
                'message': 'Pago rechazado'
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
    
    @action(detail=False, methods=['get'], url_path='medios-pago')
    def medios_pago_disponibles(self, request):
        """
        GET /api/pagos/medios-pago/
        Obtiene la lista de medios de pago disponibles
        """
        try:
            medios_pago = self.pagos_servicio.obtener_medios_pago_disponibles()
            
            return Response({
                'success': True,
                'data': medios_pago,
                'count': len(medios_pago)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='historial-pedido/(?P<pedido_id>[0-9]+)')
    def historial_pagos_pedido(self, request, pedido_id=None):
        """
        GET /api/pagos/historial-pedido/{pedido_id}/
        Obtiene el historial completo de pagos de un pedido
        """
        try:
            pedido_id = int(pedido_id)
            historial = self.pagos_servicio.obtener_historial_pagos_pedido(pedido_id)
            
            return Response({
                'success': True,
                'data': historial
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
    
    @action(detail=False, methods=['get'], url_path='reporte-ventas')
    def reporte_ventas_por_medio_pago(self, request):
        """
        GET /api/pagos/reporte-ventas/
        Genera reporte de ventas agrupado por medio de pago
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
            
            reporte = self.pagos_servicio.obtener_reporte_ventas_por_medio_pago(fecha_inicio, fecha_fin)
            
            return Response({
                'success': True,
                'data': reporte
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='transacciones-pendientes')
    def transacciones_pendientes(self, request):
        """
        GET /api/pagos/transacciones-pendientes/
        Obtiene las transacciones que están pendientes de confirmación
        """
        try:
            transacciones = self.pagos_servicio.obtener_transacciones_pendientes()
            
            return Response({
                'success': True,
                'data': transacciones,
                'count': len(transacciones)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='estadisticas-diarias')
    def estadisticas_diarias(self, request):
        """
        GET /api/pagos/estadisticas-diarias/
        Obtiene estadísticas de pagos del día actual
        """
        try:
            hoy = timezone.now().date()
            fecha_inicio = datetime.combine(hoy, datetime.min.time())
            fecha_fin = datetime.combine(hoy, datetime.max.time())
            
            reporte = self.pagos_servicio.obtener_reporte_ventas_por_medio_pago(fecha_inicio, fecha_fin)
            transacciones_pendientes = self.pagos_servicio.obtener_transacciones_pendientes()
            
            estadisticas = {
                'fecha': hoy.isoformat(),
                'resumen_ventas': reporte['resumen_general'],
                'detalle_por_medio_pago': reporte['detalle_por_medio_pago'],
                'transacciones_pendientes': len(transacciones_pendientes)
            }
            
            return Response({
                'success': True,
                'data': estadisticas
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
