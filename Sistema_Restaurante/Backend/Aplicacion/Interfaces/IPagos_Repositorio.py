# Backend/Aplicacion/Interfaces/IPagos_Repositorio.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

class IPagosRepositorio(ABC):
    """
    Interfaz para el repositorio de Pagos
    Define los contratos para el acceso a datos de pagos y transacciones
    """
    
    @abstractmethod
    def crear_transaccion(self, datos_transaccion: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva transacción"""
        pass
    
    @abstractmethod
    def obtener_transaccion_por_id(self, transaccion_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una transacción por su ID"""
        pass
    
    @abstractmethod
    def actualizar_estado_transaccion(self, transaccion_id: int, nuevo_estado: str, datos_adicionales: Dict[str, Any] = None) -> bool:
        """Actualiza el estado de una transacción"""
        pass
    
    @abstractmethod
    def obtener_medios_pago_activos(self) -> List[Dict[str, Any]]:
        """Obtiene lista de medios de pago activos"""
        pass
    
    @abstractmethod
    def obtener_transacciones_por_pedido(self, pedido_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las transacciones de un pedido"""
        pass
    
    @abstractmethod
    def obtener_transacciones_pendientes(self) -> List[Dict[str, Any]]:
        """Obtiene transacciones pendientes de confirmación"""
        pass
    
    @abstractmethod
    def procesar_pago_unico(self, datos_pago: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa un pago único"""
        pass
    
    @abstractmethod
    def procesar_pago_dividido(self, datos_pago: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa un pago dividido en múltiples medios"""
        pass
    
    @abstractmethod
    def confirmar_transaccion(self, transaccion_id: int, datos_confirmacion: Dict[str, Any]) -> Dict[str, Any]:
        """Confirma una transacción pendiente"""
        pass
    
    @abstractmethod
    def rechazar_transaccion(self, transaccion_id: int, motivo: str) -> Dict[str, Any]:
        """Rechaza una transacción pendiente"""
        pass
    
    @abstractmethod
    def obtener_reporte_ventas_por_medio_pago(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Genera reporte de ventas agrupado por medio de pago"""
        pass
    
    @abstractmethod
    def calcular_comisiones_periodo(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Calcula las comisiones del período"""
        pass
    
    @abstractmethod
    def obtener_estadisticas_pagos(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Obtiene estadísticas generales de pagos"""
        pass
