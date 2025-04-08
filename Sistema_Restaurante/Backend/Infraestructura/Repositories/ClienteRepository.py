from typing import List, Optional, Any
from django.db.models import Q

from ...Dominio.Interfaces.IRepository import IRepository
from ..ORM.Cliente import Cliente

class ClienteRepository(IRepository[Cliente]):
    """
    Implementación concreta del repositorio para la entidad Cliente.
    """
    
    def get(self, rut: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su RUT.
        
        Args:
            rut: El RUT del cliente.
            
        Returns:
            El cliente encontrado o None si no existe.
        """
        try:
            return Cliente.objects.get(rut=rut)
        except Cliente.DoesNotExist:
            return None
    
    def get_all(self) -> List[Cliente]:
        """
        Obtiene todos los clientes activos.
        
        Returns:
            Lista de todos los clientes.
        """
        return list(Cliente.objects.all())
    
    def add(self, entity: Cliente) -> Cliente:
        """
        Añade un nuevo cliente al repositorio.
        
        Args:
            entity: El cliente a añadir.
            
        Returns:
            El cliente añadido.
        """
        entity.save()
        return entity
    
    def update(self, entity: Cliente) -> Cliente:
        """
        Actualiza un cliente existente.
        
        Args:
            entity: El cliente con los datos actualizados.
            
        Returns:
            El cliente actualizado.
        """
        entity.save()
        return entity
    
    def delete(self, rut: str) -> bool:
        """
        Elimina un cliente por su RUT.
        
        Args:
            rut: El RUT del cliente.
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            cliente = Cliente.objects.get(rut=rut)
            cliente.delete()
            return True
        except Cliente.DoesNotExist:
            return False
    
    # Métodos específicos para Cliente
    
    def find_by_name(self, name: str) -> List[Cliente]:
        """
        Busca clientes por nombre.
        
        Args:
            name: Nombre o parte del nombre a buscar.
            
        Returns:
            Lista de clientes que coinciden con el criterio.
        """
        return list(Cliente.objects.filter(nombre__icontains=name))
    
    def find_by_email(self, email: str) -> Optional[Cliente]:
        """
        Busca un cliente por su correo electrónico.
        
        Args:
            email: Correo electrónico a buscar.
            
        Returns:
            El cliente encontrado o None si no existe.
        """
        try:
            return Cliente.objects.get(correo=email)
        except Cliente.DoesNotExist:
            return None
        except Cliente.MultipleObjectsReturned:
            # En caso de correos duplicados (no debería ocurrir), devuelve el primero
            return Cliente.objects.filter(correo=email).first()
    
    def find_by_phone(self, phone: str) -> List[Cliente]:
        """
        Busca clientes por número telefónico.
        
        Args:
            phone: Número de teléfono a buscar.
            
        Returns:
            Lista de clientes que coinciden con el criterio.
        """
        return list(Cliente.objects.filter(telefono__contains=phone))
    
    def get_active_clients(self) -> List[Cliente]:
        """
        Obtiene todos los clientes en estado activo.
        
        Returns:
            Lista de clientes activos.
        """
        return list(Cliente.objects.filter(estado='activo'))
