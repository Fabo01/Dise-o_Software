from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class MenuDTO:
    """
    DTO para transferir datos del menú entre capas.
    """
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    precio: Decimal = Decimal('0.00')
    categoria: str = ""
    tipo: str = ""
    imagen: str = ""
    disponible: bool = True
    tiempo_preparacion: int = 15
    veces_ordenado: int = 0
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    ingredientes: List[Dict] = None
    
    def __post_init__(self):
        """Inicializa valores por defecto después de la creación."""
        if self.ingredientes is None:
            self.ingredientes = []

@dataclass
class MenuCrearDTO:
    """
    DTO específico para crear un nuevo menú.
    Contiene solo los campos necesarios para la creación.
    """
    nombre: str
    descripcion: str
    precio: Decimal
    categoria: str = ""
    tipo: str = ""
    imagen: str = ""
    tiempo_preparacion: int = 15

@dataclass
class MenuActualizarDTO:
    """
    DTO específico para actualizar un menú existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    categoria: Optional[str] = None
    tipo: Optional[str] = None
    imagen: Optional[str] = None
    disponible: Optional[bool] = None
    tiempo_preparacion: Optional[int] = None

@dataclass
class MenuIngredienteDTO:
    """
    DTO para representar la relación entre menú e ingrediente.
    """
    ingrediente_id: int
    ingrediente_nombre: Optional[str] = None
    cantidad: Decimal = Decimal('0.00')
    unidad: Optional[str] = None

@dataclass
class MenuBusquedaDTO:
    """
    DTO para criterios de búsqueda de menús.
    """
    texto: Optional[str] = None
    categoria: Optional[str] = None
    tipo: Optional[str] = None
    precio_min: Optional[Decimal] = None
    precio_max: Optional[Decimal] = None
    disponible: Optional[bool] = None
    con_ingrediente: Optional[int] = None

@dataclass
class MenuDisponibilidadDTO:
    """
    DTO para verificar la disponibilidad de un menú.
    """
    menu_id: int
    menu_nombre: str
    disponible: bool
    razon_no_disponible: Optional[str] = None
    ingredientes_faltantes: List[str] = None
    
    def __post_init__(self):
        """Inicializa valores por defecto después de la creación."""
        if self.ingredientes_faltantes is None:
            self.ingredientes_faltantes = []

@dataclass
class MenuEstadisticasDTO:
    """
    DTO para estadísticas de menús.
    """
    total_menus: int = 0
    menus_disponibles: int = 0
    menus_no_disponibles: int = 0
    por_categoria: Dict[str, int] = None
    por_tipo: Dict[str, int] = None
    precio_promedio: Decimal = Decimal('0.00')
    precio_minimo: Decimal = Decimal('0.00')
    precio_maximo: Decimal = Decimal('0.00')
    
    def __post_init__(self):
        """Inicializa valores por defecto después de la creación."""
        if self.por_categoria is None:
            self.por_categoria = {}
        if self.por_tipo is None:
            self.por_tipo = {}

@dataclass
class MenuListaDTO:
    """
    DTO para listas de menús con información resumida.
    """
    id: str
    nombre: str
    precio: Decimal
    categoria: str
    disponible: bool
    imagen: str = ""

@dataclass
class MenuDetalleDTO:
    """
    DTO para información detallada de un menú específico.
    """
    id: str
    nombre: str
    descripcion: str
    precio: Decimal
    categoria: str
    tipo: str
    imagen: str
    disponible: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    ingredientes: List[MenuIngredienteDTO]
    costo_ingredientes: Optional[Decimal] = None
    margen_ganancia: Optional[Decimal] = None
