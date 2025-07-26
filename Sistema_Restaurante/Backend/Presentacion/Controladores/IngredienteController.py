"""
Controlador para gestión de ingredientes
Implementa endpoints RESTful para operaciones CRUD
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models

from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Presentacion.Serializadores.IngredienteSerializer import IngredienteSerializer


class IngredienteController(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ingredientes
    Proporciona operaciones CRUD completas
    """
    queryset = IngredienteModelo.objects.all()
    serializer_class = IngredienteSerializer
    lookup_field = 'pk'
    
    def list(self, request):
        """Listar todos los ingredientes"""
        ingredientes = self.get_queryset()
        serializer = self.get_serializer(ingredientes, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': ingredientes.count()
        })
    
    def create(self, request):
        """Crear un nuevo ingrediente"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ingrediente = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Ingrediente creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Error al crear ingrediente',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Obtener un ingrediente específico"""
        ingrediente = get_object_or_404(IngredienteModelo, pk=pk)
        serializer = self.get_serializer(ingrediente)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def update(self, request, pk=None):
        """Actualizar un ingrediente completamente"""
        ingrediente = get_object_or_404(IngredienteModelo, pk=pk)
        serializer = self.get_serializer(ingrediente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Ingrediente actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Error al actualizar ingrediente',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """Actualizar un ingrediente parcialmente"""
        ingrediente = get_object_or_404(IngredienteModelo, pk=pk)
        serializer = self.get_serializer(ingrediente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Ingrediente actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Error al actualizar ingrediente',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """Eliminar un ingrediente"""
        ingrediente = get_object_or_404(IngredienteModelo, pk=pk)
        ingrediente.delete()
        return Response({
            'status': 'success',
            'message': 'Ingrediente eliminado exitosamente'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Buscar ingredientes por nombre o categoría"""
        query = request.query_params.get('q', '')
        categoria = request.query_params.get('categoria', '')
        
        ingredientes = self.get_queryset()
        
        if query:
            ingredientes = ingredientes.filter(nombre__icontains=query)
        
        if categoria:
            ingredientes = ingredientes.filter(categoria__icontains=categoria)
        
        serializer = self.get_serializer(ingredientes, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': ingredientes.count(),
            'query': query,
            'categoria': categoria
        })
    
    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        """Obtener ingredientes con stock bajo (en nivel crítico)"""
        ingredientes = self.get_queryset().filter(
            cantidad__lte=models.F('nivel_critico')
        )
        
        serializer = self.get_serializer(ingredientes, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': ingredientes.count(),
            'message': f'Se encontraron {ingredientes.count()} ingredientes con stock bajo'
        })
    
    @action(detail=False, methods=['get'])
    def categorias(self, request):
        """Obtener todas las categorías de ingredientes disponibles"""
        categorias = IngredienteModelo.objects.values_list('categoria', flat=True).distinct()
        return Response({
            'status': 'success',
            'data': list(categorias),
            'count': len(categorias)
        })
    
    @action(detail=True, methods=['post'])
    def ajustar_stock(self, request, pk=None):
        """Ajustar el stock de un ingrediente"""
        ingrediente = get_object_or_404(IngredienteModelo, pk=pk)
        
        tipo_ajuste = request.data.get('tipo')  # 'suma' o 'resta'
        cantidad = request.data.get('cantidad', 0)
        motivo = request.data.get('motivo', '')
        
        try:
            cantidad = float(cantidad)
        except (ValueError, TypeError):
            return Response({
                'status': 'error',
                'message': 'La cantidad debe ser un número válido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if tipo_ajuste == 'suma':
            ingrediente.cantidad += cantidad
        elif tipo_ajuste == 'resta':
            if ingrediente.cantidad >= cantidad:
                ingrediente.cantidad -= cantidad
            else:
                return Response({
                    'status': 'error',
                    'message': f'No hay suficiente stock. Stock actual: {ingrediente.cantidad}'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'error',
                'message': 'Tipo de ajuste inválido. Use "suma" o "resta"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ingrediente.save()
        
        # Aquí se podría registrar el movimiento en un log de inventario
        
        serializer = self.get_serializer(ingrediente)
        return Response({
            'status': 'success',
            'message': f'Stock ajustado exitosamente. {tipo_ajuste.title()}: {cantidad}',
            'data': serializer.data,
            'motivo': motivo
        })
