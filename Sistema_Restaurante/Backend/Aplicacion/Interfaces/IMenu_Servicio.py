from abc import ABC, abstractmethod
from typing import List, Optional
from ..DTOs.MenuDTO import (
    MenuDTO, MenuCrearDTO, MenuActualizarDTO, MenuBusquedaDTO,
    MenuDisponibilidadDTO, MenuEstadisticasDTO, MenuListaDTO
)
from decimal import Decimal

class IMenuServicio(ABC):
    """
    Interfaz del servicio de aplicación para menús.
    Define los contratos de los casos de uso relacionados con menús.
    """
    
    @abstractmethod
    def crear_menu(self, menu_data: MenuCrearDTO) -> MenuDTO:
        """
        Caso de uso: Crear un nuevo menú.
        
        Args:
            menu_data (MenuCrearDTO): Datos del menú a crear
            
        Returns:
            MenuDTO: El menú creado
        """
        pass
    
    @abstractmethod
    def obtener_menu_por_id(self, menu_id: str) -> Optional[MenuDTO]:
        """
        Caso de uso: Obtener un menú por su ID.
        
        Args:
            menu_id (str): ID del menú
            
        Returns:
            Optional[MenuDTO]: El menú encontrado o None
        """
        pass
    
    @abstractmethod
    def obtener_menu_por_nombre(self, nombre: str) -> Optional[MenuDTO]:
        """
        Caso de uso: Obtener un menú por su nombre.
        
        Args:
            nombre (str): Nombre del menú
            
        Returns:
            Optional[MenuDTO]: El menú encontrado o None
        """
        pass
    
    @abstractmethod
    def actualizar_menu(self, menu_id: str, datos_actualizacion: MenuActualizarDTO) -> MenuDTO:
        """
        Caso de uso: Actualizar un menú existente.
        
        Args:
            menu_id (str): ID del menú a actualizar
            datos_actualizacion (MenuActualizarDTO): Datos de actualización
            
        Returns:
            MenuDTO: El menú actualizado
        """
        pass
    
    @abstractmethod
    def eliminar_menu(self, menu_id: str) -> bool:
        """
        Caso de uso: Eliminar un menú.
        
        Args:
            menu_id (str): ID del menú a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def listar_menus(self, filtros: Optional[MenuBusquedaDTO] = None) -> List[MenuListaDTO]:
        """
        Caso de uso: Listar menús con filtros opcionales.
        
        Args:
            filtros (Optional[MenuBusquedaDTO]): Filtros de búsqueda
            
        Returns:
            List[MenuListaDTO]: Lista de menús
        """
        pass
        """
        Caso de uso: Actualizar un menú existente.
        
        Args:
            menu_id (str): ID del menú a actualizar
            datos_actualizacion (MenuActualizarDTO): Datos de actualización
            
        Returns:
            MenuDTO: El menú actualizado
        """
        pass
    
    @abstractmethod
    def eliminar_menu(self, menu_id: str) -> bool:
        """
        Caso de uso: Eliminar un menú.
        
        Args:
            menu_id (str): ID del menú a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def listar_menus(self) -> List[MenuListaDTO]:
        """
        Caso de uso: Listar todos los menús.
        
        Returns:
            List[MenuListaDTO]: Lista de menús
        """
        pass
    
    @abstractmethod
    def buscar_menus(self, criterios: MenuBusquedaDTO) -> List[MenuListaDTO]:
        """
        Caso de uso: Buscar menús según criterios específicos.
        
        Args:
            criterios (MenuBusquedaDTO): Criterios de búsqueda
            
        Returns:
            List[MenuListaDTO]: Lista de menús que cumplen los criterios
        """
        pass
    
    @abstractmethod
    def obtener_menus_disponibles(self) -> List[MenuListaDTO]:
        """
        Caso de uso: Obtener solo los menús disponibles para venta.
        
        Returns:
            List[MenuListaDTO]: Lista de menús disponibles
        """
        pass
    
    @abstractmethod
    def verificar_disponibilidad_menu(self, menu_id: str) -> MenuDisponibilidadDTO:
        """
        Caso de uso: Verificar si un menú está disponible considerando ingredientes.
        
        Args:
            menu_id (str): ID del menú a verificar
            
        Returns:
            MenuDisponibilidadDTO: Estado de disponibilidad del menú
        """
        pass
    
    @abstractmethod
    def agregar_ingrediente_a_menu(self, menu_id: str, ingrediente_id: str, cantidad: Decimal) -> MenuDTO:
        """
        Caso de uso: Agregar un ingrediente a un menú.
        
        Args:
            menu_id (str): ID del menú
            ingrediente_id (str): ID del ingrediente
            cantidad (Decimal): Cantidad del ingrediente
            
        Returns:
            MenuDTO: El menú actualizado
        """
        pass
    
    @abstractmethod
    def obtener_estadisticas_menus(self) -> MenuEstadisticasDTO:
        """
        Caso de uso: Obtener estadísticas generales de los menús.
        
        Returns:
            MenuEstadisticasDTO: Estadísticas de los menús
        """
        pass
