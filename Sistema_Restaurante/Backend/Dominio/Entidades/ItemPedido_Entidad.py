from decimal import Decimal
from typing import Optional, Dict, Any
from .EntidadBase import EntidadBase
from ..Excepciones.DominioExcepcion import ValidacionExcepcion

class ItemPedido(EntidadBase):
    """
    Entidad que representa un ítem específico dentro de un pedido.
    """
    
    def __init__(self, menu_id: int, cantidad: int, precio_unitario: Decimal, 
                 notas: str = "", personalizaciones: Optional[Dict[str, Any]] = None):
        """
        Constructor de la entidad ItemPedido.
        
        Args:
            menu_id (int): ID del menú solicitado
            cantidad (int): Cantidad solicitada
            precio_unitario (Decimal): Precio unitario en el momento del pedido
            notas (str, opcional): Notas especiales para la preparación
            personalizaciones (dict, opcional): Personalizaciones específicas del ítem
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        super().__init__()
        
        if cantidad <= 0:
            raise ValidacionExcepcion("La cantidad debe ser mayor que cero")
        if precio_unitario <= Decimal('0'):
            raise ValidacionExcepcion("El precio unitario debe ser mayor que cero")
        
        self._menu_id = menu_id
        self._cantidad = cantidad
        self._precio_unitario = precio_unitario
        self._notas = notas
        self._personalizaciones = personalizaciones or {}
        self._subtotal = precio_unitario * Decimal(cantidad)
        self._descuento = Decimal('0')
    
    # Getters
    @property
    def menu_id(self) -> int:
        return self._menu_id
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @property
    def precio_unitario(self) -> Decimal:
        return self._precio_unitario
    
    @property
    def notas(self) -> str:
        return self._notas
    
    @property
    def personalizaciones(self) -> Dict[str, Any]:
        return self._personalizaciones.copy()
    
    @property
    def subtotal(self) -> Decimal:
        return self._subtotal
    
    @property
    def descuento(self) -> Decimal:
        return self._descuento
    
    @property
    def total(self) -> Decimal:
        """
        Calcula el total de este ítem (subtotal - descuento).
        
        Returns:
            Decimal: Importe total de este ítem
        """
        return self._subtotal - self._descuento
    
    # Métodos de negocio
    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        """
        Actualiza la cantidad del ítem y recalcula el subtotal.
        
        Args:
            nueva_cantidad (int): Nueva cantidad
            
        Raises:
            ValidacionExcepcion: Si la cantidad es inválida
        """
        if nueva_cantidad <= 0:
            raise ValidacionExcepcion("La cantidad debe ser mayor que cero")
        
        self._cantidad = nueva_cantidad
        self._recalcular_subtotal()
        self.actualizar_fecha()
    
    def aplicar_descuento(self, monto_descuento: Decimal) -> None:
        """
        Aplica un descuento al ítem.
        
        Args:
            monto_descuento (Decimal): Monto a descontar
            
        Raises:
            ValidacionExcepcion: Si el descuento es inválido
        """
        if monto_descuento < Decimal('0'):
            raise ValidacionExcepcion("El descuento no puede ser negativo")
        if monto_descuento > self._subtotal:
            raise ValidacionExcepcion("El descuento no puede ser mayor que el subtotal")
        
        self._descuento = monto_descuento
        self.actualizar_fecha()
    
    def agregar_nota(self, nota: str) -> None:
        """
        Agrega una nota al ítem.
        
        Args:
            nota (str): Nota a agregar
        """
        if not nota:
            return
            
        if self._notas:
            self._notas += f"; {nota}"
        else:
            self._notas = nota
            
        self.actualizar_fecha()
    
    def agregar_personalizacion(self, clave: str, valor: Any) -> None:
        """
        Agrega una personalización al ítem.
        
        Args:
            clave (str): Nombre de la personalización
            valor: Valor de la personalización
        """
        self._personalizaciones[clave] = valor
        self.actualizar_fecha()
    
    def _recalcular_subtotal(self) -> None:
        """
        Recalcula el subtotal basado en la cantidad y precio unitario.
        """
        self._subtotal = self._precio_unitario * Decimal(self._cantidad)
    
    def __str__(self) -> str:
        return f"{self._cantidad} x Menú #{self._menu_id} - {self._subtotal}"
