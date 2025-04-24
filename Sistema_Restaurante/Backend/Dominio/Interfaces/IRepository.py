from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')

class IRepository(Generic[T], ABC):
    """
    Interface genérica para repositorios que define operaciones CRUD básicas.
    
    Args:
        T: Tipo de entidad que maneja el repositorio
    """
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[T]:
        """
        Obtiene una entidad por su ID
        
        Args:
            id: Identificador único de la entidad
            
        Returns:
            La entidad si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def listar(self, filtros: Optional[Dict[str, Any]] = None) -> List[T]:
        """
        Lista entidades con filtros opcionales
        
        Args:
            filtros: Diccionario de condiciones para filtrar resultados
            
        Returns:
            Lista de entidades que cumplen los criterios
        """
        pass
    
    @abstractmethod
    def crear(self, entidad: T) -> T:
        """
        Crea una nueva entidad
        
        Args:
            entidad: La entidad a crear
            
        Returns:
            La entidad creada con su ID asignado
        """
        pass
    
    @abstractmethod
    def actualizar(self, entidad: T) -> T:
        """
        Actualiza una entidad existente
        
        Args:
            entidad: La entidad con los datos actualizados
            
        Returns:
            La entidad actualizada
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina una entidad por su ID
        
        Args:
            id: Identificador único de la entidad
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass
