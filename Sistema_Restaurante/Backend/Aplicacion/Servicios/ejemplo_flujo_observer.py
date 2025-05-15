from Backend.Aplicacion.Servicios.Observer_Servicio import ObserverService
from Backend.Aplicacion.Servicios.ObserversNotificaciones import CocinaNotificationObserver, MeseroNotificationObserver
from Backend.Dominio.Entidades.Pedido_Entidad import Pedido

# Inicialización del servicio de observadores en la capa de aplicación
observer_service = ObserverService()
observer_service.registrar_observador(CocinaNotificationObserver())
observer_service.registrar_observador(MeseroNotificationObserver())

# Ejemplo de creación y uso de un pedido
# pedido = Pedido(cliente, items, mesa, observer_service=observer_service)
# pedido.cambiar_estado("en_preparacion")
# pedido.cambiar_estado("listo")
# pedido.cambiar_estado("entregado")
