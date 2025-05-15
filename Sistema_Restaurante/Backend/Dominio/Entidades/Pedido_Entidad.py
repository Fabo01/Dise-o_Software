from datetime import datetime
from typing import List, Optional, Dict
from .EntidadBase import EntidadBase
from .Cliente_Entidad import Cliente
from .Mesa_Entidad import Mesa
from .ItemPedido_Entidad import ItemPedido
from ..Excepciones.DominioExcepcion import ValidacionExcepcion, OperacionInvalidaExcepcion
from Backend.Aplicacion.Servicios.Observer_Servicio import ObserverService
from Backend.Aplicacion.Servicios.ObserversNotificaciones import CocinaNotificationObserver, MeseroNotificationObserver

class Pedido(EntidadBase):
    """
    Entidad que representa un pedido en el restaurante.
    """
    
    # Estados posibles para un pedido
    ESTADOS = ["recibido", "en_preparacion", "listo", "entregado", "pagado", "cancelado"]
    
    def __init__(self, cliente: Cliente, items: List[ItemPedido] = None, mesa: Mesa = None, observer_service: ObserverService = None):
        """
        Constructor para la entidad Pedido
        
        Args:
            cliente (Cliente): El cliente que realiza el pedido
            items (List[ItemPedido], opcional): Lista inicial de ítems del pedido
            mesa (Mesa, opcional): Mesa asociada al pedido (None para delivery/takeaway)
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        super().__init__()
        
        if not cliente:
            raise ValidacionExcepcion("El cliente es obligatorio")
        
        self._cliente = cliente
        self._items = items or []
        self._mesa = mesa
        self._estado = "recibido"  # Estado inicial
        self._fecha_pedido = datetime.now()
        self._hora_entrega = None
        self._notas = ""
        self._observer_service = observer_service
    
    # Getters
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def items(self) -> List[ItemPedido]:
        # Devolvemos una copia para evitar modificaciones directas
        return self._items.copy()
    
    @property
    def mesa(self) -> Optional[Mesa]:
        return self._mesa
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @property
    def fecha_pedido(self) -> datetime:
        return self._fecha_pedido
    
    @property
    def hora_entrega(self) -> Optional[datetime]:
        return self._hora_entrega
    
    @property
    def notas(self) -> str:
        return self._notas
    
    @property
    def total(self) -> float:
        """
        Calcula el total del pedido sumando los subtotales de cada ítem
        
        Returns:
            float: Total del pedido
        """
        return sum(item.subtotal for item in self._items)
    
    @property
    def tiempo_espera(self) -> Optional[int]:
        """
        Calcula el tiempo de espera desde que se realizó el pedido en minutos
        
        Returns:
            int: Tiempo en minutos, None si ya fue entregado
        """
        if self._estado == "entregado" and self._hora_entrega:
            delta = self._hora_entrega - self._fecha_pedido
            return int(delta.total_seconds() / 60)
            
        if self._estado in ["pagado", "cancelado"]:
            return None
            
        delta = datetime.now() - self._fecha_pedido
        return int(delta.total_seconds() / 60)
    
    # Métodos de negocio
    def agregar_item(self, item: ItemPedido):
        """
        Agrega un ítem al pedido
        
        Args:
            item (ItemPedido): Ítem a agregar
            
        Raises:
            ValidacionExcepcion: Si el ítem no es válido
            OperacionInvalidaExcepcion: Si el pedido ya no está en estado modificable
        """
        if not item:
            raise ValidacionExcepcion("El ítem no puede ser nulo")
        if self._estado not in ["recibido", "en_preparacion"]:
            raise OperacionInvalidaExcepcion(f"No se puede modificar un pedido en estado: {self._estado}")
        
        self._items.append(item)
        self.actualizar_fecha()
    
    def eliminar_item(self, item: ItemPedido) -> bool:
        """
        Elimina un ítem del pedido
        
        Args:
            item (ItemPedido): Ítem a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
            
        Raises:
            OperacionInvalidaExcepcion: Si el pedido ya no está en estado modificable
        """
        if self._estado not in ["recibido", "en_preparacion"]:
            raise OperacionInvalidaExcepcion(f"No se puede modificar un pedido en estado: {self._estado}")
        
        if item in self._items:
            self._items.remove(item)
            self.actualizar_fecha()
            return True
        return False
    
    def cambiar_estado(self, nuevo_estado: str):
        """
        Cambia el estado del pedido
        
        Args:
            nuevo_estado (str): Nuevo estado a asignar
            
        Raises:
            ValidacionExcepcion: Si el estado no es válido
            OperacionInvalidaExcepcion: Si la transición de estado no es válida
        """
        if nuevo_estado not in self.ESTADOS:
            raise ValidacionExcepcion(f"Estado no válido: {nuevo_estado}")
        
        # Validar transiciones de estado permitidas
        transiciones_permitidas = {
            "recibido": ["en_preparacion", "cancelado"],
            "en_preparacion": ["listo", "cancelado"],
            "listo": ["entregado", "cancelado"],
            "entregado": ["pagado"],
            "pagado": [],
            "cancelado": []
        }
        
        if nuevo_estado not in transiciones_permitidas[self._estado]:
            raise OperacionInvalidaExcepcion(
                f"No se puede cambiar de {self._estado} a {nuevo_estado}"
            )
        
        self._estado = nuevo_estado
        
        # Actualizar hora de entrega si corresponde
        if nuevo_estado == "entregado":
            self._hora_entrega = datetime.now()
            
        self.actualizar_fecha()
        
        # Notificar a observadores si hay observer_service
        if self._observer_service:
            mensaje = f"Pedido #{self._id or 'nuevo'} cambió a estado: {nuevo_estado}"
            self._observer_service.notificar(mensaje)
    
    def agregar_nota(self, nota: str):
        """
        Agrega una nota al pedido
        
        Args:
            nota (str): Nota a agregar
        """
        if self._notas:
            self._notas += f"\n{nota}"
        else:
            self._notas = nota
        self.actualizar_fecha()
    
    def asignar_mesa(self, mesa: Mesa):
        """
        Asigna una mesa al pedido
        
        Args:
            mesa (Mesa): Mesa a asignar
            
        Raises:
            ValidacionExcepcion: Si la mesa no es válida
            OperacionInvalidaExcepcion: Si la mesa no está libre o no se puede asignar
        """
        if not mesa:
            raise ValidacionExcepcion("La mesa no puede ser nula")
        if self._estado not in ["recibido"]:
            raise OperacionInvalidaExcepcion(f"No se puede asignar mesa a un pedido en estado: {self._estado}")
        
        self._mesa = mesa
        self.actualizar_fecha()
    
    def puede_cancelar(self) -> bool:
        """
        Verifica si el pedido puede ser cancelado según su estado actual
        
        Returns:
            bool: True si puede cancelarse, False en caso contrario
        """
        return self._estado in ["recibido", "en_preparacion", "listo"]
    
    def __str__(self):
        return f"Pedido #{self._id or 'nuevo'} - {self._estado} - Total: ${self.total:.2f}"
