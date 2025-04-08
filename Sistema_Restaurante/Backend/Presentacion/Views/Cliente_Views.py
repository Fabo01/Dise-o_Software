from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Presentacion.Serializadores.Cliente_Serializador import ClienteSerializador
from Backend.Aplicacion.Servicios.Cliente_Servicio import ClienteServicio
from Backend.Infraestructura.Repositorios.Cliente_Repositorio import ClienteRepositorio  # Add this import

class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoints para la gestión de clientes
    """
    queryset = ClienteModelo.objects.filter(estado='activo')
    serializer_class = ClienteSerializador
    
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo cliente
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Pass validated data to registrar_cliente
            cliente = ClienteServicio(ClienteRepositorio()).registrar_cliente(serializer.validated_data)
            return Response(
                ClienteSerializador(ClienteModelo.objects.get(id=cliente.id)).data,
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, *args, **kwargs):
        """
        Actualiza un cliente existente
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Llama al servicio con los argumentos correctos
            cliente = ClienteServicio(ClienteRepositorio()).actualizar_cliente(instance.id, serializer.validated_data)
            return Response(ClienteSerializador(cliente).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """
        Eliminación lógica del cliente
        """
        instance = self.get_object()
        try:
            ClienteServicio(ClienteRepositorio()).eliminar_cliente(instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """
        Búsqueda de clientes por criterios
        """
        criterio = request.query_params.get('q', '')
        if not criterio:
            return Response(self.get_serializer(self.get_queryset(), many=True).data)
            
        queryset = ClienteModelo.objects.filter(
            estado='activo',
        ).filter(
            models.Q(nombre__icontains=criterio) | 
            models.Q(rut__icontains=criterio)
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
