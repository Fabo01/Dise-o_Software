from datetime import datetime
from typing import List, Optional
from enum import Enum
from .EntidadBase import EntidadBase
from ..Objetos_Valor.PrecioVO import PrecioVO
from ..Excepciones.DominioExcepcion import DominioExcepcion


class EstadoPedido(Enum):
    """Estados posibles de un pedido"""
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class TipoPedido(Enum):
    """Tipos de pedido disponibles"""
    MESA = "mesa"
    DELIVERY = "delivery"
    PARA_LLEVAR = "para_llevar"


class ItemPedido:
    """Representa un item individual dentro de un pedido"""
    
    def __init__(
        self,
        menu_id: int,
        nombre_menu: str,
        precio_unitario: PrecioVO,
        cantidad: int,
        observaciones: Optional[str] = None
    ):
        self._menu_id = menu_id
        self._nombre_menu = nombre_menu
        self._precio_unitario = precio_unitario
        self._cantidad = self._validar_cantidad(cantidad)
        self._observaciones = observaciones

    def _validar_cantidad(self, cantidad: int) -> int:
        """Valida que la cantidad sea válida"""
        if cantidad <= 0:
            raise DominioExcepcion("La cantidad debe ser mayor a 0")
        if cantidad > 50:  # Límite razonable
            raise DominioExcepcion("La cantidad no puede ser mayor a 50 unidades por item")
        return cantidad

    @property
    def menu_id(self) -> int:
        return self._menu_id

    @property
    def nombre_menu(self) -> str:
        return self._nombre_menu

    @property
    def precio_unitario(self) -> PrecioVO:
        return self._precio_unitario

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def observaciones(self) -> Optional[str]:
        return self._observaciones

    @property
    def subtotal(self) -> PrecioVO:
        """Calcula el subtotal del item"""
        return PrecioVO(self._precio_unitario.valor * self._cantidad)

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        """Actualiza la cantidad del item"""
        self._cantidad = self._validar_cantidad(nueva_cantidad)

    def actualizar_observaciones(self, observaciones: str) -> None:
        """Actualiza las observaciones del item"""
        self._observaciones = observaciones


