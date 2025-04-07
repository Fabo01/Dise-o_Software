from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict, db_session

class Ingrediente(Base):
    """
    Modelo para gestionar los ingredientes del inventario.
    """
    __tablename__ = 'ingredientes'
    
    # Estados disponibles para un ingrediente
    ESTADOS = ['disponible', 'bajo', 'critico', 'agotado', 'descontinuado']
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=True)
    cantidad = Column(Float, default=0)
    unidad = Column(String(20), nullable=False)  # kg, l, unidad, etc.
    nivel_critico = Column(Float, default=0)
    codigo_barras = Column(String(30), nullable=True)
    imagen = Column(String(255), nullable=True)  # URL o path a imagen
    proveedor = Column(String(100), nullable=True)
    estado = Column(String(15), default='disponible')
    costo_unitario = Column(Float, nullable=True)  # Costo por unidad
    notas = Column(Text, nullable=True)
    
    # Relaciones
    menu_ingredientes = relationship("MenuIngrediente", back_populates="ingrediente")
    movimientos = relationship("MovimientoInventario", back_populates="ingrediente")
    
    def __init__(self, nombre, unidad, **kwargs):
        self.nombre = nombre
        self.unidad = unidad
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        # Actualizar estado según nivel de stock
        self._actualizar_estado()
    
    def _actualizar_estado(self):
        """Actualiza el estado del ingrediente según su nivel de stock"""
        if self.cantidad <= 0:
            self.estado = 'agotado'
        elif self.cantidad <= self.nivel_critico:
            self.estado = 'critico'
        elif self.cantidad <= self.nivel_critico * 1.5:
            self.estado = 'bajo'
        else:
            self.estado = 'disponible'
    
    def actualizar_stock(self, cantidad, motivo=None, usuario=None):
        """
        Actualiza el stock del ingrediente registrando el movimiento
        
        Args:
            cantidad: Cantidad a añadir (positivo) o restar (negativo)
            motivo: Razón del cambio de stock
            usuario: Usuario que realiza el cambio
            
        Returns:
            Nueva cantidad del ingrediente
        """
        from .movimiento_inventario import MovimientoInventario
        
        self.cantidad += cantidad
        self._actualizar_estado()
        
        # Registrar movimiento en historial
        movimiento = MovimientoInventario(
            ingrediente=self,
            cantidad=cantidad,
            motivo=motivo or ('Entrada' if cantidad > 0 else 'Salida'),
            usuario=usuario
        )
        db_session.add(movimiento)
        
        return self.cantidad
    
    def calcular_valor_inventario(self):
        """Calcula el valor total del inventario de este ingrediente"""
        if self.costo_unitario is not None:
            return self.cantidad * self.costo_unitario
        return None
    
    def get_menus_relacionados(self):
        """Obtiene los menús que utilizan este ingrediente"""
        return [rel.menu for rel in self.menu_ingredientes]
    
    def to_dict(self):
        """Convierte el ingrediente a un diccionario"""
        return to_dict(self)
    
    def __repr__(self):
        return f"<Ingrediente {self.nombre} ({self.cantidad} {self.unidad})>"


class MovimientoInventario(Base):
    """
    Registra los movimientos de entrada y salida de ingredientes.
    """
    __tablename__ = 'movimientos_inventario'
    
    id = Column(Integer, primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id'), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    cantidad = Column(Float, nullable=False)  # Positivo para entrada, negativo para salida
    motivo = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    
    # Relaciones
    ingrediente = relationship("Ingrediente", back_populates="movimientos")
    usuario = relationship("Usuario", back_populates="movimientos_inventario")
    
    def __init__(self, ingrediente, cantidad, motivo, usuario=None):
        self.ingrediente = ingrediente
        self.cantidad = cantidad
        self.motivo = motivo
        self.usuario = usuario
    
    def es_entrada(self):
        """Determina si el movimiento es una entrada al inventario"""
        return self.cantidad > 0
    
    def to_dict(self):
        """Convierte el movimiento a un diccionario"""
        return to_dict(self)
    
    def __repr__(self):
        tipo = "Entrada" if self.cantidad > 0 else "Salida"
        return f"<{tipo} de {abs(self.cantidad)} {self.ingrediente.unidad} de {self.ingrediente.nombre}>"
