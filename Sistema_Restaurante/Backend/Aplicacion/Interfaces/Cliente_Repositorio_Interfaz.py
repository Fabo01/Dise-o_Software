from abc import ABC, abstractmethod
from typing import List, Optional

class IClienteRepositorio(ABC):
    """
    Interfaz que define los métodos necesarios para un repositorio de clientes.
    Sigue el patrón Repository para desacoplar la lógica de dominio del acceso a datos.
    """
    
    @abstractmethod
    def guardar(self, cliente):
        """
        Guarda o actualiza un cliente en el repositorio
        
        Args:
            cliente: La entidad cliente a guardar
            
        Returns:
            La entidad cliente actualizada
        """
        pass
        
    @abstractmethod
    def buscar_por_id(self, id):
        """
        Busca un cliente por su ID
        
        Args:
            id: El ID del cliente a buscar
            
        Returns:
            La entidad cliente o None si no se encuentra
        """
        pass
        
    @abstractmethod
    def buscar_por_rut(self, rut):
        """
        Busca un cliente por su RUT
        
        Args:
            rut: El RUT del cliente a buscar
            
        Returns:
            La entidad cliente o None si no se encuentra
        """
        pass
        
    @abstractmethod
    def buscar_por_nombre(self, nombre):
        """
        Busca clientes que contengan el nombre especificado
        
        Args:
            nombre: El nombre o parte del nombre a buscar
            
        Returns:
            Lista de entidades cliente que coinciden con la búsqueda
        """
        pass
        
    @abstractmethod
    def listar_todos(self):
        """
        Lista todos los clientes
        
        Returns:
            Lista de todas las entidades cliente
        """
        pass
        
    @abstractmethod
    def listar_activos(self):
        """
        Lista todos los clientes activos
        
        Returns:
            Lista de entidades cliente activas
        """
        pass
        
    @abstractmethod
    def eliminar(self, id):
        """
        Elimina un cliente por su ID
        
        Args:
            id: El ID del cliente a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass