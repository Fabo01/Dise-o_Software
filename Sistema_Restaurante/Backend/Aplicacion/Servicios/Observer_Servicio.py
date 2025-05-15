from typing import List
from Backend.Dominio.Interfaces.INotificationObserver import INotificationObserver

class ObserverService:
    """
    Servicio para gestionar observadores y notificar eventos (patrón Observer) en la capa de aplicación.
    """
    def __init__(self):
        self._observers: List[INotificationObserver] = []

    def registrar_observador(self, observer: INotificationObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def eliminar_observador(self, observer: INotificationObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar(self, mensaje: str):
        for observer in self._observers:
            observer.update(mensaje)
