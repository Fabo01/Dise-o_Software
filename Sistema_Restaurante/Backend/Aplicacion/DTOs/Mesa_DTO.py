"""
Data Transfer Objects para la gestión de Mesas.
Define las estructuras de datos para transferir información de mesas entre capas.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class MesaDTO:
    """
    DTO base para representar una mesa.
    """
    id: int
    numero: str
    capacidad: int
    estado: str
    ubicacion: Optional[str] = None
    caracteristicas: Optional[str] = None
    tipo_mesa: Optional[str] = None
    activa: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None


@dataclass
class CrearMesaDTO:
    """
    DTO para crear una nueva mesa.
    """
    numero: str
    capacidad: int
    ubicacion: Optional[str] = None
    caracteristicas: Optional[str] = None
    tipo_mesa: Optional[str] = None
    estado: str = 'libre'


@dataclass
class ActualizarMesaDTO:
    """
    DTO para actualizar una mesa existente.
    """
    numero: Optional[str] = None
    capacidad: Optional[int] = None
    ubicacion: Optional[str] = None
    caracteristicas: Optional[str] = None
    tipo_mesa: Optional[str] = None
    estado: Optional[str] = None


@dataclass
class CambiarEstadoMesaDTO:
    """
    DTO para cambiar el estado de una mesa.
    """
    estado: str


@dataclass
class EstadisticasMesasDTO:
    """
    DTO para estadísticas de mesas.
    """
    total_mesas: int
    mesas_disponibles: int
    mesas_ocupadas: int
    mesas_reservadas: int
    mesas_fuera_servicio: int
    porcentaje_ocupacion: float
    capacidad_total: int
    capacidad_disponible: int
