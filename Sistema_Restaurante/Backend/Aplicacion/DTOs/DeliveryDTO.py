# Backend/Aplicacion/DTOs/DeliveryDTO.py
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime

@dataclass
class CrearDeliveryDTO:
    """
    DTO para crear un nuevo pedido de delivery.
    """
    pedido_id: int
    direccion_entrega: str
    telefono_contacto: str
    coordenadas_lat: Decimal
    coordenadas_lng: Decimal
    tiempo_estimado: int  # minutos
    costo_delivery: Decimal
    notas_especiales: Optional[str] = None

@dataclass
class DeliveryPedidoDTO:
    """
    DTO para representar un pedido de delivery completo.
    """
    id: Optional[int] = None
    pedido_id: int = None
    direccion_entrega: str = None
    telefono_contacto: str = None
    coordenadas_lat: Decimal = None
    coordenadas_lng: Decimal = None
    tiempo_estimado: int = None
    costo_delivery: Decimal = None
    estado: str = None
    repartidor_id: Optional[int] = None
    ubicacion_actual_lat: Optional[Decimal] = None
    ubicacion_actual_lng: Optional[Decimal] = None
    fecha_creacion: Optional[datetime] = None
    fecha_entrega: Optional[datetime] = None
    notas_especiales: Optional[str] = None

@dataclass
class ActualizarUbicacionDTO:
    """
    DTO para actualizar la ubicación del repartidor.
    """
    delivery_id: int
    latitud: Decimal
    longitud: Decimal

@dataclass
class AsignarRepartidorDTO:
    """
    DTO para asignar un repartidor a un delivery.
    """
    delivery_id: int
    repartidor_id: int
