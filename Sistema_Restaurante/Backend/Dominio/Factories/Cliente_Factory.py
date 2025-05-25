from Backend.Dominio.Interfaces.IEntidad_Factory import IEntidadFactory
from Backend.Dominio.Entidades.Cliente_Entidad import ClienteEntidad

class ClienteFactory(IEntidadFactory):
    '''
    Clase para crear instancias de la entidad Cliente.
    '''
    def crear(self, nombre, correo, rut, telefono, direccion):
        return ClienteEntidad(nombre=nombre, correo=correo, rut=rut, telefono=telefono, direccion=direccion)
