from Backend.Dominio.Objetos_Valor.Correo_VO import CorreoVO
from Backend.Infraestructura.Repositorios.Usuario_Repositorio import UsuarioRepositorio
from Backend.Aplicacion.Servicios.Observer_Servicio import ObserverServicio
from Backend.Dominio.Factories.Usuario_Factory import UsuarioFactory  # Importa la factory

class UsuarioServicio:
    """
    Servicio que implementa los casos de uso relacionados con la gestión de usuarios.
    """
    def __init__(self, usuario_repositorio, observer_service=None):
        # Inyección de dependencias (Dependency Injection)
        self.usuario_repositorio = usuario_repositorio
        self.observer_service = observer_service or ObserverServicio()
        self.usuario_factory = UsuarioFactory()

    def registrar_usuario(self, datos_usuario):
        usuario = self.usuario_factory.crear(**datos_usuario)
        usuario_guardado = self.usuario_repositorio.guardar(usuario)
        self.observer_service.notificar("Usuario registrado", usuario_guardado)
        return usuario_guardado

    def obtener_usuario(self, rut):
        usuario = self.usuario_repositorio.buscar_por_rut(rut)
        if usuario is None:
            raise ValueError("Usuario no encontrado")
        return usuario
    
    def buscar_usuario_por_correo(self, correo):
        return self.usuario_repositorio.buscar_por_correo(correo)
    
    def listar_usuarios(self):
        return self.usuario_repositorio.listar_todos()
    
    def eliminar_usuario(self, rut):
        if self.usuario_repositorio.eliminar(rut):
            self.observer_service.notificar("Usuario eliminado", rut)
            return True
        return False
    
    def actualizar_usuario(self, rut, datos_usuario):
        usuario = self.usuario_repositorio.buscar_por_rut(rut)
        if usuario is None:
            raise ValueError("Usuario no encontrado")
        
        # Actualiza solo los campos permitidos usando el método de la entidad
        usuario.actualizar_datos(
            nombre=datos_usuario.get('nombre'),
            apellido=datos_usuario.get('apellido'),
            email=datos_usuario.get('email'),
            telefono=datos_usuario.get('telefono'),
            rol=datos_usuario.get('rol'),
            direccion=datos_usuario.get('direccion')
        )
        # Si se quiere actualizar la contraseña:
        if 'password' in datos_usuario and datos_usuario['password']:
            usuario.password = datos_usuario['password']

        self.usuario_repositorio.guardar(usuario)
        self.observer_service.notificar("Usuario actualizado", usuario)
        return usuario
    
    def autenticar_usuario(self, username, password):
        usuario = self.usuario_repositorio.buscar_por_username(username)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        if usuario.password != password:
            raise ValueError("Contraseña incorrecta")
        self.observer_service.notificar("Usuario autenticado", usuario)
        return usuario
    
    def cambiar_contrasena(self, id, nueva_contrasena):
        """
        Cambia la contraseña de un usuario.
        Args:
            id (int): ID del usuario
            nueva_contrasena (str): Nueva contraseña en texto plano
        Returns:
            UsuarioEntidad: El usuario con la contraseña actualizada
        Raises:
            ValueError: Si el usuario no existe o la contraseña es inválida
        """
        usuario = self.usuario_repositorio.buscar_por_id(id)
        if usuario is None:
            raise ValueError("Usuario no encontrado")
        if not nueva_contrasena or len(nueva_contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        usuario.password = nueva_contrasena  # Setter encripta
        self.usuario_repositorio.guardar(usuario)
        self.observer_service.notificar("Contraseña actualizada", usuario)
        return usuario



