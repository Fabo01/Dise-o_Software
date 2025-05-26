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
        self.usuario_repositorio.guardar(usuario)
        self.observer_service.notificar("Usuario registrado", usuario)

    def obtener_usuario(self, id):
        return self.usuario_repositorio.buscar_por_id(id)
    
    def buscar_usuario_por_correo(self, correo):
        return self.usuario_repositorio.buscar_por_correo(correo)
    
    def listar_usuarios(self):
        return self.usuario_repositorio.listar_todos()
    
    def eliminar_usuario(self, id):
        if self.usuario_repositorio.eliminar(id):
            self.observer_service.notificar("Usuario eliminado", id)
            return True
        return False
    
    def actualizar_usuario(self, id, datos_usuario):
        usuario = self.usuario_repositorio.buscar_por_id(id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        for key, value in datos_usuario.items():
            setattr(usuario, key, value)
        
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



