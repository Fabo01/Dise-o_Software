from datetime import datetime
from typing import Optional
from .Pedido_Entidad import Pedido
from .Cliente_Entidad import Cliente
from .ItemPedido_Entidad import ItemPedido
from ..Excepciones.DominioExcepcion import ValidacionExcepcion, OperacionInvalidaExcepcion

class DireccionEntrega:
    """
    Clase auxiliar que representa una dirección de entrega para pedidos delivery
    """
    
    def __init__(self, calle, numero, ciudad, referencias="", codigo_postal=""):
        self.calle = calle
        self.numero = numero
        self.ciudad = ciudad
        self.referencias = referencias
        self.codigo_postal = codigo_postal
    
    def __str__(self):
        return f"{self.calle} {self.numero}, {self.ciudad}"

class DeliveryPedido(Pedido):
    """
    Entidad que representa un pedido para entrega a domicilio (delivery).
    Extiende la clase Pedido con funcionalidades específicas para delivery.
    """
    
    # Estados adicionales para delivery
    ESTADOS_DELIVERY = ["recibido", "en_preparacion", "listo", "en_camino", "entregado", "pagado", "cancelado"]
    
    def __init__(self, cliente: Cliente, items=None, direccion_entrega=None, telefono_contacto="", aplicacion_externa=None, costo_envio=0.0):
        """
        Constructor para la entidad DeliveryPedido
        
        Args:
            cliente (Cliente): Cliente que realiza el pedido
            items (list, opcional): Lista inicial de ítems del pedido
            direccion_entrega (DireccionEntrega, opcional): Dirección donde entregar el pedido
            telefono_contacto (str, opcional): Teléfono para contacto durante la entrega
            aplicacion_externa (str, opcional): Nombre de la app si el pedido viene de plataforma externa
            costo_envio (float, opcional): Costo adicional por la entrega
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        # Llamamos al constructor de la clase padre
        super().__init__(cliente, items, mesa=None)
        
        # Inicializamos propiedades específicas de delivery
        self._direccion_entrega = direccion_entrega
        self._telefono_contacto = telefono_contacto
        self._aplicacion_externa = aplicacion_externa
        self._costo_envio = costo_envio
        self._repartidor = None
        self._codigo_seguimiento = None
        self._hora_salida = None
        self._tiempo_estimado_entrega = None
    
    # Sobrescribimos la propiedad para usar los estados de delivery
    @property
    def estado(self) -> str:
        return self._estado
    
    # Getters específicos de delivery
    @property
    def direccion_entrega(self) -> Optional[DireccionEntrega]:
        return self._direccion_entrega
    
    @property
    def telefono_contacto(self) -> str:
        return self._telefono_contacto
    
    @property
    def aplicacion_externa(self) -> Optional[str]:
        return self._aplicacion_externa
    
    @property
    def costo_envio(self) -> float:
        return self._costo_envio
    
    @property
    def repartidor(self):
        return self._repartidor
    
    @property
    def codigo_seguimiento(self) -> Optional[str]:
        return self._codigo_seguimiento
    
    @property
    def hora_salida(self) -> Optional[datetime]:
        return self._hora_salida
    
    @property
    def tiempo_estimado_entrega(self) -> Optional[int]:
        """
        Tiempo estimado de entrega en minutos
        """
        return self._tiempo_estimado_entrega
    
    # Sobrescribimos el cálculo del total para incluir costo de envío
    @property
    def total(self) -> float:
        return super().total + self._costo_envio
    
    # Métodos específicos de delivery
    def asignar_repartidor(self, repartidor):
        """
        Asigna un repartidor al pedido
        
        Args:
            repartidor: Repartidor a asignar
            
        Raises:
            ValidacionExcepcion: Si el repartidor no es válido
            OperacionInvalidaExcepcion: Si el pedido no está en estado válido para asignar repartidor
        """
        if not repartidor:
            raise ValidacionExcepcion("El repartidor no puede ser nulo")
        
        if self._estado not in ["listo"]:
            raise OperacionInvalidaExcepcion(
                f"No se puede asignar repartidor a un pedido en estado: {self._estado}"
            )
        
        self._repartidor = repartidor
        self._codigo_seguimiento = self._generar_codigo_seguimiento()
        self.actualizar_fecha()
    
    def marcar_en_camino(self, tiempo_estimado_minutos=None):
        """
        Marca el pedido como en camino al destino
        
        Args:
            tiempo_estimado_minutos (int, opcional): Tiempo estimado de llegada en minutos
            
        Raises:
            OperacionInvalidaExcepcion: Si el pedido no está en estado válido o no tiene repartidor
        """
        if self._estado != "listo":
            raise OperacionInvalidaExcepcion(
                f"No se puede marcar en camino un pedido en estado: {self._estado}"
            )
        
        if not self._repartidor:
            raise OperacionInvalidaExcepcion(
                "No se puede marcar en camino un pedido sin repartidor asignado"
            )
        
        self._estado = "en_camino"
        self._hora_salida = datetime.now()
        self._tiempo_estimado_entrega = tiempo_estimado_minutos
        self.actualizar_fecha()
    
    def definir_direccion_entrega(self, direccion: DireccionEntrega):
        """
        Define o actualiza la dirección de entrega
        
        Args:
            direccion (DireccionEntrega): Dirección de entrega
            
        Raises:
            ValidacionExcepcion: Si la dirección no es válida
        """
        if not direccion:
            raise ValidacionExcepcion("La dirección no puede ser nula")
        
        self._direccion_entrega = direccion
        self.actualizar_fecha()
    
    def actualizar_costo_envio(self, nuevo_costo: float):
        """
        Actualiza el costo de envío
        
        Args:
            nuevo_costo (float): Nuevo costo de envío
            
        Raises:
            ValidacionExcepcion: Si el costo no es válido
        """
        if nuevo_costo < 0:
            raise ValidacionExcepcion("El costo de envío no puede ser negativo")
        
        self._costo_envio = nuevo_costo
        self.actualizar_fecha()
    
    def _generar_codigo_seguimiento(self) -> str:
        """
        Genera un código único de seguimiento para el pedido
        
        Returns:
            str: Código de seguimiento
        """
        import uuid
        import random
        
        # Generamos un código aleatorio basado en timestamp y UUID
        seed = f"{datetime.now().timestamp()}-{uuid.uuid4()}"
        return f"DEL-{hash(seed) % 100000:05d}"
    
    def __str__(self):
        app_info = f" via {self._aplicacion_externa}" if self._aplicacion_externa else ""
        return f"Delivery{app_info} #{self._id or 'nuevo'} - {self._estado} - Total: ${self.total:.2f}"
