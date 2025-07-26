from decimal import Decimal, ROUND_HALF_UP
from ..Excepciones.DominioExcepcion import ValidacionExcepcion

class PrecioVO:
    """
    Objeto de valor que representa un precio monetario.
    Garantiza que el precio sea válido y esté correctamente formateado.
    """
    
    def __init__(self, valor):
        """
        Constructor del objeto de valor Precio.
        
        Args:
            valor: El valor del precio (puede ser str, int, float, o Decimal)
            
        Raises:
            ValidacionExcepcion: Si el precio no es válido
        """
        self._valor = self._validar_y_convertir(valor)
    
    def _validar_y_convertir(self, valor) -> Decimal:
        """
        Valida y convierte el valor a Decimal con 2 decimales.
        
        Args:
            valor: El valor a validar y convertir
            
        Returns:
            Decimal: El valor convertido a Decimal
            
        Raises:
            ValidacionExcepcion: Si el valor no es válido
        """
        try:
            # Convertir a Decimal
            if isinstance(valor, str):
                valor = valor.replace(",", ".")  # Permitir comas como separador decimal
            
            decimal_valor = Decimal(str(valor))
            
            # Validar que sea positivo
            if decimal_valor < 0:
                raise ValidacionExcepcion("El precio no puede ser negativo")
            
            # Validar que no sea excesivamente grande
            if decimal_valor > Decimal('999999.99'):
                raise ValidacionExcepcion("El precio excede el límite máximo permitido")
            
            # Redondear a 2 decimales
            return decimal_valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        except (ValueError, TypeError, ArithmeticError) as e:
            raise ValidacionExcepcion(f"Formato de precio inválido: {str(e)}")
    
    @property
    def valor(self) -> Decimal:
        """Retorna el valor del precio como Decimal."""
        return self._valor
    
    def formato_moneda(self, simbolo_moneda: str = "$") -> str:
        """
        Retorna el precio formateado como moneda.
        
        Args:
            simbolo_moneda (str): Símbolo de la moneda (por defecto "$")
            
        Returns:
            str: Precio formateado como moneda
        """
        return f"{simbolo_moneda}{self._valor:,.2f}"
    
    def es_gratis(self) -> bool:
        """
        Verifica si el precio es gratuito (0).
        
        Returns:
            bool: True si el precio es 0, False en caso contrario
        """
        return self._valor == Decimal('0.00')
    
    def aplicar_descuento(self, porcentaje: Decimal) -> 'PrecioVO':
        """
        Aplica un descuento al precio y retorna un nuevo objeto PrecioVO.
        
        Args:
            porcentaje (Decimal): Porcentaje de descuento (0-100)
            
        Returns:
            PrecioVO: Nuevo objeto con el precio con descuento aplicado
            
        Raises:
            ValidacionExcepcion: Si el porcentaje no es válido
        """
        if porcentaje < 0 or porcentaje > 100:
            raise ValidacionExcepcion("El porcentaje de descuento debe estar entre 0 y 100")
        
        descuento = self._valor * (porcentaje / Decimal('100'))
        nuevo_precio = self._valor - descuento
        
        return PrecioVO(nuevo_precio)
    
    def aplicar_incremento(self, porcentaje: Decimal) -> 'PrecioVO':
        """
        Aplica un incremento al precio y retorna un nuevo objeto PrecioVO.
        
        Args:
            porcentaje (Decimal): Porcentaje de incremento
            
        Returns:
            PrecioVO: Nuevo objeto con el precio incrementado
            
        Raises:
            ValidacionExcepcion: Si el porcentaje no es válido
        """
        if porcentaje < 0:
            raise ValidacionExcepcion("El porcentaje de incremento no puede ser negativo")
        
        incremento = self._valor * (porcentaje / Decimal('100'))
        nuevo_precio = self._valor + incremento
        
        return PrecioVO(nuevo_precio)
    
    def __str__(self) -> str:
        return self.formato_moneda()
    
    def __repr__(self) -> str:
        return f"PrecioVO({self._valor})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, PrecioVO):
            return False
        return self._valor == other._valor
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, PrecioVO):
            return NotImplemented
        return self._valor < other._valor
    
    def __le__(self, other) -> bool:
        if not isinstance(other, PrecioVO):
            return NotImplemented
        return self._valor <= other._valor
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, PrecioVO):
            return NotImplemented
        return self._valor > other._valor
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, PrecioVO):
            return NotImplemented
        return self._valor >= other._valor
    
    def __hash__(self) -> int:
        return hash(self._valor)
    
    def __add__(self, other) -> 'PrecioVO':
        if isinstance(other, PrecioVO):
            return PrecioVO(self._valor + other._valor)
        elif isinstance(other, (int, float, Decimal)):
            return PrecioVO(self._valor + Decimal(str(other)))
        return NotImplemented
    
    def __sub__(self, other) -> 'PrecioVO':
        if isinstance(other, PrecioVO):
            return PrecioVO(self._valor - other._valor)
        elif isinstance(other, (int, float, Decimal)):
            return PrecioVO(self._valor - Decimal(str(other)))
        return NotImplemented
    
    def __mul__(self, other) -> 'PrecioVO':
        if isinstance(other, (int, float, Decimal)):
            return PrecioVO(self._valor * Decimal(str(other)))
        return NotImplemented
    
    def __truediv__(self, other) -> 'PrecioVO':
        if isinstance(other, (int, float, Decimal)):
            if Decimal(str(other)) == 0:
                raise ValidacionExcepcion("No se puede dividir por cero")
            return PrecioVO(self._valor / Decimal(str(other)))
        return NotImplemented
