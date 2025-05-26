from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo
from Backend.Presentacion.Serializadores.Usuario_Serializador import UsuarioSerializador
from Backend.Aplicacion.Servicios.Usuario_Servicio import UsuarioServicio
from Backend.Infraestructura.Repositorios.Usuario_Repositorio import UsuarioRepositorio

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoints para la gestión de usuarios
    """
    queryset = UsuarioModelo.objects.all()
    serializer_class = UsuarioSerializador

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            usuario = UsuarioServicio(UsuarioRepositorio()).registrar_usuario(serializer.validated_data)
            return Response(
                UsuarioSerializador(UsuarioModelo.objects.get(id=usuario.id)).data,
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            usuario = UsuarioServicio(UsuarioRepositorio()).actualizar_usuario(instance.id, serializer.validated_data)
            return Response(UsuarioSerializador(usuario).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            UsuarioServicio(UsuarioRepositorio()).eliminar_usuario(instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """
        Búsqueda de usuarios por criterios (nombre, username o email)
        """
        criterio = request.query_params.get('q', '')
        if not criterio:
            return Response(self.get_serializer(self.get_queryset(), many=True).data)
        queryset = UsuarioModelo.objects.filter(
            models.Q(nombre__icontains=criterio) |
            models.Q(username__icontains=criterio) |
            models.Q(email__icontains=criterio)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
