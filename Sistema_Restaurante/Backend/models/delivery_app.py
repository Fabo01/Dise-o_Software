from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from .base import Base, to_dict

class DeliveryApp(Base):
    """
    Configuración de las aplicaciones de delivery externas.
    """
    __tablename__ = 'delivery_apps'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    comision = Column(Float, default=0)  # Porcentaje de comisión (0.1 = 10%)
    activa = Column(Boolean, default=True)
    api_key = Column(String(255), nullable=True)
    api_secret = Column(String(255), nullable=True)
    
    # Relaciones
    pedidos = relationship("DeliveryPedido", back_populates="app")
    
    def __init__(self, nombre, **kwargs):
        self.nombre = nombre
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calcular_comision(self, monto):
        """Calcula la comisión para un monto específico"""
        return round(monto * self.comision)
    
    def to_dict(self):
        """Convierte la app a un diccionario"""
        # Excluir datos sensibles
        return to_dict(self, exclude=['api_key', 'api_secret'])
    
    def __repr__(self):
        return f"<DeliveryApp {self.nombre} ({self.comision*100}%)>"
