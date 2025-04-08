from typing import List, Optional, Any
from django.db.models import Q

from ...Dominio.Interfaces.IRepository import IRepository
from ..ORM.Ingrediente import Ingrediente

class IngredienteRepository(IRepository[Ingrediente]):
    """
    Implementación concreta del repositorio para la entidad Ingrediente.
    """
    
    def get(self, id: int) -> Optional[Ingrediente]:
        """
        Obtiene un ingrediente por su ID.
        
        Args:
            id: El ID del ingrediente.
            
        Returns:
            El ingrediente encontrado o None si no existe.
        """
        try:
            return Ingrediente.objects.get(pk=id)
        except Ingrediente.DoesNotExist:
            return None
    
    def get_all(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes disponibles.
        
        Returns:
            Lista de todos los ingredientes.
        """
        return list(Ingrediente.objects.all())
    
    def add(self, entity: Ingrediente) -> Ingrediente:
        """
        Añade un nuevo ingrediente al repositorio.
        
        Args:
            entity: El ingrediente a añadir.
            
        Returns:
            El ingrediente añadido con su ID asignado.
        """
        entity.save()
        return entity
    
    def update(self, entity: Ingrediente) -> Ingrediente:
        """
        Actualiza un ingrediente existente.
        
        Args:
            entity: El ingrediente con los datos actualizados.
            
        Returns:
            El ingrediente actualizado.
        """
        entity.save()
        return entity
    
    def delete(self, id: int) -> bool:
        """
        Elimina un ingrediente por su ID.
        
        Args:
            id: El ID del ingrediente.
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            ingrediente = Ingrediente.objects.get(pk=id)
            ingrediente.delete()
            return True
        except Ingrediente.DoesNotExist:
            return False
    
    # Métodos específicos para Ingrediente
    
    def find_by_name(self, name: str) -> List[Ingrediente]:
        """
        Busca ingredientes por nombre.
        
        Args:
            name: Nombre o parte del nombre a buscar.
            
        Returns:
            Lista de ingredientes que coinciden con el criterio.
        """
        return list(Ingrediente.objects.filter(nombre__icontains=name))
    
    def find_by_category(self, category: str) -> List[Ingrediente]:
        """
        Busca ingredientes por categoría.
        
        Args:
            category: Categoría a buscar.
            
        Returns:
            Lista de ingredientes de la categoría especificada.
        """
        return list(Ingrediente.objects.filter(categoria=category))
    
    def find_low_stock(self) -> List[Ingrediente]:
        """
        Encuentra ingredientes con stock bajo (por debajo del nivel crítico).
        
        Returns:
            Lista de ingredientes con stock bajo.
        """
        return list(Ingrediente.objects.filter(
            Q(cantidad__lte=models.F('nivel_critico')) | 
            Q(estado='agotado')
        ))
