from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict

class HistorialEstadoPedido(Base):
    """
    Registro de cambios de estado de los pedidos.
    """
    __tablename__ = 'historial_estado_pedido'
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    estado_anterior = Column(String(15), nullable=False)
    estado_nuevo = Column(String(15), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    comentario = Column(String(255), nullable=True)
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="historial_estados")
    usuario = relationship("Usuario", back_populates="cambios_estado")
    
    def __init__(self, pedido, estado_anterior, estado_nuevo, usuario=None, comentario=None):
        self.pedido = pedido
        self.estado_anterior = estado_anterior
        self.estado_nuevo = estado_nuevo
        self.usuario = usuario
        self.comentario = comentario
    
    def to_dict(self):
        """Convierte el registro a un diccionario"""
        result = to_dict(self)
        
        if self.usuario:
            result['usuario_nombre'] = self.usuario.nombre
            
        return result
    
    def __repr__(self):
        return f"<HistorialEstado Pedido #{self.pedido_id}: {self.estado_anterior} -> {self.estado_nuevo}>"
