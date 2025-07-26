from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from ..Entidades.Menu_Entidad import MenuEntidad

class IMenuRepositorio(ABC):
    """
    Interfaz del repositorio para la entidad Menu.
    Define los contratos que debe cumplir cualquier implementación del repositorio de menús.
    """
    
    @abstractmethod
    def guardar(self, menu: MenuEntidad) -> MenuEntidad:
        """
        Guarda un menú en el repositorio.
        
        Args:
            menu (MenuEntidad): La entidad menú a guardar
            
        Returns:
            MenuEntidad: El menú guardado con su ID asignado
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al guardar
        """
        pass
    
    @abstractmethod
    def buscar_por_id(self, menu_id: int) -> Optional[MenuEntidad]:
        """
        Busca un menú por su ID.
        
        Args:
            menu_id (int): ID del menú a buscar
            
        Returns:
            Optional[MenuEntidad]: El menú encontrado o None si no existe
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al buscar
        """
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[MenuEntidad]:
        """
        Busca menús que contengan el nombre especificado.
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            List[MenuEntidad]: Lista de menús encontrados
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al buscar
        """
        pass
    
    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> List[MenuEntidad]:
        """
        Busca menús por categoría.
        
        Args:
            categoria (str): Categoría a buscar
            
        Returns:
            List[MenuEntidad]: Lista de menús de la categoría
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al buscar
        """
        pass
    
    @abstractmethod
    def buscar_por_tipo(self, tipo: str) -> List[MenuEntidad]:
        """
        Busca menús por tipo.
        
        Args:
            tipo (str): Tipo a buscar
            
        Returns:
            List[MenuEntidad]: Lista de menús del tipo especificado
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al buscar
        """
        pass
    
    @abstractmethod
    def buscar_por_rango_precio(self, precio_min: Decimal, precio_max: Decimal) -> List[MenuEntidad]:
        """
        Busca menús dentro de un rango de precios.
        
        Args:
            precio_min (Decimal): Precio mínimo
            precio_max (Decimal): Precio máximo
            
        Returns:
            List[MenuEntidad]: Lista de menús en el rango de precios
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al buscar
        """
        pass
    
    @abstractmethod
    def listar_disponibles(self) -> List[MenuEntidad]:
        """
        Lista todos los menús disponibles.
        
        Returns:
            List[MenuEntidad]: Lista de menús disponibles
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al listar
        """
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[MenuEntidad]:
        """
        Lista todos los menús.
        
        Returns:
            List[MenuEntidad]: Lista de todos los menús
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al listar
        """
        pass
    
    @abstractmethod
    def listar_por_popularidad(self, limite: int = 10) -> List[MenuEntidad]:
        """
        Lista los menús más populares (más ordenados).
        
        Args:
            limite (int): Número máximo de menús a retornar
            
        Returns:
            List[MenuEntidad]: Lista de menús ordenados por popularidad
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al listar
        """
        pass
    
    @abstractmethod
    def buscar_con_ingrediente(self, ingrediente_id: int) -> List[MenuEntidad]:
        """
        Busca menús que contengan un ingrediente específico.
        
        Args:
            ingrediente_id (int): ID del ingrediente
            
        Returns:
            List[MenuEntidad]: Lista de menús que contienen el ingrediente
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al buscar
        """
        pass
    
    @abstractmethod
    def contar_total(self) -> int:
        """
        Cuenta el total de menús.
        
        Returns:
            int: Número total de menús
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al contar
        """
        pass
    
    @abstractmethod
    def contar_disponibles(self) -> int:
        """
        Cuenta los menús disponibles.
        
        Returns:
            int: Número de menús disponibles
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al contar
        """
        pass
    
    @abstractmethod
    def obtener_precio_promedio(self) -> Decimal:
        """
        Obtiene el precio promedio de los menús disponibles.
        
        Returns:
            Decimal: Precio promedio
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al calcular
        """
        pass
    
    @abstractmethod
    def obtener_estadisticas_categoria(self) -> dict:
        """
        Obtiene estadísticas por categoría.
        
        Returns:
            dict: Estadísticas agrupadas por categoría
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al obtener estadísticas
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina un menú del repositorio.
        
        Args:
            id (int): ID del menú a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al eliminar
        """
        pass
    
    @abstractmethod
    def existe(self, id: int) -> bool:
        """
        Verifica si existe un menú con el ID especificado.
        
        Args:
            id (int): ID del menú a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al verificar
        """
        pass
        """
        Elimina un menú del repositorio.
        
        Args:
            menu_id (str): ID del menú a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al eliminar
        """
        pass
    
    @abstractmethod
    def existe(self, menu_id: str) -> bool:
        """
        Verifica si existe un menú con el ID especificado.
        
        Args:
            menu_id (str): ID del menú a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al verificar
        """
        pass
    
    @abstractmethod
    def existe_por_nombre(self, nombre: str) -> bool:
        """
        Verifica si existe un menú con el nombre especificado.
        
        Args:
            nombre (str): Nombre del menú a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al verificar
        """
        pass
    
    @abstractmethod
    def contar_total(self) -> int:
        """
        Cuenta el total de menús en el repositorio.
        
        Returns:
            int: Número total de menús
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al contar
        """
        pass
    
    @abstractmethod
    def obtener_estadisticas_categoria(self) -> dict:
        """
        Obtiene estadísticas de menús por categoría.
        
        Returns:
            dict: Diccionario con estadísticas por categoría
            
        Raises:
            RepositorioExcepcion: Si ocurre un error al obtener estadísticas
        """
        pass
