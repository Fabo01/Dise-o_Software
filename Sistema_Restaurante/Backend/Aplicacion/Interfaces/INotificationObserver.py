from abc import ABC, abstractmethod

class INotificationObserver(ABC):
    """
    Interfaz para el patrón Observer, que permite a los observadores recibir notificaciones de eventos.
    
    Métodos:
        - update: Método que se llama cuando se produce un evento al que el observador está suscrito.
    """
    
    @abstractmethod
    def update(self, mensaje: str) -> None:
        """
        Método que se llama cuando se produce un evento al que el observador está suscrito.
        
        Args:
            mensaje (str): Mensaje o información sobre el evento.
        """
        pass