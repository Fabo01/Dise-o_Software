from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict

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
