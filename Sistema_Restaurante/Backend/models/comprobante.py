from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict

class Comprobante(Base):
    """
    Comprobantes fiscales emitidos (boleta, factura).
    """
    __tablename__ = 'comprobantes'
    
    # Tipos de comprobantes
    TIPOS = ['boleta', 'factura', 'nota_credito']
    
    id = Column(Integer, primary_key=True)
    transaccion_id = Column(Integer, ForeignKey('transacciones.id'), nullable=False, unique=True)
    tipo = Column(String(15), nullable=False, default='boleta')
    numero = Column(String(20), nullable=False, unique=True)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Integer, nullable=False)
    impuestos = Column(Integer, nullable=False)  # Monto de impuestos incluidos
    #datos_fiscales = Column(JSON, default=dict)  # Datos para factura (RUT, razón social, etc.)
    
    # Relaciones
    transaccion = relationship("Transaccion", back_populates="comprobante")
    
    def __init__(self, transaccion, tipo, numero, total, impuestos, datos_fiscales=None):
        self.transaccion = transaccion
        self.tipo = tipo
        self.numero = numero
        self.total = total
        self.impuestos = impuestos
        self.datos_fiscales = datos_fiscales or {}
    
    def get_neto(self):
        """Calcula el monto neto sin impuestos"""
        return self.total - self.impuestos
    
    def enviar_por_email(self, email):
        """Envía el comprobante por email (a implementar)"""
        # Implementación de envío por email
        pass
    
    def to_dict(self):
        """Convierte el comprobante a un diccionario"""
        result = to_dict(self)
        
        result['neto'] = self.get_neto()
        
        if self.transaccion:
            result['medio_pago'] = self.transaccion.medio_pago.nombre
            result['pedido_id'] = self.transaccion.pedido_id
            
        return result
    
    def __repr__(self):
        return f"<Comprobante {self.tipo} {self.numero} - ${self.total}>"
