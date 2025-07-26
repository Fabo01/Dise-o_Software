# Backend/Dominio/Interfaces/IAnalyticsRepositorio.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal

class IAnalyticsRepositorio(ABC):
    """
    Interfaz para el repositorio de analytics y reportes.
    Define las operaciones de acceso a datos para el sistema de analytics.
    """
    
    @abstractmethod
    def obtener_ventas_por_periodo(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene datos de ventas en un período específico"""
        pass
    
    @abstractmethod
    def obtener_productos_mas_vendidos(self, limite: int = 10, fecha_inicio: Optional[date] = None, 
                                     fecha_fin: Optional[date] = None) -> List[Dict[str, Any]]:
        """Obtiene los productos más vendidos"""
        pass
    
    @abstractmethod
    def obtener_estadisticas_mesas(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene estadísticas de uso de mesas"""
        pass
    
    @abstractmethod
    def obtener_ingresos_por_metodo_pago(self, fecha_inicio: date, fecha_fin: date) -> List[Dict[str, Any]]:
        """Obtiene ingresos desglosados por método de pago"""
        pass
    
    @abstractmethod
    def obtener_tendencias_pedidos(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene tendencias de pedidos por horas/días"""
        pass
    
    @abstractmethod
    def obtener_estadisticas_delivery(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene estadísticas del servicio de delivery"""
        pass
    
    @abstractmethod
    def obtener_satisfaccion_cliente(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene métricas de satisfacción del cliente"""
        pass
    
    @abstractmethod
    def obtener_rendimiento_empleados(self, fecha_inicio: date, fecha_fin: date) -> List[Dict[str, Any]]:
        """Obtiene métricas de rendimiento de empleados"""
        pass
    
    @abstractmethod
    def obtener_costos_operacionales(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene análisis de costos operacionales"""
        pass
    
    @abstractmethod
    def generar_reporte_ejecutivo(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Genera reporte ejecutivo consolidado"""
        pass
    
    @abstractmethod
    def obtener_predicciones_demanda(self, dias_adelante: int = 7) -> Dict[str, Any]:
        """Obtiene predicciones de demanda basadas en datos históricos"""
        pass
