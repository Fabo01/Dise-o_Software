from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
from typing import List

from ..Serializadores.Menu_Serializador import (
    MenuSerializador, MenuCrearSerializador, MenuActualizarSerializador,
    MenuBusquedaSerializador, MenuEstadisticasSerializador
)
from ...Aplicacion.DTOs.MenuDTO import (
    MenuCrearDTO, MenuActualizarDTO, MenuBusquedaDTO
)
from ...Aplicacion.Excepciones.AplicacionExcepcion import (
    ServicioExcepcion, EntidadNoEncontradaExcepcion, ConflictoExcepcion
)


class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar menús.
    Proporciona operaciones CRUD y funcionalidades adicionales para menús.
    """
    
    serializer_class = MenuSerializador
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias - Importar aquí para evitar problemas de inicialización
        from Backend.Infraestructura.Repositorios.Menu_Repositorio import MenuRepositorio
        from Backend.Infraestructura.Repositorios.Ingrediente_Repositorio import IngredienteRepositorio
        from Backend.Aplicacion.Servicios.Menu_Servicio import MenuServicio
        
        menu_repositorio = MenuRepositorio()
        ingrediente_repositorio = IngredienteRepositorio()
        self.menu_servicio = MenuServicio(menu_repositorio, ingrediente_repositorio)
    
    def get_queryset(self):
        """
        Método requerido por Django REST Framework.
        Retorna el queryset base para el ViewSet.
        """
        if hasattr(self, 'swagger_fake_view'):
            # Para la generación de documentación Swagger
            from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
            return MenuModelo.objects.none()
        
        # En operaciones normales, usar el servicio
        return None
    
    def get_serializer_class(self):
        """Retorna la clase de serializador apropiada según la acción."""
        if self.action == 'create':
            return MenuCrearSerializador
        elif self.action in ['update', 'partial_update']:
            return MenuActualizarSerializador
        elif self.action == 'buscar':
            return MenuBusquedaSerializador
        elif self.action == 'estadisticas':
            return MenuEstadisticasSerializador
        return self.serializer_class
    
    def list(self, request):
        """
        Lista todos los menús.
        
        GET /api/menus/
        """
        try:
            menus = self.menu_servicio.listar_menus()
            serializer = self.get_serializer(menus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """
        Crea un nuevo menú.
        
        POST /api/menus/
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Convertir a DTO
            menu_data = MenuCrearDTO(
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data['descripcion'],
                precio=Decimal(str(serializer.validated_data['precio'])),
                categoria=serializer.validated_data.get('categoria', ''),
                tipo=serializer.validated_data.get('tipo', ''),
                imagen=serializer.validated_data.get('imagen', ''),
                tiempo_preparacion=serializer.validated_data.get('tiempo_preparacion', 15)
            )
            
            # Crear menú usando el servicio
            menu_creado = self.menu_servicio.crear_menu(menu_data)
            
            # Serializar la respuesta
            response_serializer = MenuSerializador(menu_creado)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except ConflictoExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_409_CONFLICT
            )
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        """
        Obtiene un menú específico.
        
        GET /api/menus/{id}/
        """
        try:
            menu = self.menu_servicio.obtener_menu_por_id(int(pk))
            if menu is None:
                return Response(
                    {"error": "Menú no encontrado"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = self.get_serializer(menu)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response(
                {"error": "ID inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """
        Actualiza un menú completo.
        
        PUT /api/menus/{id}/
        """
        return self._actualizar_menu(request, pk, parcial=False)
    
    def partial_update(self, request, pk=None):
        """
        Actualiza parcialmente un menú.
        
        PATCH /api/menus/{id}/
        """
        return self._actualizar_menu(request, pk, parcial=True)
    
    def _actualizar_menu(self, request, pk, parcial=False):
        """Método auxiliar para actualizar menús."""
        try:
            serializer = self.get_serializer(data=request.data, partial=parcial)
            serializer.is_valid(raise_exception=True)
            
            # Convertir a DTO
            datos_actualizacion = MenuActualizarDTO()
            validated_data = serializer.validated_data
            
            if 'nombre' in validated_data:
                datos_actualizacion.nombre = validated_data['nombre']
            if 'descripcion' in validated_data:
                datos_actualizacion.descripcion = validated_data['descripcion']
            if 'precio' in validated_data:
                datos_actualizacion.precio = Decimal(str(validated_data['precio']))
            if 'categoria' in validated_data:
                datos_actualizacion.categoria = validated_data['categoria']
            if 'tipo' in validated_data:
                datos_actualizacion.tipo = validated_data['tipo']
            if 'imagen' in validated_data:
                datos_actualizacion.imagen = validated_data['imagen']
            if 'disponible' in validated_data:
                datos_actualizacion.disponible = validated_data['disponible']
            if 'tiempo_preparacion' in validated_data:
                datos_actualizacion.tiempo_preparacion = validated_data['tiempo_preparacion']
            
            # Actualizar usando el servicio
            menu_actualizado = self.menu_servicio.actualizar_menu(int(pk), datos_actualizacion)
            
            # Serializar la respuesta
            response_serializer = MenuSerializador(menu_actualizado)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except EntidadNoEncontradaExcepcion:
            return Response(
                {"error": "Menú no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ConflictoExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_409_CONFLICT
            )
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk=None):
        """
        Elimina un menú.
        
        DELETE /api/menus/{id}/
        """
        try:
            eliminado = self.menu_servicio.eliminar_menu(int(pk))
            if eliminado:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Menú no encontrado"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except ValueError:
            return Response(
                {"error": "ID inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Obtiene menús disponibles.
        
        GET /api/menus/disponibles/
        """
        try:
            menus = self.menu_servicio.obtener_menus_disponibles()
            serializer = self.get_serializer(menus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def buscar(self, request):
        """
        Busca menús según criterios.
        
        POST /api/menus/buscar/
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Convertir a DTO
            criterios = MenuBusquedaDTO(
                texto=serializer.validated_data.get('texto'),
                categoria=serializer.validated_data.get('categoria'),
                tipo=serializer.validated_data.get('tipo'),
                precio_min=serializer.validated_data.get('precio_min'),
                precio_max=serializer.validated_data.get('precio_max'),
                disponible=serializer.validated_data.get('disponible')
            )
            
            menus = self.menu_servicio.buscar_menus(criterios)
            response_serializer = MenuSerializador(menus, many=True)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def verificar_disponibilidad(self, request, pk=None):
        """
        Verifica la disponibilidad de un menú.
        
        GET /api/menus/{id}/verificar_disponibilidad/
        """
        try:
            disponibilidad = self.menu_servicio.verificar_disponibilidad_menu(int(pk))
            return Response({
                "disponible": disponibilidad.disponible,
                "razon_no_disponible": disponibilidad.razon_no_disponible,
                "ingredientes_faltantes": disponibilidad.ingredientes_faltantes
            }, status=status.HTTP_200_OK)
            
        except EntidadNoEncontradaExcepcion:
            return Response(
                {"error": "Menú no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Obtiene estadísticas de menús.
        
        GET /api/menus/estadisticas/
        """
        try:
            estadisticas = self.menu_servicio.obtener_estadisticas_menus()
            serializer = self.get_serializer(estadisticas)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """
        Obtiene menús filtrados por categoría.
        
        GET /api/menus/por_categoria/?categoria=entrada
        """
        try:
            categoria = request.query_params.get('categoria')
            if not categoria:
                return Response(
                    {"error": "Parámetro 'categoria' es requerido"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            menus = self.menu_servicio.obtener_menus_por_categoria(categoria)
            serializer = self.get_serializer(menus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def populares(self, request):
        """
        Obtiene menús más populares.
        
        GET /api/menus/populares/?limite=5
        """
        try:
            limite = int(request.query_params.get('limite', 10))
            menus = self.menu_servicio.obtener_menus_por_popularidad(limite)
            serializer = self.get_serializer(menus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response(
                {"error": "El parámetro 'limite' debe ser un número entero"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ServicioExcepcion as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
