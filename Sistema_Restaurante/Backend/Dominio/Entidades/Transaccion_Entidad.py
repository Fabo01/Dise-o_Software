# Backend/Dominio/Entidades/Transaccion_Entidad.py
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime

@dataclass
class TransaccionEntidad:
    """
    Entidad que representa una transacción de pago.
    """
    id: Optional[int] = None
    pedido_id: int = None
    medio_pago_id: int = None
    monto: Decimal = None
    comision: Decimal = None
    estado: str = None  # pendiente, completado, fallido, cancelado
    referencia_externa: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_procesamiento: Optional[datetime] = None
    notas: Optional[str] = None
