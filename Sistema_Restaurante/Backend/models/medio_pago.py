from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base, to_dict

class MedioPago(Base):
    """
    Configuración de los medios de pago aceptados.
    """
    __tablename__ = 'medios_pago'
    
    # Tipos de medios de pago
    TIPOS = ['efectivo', 'tarjeta', 'transferencia', 'app', 'otro']
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(15), nullable=False)
    comision = Column(Float, default=0)  # Porcentaje de comisión (0.03 = 3%)
    activo = Column(Boolean, default=True)
    configuracion = Column(JSON, default=dict)  # Configuración adicional específica
    
    # Relaciones
    transacciones = relationship("Transaccion", back_populates="medio_pago")
    
    def __init__(self, nombre, tipo, **kwargs):
        self.nombre = nombre
        self.tipo = tipo
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calcular_comision(self, monto):
        """Calcula la comisión para un monto específico"""
        return round(monto * self.comision)
    
    def to_dict(self):
        """Convierte el medio de pago a un diccionario"""
        return to_dict(self)
    
    def __repr__(self):
        return f"<MedioPago {self.nombre} ({self.tipo})>"
