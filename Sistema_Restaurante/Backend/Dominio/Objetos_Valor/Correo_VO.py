import re

class CorreoVO:
    """
    Objeto de valor inmutable que representa un correo.
    Encapsula la validación y comportamiento del correo.
    """
    
    def __init__(self, direccion):
        """
        Constructor del objeto de valor correo
        
        Args:
            direccion (str): La dirección de correo a validar
            
        Raises:
            ValueError: Si la dirección de correo no es válida
        """
        if not self._es_valido(direccion):
            raise ValueError(f"Dirección de correo inválida: {direccion}")
        self._direccion = direccion.lower()
        
    def _es_valido(self, direccion):
        """
        Valida si la dirección de correo tiene un formato correcto
        
        Args:
            direccion (str): La dirección de correo a validar
            
        Returns:
            bool: True si la dirección es válida, False en caso contrario
        """
        if not direccion:
            return False
            
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, direccion) is not None
        
    @property
    def valor(self):
        """
        Retorna el valor de la dirección de correo
        
        Returns:
            str: La dirección de correo
        """
        return self._direccion
        
    def es_dominio(self, dominio):
        """
        Verifica si el correo pertenece a un dominio específico
        
        Args:
            dominio (str): Dominio a verificar (ej. "gmail.com")
            
        Returns:
            bool: True si el correo pertenece al dominio, False en caso contrario
        """
        return self._direccion.endswith('@' + dominio.lower())