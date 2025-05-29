from typing import List, Dict, Type
from Backend.Aplicacion.Interfaces.INotificationObserver import INotificationObserver

class ObserverServicio:
    '''
    Servicio para gestionar la notificación a los observadores.
    Permite registrar, eliminar y notificar a los observadores
    que implementan la interfaz INotificationObserver.
    '''
    def __init__(self):
        self._observers: list[INotificationObserver] = []
        self._event_observers: dict[str, list[INotificationObserver]] = {}

    def registrar_observador(self, observer: INotificationObserver) -> None:
        '''
        Registra un nuevo observador.
        Args:
            observer (INotificationObserver): El observador a registrar.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def eliminar_observador(self, observer: INotificationObserver) -> None:
        '''
        Elimina un observador registrado.
        
        Args:
            observador (INotificationObserver): El observador a eliminar.
        '''
        if observer in self._observers:
            self._observers.remove(observer)

    def registrar_observador_para_evento(self, evento: str, observer: INotificationObserver) -> None:
        '''
        Registra un observador para un evento específico.
        
        Args:
            evento (str): El nombre del evento.
            observer (INotificationObserver): El observador a registrar.
        '''
        if evento not in self._event_observers:
            self._event_observers[evento] = []
        if observer not in self._event_observers[evento]:
            self._event_observers[evento].append(observer)

    def eliminar_observador_para_evento(self, evento: str, observer: INotificationObserver) -> None:
        '''
        Elimina un observador registrado para un evento específico.
        
        Args:
            evento (str): El nombre del evento.
            observador (INotificationObserver): El observador a eliminar.
        '''
        if evento in self._event_observers and observer in self._event_observers[evento]:
            self._event_observers[evento].remove(observer)
            if not self._event_observers[evento]:
                del self._event_observers[evento]

    def notificar(self, mensaje: str, data=None) -> None:
        '''
        Notifica a todos los observadores registrados.
        Argumentos:
            mensaje (str): El mensaje a enviar a los observadores.
        '''
        for observer in self._observers:
            observer.update(mensaje, data)
    
    def notificar_evento(self, evento: str, mensaje: str) -> None:
        '''
        Notifica a los observadores registrados para un evento específico.
        
        Args:
            evento (str): El nombre del evento.
            mensaje (str): El mensaje a enviar a los observadores.
        '''
        if evento in self._event_observers:
            for observer in self._event_observers[evento]:
                observer.update(mensaje)


