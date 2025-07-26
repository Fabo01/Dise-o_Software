# Backend/Dominio/Interfaces/IDeliveryRepositorio.py
from abc import ABC, abstractmethod
from typing import List, Optional
from Backend.Dominio.Entidades.DeliveryPedido_Entidad import DeliveryPedidoEntidad

class IDeliveryRepositorio(ABC):
    """
    Interfaz para el repositorio de delivery.
    Define las operaciones de acceso a datos para pedidos de delivery.
    """
    
    @abstractmethod
    def crear_pedido_delivery(self, delivery_pedido: DeliveryPedidoEntidad) -> DeliveryPedidoEntidad:
        """Crea un nuevo pedido de delivery"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, pedido_id: int) -> Optional[DeliveryPedidoEntidad]:
        """Obtiene un pedido de delivery por su ID"""
        pass
    
    @abstractmethod
    def listar_pedidos_activos(self) -> List[DeliveryPedidoEntidad]:
        """Lista todos los pedidos de delivery activos"""
        pass
    
    @abstractmethod
    def listar_por_estado(self, estado: str) -> List[DeliveryPedidoEntidad]:
        """Lista pedidos de delivery filtrados por estado"""
        pass
    
    @abstractmethod
    def asignar_repartidor(self, pedido_id: int, repartidor_id: int) -> bool:
        """Asigna un repartidor a un pedido de delivery"""
        pass
    
    @abstractmethod
    def actualizar_estado(self, pedido_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de un pedido de delivery"""
        pass
    
    @abstractmethod
    def obtener_repartidores_disponibles(self) -> List:
        """Obtiene lista de repartidores disponibles"""
        pass
    
    @abstractmethod
    def actualizar_ubicacion_repartidor(self, repartidor_id: int, latitud: float, longitud: float) -> bool:
        """Actualiza la ubicación de un repartidor"""
        pass
