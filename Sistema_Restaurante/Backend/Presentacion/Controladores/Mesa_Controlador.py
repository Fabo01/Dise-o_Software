"""
Controlador para la gestión de Mesas en la capa de presentación.
Implementa los endpoints REST para el manejo de mesas del restaurante.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from typing import Dict, Any

from Backend.Aplicacion.DTOs.Mesa_DTO import MesaDTO, CrearMesaDTO, ActualizarMesaDTO
from Backend.Aplicacion.Servicios.Mesa_Servicio import MesaServicio
from Backend.Presentacion.Serializadores.Mesa_Serializador import (
    MesaSerializador, 
    MesaDTOSerializador,
    CrearMesaSerializador, 
    ActualizarMesaSerializador,
    CambiarEstadoMesaSerializador
)
from Backend.Dominio.Excepciones.Mesa_Excepciones import (
    MesaNoEncontradaExcepcion,
    MesaEstadoInvalidoExcepcion,
    MesaOcupadaExcepcion
)


class MesaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión completa de mesas.
    
    Proporciona operaciones CRUD y funcionalidades específicas como:
    - Cambio de estado de mesas
    - Búsqueda por capacidad
    - Obtención de mesas disponibles
    - Estadísticas de ocupación
    """
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mesa_servicio = MesaServicio()
    
    def get_queryset(self):
        """
        Método requerido por Django REST Framework.
        Retorna el queryset base para el ViewSet.
        """
        if hasattr(self, 'swagger_fake_view'):
            # Para la generación de documentación Swagger
            from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
            return MesaModelo.objects.none()
        
        # En operaciones normales, usar el servicio
        return None
    
    def get_serializer_class(self):
        """
        Retorna la clase de serializador apropiada según la acción.
        """
        if self.action == 'create':
            return CrearMesaSerializador
        elif self.action in ['update', 'partial_update']:
            return ActualizarMesaSerializador
        return MesaSerializador
    
    @swagger_auto_schema(
        operation_description="Obtiene la lista de todas las mesas con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('estado', openapi.IN_QUERY, description="Filtrar por estado", type=openapi.TYPE_STRING),
            openapi.Parameter('capacidad_min', openapi.IN_QUERY, description="Capacidad mínima", type=openapi.TYPE_INTEGER),
            openapi.Parameter('capacidad_max', openapi.IN_QUERY, description="Capacidad máxima", type=openapi.TYPE_INTEGER),
            openapi.Parameter('disponible', openapi.IN_QUERY, description="Solo mesas disponibles", type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request):
        """
        Obtiene la lista de mesas con filtros opcionales.
        """
        try:
            filtros = {}
            
            # Aplicar filtros desde query parameters
            if 'estado' in request.GET:
                filtros['estado'] = request.GET['estado']
            
            if 'capacidad_min' in request.GET:
                filtros['capacidad_min'] = int(request.GET['capacidad_min'])
            
            if 'capacidad_max' in request.GET:
                filtros['capacidad_max'] = int(request.GET['capacidad_max'])
            
            if 'disponible' in request.GET:
                filtros['disponible'] = request.GET['disponible'].lower() == 'true'
            
            mesas = self.mesa_servicio.obtener_todas_las_mesas(filtros)
            
            # Convertir entidades a DTOs
            mesas_dto = []
            for mesa in mesas:
                mesa_dto = {
                    'id': mesa.id if hasattr(mesa, 'id') else 0,
                    'numero': mesa.numero,
                    'capacidad': mesa.capacidad,
                    'estado': mesa.estado.value if hasattr(mesa.estado, 'value') else mesa.estado,
                    'ubicacion': mesa.ubicacion,
                    'caracteristicas': mesa.caracteristicas,
                    'tipo_mesa': mesa.tipo_mesa.value if hasattr(mesa.tipo_mesa, 'value') else mesa.tipo_mesa,
                    'activa': mesa.activa,
                    'fecha_creacion': mesa.fecha_creacion if hasattr(mesa, 'fecha_creacion') else None,
                    'fecha_modificacion': mesa.fecha_actualizacion if hasattr(mesa, 'fecha_actualizacion') else None,
                }
                mesas_dto.append(mesa_dto)
            
            serializer = MesaDTOSerializador(mesas_dto, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Mesas obtenidas exitosamente'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al obtener las mesas'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Obtiene una mesa específica por ID"
    )
    def retrieve(self, request, pk=None):
        """
        Obtiene una mesa específica por ID.
        """
        try:
            mesa = self.mesa_servicio.obtener_mesa_por_id(int(pk))
            serializer = MesaSerializador(mesa)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Mesa obtenida exitosamente'
            })
            
        except MesaNoEncontradaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Mesa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al obtener la mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Crea una nueva mesa",
        request_body=CrearMesaSerializador
    )
    def create(self, request):
        """
        Crea una nueva mesa.
        """
        serializer = CrearMesaSerializador(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Datos inválidos para crear la mesa'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Crear DTO desde los datos validados
                mesa_dto = CrearMesaDTO(**serializer.validated_data)
                
                # Crear mesa a través del servicio
                mesa_creada = self.mesa_servicio.crear_mesa(mesa_dto)
                
                # Serializar respuesta
                response_serializer = MesaSerializador(mesa_creada)
                
                return Response({
                    'success': True,
                    'data': response_serializer.data,
                    'message': 'Mesa creada exitosamente'
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al crear la mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Actualiza una mesa existente",
        request_body=ActualizarMesaSerializador
    )
    def update(self, request, pk=None):
        """
        Actualiza una mesa existente.
        """
        serializer = ActualizarMesaSerializador(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Datos inválidos para actualizar la mesa'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Crear DTO desde los datos validados
                mesa_dto = ActualizarMesaDTO(**serializer.validated_data)
                
                # Actualizar mesa a través del servicio
                mesa_actualizada = self.mesa_servicio.actualizar_mesa(int(pk), mesa_dto)
                
                # Serializar respuesta
                response_serializer = MesaSerializador(mesa_actualizada)
                
                return Response({
                    'success': True,
                    'data': response_serializer.data,
                    'message': 'Mesa actualizada exitosamente'
                })
                
        except MesaNoEncontradaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Mesa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al actualizar la mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Elimina una mesa",
        responses={204: "Mesa eliminada exitosamente"}
    )
    def destroy(self, request, pk=None):
        """
        Elimina una mesa.
        """
        try:
            self.mesa_servicio.eliminar_mesa(int(pk))
            
            return Response({
                'success': True,
                'message': 'Mesa eliminada exitosamente'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except MesaNoEncontradaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Mesa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        except MesaOcupadaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'No se puede eliminar una mesa ocupada'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al eliminar la mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        method='post',
        operation_description="Cambia el estado de una mesa",
        request_body=CambiarEstadoMesaSerializador,
        responses={
            200: openapi.Response('Estado cambiado exitosamente', MesaSerializador),
            400: 'Estado inválido',
            404: 'Mesa no encontrada'
        }
    )
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado de una mesa específica.
        """
        serializer = CambiarEstadoMesaSerializador(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Estado inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nuevo_estado = serializer.validated_data['estado']
            mesa_actualizada = self.mesa_servicio.cambiar_estado_mesa(int(pk), nuevo_estado)
            
            response_serializer = MesaSerializador(mesa_actualizada)
            
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': f'Estado de mesa cambiado a {nuevo_estado}'
            })
            
        except MesaNoEncontradaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Mesa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        except MesaEstadoInvalidoExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Estado de mesa inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al cambiar el estado de la mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene las mesas disponibles",
        manual_parameters=[
            openapi.Parameter('capacidad_min', openapi.IN_QUERY, description="Capacidad mínima requerida", type=openapi.TYPE_INTEGER),
        ]
    )
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Obtiene todas las mesas disponibles opcionalmente filtradas por capacidad.
        """
        try:
            capacidad_min = request.GET.get('capacidad_min')
            if capacidad_min:
                capacidad_min = int(capacidad_min)
            
            mesas_disponibles = self.mesa_servicio.obtener_mesas_disponibles(capacidad_min)
            serializer = MesaSerializador(mesas_disponibles, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Mesas disponibles obtenidas exitosamente'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al obtener mesas disponibles'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene estadísticas de ocupación de mesas"
    )
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Obtiene estadísticas de ocupación de mesas.
        """
        try:
            estadisticas = self.mesa_servicio.obtener_estadisticas_mesas()
            
            return Response({
                'success': True,
                'data': estadisticas,
                'message': 'Estadísticas obtenidas exitosamente'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al obtener estadísticas'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        method='post',
        operation_description="Asigna una mesa a un pedido",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'pedido_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del pedido')
            }
        )
    )
    @action(detail=True, methods=['post'])
    def asignar_pedido(self, request, pk=None):
        """
        Asigna un pedido a una mesa específica.
        """
        try:
            pedido_id = request.data.get('pedido_id')
            if not pedido_id:
                return Response({
                    'success': False,
                    'message': 'pedido_id es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            mesa_actualizada = self.mesa_servicio.asignar_pedido_a_mesa(int(pk), int(pedido_id))
            serializer = MesaSerializador(mesa_actualizada)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Pedido asignado a mesa exitosamente'
            })
            
        except MesaNoEncontradaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Mesa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al asignar pedido a mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        method='post',
        operation_description="Libera una mesa (la marca como disponible)"
    )
    @action(detail=True, methods=['post'])
    def liberar(self, request, pk=None):
        """
        Libera una mesa marcándola como disponible.
        """
        try:
            mesa_liberada = self.mesa_servicio.liberar_mesa(int(pk))
            serializer = MesaSerializador(mesa_liberada)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Mesa liberada exitosamente'
            })
            
        except MesaNoEncontradaExcepcion as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Mesa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Error al liberar mesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