class PedidoEntidad(EntidadBase):
    """Entidad de dominio que representa un pedido en el restaurante"""
    
    def __init__(
        self,
        cliente_id: int,
        tipo_pedido: TipoPedido,
        items: List[ItemPedido],
        mesa_id: Optional[int] = None,
        direccion_entrega: Optional[str] = None,
        telefono_contacto: Optional[str] = None,
        observaciones_generales: Optional[str] = None,
        id: Optional[int] = None,
        fecha_creacion: Optional[datetime] = None
    ):
        super().__init__(id, fecha_creacion)
        self._cliente_id = cliente_id
        self._tipo_pedido = tipo_pedido
        self._items = self._validar_items(items)
        self._mesa_id = mesa_id
        self._direccion_entrega = direccion_entrega
        self._telefono_contacto = telefono_contacto
        self._observaciones_generales = observaciones_generales
        self._estado = EstadoPedido.PENDIENTE
        self._fecha_confirmacion: Optional[datetime] = None
        self._fecha_entrega: Optional[datetime] = None
        self._tiempo_preparacion_estimado: Optional[int] = None  # en minutos
        
        self._validar_tipo_pedido()

    def _validar_items(self, items: List[ItemPedido]) -> List[ItemPedido]:
        """Valida que los items del pedido sean válidos"""
        if not items:
            raise DominioExcepcion("Un pedido debe tener al menos un item")
        if len(items) > 100:  # Límite razonable
            raise DominioExcepcion("Un pedido no puede tener más de 100 items")
        return items

    def _validar_tipo_pedido(self) -> None:
        """Valida que el tipo de pedido sea consistente con los datos"""
        if self._tipo_pedido == TipoPedido.MESA and self._mesa_id is None:
            raise DominioExcepcion("Un pedido de mesa debe tener un ID de mesa")
        if self._tipo_pedido == TipoPedido.DELIVERY and not self._direccion_entrega:
            raise DominioExcepcion("Un pedido de delivery debe tener dirección de entrega")

    @property
    def cliente_id(self) -> int:
        return self._cliente_id

    @property
    def tipo_pedido(self) -> TipoPedido:
        return self._tipo_pedido

    @property
    def items(self) -> List[ItemPedido]:
        return self._items.copy()

    @property
    def mesa_id(self) -> Optional[int]:
        return self._mesa_id

    @property
    def direccion_entrega(self) -> Optional[str]:
        return self._direccion_entrega

    @property
    def telefono_contacto(self) -> Optional[str]:
        return self._telefono_contacto

    @property
    def observaciones_generales(self) -> Optional[str]:
        return self._observaciones_generales

    @property
    def estado(self) -> EstadoPedido:
        return self._estado

    @property
    def fecha_confirmacion(self) -> Optional[datetime]:
        return self._fecha_confirmacion

    @property
    def fecha_entrega(self) -> Optional[datetime]:
        return self._fecha_entrega

    @property
    def tiempo_preparacion_estimado(self) -> Optional[int]:
        return self._tiempo_preparacion_estimado

    @property
    def total(self) -> PrecioVO:
        """Calcula el total del pedido"""
        total_valor = sum(item.subtotal.valor for item in self._items)
        return PrecioVO(total_valor)

    @property
    def cantidad_total_items(self) -> int:
        """Retorna la cantidad total de items en el pedido"""
        return sum(item.cantidad for item in self._items)

    def agregar_item(self, item: ItemPedido) -> None:
        """Agrega un item al pedido si está en estado modificable"""
        if not self._puede_modificar_items():
            raise DominioExcepcion(f"No se pueden agregar items en estado {self._estado.value}")
        
        self._items.append(item)
        
        if len(self._items) > 100:
            raise DominioExcepcion("Un pedido no puede tener más de 100 items")

    def remover_item(self, index: int) -> None:
        """Remueve un item del pedido por índice"""
        if not self._puede_modificar_items():
            raise DominioExcepcion(f"No se pueden remover items en estado {self._estado.value}")
        
        if index < 0 or index >= len(self._items):
            raise DominioExcepcion("Índice de item inválido")
        
        self._items.pop(index)
        
        if not self._items:
            raise DominioExcepcion("Un pedido debe tener al menos un item")

    def actualizar_item(self, index: int, item: ItemPedido) -> None:
        """Actualiza un item específico del pedido"""
        if not self._puede_modificar_items():
            raise DominioExcepcion(f"No se pueden modificar items en estado {self._estado.value}")
        
        if index < 0 or index >= len(self._items):
            raise DominioExcepcion("Índice de item inválido")
        
        self._items[index] = item

    def confirmar_pedido(self, tiempo_preparacion: Optional[int] = None) -> None:
        """Confirma el pedido y establece el tiempo de preparación"""
        if self._estado != EstadoPedido.PENDIENTE:
            raise DominioExcepcion(f"Solo se pueden confirmar pedidos pendientes, estado actual: {self._estado.value}")
        
        self._estado = EstadoPedido.CONFIRMADO
        self._fecha_confirmacion = datetime.now()
        
        if tiempo_preparacion:
            self._tiempo_preparacion_estimado = tiempo_preparacion

    def iniciar_preparacion(self) -> None:
        """Marca el pedido como en preparación"""
        if self._estado != EstadoPedido.CONFIRMADO:
            raise DominioExcepcion(f"Solo se pueden preparar pedidos confirmados, estado actual: {self._estado.value}")
        
        self._estado = EstadoPedido.EN_PREPARACION

    def marcar_listo(self) -> None:
        """Marca el pedido como listo para entrega"""
        if self._estado != EstadoPedido.EN_PREPARACION:
            raise DominioExcepcion(f"Solo se pueden marcar como listos pedidos en preparación, estado actual: {self._estado.value}")
        
        self._estado = EstadoPedido.LISTO

    def entregar_pedido(self) -> None:
        """Marca el pedido como entregado"""
        if self._estado != EstadoPedido.LISTO:
            raise DominioExcepcion(f"Solo se pueden entregar pedidos listos, estado actual: {self._estado.value}")
        
        self._estado = EstadoPedido.ENTREGADO
        self._fecha_entrega = datetime.now()

    def cancelar_pedido(self, motivo: Optional[str] = None) -> None:
        """Cancela el pedido si está en estado cancelable"""
        if self._estado in [EstadoPedido.ENTREGADO, EstadoPedido.CANCELADO]:
            raise DominioExcepcion(f"No se puede cancelar un pedido {self._estado.value}")
        
        self._estado = EstadoPedido.CANCELADO
        if motivo:
            self._observaciones_generales = f"CANCELADO: {motivo}"

    def actualizar_observaciones(self, observaciones: str) -> None:
        """Actualiza las observaciones generales del pedido"""
        self._observaciones_generales = observaciones

    def actualizar_telefono_contacto(self, telefono: str) -> None:
        """Actualiza el teléfono de contacto"""
        self._telefono_contacto = telefono

    def _puede_modificar_items(self) -> bool:
        """Determina si los items del pedido pueden ser modificados"""
        return self._estado in [EstadoPedido.PENDIENTE, EstadoPedido.CONFIRMADO]

    def obtener_tiempo_transcurrido(self) -> Optional[int]:
        """Retorna el tiempo transcurrido desde la confirmación en minutos"""
        if not self._fecha_confirmacion:
            return None
        
        tiempo_transcurrido = datetime.now() - self._fecha_confirmacion
        return int(tiempo_transcurrido.total_seconds() / 60)

    def esta_atrasado(self) -> bool:
        """Determina si el pedido está atrasado según el tiempo estimado"""
        if not self._tiempo_preparacion_estimado or not self._fecha_confirmacion:
            return False
        
        tiempo_transcurrido = self.obtener_tiempo_transcurrido()
        return tiempo_transcurrido > self._tiempo_preparacion_estimado

    def obtener_resumen(self) -> str:
        """Retorna un resumen del pedido para mostrar"""
        items_resumen = ", ".join([f"{item.cantidad}x {item.nombre_menu}" for item in self._items])
        return f"Pedido #{self.id} - {self._tipo_pedido.value} - ${self.total.valor} - {items_resumen}"
