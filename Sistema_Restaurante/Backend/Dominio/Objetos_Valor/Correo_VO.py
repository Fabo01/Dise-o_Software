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
        
    def __str__(self):
        return self._direccion
        
    def __eq__(self, other):
        """
        Compara si dos correos son iguales basándose en su dirección
        
        Args:
            other (CorreoVO): El otro objeto de valor correo a comparar
            
        Returns:
            bool: True si son iguales, False en caso contrario
        """
        if not isinstance(other, CorreoVO):
            return False
        return self._direccion == other._direccion