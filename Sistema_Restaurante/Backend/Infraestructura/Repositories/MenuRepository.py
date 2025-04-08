from typing import List, Optional, Any
from django.db.models import Q, Prefetch

from ...Dominio.Interfaces.IRepository import IRepository
from ..ORM.Menu import Menu
from ..ORM.MenuIngrediente import MenuIngrediente
from ..ORM.Ingrediente import Ingrediente

class MenuRepository(IRepository[Menu]):
    """
    Implementación concreta del repositorio para la entidad Menu.
    """
    
    def get(self, id: int) -> Optional[Menu]:
        """
        Obtiene un menú por su ID.
        
        Args:
            id: El ID del menú.
            
        Returns:
            El menú encontrado o None si no existe.
        """
        try:
            return Menu.objects.get(pk=id)
        except Menu.DoesNotExist:
            return None
    
    def get_all(self) -> List[Menu]:
        """
        Obtiene todos los menús disponibles.
        
        Returns:
            Lista de todos los menús.
        """
        return list(Menu.objects.all())
    
    def add(self, entity: Menu) -> Menu:
        """
        Añade un nuevo menú al repositorio.
        
        Args:
            entity: El menú a añadir.
            
        Returns:
            El menú añadido con su ID asignado.
        """
        entity.save()
        return entity
    
    def update(self, entity: Menu) -> Menu:
        """
        Actualiza un menú existente.
        
        Args:
            entity: El menú con los datos actualizados.
            
        Returns:
            El menú actualizado.
        """
        entity.save()
        return entity
    
    def delete(self, id: int) -> bool:
        """
        Elimina un menú por su ID.
        
        Args:
            id: El ID del menú.
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            menu = Menu.objects.get(pk=id)
            menu.delete()
            return True
        except Menu.DoesNotExist:
            return False
    
    # Métodos específicos para Menu
    
    def find_by_category(self, category: str) -> List[Menu]:
        """
        Busca menús por categoría.
        
        Args:
            category: Categoría a buscar.
            
        Returns:
            Lista de menús de la categoría especificada.
        """
        return list(Menu.objects.filter(categoria=category))
    
    def find_by_name(self, name: str) -> List[Menu]:
        """
        Busca menús por nombre.
        
        Args:
            name: Nombre o parte del nombre a buscar.
            
        Returns:
            Lista de menús que coinciden con el criterio.
        """
        return list(Menu.objects.filter(nombre__icontains=name))
    
    def get_with_ingredients(self, id: int) -> Optional[Menu]:
        """
        Obtiene un menú con todos sus ingredientes.
        
        Args:
            id: El ID del menú.
            
        Returns:
            El menú con sus ingredientes o None si no existe.
        """
        try:
            return Menu.objects.prefetch_related(
                Prefetch(
                    'menuingrediente_set',
                    queryset=MenuIngrediente.objects.select_related('ingrediente')
                )
            ).get(pk=id)
        except Menu.DoesNotExist:
            return None
    
    def get_available_menus(self) -> List[Menu]:
        """
        Obtiene todos los menús que están disponibles.
        
        Returns:
            Lista de menús disponibles.
        """
        return list(Menu.objects.filter(disponible=True))
    
    def get_delivery_available_menus(self) -> List[Menu]:
        """
        Obtiene los menús disponibles para delivery.
        
        Returns:
            Lista de menús disponibles para delivery.
        """
        return list(Menu.objects.filter(disponible=True, disponible_delivery=True))
