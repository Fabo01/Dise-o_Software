from django.db.models import Q
from datetime import datetime

from Backend.Dominio.Entidades.Cliente_Entidad import Cliente
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

class ClienteRepositorio:
    """
    Implementación concreta del repositorio de clientes usando Django ORM.
    """
    
    def guardar(self, cliente):
        """
        Guarda o actualiza un cliente en la base de datos
        """
        if cliente.id:
            cliente_modelo = ClienteModelo.objects.get(id=cliente.id)
            cliente_modelo.nombre = cliente.nombre
            cliente_modelo.correo = cliente.correo
            cliente_modelo.rut = cliente.rut
            cliente_modelo.telefono = cliente.telefono
            cliente_modelo.direccion = cliente.direccion
            cliente_modelo.estado = cliente.estado
            cliente_modelo.ultima_visita = cliente.ultima_visita
            cliente_modelo.save()
        else:
            cliente_modelo = ClienteModelo.objects.create(
                nombre=cliente.nombre,
                correo=cliente.correo,
                rut=cliente.rut,
                telefono=cliente.telefono,
                direccion=cliente.direccion,
                estado=cliente.estado,
                ultima_visita=cliente.ultima_visita
            )
            cliente.id = cliente_modelo.id
        
        return self._convertir_a_entidad(cliente_modelo)
        
    def buscar_por_id(self, id):
        """
        Busca un cliente por su ID
        """
        try:
            cliente_modelo = ClienteModelo.objects.get(id=id)
            return self._convertir_a_entidad(cliente_modelo)
        except ClienteModelo.DoesNotExist:
            return None
            
    def buscar_por_rut(self, rut):
        """
        Busca un cliente por su RUT
        """
        try:
            cliente_modelo = ClienteModelo.objects.get(rut=rut)
            return self._convertir_a_entidad(cliente_modelo)
        except ClienteModelo.DoesNotExist:
            return None
            
    def listar_todos(self):
        """
        Lista todos los clientes
        """
        clientes_modelo = ClienteModelo.objects.all()
        return [self._convertir_a_entidad(cliente) for cliente in clientes_modelo]
        
    def listar_activos(self):
        """
        Lista todos los clientes activos
        """
        clientes_modelo = ClienteModelo.objects.filter(estado="activo")
        return [self._convertir_a_entidad(cliente) for cliente in clientes_modelo]
        
    def eliminar(self, id):
        """
        Elimina un cliente por su ID
        """
        try:
            cliente = ClienteModelo.objects.get(id=id)
            cliente.delete()
            return True
        except ClienteModelo.DoesNotExist:
            return False
            
    def _convertir_a_entidad(self, cliente_modelo):
        """
        Convierte un modelo ORM a una entidad de dominio
        """
        cliente = ClienteEntidad(
            nombre=cliente_modelo.nombre,
            correo=cliente_modelo.correo,
            rut=cliente_modelo.rut,
            telefono=cliente_modelo.telefono or "",
            direccion=cliente_modelo.direccion or ""
        )
        cliente.id = cliente_modelo.id
        cliente.estado = cliente_modelo.estado
        cliente.fecha_registro = cliente_modelo.fecha_registro
        cliente.ultima_visita = cliente_modelo.ultima_visita
        return cliente