from datetime import datetime, timedelta

class IngredienteEntidad:
    """
    Clase que representa un ingrediente en el sistema de restaurante.
    
    Atributos:
        id (int): Identificador único del ingrediente.
        nombre (str): Nombre del ingrediente.
        cantidad (float): Cantidad disponible del ingrediente.
        unidad_medida (str): Unidad de medida del ingrediente (ej. kg, g, l).
        fecha_vencimiento (datetime): Fecha de vencimiento del ingrediente.
        estado (str): Estado del ingrediente (ej. activo, inactivo).
        nivel_critico (float): Nivel mínimo de stock antes de generar alertas.
        tipo (str): Categoría del ingrediente (ej. proteína, vegetal, lácteo).
    """
    
    def __init__(self, nombre, cantidad, unidad_medida, fecha_vencimiento, nivel_critico=None, tipo=None):
        if not nombre:
            raise ValueError("El nombre del ingrediente es obligatorio")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if fecha_vencimiento and fecha_vencimiento < datetime.now():
            raise ValueError("La fecha de vencimiento no puede ser en el pasado")
        
        self.id = None
        self.nombre = nombre
        self.cantidad = cantidad
        self.unidad_medida = unidad_medida
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = "activo"
        self.fecha_registro = datetime.now()
        self.nivel_critico = nivel_critico
        self.tipo = tipo
    
    def verificar_disponibilidad(self, cantidad_requerida):
        """
        Verifica si hay suficiente stock del ingrediente.
        
        Args:
            cantidad_requerida (float): Cantidad necesaria del ingrediente.
            
        Returns:
            bool: True si hay suficiente stock, False en caso contrario.
        """
        return self.cantidad >= cantidad_requerida
    
    def actualizar_stock(self, cantidad_delta):
        """
        Actualiza el stock del ingrediente sumando o restando una cantidad.
        
        Args:
            cantidad_delta (float): Cantidad a sumar (positiva) o restar (negativa).
            
        Returns:
            float: Nueva cantidad después de la actualización.
            
        Raises:
            ValueError: Si la cantidad resultante sería negativa.
        """
        nueva_cantidad = self.cantidad + cantidad_delta
        if nueva_cantidad < 0:
            raise ValueError("No hay suficiente stock para realizar esta operación")
        
        self.cantidad = nueva_cantidad
        self._actualizar_estado_por_cantidad()
        return self.cantidad
    
    def _actualizar_estado_por_cantidad(self):
        """
        Actualiza el estado del ingrediente según su disponibilidad.
        """
        if self.cantidad == 0:
            self.estado = "agotado"
        elif self.nivel_critico and self.cantidad <= self.nivel_critico:
            self.estado = "stock_critico"
        else:
            if self.estado in ["agotado", "stock_critico"]:
                self.estado = "activo"
                
    def esta_por_vencer(self, dias_limite=7):
        """
        Verifica si el ingrediente está próximo a vencer.
        
        Args:
            dias_limite (int): Días límite para considerar un ingrediente próximo a vencer.
            
        Returns:
            bool: True si está por vencer, False en caso contrario.
        """
        if not self.fecha_vencimiento:
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
        if not self.fecha_vencimiento:
            return None
            
        delta = self.fecha_vencimiento - datetime.now()
        return delta.days
    
    def actualizar_estado_por_vencimiento(self):
        """
        Actualiza el estado basado en la fecha de vencimiento.
        
        Returns:
            bool: True si el estado cambió, False en caso contrario.
        """
        if not self.fecha_vencimiento:
            return False
            
        if datetime.now() > self.fecha_vencimiento:
            if self.estado != "vencido":
                self.estado = "vencido"
                return True
        return False
    
    def esta_bajo_nivel_critico(self):
        """
        Verifica si el ingrediente está por debajo del nivel crítico de stock.
        
        Returns:
            bool: True si está bajo el nivel crítico, False en caso contrario.
        """
        if self.nivel_critico is None:
            return False
        return self.cantidad <= self.nivel_critico
