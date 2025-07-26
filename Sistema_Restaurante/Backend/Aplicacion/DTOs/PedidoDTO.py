from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from Backend.Dominio.Entidades.Pedido_Entidad import EstadoPedido, TipoPedido


@dataclass
class ItemPedidoDTO:
    """DTO para un item individual de pedido"""
    menu_id: int
    nombre_menu: str
    precio_unitario: float
    cantidad: int
    observaciones: Optional[str] = None
    subtotal: Optional[float] = None


@dataclass
class PedidoDTO:
    """DTO principal para pedidos"""
    id: Optional[int]
    cliente_id: int
    cliente_nombre: Optional[str]
    cliente_rut: Optional[str]
    tipo_pedido: str
    estado: str
    mesa_id: Optional[int]
    mesa_numero: Optional[str]
    direccion_entrega: Optional[str]
    telefono_contacto: Optional[str]
    observaciones_generales: Optional[str]
    fecha_creacion: Optional[datetime]
    fecha_confirmacion: Optional[datetime]
    fecha_entrega: Optional[datetime]
    tiempo_preparacion_estimado: Optional[int]
    total: float
    items: List[ItemPedidoDTO]
    cantidad_total_items: Optional[int] = None
    tiempo_transcurrido: Optional[int] = None
    esta_atrasado: Optional[bool] = None


@dataclass
class PedidoCrearDTO:
    """DTO para crear un nuevo pedido"""
    cliente_id: int
    tipo_pedido: str
    items: List[Dict[str, Any]]  # Lista de dicts con menu_id, cantidad, observaciones
    mesa_id: Optional[int] = None
    direccion_entrega: Optional[str] = None
    telefono_contacto: Optional[str] = None
    observaciones_generales: Optional[str] = None
    tiempo_preparacion_estimado: Optional[int] = None


@dataclass
class PedidoActualizarDTO:
    """DTO para actualizar un pedido existente"""
    id: int
    tipo_pedido: Optional[str] = None
    mesa_id: Optional[int] = None
    direccion_entrega: Optional[str] = None
    telefono_contacto: Optional[str] = None
    observaciones_generales: Optional[str] = None
    tiempo_preparacion_estimado: Optional[int] = None
    items: Optional[List[Dict[str, Any]]] = None


@dataclass
class PedidoCambiarEstadoDTO:
    """DTO para cambiar el estado de un pedido"""
    id: int
    nuevo_estado: str
    tiempo_preparacion: Optional[int] = None
    motivo_cancelacion: Optional[str] = None


@dataclass
class PedidoBusquedaDTO:
    """DTO para criterios de búsqueda de pedidos"""
    cliente_id: Optional[int] = None
    estado: Optional[str] = None
    tipo_pedido: Optional[str] = None
    mesa_id: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    texto: Optional[str] = None
    solo_activos: bool = False
    limite: Optional[int] = None
    desplazamiento: int = 0


@dataclass
class PedidoResumenDTO:
    """DTO con información resumida de un pedido"""
    id: int
    cliente_nombre: str
    tipo_pedido: str
    estado: str
    mesa_numero: Optional[str]
    total: float
    cantidad_items: int
    fecha_creacion: datetime
    tiempo_transcurrido: Optional[int]
    esta_atrasado: bool


@dataclass
class PedidoEstadisticasDTO:
    """DTO para estadísticas de pedidos"""
    total_pedidos: int
    total_ventas: float
    pedidos_por_estado: Dict[str, int]
    pedidos_por_tipo: Dict[str, int]
    tiempo_promedio_preparacion: float
    pedidos_atrasados: int
    ventas_por_fecha: Dict[str, float]


@dataclass
class PedidoHistorialDTO:
    """DTO para el historial de pedidos de un cliente"""
    cliente_id: int
    cliente_nombre: str
    total_pedidos: int
    total_gastado: float
    ultimo_pedido: Optional[datetime]
    pedidos: List[PedidoResumenDTO]


@dataclass
class ItemMenuDisponibleDTO:
    """DTO para items del menú disponibles para pedidos"""
    id: int
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    disponible: bool
    tiempo_preparacion: Optional[int]
    ingredientes: List[str]


@dataclass
class PedidoValidacionDTO:
    """DTO para validar un pedido antes de crearlo"""
    es_valido: bool
    errores: List[str]
    advertencias: List[str]
    total_estimado: float
    tiempo_preparacion_total: Optional[int]


@dataclass
class PedidoCocinaDTO:
    """DTO optimizado para mostrar pedidos en cocina"""
    id: int
    numero_mesa: Optional[str]
    tipo_pedido: str
    estado: str
    tiempo_transcurrido: Optional[int]
    tiempo_estimado: Optional[int]
    esta_atrasado: bool
    items: List[Dict[str, Any]]  # Solo info relevante para cocina
    observaciones: Optional[str]
    prioridad: str  # alta, media, baja


@dataclass
class PedidoEntregaDTO:
    """DTO para información de entrega de pedidos"""
    id: int
    cliente_nombre: str
    telefono: Optional[str]
    direccion: Optional[str]
    tipo_pedido: str
    total: float
    estado: str
    items_resumen: str
    tiempo_preparacion: Optional[int]


@dataclass
class PedidoReporteDTO:
    """DTO para reportes de pedidos"""
    fecha: date
    total_pedidos: int
    total_ventas: float
    pedidos_completados: int
    pedidos_cancelados: int
    tiempo_promedio: float
    item_mas_vendido: Optional[str]
    hora_pico: Optional[str]
