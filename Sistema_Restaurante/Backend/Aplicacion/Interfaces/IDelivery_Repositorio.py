# Backend/Aplicacion/Interfaces/IDelivery_Repositorio.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

class IDeliveryRepositorio(ABC):
    """
    Interfaz para el repositorio de Delivery
    Define los contratos para el acceso a datos de delivery
    """
    
    @abstractmethod
    def crear_pedido_delivery(self, datos_pedido: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo pedido delivery"""
        pass
    
    @abstractmethod
    def obtener_pedido_delivery_por_id(self, pedido_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un pedido delivery por su ID"""
        pass
    
    @abstractmethod
    def obtener_pedidos_pendientes_asignacion(self) -> List[Dict[str, Any]]:
        """Obtiene pedidos pendientes de asignar repartidor"""
        pass
    
    @abstractmethod
    def asignar_repartidor_a_pedido(self, pedido_id: int, repartidor_id: int) -> bool:
        """Asigna un repartidor a un pedido"""
        pass
    
    @abstractmethod
    def obtener_repartidores_disponibles(self) -> List[Dict[str, Any]]:
        """Obtiene lista de repartidores disponibles"""
        pass
    
    @abstractmethod
    def actualizar_estado_delivery(self, pedido_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de un delivery"""
        pass
    
    @abstractmethod
    def completar_entrega(self, pedido_id: int, datos_entrega: Dict[str, Any]) -> Dict[str, Any]:
        """Marca una entrega como completada"""
        pass
    
    @abstractmethod
    def obtener_estadisticas_delivery(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Obtiene estadísticas de delivery para un período"""
        pass
    
    @abstractmethod
    def obtener_apps_delivery_activas(self) -> List[Dict[str, Any]]:
        """Obtiene las aplicaciones de delivery activas"""
        pass
    
    @abstractmethod
    def registrar_pedido_app_externa(self, datos_pedido: Dict[str, Any]) -> Dict[str, Any]:
        """Registra un pedido proveniente de app externa"""
        pass
