from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Backend.Aplicacion.Servicios.Usuario_Servicio import UsuarioServicio
from Backend.Infraestructura.Repositorios.Usuario_Repositorio import UsuarioRepositorio
from Backend.Presentacion.Serializadores.Usuario_Serializador import UsuarioSerializador
from Backend.Aplicacion.Servicios.ConsoleNotificationObserver import ConsoleNotificationObserver
from Backend.Aplicacion.Servicios.Observer_Servicio import ObserverServicio

class UsuarioAPI(APIView):
    """
    Controlador para la gestión de usuarios.
    Permite operaciones CRUD sobre los usuarios.
    """
    observer_service = ObserverServicio()
    observer_registrado = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias
        self.servicio_usuario = UsuarioServicio(UsuarioRepositorio())
        # Registrar observer solo una vez
        if not UsuarioAPI.observer_registrado:
            UsuarioAPI.observer_service.registrar_observador(ConsoleNotificationObserver())
            UsuarioAPI.observer_registrado = True

    def get(self, request, rut=None):
        """
        Obtener uno o todos los usuarios.
        Si se proporciona rut, retorna un usuario específico.
        """
        if rut:
            usuario = self.servicio_usuario.obtener_usuario(rut)
            if usuario:
                serializador = UsuarioSerializador(usuario)
                return Response(serializador.data, status=status.HTTP_200_OK)
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                usuarios = self.servicio_usuario.listar_usuarios()
                if isinstance(usuarios, set):
                    usuarios = list(usuarios)
                elif not isinstance(usuarios, list):
                    usuarios = list(usuarios)
                serializer = UsuarioSerializador(usuarios, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Crear un nuevo usuario.
        """
        serializador = UsuarioSerializador(data=request.data)
        if serializador.is_valid():
            usuario = self.servicio_usuario.crear_usuario(serializador.validated_data)
            UsuarioAPI.observer_service.notificar("Usuario creado exitosamente.")
            return Response(UsuarioSerializador(usuario).data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, rut):
        """
        Actualizar un usuario existente.
        """
        if not rut:
            return Response({"error": "Se requiere el RUT del usuario para actualizar."}, status=status.HTTP_400_BAD_REQUEST)
        usuario = self.servicio_usuario.obtener_usuario(rut)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializador = UsuarioSerializador(usuario, data=request.data, partial=True)
        if serializador.is_valid():
            usuario_actualizado = self.servicio_usuario.actualizar_usuario(rut, serializador.validated_data)
            UsuarioAPI.observer_service.notificar("Usuario actualizado exitosamente.")
            return Response(UsuarioSerializador(usuario_actualizado).data, status=status.HTTP_200_OK)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, rut):
        """
        Eliminar un usuario existente.
        """
        if not rut:
            return Response({"error": "Se requiere el RUT del usuario para eliminar."}, status=status.HTTP_400_BAD_REQUEST)
        eliminado = self.servicio_usuario.eliminar_usuario(rut)
        if eliminado:
            UsuarioAPI.observer_service.notificar("Usuario eliminado exitosamente.")
            return Response({"mensaje": "Usuario eliminado"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id=None):
        """
        Permite cambiar la contraseña de un usuario.
        Espera {"nueva_contrasena": "...}
        """
        if not id:
            return Response({"error": "Se requiere el ID del usuario para cambiar la contraseña."}, status=status.HTTP_400_BAD_REQUEST)
        nueva_contrasena = request.data.get("nueva_contrasena")
        if not nueva_contrasena:
            return Response({"error": "Debe proporcionar la nueva contraseña."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            usuario_actualizado = self.servicio_usuario.cambiar_contrasena(id, nueva_contrasena)
            UsuarioAPI.observer_service.notificar("Contraseña cambiada exitosamente.")
            return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

