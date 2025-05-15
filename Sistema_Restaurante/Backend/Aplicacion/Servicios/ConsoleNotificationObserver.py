from datetime import datetime
from Backend.Aplicacion.Interfaces.INotificationObserver import INotificationObserver

class ConsoleNotificationObserver(INotificationObserver):
    """
    Observador que muestra las notificaciones en la consola.
    Implementa la interfaz INotificationObserver para poder ser registrado
    en el servicio de observadores.
    """
    
    def __init__(self, prefix="[SISTEMA]"):
        """
        Constructor del observador de consola.
        
        Args:
            prefix (str, opcional): Prefijo para los mensajes. Por defecto "[SISTEMA]".
        """
        self.prefix = prefix
        self.log_enabled = True
        print(f"{self.prefix} ConsoleNotificationObserver inicializado y listo para recibir notificaciones.")
    
    def update(self, mensaje: str) -> None:
        """
        Implementación del método de la interfaz INotificationObserver.
        Muestra el mensaje en la consola con timestamp y formato.
        
        Args:
            mensaje (str): El mensaje a mostrar
        """
        if not self.log_enabled:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{self.prefix} [{timestamp}] {mensaje}")
    
    def enable_logging(self) -> None:
        """
        Activa el registro de mensajes en consola.
        """
        self.log_enabled = True
        print(f"{self.prefix} Registro de notificaciones activado.")
    
    def disable_logging(self) -> None:
        """
        Desactiva el registro de mensajes en consola.
        """
        print(f"{self.prefix} Registro de notificaciones desactivado.")
        self.log_enabled = False
    
    def change_prefix(self, new_prefix: str) -> None:
        """
        Cambia el prefijo de los mensajes.
        
        Args:
            new_prefix (str): El nuevo prefijo a utilizar
        """
        old_prefix = self.prefix
        self.prefix = new_prefix
        print(f"{old_prefix} Prefijo cambiado a: {self.prefix}")