from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict

class Transaccion(Base):
    """
    Registro de transacciones de pago.
    """
    __tablename__ = 'transacciones'
    
    # Estados de transacción
    ESTADOS = ['pendiente', 'procesando', 'completada', 'rechazada', 'cancelada', 'reembolsada']
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    medio_pago_id = Column(Integer, ForeignKey('medios_pago.id'), nullable=False)
    monto = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    estado = Column(String(15), default='pendiente')
    referencia_externa = Column(String(100), nullable=True)  # Referencia externa de la pasarela de pago
    datos_adicionales = Column(JSON, default=dict)  # Datos adicionales como voucher, autorización, etc.
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="transacciones")
    medio_pago = relationship("MedioPago", back_populates="transacciones")
    comprobante = relationship("Comprobante", back_populates="transaccion", uselist=False, cascade="all, delete-orphan")
    
    def __init__(self, pedido, medio_pago, monto, **kwargs):
        self.pedido = pedido
        self.medio_pago = medio_pago
        self.monto = monto
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calcular_comision(self):
        """Calcula el monto de comisión según el medio de pago"""
        return self.medio_pago.calcular_comision(self.monto)
    
    def marcar_completada(self, referencia=None):
        """Marca la transacción como completada y actualiza el estado del pedido"""
        self.estado = 'completada'
        if referencia:
            self.referencia_externa = referencia
            
        # Actualizar el estado del pedido
        self.pedido.cambiar_estado('pagado')
        
        return True
    
    def marcar_rechazada(self, motivo=None):
        """Marca la transacción como rechazada"""
        self.estado = 'rechazada'
        if motivo:
            datos = self.datos_adicionales or {}
            datos['motivo_rechazo'] = motivo
            self.datos_adicionales = datos
            
        return True
    
    def generar_comprobante(self, tipo='boleta', datos_fiscales=None):
        """Genera un comprobante para la transacción"""
        from .comprobante import Comprobante
        
        if self.estado != 'completada':
            return None
            
        # Calcular impuestos (ejemplo: 19% IVA)
        impuestos = round(self.monto * 0.19)
        
        # Generar número de comprobante
        numero = f"{tipo[0].upper()}-{datetime.now().strftime('%Y%m%d')}-{self.id}"
        
        comprobante = Comprobante(
            transaccion=self,
            tipo=tipo,
            numero=numero,
            total=self.monto,
            impuestos=impuestos,
            datos_fiscales=datos_fiscales or {}
        )
        
        return comprobante
    
    def to_dict(self):
        """Convierte la transacción a un diccionario"""
        result = to_dict(self)
        
        result['medio_pago_nombre'] = self.medio_pago.nombre if self.medio_pago else None
        result['comision'] = self.calcular_comision()
        
        return result
    
    def __repr__(self):
        return f"<Transaccion #{self.id} - Pedido #{self.pedido_id} - ${self.monto} ({self.estado})>"
