from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from Backend.Dominio.Entidades.Menu_Entidad import MenuEntidad

class IMenuRepositorio(ABC):
    """
    Interfaz para el repositorio de menús.
    Define los contratos que debe cumplir cualquier implementación del repositorio de menús.
    """
    
    @abstractmethod
    def guardar(self, menu: MenuEntidad) -> MenuEntidad:
        """
        Guarda un menú en el repositorio.
        
        Args:
            menu: La entidad menú a guardar
            
        Returns:
            La entidad menú guardada
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[MenuEntidad]:
        """
        Busca un menú por su ID.
        
        Args:
            id: El ID del menú a buscar
            
        Returns:
            La entidad menú si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[MenuEntidad]:
        """
        Busca un menú por su nombre exacto.
        
        Args:
            nombre: El nombre del menú a buscar
            
        Returns:
            La entidad menú si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[MenuEntidad]:
        """
        Lista todos los menús del repositorio.
        
        Returns:
            Lista de todas las entidades menú
        """
        pass
    
    @abstractmethod
    def listar_disponibles(self) -> List[MenuEntidad]:
        """
        Lista menús que están disponibles.
        
        Returns:
            Lista de menús disponibles
        """
        pass
    
    @abstractmethod
    def listar_por_categoria(self, categoria: str) -> List[MenuEntidad]:
        """
        Lista menús filtrados por categoría.
        
        Args:
            categoria: La categoría a filtrar
            
        Returns:
            Lista de menús de la categoría especificada
        """
        pass
    
    @abstractmethod
    def actualizar(self, menu: MenuEntidad) -> MenuEntidad:
        """
        Actualiza un menú existente.
        
        Args:
            menu: La entidad menú con los datos actualizados
            
        Returns:
            La entidad menú actualizada
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina un menú del repositorio.
        
        Args:
            id: El ID del menú a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def cambiar_disponibilidad(self, id: int, disponible: bool) -> bool:
        """
        Cambia la disponibilidad de un menú.
        
        Args:
            id: El ID del menú
            disponible: True para disponible, False para no disponible
            
        Returns:
            True si se cambió correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def buscar_por_texto(self, texto: str) -> List[MenuEntidad]:
        """
        Busca menús que contengan el texto en nombre o descripción.
        
        Args:
            texto: Texto a buscar
            
        Returns:
            Lista de menús encontrados
        """
        pass
    
    @abstractmethod
    def obtener_por_categoria(self, categoria: str) -> List[MenuEntidad]:
        """
        Obtiene menús por categoría.
        
        Args:
            categoria: Categoría a buscar
            
        Returns:
            Lista de menús de la categoría
        """
        pass
    
    @abstractmethod
    def obtener_disponibles(self) -> List[MenuEntidad]:
        """
        Obtiene todos los menús disponibles.
        
        Returns:
            Lista de menús disponibles
        """
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[MenuEntidad]:
        """
        Obtiene todos los menús.
        
        Returns:
            Lista de todos los menús
        """
        pass
    
    @abstractmethod
    def existe_por_nombre(self, nombre: str) -> bool:
        """
        Verifica si existe un menú con el nombre dado.
        
        Args:
            nombre: Nombre del menú
            
        Returns:
            True si existe, False en caso contrario
        """
        pass
    
    @abstractmethod
    def existe(self, id: int) -> bool:
        """
        Verifica si existe un menú con el ID dado.
        
        Args:
            id: ID del menú
            
        Returns:
            True si existe, False en caso contrario
        """
        pass
