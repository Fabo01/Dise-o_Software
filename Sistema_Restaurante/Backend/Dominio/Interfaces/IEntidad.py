from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class IEntidad(ABC):
    """
    Interfaz base para todas las entidades del dominio.
    Define el contrato mínimo que deben cumplir.
    """
    
    @property
    @abstractmethod
    def id(self) -> Optional[int]:
        """Obtiene el identificador único de la entidad."""
        pass
    
    @property
    @abstractmethod
    def fecha_creacion(self) -> datetime:
        """Obtiene la fecha de creación de la entidad."""
        pass
    
    @property
    @abstractmethod
    def fecha_actualizacion(self) -> datetime:
        """Obtiene la fecha de última actualización de la entidad."""
        pass
    
    @abstractmethod
    def es_igual(self, otra_entidad) -> bool:
        """
        Determina si esta entidad es igual a otra.
        
        Args:
            otra_entidad: Otra entidad para comparar
            
        Returns:
            bool: True si son iguales, False en caso contrario
        """
        pass
