from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, to_dict

class DeliveryPedido(Base):
    """
    Extensión del pedido para delivery con información específica.
    """
    __tablename__ = 'delivery_pedidos'
    
    # Estados específicos de delivery
    ESTADOS_DELIVERY = ['asignado', 'en_camino', 'entregado', 'cancelado']
    
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), primary_key=True)
    direccion_entrega = Column(Text, nullable=False)
    tiempo_estimado = Column(Integer, nullable=True)  # Tiempo en minutos
    repartidor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    estado_delivery = Column(String(15), default='asignado')
    app_id = Column(Integer, ForeignKey('delivery_apps.id'), nullable=True)
    codigo_externo = Column(String(50), nullable=True)
    costo_envio = Column(Float, default=0)
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="delivery")
    repartidor = relationship("Usuario", foreign_keys=[repartidor_id], back_populates="pedidos_entrega")
    app = relationship("DeliveryApp", back_populates="pedidos")
    
    def __init__(self, pedido, direccion_entrega, **kwargs):
        self.pedido = pedido
        self.direccion_entrega = direccion_entrega
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def asignar_repartidor(self, repartidor):
        """Asigna un repartidor al pedido delivery"""
        self.repartidor = repartidor
        self.estado_delivery = 'asignado'
        return True
    
    def marcar_en_camino(self):
        """Marca el pedido como en camino"""
        if self.estado_delivery == 'asignado' and self.repartidor:
            self.estado_delivery = 'en_camino'
            return True
        return False
    
    def marcar_entregado(self):
        """Marca el pedido como entregado"""
        if self.estado_delivery == 'en_camino':
            self.estado_delivery = 'entregado'
            # También actualizar el estado del pedido principal
            self.pedido.cambiar_estado('entregado')
            return True
        return False
    
    def calcular_tiempo_total(self):
        """Calcula el tiempo total estimado incluyendo preparación y entrega"""
        tiempo_preparacion = self.pedido.get_tiempo_estimado()
        return tiempo_preparacion + (self.tiempo_estimado or 30)  # 30 min por defecto
    
    def to_dict(self):
        """Convierte el pedido delivery a un diccionario"""
        result = to_dict(self)
        
        if self.repartidor:
            result['repartidor_nombre'] = self.repartidor.nombre
            
        if self.app:
            result['app_nombre'] = self.app.nombre
            
        return result
    
    def __repr__(self):
        return f"<DeliveryPedido #{self.pedido_id} - {self.estado_delivery}>"
