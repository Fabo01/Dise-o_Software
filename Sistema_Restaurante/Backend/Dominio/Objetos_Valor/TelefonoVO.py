import re

class TelefonoVO:
    """
    Objeto de valor inmutable que representa un número de teléfono.
    Encapsula la validación y comportamiento del teléfono.
    """
    
    def __init__(self, telefono):
        """
        Constructor del objeto de valor teléfono
        
        Args:
            telefono (str): El número de teléfono a validar
            
        Raises:
            ValueError: Si el teléfono no es válido
        """
        # Si es vacío, lo permitimos (teléfono opcional)
        if not telefono:
            self._telefono = ""
            return
            
        if not self._es_valido(telefono):
            raise ValueError(f"Número de teléfono inválido: {telefono}")
            
        self._telefono = self._formatear(telefono)
        
    def _es_valido(self, telefono):
        """
        Valida si el número de teléfono tiene un formato correcto
        
        Args:
            telefono (str): El número a validar
            
        Returns:
            bool: True si el teléfono es válido, False en caso contrario
        """
        # Eliminar espacios, paréntesis, guiones y otros caracteres comunes
        telefono_limpio = re.sub(r'[\s\-\(\)\+]', '', telefono)
        
        # Verificar que solo contiene dígitos
        if not telefono_limpio.isdigit():
            return False
            
        # Verificar longitud adecuada (entre 8 y 15 dígitos)
        return 8 <= len(telefono_limpio) <= 15
    
    def _formatear(self, telefono):
        """
        Formatea el número de teléfono a un formato estándar
        
        Args:
            telefono (str): El teléfono a formatear
            
        Returns:
            str: El teléfono formateado
        """
        # Eliminar todos los caracteres no numéricos
        telefono_limpio = re.sub(r'[^\d]', '', telefono)
        
        # Si es un teléfono chileno (9 dígitos sin el código de país)
        if len(telefono_limpio) == 9:
            return f"+56 {telefono_limpio[:1]} {telefono_limpio[1:5]} {telefono_limpio[5:]}"
        
        # Otros formatos, devolver como está pero limpio
        return telefono_limpio
    
    @property
    def valor(self):
        """
        Retorna el valor del teléfono formateado
        
        Returns:
            str: El teléfono formateado
        """
        return self._telefono
