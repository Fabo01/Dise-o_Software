from django.db.models import Q
from datetime import datetime

from Backend.Dominio.Entidades.Usuario_Entidad import UsuarioEntidad
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo
from Backend.Aplicacion.Interfaces.Usuario_Repositorio_Interfaz import IUsuarioRepositorio

class UsuarioRepositorio(IUsuarioRepositorio):
    
    def guardar(self, usuario):
        if usuario.id:
            usuario_modelo = UsuarioModelo.get(id=usuario.id)
            usuario_modelo.username = usuario.username
            usuario_modelo.password = usuario.password
            usuario_modelo.mail = usuario.mail
            usuario_modelo.nombre = usuario.nombre
            usuario_modelo.apellido = usuario.apellido
            usuario_modelo.rol = usuario.rol
            usuario_modelo.telefono = usuario.telefono
            usuario_modelo.fecha_registro = usuario.fecha_registro
            usuario_modelo.ultima_sesion = usuario.ultima_sesion
            usuario_modelo.save()
        else:
            usuario_modelo = UsuarioModelo.objects.create(
                username=usuario.username,
                password=usuario.password,
                mail=usuario.mail,
                nombre=usuario.nombre,
                apellido=usuario.apellido,
                rol=usuario.rol,
                telefono=usuario.telefono,
                fecha_registro=usuario.fecha_registro,
                ultima_sesion=usuario.ultima_sesion
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
        return UsuarioEntidad(
            id=usuario_modelo.id,
            username=usuario_modelo.username,
            password=usuario_modelo.password,
            mail=usuario_modelo.mail,
            nombre=usuario_modelo.nombre,
            apellido=usuario_modelo.apellido,
            rol=usuario_modelo.rol,
            telefono=usuario_modelo.telefono,
            fecha_registro=usuario_modelo.fecha_registro,
            ultima_sesion=usuario_modelo.ultima_sesion
        )
