'''
Observadores para las notificaciones del sistema.
'''
from ..Interfaces.INotificationObserver import INotificationObserver

class CocinaNotificationObserver(INotificationObserver):
    def update(self, mensaje: str) -> None:
        # Lógica para notificar a la cocina (ejemplo: actualizar panel de cocina)
        print(f"[Cocina] Notificación: {mensaje}")

class MeseroNotificationObserver(INotificationObserver):
    def update(self, mensaje: str) -> None:
        # Lógica para notificar al mesero (ejemplo: enviar alerta al dispositivo del mesero)
        print(f"[Mesero] Notificación: {mensaje}")
