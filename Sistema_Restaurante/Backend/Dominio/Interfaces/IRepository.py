from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar('T')

class IRepository(Generic[T], ABC):
    """
    Interfaz genérica que define las operaciones básicas CRUD
    que todos los repositorios deben implementar.
    """
    
    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        """
        Obtiene una entidad por su identificador.
        
        Args:
            id: El identificador único de la entidad.
            
        Returns:
            La entidad encontrada o None si no existe.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades disponibles.
        
        Returns:
            Lista de todas las entidades.
        """
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """
        Añade una nueva entidad al repositorio.
        
        Args:
            entity: La entidad a añadir.
            
        Returns:
            La entidad añadida con su ID asignado.
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.
        
        Args:
            entity: La entidad con los datos actualizados.
            
        Returns:
            La entidad actualizada.
        """
        pass
    
    @abstractmethod
    def delete(self, id: Any) -> bool:
        """
        Elimina una entidad por su identificador.
        
        Args:
            id: El identificador único de la entidad.
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario.
        """
        pass
