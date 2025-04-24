from datetime import datetime, timedelta
from .EntidadBase import EntidadBase
from ..Excepciones.DominioExcepcion import ValidacionExcepcion

class Ingrediente(EntidadBase):
    """
    Clase que representa un ingrediente en el sistema de restaurante.
    
    Atributos:
        nombre (str): Nombre del ingrediente.
        cantidad (float): Cantidad disponible del ingrediente.
        unidad_medida (str): Unidad de medida del ingrediente (ej. kg, g, l).
        fecha_vencimiento (datetime): Fecha de vencimiento del ingrediente.
        estado (str): Estado del ingrediente (ej. activo, inactivo).
        nivel_critico (float): Nivel mínimo de stock antes de generar alertas.
        tipo (str): Categoría del ingrediente (ej. proteína, vegetal, lácteo).
    """
    
    def __init__(self, nombre, cantidad, unidad_medida, fecha_vencimiento, nivel_critico=None, tipo=None):
        super().__init__()
        
        if not nombre:
            raise ValidacionExcepcion("El nombre del ingrediente es obligatorio")
        if cantidad < 0:
            raise ValidacionExcepcion("La cantidad no puede ser negativa")
        if fecha_vencimiento and fecha_vencimiento < datetime.now():
            raise ValidacionExcepcion("La fecha de vencimiento no puede ser en el pasado")
        
        self._nombre = nombre
        self._cantidad = cantidad
        self._unidad_medida = unidad_medida
        self._fecha_vencimiento = fecha_vencimiento
        self._estado = "activo"
        self._fecha_registro = datetime.now()
        self._nivel_critico = nivel_critico
        self._tipo = tipo
    
    # Propiedades (getters)
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def cantidad(self):
        return self._cantidad
    
    @property
    def unidad_medida(self):
        return self._unidad_medida
    
    @property
    def fecha_vencimiento(self):
        return self._fecha_vencimiento
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def fecha_registro(self):
        return self._fecha_registro
    
    @property
    def nivel_critico(self):
        return self._nivel_critico
    
    @property
    def tipo(self):
        return self._tipo
    
    # Métodos de negocio
    def verificar_disponibilidad(self, cantidad_requerida):
        """
        Verifica si hay suficiente stock del ingrediente.
        
        Args:
            cantidad_requerida (float): Cantidad necesaria del ingrediente.
            
        Returns:
            bool: True si hay suficiente stock, False en caso contrario.
        """
        return self._cantidad >= cantidad_requerida
    
    def actualizar_stock(self, cantidad_delta):
        """
        Actualiza el stock del ingrediente sumando o restando una cantidad.
        
        Args:
            cantidad_delta (float): Cantidad a sumar (positiva) o restar (negativa).
            
        Returns:
            float: Nueva cantidad después de la actualización.
            
        Raises:
            ValidacionExcepcion: Si la cantidad resultante sería negativa.
        """
        nueva_cantidad = self._cantidad + cantidad_delta
        if nueva_cantidad < 0:
            raise ValidacionExcepcion("No hay suficiente stock para realizar esta operación")
        
        self._cantidad = nueva_cantidad
        self._actualizar_estado_por_cantidad()
        self.actualizar_fecha()
        return self._cantidad
    
    def _actualizar_estado_por_cantidad(self):
        """
        Actualiza el estado del ingrediente según su disponibilidad.
        """
        if self._cantidad == 0:
            self._estado = "agotado"
        elif self._nivel_critico and self._cantidad <= self._nivel_critico:
            self._estado = "stock_critico"
        else:
            if self._estado in ["agotado", "stock_critico"]:
                self._estado = "activo"
                
    def esta_por_vencer(self, dias_limite=7):
        """
        Verifica si el ingrediente está próximo a vencer.
        
        Args:
            dias_limite (int): Días límite para considerar un ingrediente próximo a vencer.
            
        Returns:
            bool: True si está por vencer, False en caso contrario.
        """
        if not self._fecha_vencimiento:
            return False
            
        dias_para_vencer = self.dias_para_vencer()
        return 0 < dias_para_vencer <= dias_limite
    
    def dias_para_vencer(self):
        """
        Calcula cuántos días faltan para que el ingrediente se venza.
        
        Returns:
            int: Número de días hasta la fecha de vencimiento. 
                 Negativo si ya está vencido, None si no tiene fecha de vencimiento.
        """
        if not self._fecha_vencimiento:
            return None
            
        delta = self._fecha_vencimiento - datetime.now()
        return delta.days
    
    def actualizar_estado_por_vencimiento(self):
        """
        Actualiza el estado basado en la fecha de vencimiento.
        
        Returns:
            bool: True si el estado cambió, False en caso contrario.
        """
        if not self._fecha_vencimiento:
            return False
            
        if datetime.now() > self._fecha_vencimiento:
            if self._estado != "vencido":
                self._estado = "vencido"
                self.actualizar_fecha()
                return True
        return False
    
    def esta_bajo_nivel_critico(self):
        """
        Verifica si el ingrediente está por debajo del nivel crítico de stock.
        
        Returns:
            bool: True si está bajo el nivel crítico, False en caso contrario.
        """
        if self._nivel_critico is None:
            return False
        return self._cantidad <= self._nivel_critico
        
    def __str__(self):
        return f"{self._nombre} ({self._cantidad} {self._unidad_medida})"
