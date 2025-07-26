from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from typing import Optional
from datetime import date

from Backend.Aplicacion.Servicios.Pedido_Servicio import PedidoServicio
from Backend.Aplicacion.DTOs.PedidoDTO import *
from Backend.Presentacion.Serializadores.Pedido_Serializador import *
from Backend.Aplicacion.Excepciones.AplicacionExcepcion import ServicioExcepcion, EntidadNoEncontradaExcepcion
from Backend.Dominio.Excepciones.DominioExcepcion import DominioExcepcion


class PedidoViewSet(viewsets.ViewSet):
    """ViewSet para la gestión de pedidos via API REST"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # En un entorno real, esto se inyectaría via DI
        from Backend.Infraestructura.Repositorios.Pedido_Repositorio import PedidoRepositorio
        self._pedido_servicio = PedidoServicio(PedidoRepositorio())

    def list(self, request):
        """
        GET /api/pedidos/
        Lista todos los pedidos con paginación opcional
        """
        try:
            # Parámetros de consulta
            limite = request.query_params.get('limite')
            desplazamiento = int(request.query_params.get('desplazamiento', 0))
            
            if limite:
                limite = int(limite)
            
            pedidos_dto = self._pedido_servicio.obtener_todos_los_pedidos(limite, desplazamiento)
            serializador = PedidoSerializador(pedidos_dto, many=True)
            
            return Response({
                'pedidos': serializador.data,
                'total': len(pedidos_dto),
                'desplazamiento': desplazamiento,
                'limite': limite
            })
            
        except ValueError as e:
            return Response(
                {'error': f'Parámetros inválidos: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        """
        POST /api/pedidos/
        Crea un nuevo pedido
        """
        try:
            serializador = PedidoCrearSerializador(data=request.data)
            
            if not serializador.is_valid():
                return Response(
                    {'error': 'Datos inválidos', 'detalles': serializador.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear DTO desde datos validados
            pedido_crear_dto = PedidoCrearDTO(**serializador.validated_data)
            
            # Crear pedido
            pedido_dto = self._pedido_servicio.crear_pedido(pedido_crear_dto)
            
            # Serializar respuesta
            response_serializador = PedidoSerializador(pedido_dto)
            
            return Response(
                {
                    'mensaje': 'Pedido creado exitosamente',
                    'pedido': response_serializador.data
                },
                status=status.HTTP_201_CREATED
            )
            
        except DominioExcepcion as e:
            return Response(
                {'error': f'Error de validación: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """
        GET /api/pedidos/{id}/
        Obtiene un pedido específico por ID
        """
        try:
            pedido_id = int(pk)
            pedido_dto = self._pedido_servicio.obtener_pedido_por_id(pedido_id)
            
            if not pedido_dto:
                raise Http404("Pedido no encontrado")
            
            serializador = PedidoSerializador(pedido_dto)
            return Response(serializador.data)
            
        except ValueError:
            return Response(
                {'error': 'ID de pedido inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        """
        PUT /api/pedidos/{id}/
        Actualiza un pedido completo
        """
        try:
            pedido_id = int(pk)
            
            serializador = PedidoActualizarSerializador(data=request.data)
            
            if not serializador.is_valid():
                return Response(
                    {'error': 'Datos inválidos', 'detalles': serializador.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear DTO con ID
            datos_actualizacion = serializador.validated_data
            datos_actualizacion['id'] = pedido_id
            pedido_actualizar_dto = PedidoActualizarDTO(**datos_actualizacion)
            
            # Actualizar pedido
            pedido_dto = self._pedido_servicio.actualizar_pedido(pedido_actualizar_dto)
            
            # Serializar respuesta
            response_serializador = PedidoSerializador(pedido_dto)
            
            return Response({
                'mensaje': 'Pedido actualizado exitosamente',
                'pedido': response_serializador.data
            })
            
        except ValueError:
            return Response(
                {'error': 'ID de pedido inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EntidadNoEncontradaExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except DominioExcepcion as e:
            return Response(
                {'error': f'Error de validación: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        """
        DELETE /api/pedidos/{id}/
        Elimina un pedido
        """
        try:
            pedido_id = int(pk)
            eliminado = self._pedido_servicio.eliminar_pedido(pedido_id)
            
            if eliminado:
                return Response(
                    {'mensaje': 'Pedido eliminado exitosamente'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'error': 'Pedido no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except ValueError:
            return Response(
                {'error': 'ID de pedido inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        PATCH /api/pedidos/{id}/cambiar_estado/
        Cambia el estado de un pedido
        """
        try:
            pedido_id = int(pk)
            
            serializador = PedidoCambiarEstadoSerializador(data=request.data)
            
            if not serializador.is_valid():
                return Response(
                    {'error': 'Datos inválidos', 'detalles': serializador.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Crear DTO
            datos_cambio = serializador.validated_data
            datos_cambio['id'] = pedido_id
            cambiar_estado_dto = PedidoCambiarEstadoDTO(**datos_cambio)
            
            # Cambiar estado
            pedido_dto = self._pedido_servicio.cambiar_estado_pedido(cambiar_estado_dto)
            
            # Serializar respuesta
            response_serializador = PedidoSerializador(pedido_dto)
            
            return Response({
                'mensaje': f'Estado del pedido cambiado a {datos_cambio["nuevo_estado"]}',
                'pedido': response_serializador.data
            })
            
        except ValueError:
            return Response(
                {'error': 'ID de pedido inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EntidadNoEncontradaExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except DominioExcepcion as e:
            return Response(
                {'error': f'Error de validación: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """
        GET /api/pedidos/buscar/
        Busca pedidos con múltiples filtros
        """
        try:
            # Construir DTO de búsqueda desde query params
            busqueda_data = {
                'cliente_id': request.query_params.get('cliente_id'),
                'estado': request.query_params.get('estado'),
                'tipo_pedido': request.query_params.get('tipo_pedido'),
                'mesa_id': request.query_params.get('mesa_id'),
                'fecha_inicio': request.query_params.get('fecha_inicio'),
                'fecha_fin': request.query_params.get('fecha_fin'),
                'texto': request.query_params.get('texto'),
                'solo_activos': request.query_params.get('solo_activos', 'false').lower() == 'true',
                'limite': request.query_params.get('limite'),
                'desplazamiento': int(request.query_params.get('desplazamiento', 0))
            }
            
            # Convertir strings a tipos apropiados
            if busqueda_data['cliente_id']:
                busqueda_data['cliente_id'] = int(busqueda_data['cliente_id'])
            
            if busqueda_data['mesa_id']:
                busqueda_data['mesa_id'] = int(busqueda_data['mesa_id'])
            
            if busqueda_data['fecha_inicio']:
                busqueda_data['fecha_inicio'] = date.fromisoformat(busqueda_data['fecha_inicio'])
            
            if busqueda_data['fecha_fin']:
                busqueda_data['fecha_fin'] = date.fromisoformat(busqueda_data['fecha_fin'])
            
            if busqueda_data['limite']:
                busqueda_data['limite'] = int(busqueda_data['limite'])
            
            # Filtrar valores None
            busqueda_data = {k: v for k, v in busqueda_data.items() if v is not None}
            
            busqueda_dto = PedidoBusquedaDTO(**busqueda_data)
            
            # Buscar pedidos
            pedidos_dto = self._pedido_servicio.buscar_pedidos(busqueda_dto)
            
            serializador = PedidoSerializador(pedidos_dto, many=True)
            
            return Response({
                'pedidos': serializador.data,
                'total': len(pedidos_dto),
                'criterios': busqueda_data
            })
            
        except ValueError as e:
            return Response(
                {'error': f'Parámetros inválidos: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """
        GET /api/pedidos/por_cliente/
        Obtiene pedidos de un cliente específico
        """
        try:
            cliente_id = request.query_params.get('cliente_id')
            if not cliente_id:
                return Response(
                    {'error': 'Se requiere cliente_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cliente_id = int(cliente_id)
            pedidos_dto = self._pedido_servicio.obtener_pedidos_por_cliente(cliente_id)
            
            serializador = PedidoSerializador(pedidos_dto, many=True)
            
            return Response({
                'cliente_id': cliente_id,
                'pedidos': serializador.data,
                'total': len(pedidos_dto)
            })
            
        except ValueError:
            return Response(
                {'error': 'cliente_id debe ser un número válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def por_estado(self, request):
        """
        GET /api/pedidos/por_estado/
        Obtiene pedidos por estado
        """
        try:
            estado = request.query_params.get('estado')
            if not estado:
                return Response(
                    {'error': 'Se requiere estado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            pedidos_dto = self._pedido_servicio.obtener_pedidos_por_estado(estado)
            
            serializador = PedidoSerializador(pedidos_dto, many=True)
            
            return Response({
                'estado': estado,
                'pedidos': serializador.data,
                'total': len(pedidos_dto)
            })
            
        except DominioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        GET /api/pedidos/activos/
        Obtiene todos los pedidos activos
        """
        try:
            pedidos_dto = self._pedido_servicio.obtener_pedidos_activos()
            
            serializador = PedidoSerializador(pedidos_dto, many=True)
            
            return Response({
                'pedidos': serializador.data,
                'total': len(pedidos_dto)
            })
            
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def cocina(self, request):
        """
        GET /api/pedidos/cocina/
        Obtiene pedidos optimizados para mostrar en cocina
        """
        try:
            pedidos_cocina = self._pedido_servicio.obtener_pedidos_cocina()
            
            serializador = PedidoCocinaSerializador(pedidos_cocina, many=True)
            
            return Response({
                'pedidos': serializador.data,
                'total': len(pedidos_cocina)
            })
            
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        GET /api/pedidos/estadisticas/
        Obtiene estadísticas de pedidos
        """
        try:
            fecha_inicio = request.query_params.get('fecha_inicio')
            fecha_fin = request.query_params.get('fecha_fin')
            
            if not fecha_inicio:
                return Response(
                    {'error': 'Se requiere fecha_inicio'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            fecha_inicio = date.fromisoformat(fecha_inicio)
            fecha_fin = date.fromisoformat(fecha_fin) if fecha_fin else None
            
            estadisticas_dto = self._pedido_servicio.obtener_estadisticas_pedidos(fecha_inicio, fecha_fin)
            
            serializador = PedidoEstadisticasSerializador(estadisticas_dto)
            
            return Response(serializador.data)
            
        except ValueError as e:
            return Response(
                {'error': f'Formato de fecha inválido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def historial_cliente(self, request):
        """
        GET /api/pedidos/historial_cliente/
        Obtiene el historial de pedidos de un cliente
        """
        try:
            cliente_id = request.query_params.get('cliente_id')
            limite = request.query_params.get('limite')
            
            if not cliente_id:
                return Response(
                    {'error': 'Se requiere cliente_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cliente_id = int(cliente_id)
            limite = int(limite) if limite else None
            
            historial_dto = self._pedido_servicio.obtener_historial_cliente(cliente_id, limite)
            
            serializador = PedidoHistorialSerializador(historial_dto)
            
            return Response(serializador.data)
            
        except ValueError as e:
            return Response(
                {'error': f'Parámetros inválidos: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def validar(self, request):
        """
        POST /api/pedidos/validar/
        Valida un pedido antes de crearlo
        """
        try:
            serializador = PedidoCrearSerializador(data=request.data)
            
            if not serializador.is_valid():
                return Response(
                    {'error': 'Datos inválidos', 'detalles': serializador.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            pedido_crear_dto = PedidoCrearDTO(**serializador.validated_data)
            
            validacion_dto = self._pedido_servicio.validar_pedido(pedido_crear_dto)
            
            serializador_respuesta = PedidoValidacionSerializador(validacion_dto)
            
            return Response(serializador_respuesta.data)
            
        except ServicioExcepcion as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
