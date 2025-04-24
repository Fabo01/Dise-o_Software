import re

class RutVO:
    """
    Objeto de valor inmutable que representa un RUT chileno.
    Encapsula la validación y comportamiento del RUT.
    """
    
    def __init__(self, rut):
        """
        Constructor del objeto de valor RUT
        
        Args:
            rut (str): El RUT a validar
            
        Raises:
            ValueError: Si el RUT no es válido
        """
        if not self._es_valido(rut):
            raise ValueError(f"RUT inválido: {rut}")
        self._rut = self._formatear(rut)
        
    def _es_valido(self, rut):
        """
        Valida si el RUT tiene un formato correcto y dígito verificador válido
        
        Args:
            rut (str): El RUT a validar
            
        Returns:
            bool: True si el RUT es válido, False en caso contrario
        """
        if not rut:
            return False
            
        # Eliminar puntos y guiones para normalizar
        rut = rut.replace(".", "").replace("-", "")
        
        # Verificar formato básico
        patron = r'^[0-9]{7,8}[0-9Kk]$'
        if not re.match(patron, rut):
            return False
            
        # Validar dígito verificador
        try:
            cuerpo = rut[:-1]
            dv = rut[-1].upper()
            
            # Calcular dígito verificador
            suma = 0
            multiplicador = 2
            
            for c in reversed(cuerpo):
                suma += int(c) * multiplicador
                multiplicador += 1
                if multiplicador > 7:
                    multiplicador = 2
                    
            resto = suma % 11
            dv_calculado = 11 - resto if resto != 0 else 0
            
            if dv_calculado == 10:
                dv_calculado = 'K'
            else:
                dv_calculado = str(dv_calculado)
                
            return dv == dv_calculado
        except:
            return False
    
    def _formatear(self, rut):
        """
        Formatea el RUT a un formato estándar (XX.XXX.XXX-Y)
        
        Args:
            rut (str): El RUT a formatear
            
        Returns:
            str: El RUT formateado
        """
        rut = rut.replace(".", "").replace("-", "")
        cuerpo = rut[:-1]
        dv = rut[-1]
        
        # Formatear con puntos y guión
        formato = ""
        for i, c in enumerate(reversed(cuerpo)):
            if i > 0 and i % 3 == 0:
                formato = "." + formato
            formato = c + formato
            
        return formato + "-" + dv.upper()
    
    @property
    def valor(self):
        """
        Retorna el valor del RUT formateado
        
        Returns:
            str: El RUT formateado
        """
        return self._rut
    
    @property
    def numero(self):
        """
        Retorna solo el número del RUT sin dígito verificador
        
        Returns:
            str: El número del RUT
        """
        return self._rut.split('-')[0]
    
    @property
    def digito_verificador(self):
        """
        Retorna solo el dígito verificador del RUT
        
        Returns:
            str: El dígito verificador
        """
        return self._rut.split('-')[1]
        
    def __str__(self):
        return self._rut
        
    def __eq__(self, other):
        if not isinstance(other, RutVO):
            return False
        return self._rut == other._rut
