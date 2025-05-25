from Backend.Dominio.Entidades.Usuario_Entidad import UsuarioEntidad
from Sistema_Restaurante.Backend.Dominio.Interfaces.IEntidad_Factory import IEntidadFactory

class UsuarioFactory(IEntidadFactory):

    def crear(self, username, password, mail, nombre, apellido, rol, telefono, fecha_registro, ultima_sesion):
        return UsuarioEntidad(username=username, 
                              password=password,
                              mail=mail, 
                              nombre=nombre, 
                              apellido= apellido,
                              rol=rol,
                              telefono=telefono,
                              fecha_registro=fecha_registro,
                              ultima_sesion=ultima_sesion)