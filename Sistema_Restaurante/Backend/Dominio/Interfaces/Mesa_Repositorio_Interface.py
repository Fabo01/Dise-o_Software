"""
Interfaz para el repositorio de Mesas.
Define el contrato que debe cumplir cualquier implementación del repositorio de mesas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from Backend.Dominio.Entidades.Mesa_Entidad import Mesa


class MesaRepositorioInterface(ABC):
    """
    Interfaz que define las operaciones del repositorio de mesas.
    
    Esta interfaz establece el contrato que debe seguir cualquier implementación
    concreta del repositorio de mesas, siguiendo el patrón Repository.
    """
    
    @abstractmethod
    def obtener_por_id(self, mesa_id: int) -> Optional[Mesa]:
        """
        Obtiene una mesa por su ID.
        
        Args:
            mesa_id: ID único de la mesa
            
        Returns:
            Mesa si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def obtener_por_numero(self, numero: int) -> Optional[Mesa]:
        """
        Obtiene una mesa por su número.
        
        Args:
            numero: Número de la mesa
            
        Returns:
            Mesa si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def obtener_todas(self, filtros: Optional[Dict[str, Any]] = None) -> List[Mesa]:
        """
        Obtiene todas las mesas con filtros opcionales.
        
        Args:
            filtros: Diccionario con filtros a aplicar
            
        Returns:
            Lista de mesas que cumplen los filtros
        """
        pass
    
    @abstractmethod
    def crear(self, mesa: Mesa) -> Mesa:
        """
        Crea una nueva mesa.
        
        Args:
            mesa: Entidad Mesa a crear
            
        Returns:
            Mesa creada con ID asignado
        """
        pass
    
    @abstractmethod
    def actualizar(self, mesa: Mesa) -> Mesa:
        """
        Actualiza una mesa existente.
        
        Args:
            mesa: Entidad Mesa con datos actualizados
            
        Returns:
            Mesa actualizada
        """
        pass
    
    @abstractmethod
    def eliminar(self, mesa_id: int) -> bool:
        """
        Elimina una mesa por su ID.
        
        Args:
            mesa_id: ID de la mesa a eliminar
            
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: str) -> List[Mesa]:
        """
        Obtiene todas las mesas con un estado específico.
        
        Args:
            estado: Estado de las mesas a buscar
            
        Returns:
            Lista de mesas con el estado especificado
        """
        pass
    
    @abstractmethod
    def obtener_por_capacidad_minima(self, capacidad_min: int) -> List[Mesa]:
        """
        Obtiene todas las mesas con capacidad mínima especificada.
        
        Args:
            capacidad_min: Capacidad mínima requerida
            
        Returns:
            Lista de mesas que cumplen la capacidad mínima
        """
        pass
    
    @abstractmethod
    def contar_por_estado(self, estado: str) -> int:
        """
        Cuenta las mesas que tienen un estado específico.
        
        Args:
            estado: Estado a contar
            
        Returns:
            Número de mesas con el estado especificado
        """
        pass
    
    @abstractmethod
    def existe_numero(self, numero: int, excluir_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una mesa con el número especificado.
        
        Args:
            numero: Número de mesa a verificar
            excluir_id: ID de mesa a excluir de la verificación (para actualizaciones)
            
        Returns:
            True si existe una mesa con ese número, False en caso contrario
        """
        pass
