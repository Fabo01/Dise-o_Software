from Backend.Aplicacion.Interfaces.INotificationObserver import INotificationObserver
from Backend.Aplicacion.Servicios.Observer_Servicio import ObserverServicio
from Backend.Dominio.Entidades.Pedido_Entidad import PedidoEntidad

class PedidoServicio:
    """
    Servicio que gestiona los pedidos y notifica a los observadores
    cuando hay cambios relevantes.
    """
    def __init__(self, observer_servicio: ObserverServicio):
        self.observer_servicio = observer_servicio
        # Registrar eventos específicos de pedidos
        self.EVENTO_NUEVO_PEDIDO = "nuevo_pedido"
        self.EVENTO_CAMBIO_ESTADO = "cambio_estado_pedido"
        self.EVENTO_PEDIDO_LISTO = "pedido_listo"
    
    def crear_pedido(self, pedido_datos):
        """Crea un nuevo pedido y notifica a los observadores"""
        # Lógica para crear pedido...
        pedido = PedidoEntidad(...)
        
        # Notificar a todos los observadores del evento específico
        self.observer_servicio.notificar_evento(
            self.EVENTO_NUEVO_PEDIDO, 
            f"Nuevo pedido #{pedido.id} creado"
        )
        
        # También podemos notificar con datos adicionales
        self.observer_servicio.notificar(
            f"Nuevo pedido: {pedido.id}", 
            {"pedido_id": pedido.id, "cliente": pedido.cliente_nombre}
        )
        
        return pedido
    
    def cambiar_estado_pedido(self, pedido_id, nuevo_estado):
        """Cambia el estado de un pedido y notifica a los observadores"""
        # Lógica para cambiar estado...
        
        # Notificar el cambio
        self.observer_servicio.notificar_evento(
            self.EVENTO_CAMBIO_ESTADO,
            f"Pedido #{pedido_id} cambió a estado: {nuevo_estado}"
        )
        
        # Si el pedido está listo, notificar evento específico
        if nuevo_estado == "listo":
            self.observer_servicio.notificar_evento(
                self.EVENTO_PEDIDO_LISTO,
                f"Pedido #{pedido_id} está listo para servir"
            )
