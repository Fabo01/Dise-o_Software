from typing import List, Optional, Any
from django.db.models import Q, Prefetch
from datetime import datetime

from ...Dominio.Interfaces.IRepository import IRepository
from ..ORM.Pedido import Pedido
from ..ORM.Cliente import Cliente
from ..ORM.ItemPedido import ItemPedido

class PedidoRepository(IRepository[Pedido]):
    """
    Implementación concreta del repositorio para la entidad Pedido.
    """
    
    def get(self, id: int) -> Optional[Pedido]:
        """
        Obtiene un pedido por su ID.
        
        Args:
            id: El ID del pedido.
            
        Returns:
            El pedido encontrado o None si no existe.
        """
        try:
            return Pedido.objects.get(pk=id)
        except Pedido.DoesNotExist:
            return None
    
    def get_all(self) -> List[Pedido]:
        """
        Obtiene todos los pedidos.
        
        Returns:
            Lista de todos los pedidos.
        """
        return list(Pedido.objects.all())
    
    def add(self, entity: Pedido) -> Pedido:
        """
        Añade un nuevo pedido al repositorio.
        
        Args:
            entity: El pedido a añadir.
            
        Returns:
            El pedido añadido con su ID asignado.
        """
        entity.save()
        return entity
    
    def update(self, entity: Pedido) -> Pedido:
        """
        Actualiza un pedido existente.
        
        Args:
            entity: El pedido con los datos actualizados.
            
        Returns:
            El pedido actualizado.
        """
        entity.save()
        return entity
    
    def delete(self, id: int) -> bool:
        """
        Elimina un pedido por su ID.
        
        Args:
            id: El ID del pedido.
            
        Returns:
            True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            pedido = Pedido.objects.get(pk=id)
            pedido.delete()
            return True
        except Pedido.DoesNotExist:
            return False
    
    # Métodos específicos para Pedido
    
    def get_by_cliente(self, cliente_rut: str) -> List[Pedido]:
        """
        Obtiene todos los pedidos de un cliente específico.
        
        Args:
            cliente_rut: El RUT del cliente.
            
        Returns:
            Lista de pedidos del cliente.
        """
        return list(Pedido.objects.filter(cliente__rut=cliente_rut).order_by('-fecha'))
    
    def get_by_estado(self, estado: str) -> List[Pedido]:
        """
        Obtiene todos los pedidos en un estado específico.
        
        Args:
            estado: El estado de los pedidos a buscar.
            
        Returns:
            Lista de pedidos en el estado especificado.
        """
        return list(Pedido.objects.filter(estado=estado).order_by('-fecha'))
    
    def get_by_fecha_range(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Pedido]:
        """
        Obtiene todos los pedidos realizados en un rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio del rango.
            fecha_fin: Fecha de fin del rango.
            
        Returns:
            Lista de pedidos en el rango de fechas.
        """
        return list(Pedido.objects.filter(
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin
        ).order_by('-fecha'))
    
    def get_pedido_completo(self, id: int) -> Optional[Pedido]:
        """
        Obtiene un pedido con todos sus items y datos del cliente.
        
        Args:
            id: El ID del pedido.
            
        Returns:
            El pedido con todos sus detalles o None si no existe.
        """
        try:
            return Pedido.objects.select_related('cliente').prefetch_related(
                Prefetch(
                    'itempedido_set',
                    queryset=ItemPedido.objects.select_related('menu')
                )
            ).get(pk=id)
        except Pedido.DoesNotExist:
            return None
    
    def get_pending_orders(self) -> List[Pedido]:
        """
        Obtiene todos los pedidos pendientes que necesitan atención.
        
        Returns:
            Lista de pedidos pendientes.
        """
        return list(Pedido.objects.filter(
            estado__in=['recibido', 'en_preparacion', 'listo']
        ).order_by('fecha'))
