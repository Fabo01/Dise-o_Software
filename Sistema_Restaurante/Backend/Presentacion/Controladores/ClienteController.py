"""
Controlador para gestión de clientes
Implementa endpoints RESTful para operaciones CRUD
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models

from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Presentacion.Serializadores.ClienteSerializer import ClienteSerializer


class ClienteController(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes
    Proporciona operaciones CRUD completas
    """
    queryset = ClienteModelo.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = 'rut'
    
    def list(self, request):
        """Listar todos los clientes"""
        clientes = self.get_queryset()
        serializer = self.get_serializer(clientes, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': clientes.count()
        })
    
    def create(self, request):
        """Crear un nuevo cliente"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Cliente creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Error al crear cliente',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, rut=None):
        """Obtener un cliente específico por RUT"""
        cliente = get_object_or_404(ClienteModelo, rut=rut)
        serializer = self.get_serializer(cliente)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def update(self, request, rut=None):
        """Actualizar un cliente completamente"""
        cliente = get_object_or_404(ClienteModelo, rut=rut)
        serializer = self.get_serializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Cliente actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Error al actualizar cliente',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, rut=None):
        """Actualizar un cliente parcialmente"""
        cliente = get_object_or_404(ClienteModelo, rut=rut)
        serializer = self.get_serializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Cliente actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Error al actualizar cliente',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, rut=None):
        """Eliminar un cliente"""
        cliente = get_object_or_404(ClienteModelo, rut=rut)
        cliente.delete()
        return Response({
            'status': 'success',
            'message': 'Cliente eliminado exitosamente'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Buscar clientes por nombre o correo"""
        query = request.query_params.get('q', '')
        if query:
            clientes = self.get_queryset().filter(
                models.Q(nombre__icontains=query) | 
                models.Q(correo__icontains=query)
            )
        else:
            clientes = self.get_queryset()
        
        serializer = self.get_serializer(clientes, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': clientes.count(),
            'query': query
        })
    
    @action(detail=True, methods=['get'])
    def pedidos(self, request, rut=None):
        """Obtener pedidos de un cliente específico"""
        cliente = get_object_or_404(ClienteModelo, rut=rut)
        pedidos = cliente.pedidos.all().order_by('-fecha_creacion')
        
        from Backend.Presentacion.Serializadores.PedidoSerializer import PedidoSerializer
        serializer = PedidoSerializer(pedidos, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': pedidos.count(),
            'cliente': ClienteSerializer(cliente).data
        })
