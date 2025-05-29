from django.db.models import Q

from Backend.Dominio.Entidades.Usuario_Entidad import UsuarioEntidad
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo
from Backend.Aplicacion.Interfaces.IUsuario_Repositorio import IUsuarioRepositorio

class UsuarioRepositorio(IUsuarioRepositorio):
    
    def guardar(self, usuario):
        if usuario is None:
            raise ValueError("No se puede guardar un usuario nulo")
        if usuario.id:
            try:
                usuario_modelo = UsuarioModelo.objects.get(id=usuario.id)
            except UsuarioModelo.DoesNotExist:
                raise ValueError("Usuario no encontrado para actualizar")
            usuario_modelo.username = usuario.username
            usuario_modelo.password = usuario.password
            usuario_modelo.email = usuario.email.valor if hasattr(usuario.email, 'valor') else usuario.email
            usuario_modelo.nombre = usuario.nombre
            usuario_modelo.apellido = usuario.apellido
            usuario_modelo.rol = usuario.rol
            # Siempre guardar el teléfono con el formato de TelefonoVO
            usuario_modelo.telefono = usuario.telefono.valor if hasattr(usuario.telefono, 'valor') else str(usuario.telefono)
            usuario_modelo.fecha_registro = usuario.fecha_registro
            usuario_modelo.ultima_sesion = usuario.ultima_sesion
            usuario_modelo.direccion = usuario.direccion
            usuario_modelo.save()
        else:
            usuario_modelo = UsuarioModelo.objects.create(
                username=usuario.username,
                password=usuario.password,
                email=usuario.email.valor,
                nombre=usuario.nombre,
                apellido=usuario.apellido,
                rol=usuario.rol,
                # Siempre guardar el teléfono con el formato de TelefonoVO
                telefono=usuario.telefono.valor,
                fecha_registro=usuario.fecha_registro,
                ultima_sesion=usuario.ultima_sesion,
                direccion=usuario.direccion
            )
            usuario.id = usuario_modelo.id
        return self._convertir_a_entidad(usuario_modelo)
    
    def buscar_por_id(self, id):
        try:
            usuario_modelo = UsuarioModelo.objects.get(id=id)
            return self._convertir_a_entidad(usuario_modelo)
        except UsuarioModelo.DoesNotExist:
            return None
        
    def buscar_por_username(self, username):
        try:
            usuario_modelo = UsuarioModelo.objects.get(username=username)
            return self._convertir_a_entidad(usuario_modelo)
        except UsuarioModelo.DoesNotExist:
            return None
        
    def listar_todos(self):
        usuarios_modelo = UsuarioModelo.objects.all()
        return [self._convertir_a_entidad(usuario) for usuario in usuarios_modelo]
    
    def eliminar(self, id):
        try:
            usuario_modelo = UsuarioModelo.objects.get(id=id)
            usuario_modelo.delete()
            return True
        except UsuarioModelo.DoesNotExist:
            return False
        
    def _convertir_a_entidad(self, usuario_modelo):
        entidad = UsuarioEntidad(
            username=usuario_modelo.username,
            password=usuario_modelo.password,
            email=usuario_modelo.email.value,
            nombre=usuario_modelo.nombre,
            apellido=usuario_modelo.apellido,
            rol=usuario_modelo.rol,
            telefono=usuario_modelo.telefono.value,
            fecha_registro=usuario_modelo.fecha_registro,
            ultima_sesion=usuario_modelo.ultima_sesion,
            direccion=usuario_modelo.direccion
        )
        entidad.id = usuario_modelo.id
        return entidad
