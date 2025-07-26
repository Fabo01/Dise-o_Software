# Backend/Dominio/Interfaces/IPagosRepositorio.py
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from Backend.Dominio.Entidades.Transaccion_Entidad import TransaccionEntidad

class IPagosRepositorio(ABC):
    """
    Interfaz para el repositorio de pagos y transacciones.
    Define las operaciones de acceso a datos para el sistema de pagos.
    """
    
    @abstractmethod
    def crear_transaccion(self, transaccion: TransaccionEntidad) -> TransaccionEntidad:
        """Crea una nueva transacción"""
        pass
    
    @abstractmethod
    def obtener_transaccion_por_id(self, transaccion_id: int) -> Optional[TransaccionEntidad]:
        """Obtiene una transacción por su ID"""
        pass
    
    @abstractmethod
    def listar_transacciones_por_pedido(self, pedido_id: int) -> List[TransaccionEntidad]:
        """Lista todas las transacciones de un pedido específico"""
        pass
    
    @abstractmethod
    def listar_transacciones_por_periodo(self, fecha_inicio, fecha_fin) -> List[TransaccionEntidad]:
        """Lista transacciones en un período específico"""
        pass
    
    @abstractmethod
    def obtener_medios_pago_activos(self) -> List:
        """Obtiene lista de medios de pago activos"""
        pass
    
    @abstractmethod
    def validar_pago_externo(self, medio_pago_id: int, monto: Decimal, referencia: str) -> bool:
        """Valida un pago con servicio externo"""
        pass
    
    @abstractmethod
    def calcular_comisiones_periodo(self, fecha_inicio, fecha_fin) -> Decimal:
        """Calcula el total de comisiones en un período"""
        pass
    
    @abstractmethod
    def generar_comprobante_pago(self, transaccion_id: int) -> bytes:
        """Genera comprobante PDF de una transacción"""
        pass
    
    @abstractmethod
    def actualizar_estado_transaccion(self, transaccion_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de una transacción"""
        pass
