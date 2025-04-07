from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, to_dict

class ItemPedido(Base):
    """
    Detalle de un ítem incluido en un pedido.
    """
    __tablename__ = 'items_pedido'
    
    # Estados disponibles para un ítem
    ESTADOS = ['pendiente', 'en_preparacion', 'listo', 'entregado', 'cancelado']
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    menu_id = Column(Integer, ForeignKey('menus.id'), nullable=False)
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Integer, nullable=False)  # Precio al momento de compra
    subtotal = Column(Integer, nullable=False)  # precio_unitario * cantidad
    notas = Column(String(255), nullable=True)  # Personalizaciones del cliente
    estado = Column(String(15), default='pendiente')
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="items")
    menu = relationship("Menu", back_populates="items_pedido")
    
    def __init__(self, pedido, menu, cantidad, precio_unitario, subtotal=None, notas=None):
        self.pedido = pedido
        self.menu = menu
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal if subtotal is not None else precio_unitario * cantidad
        self.notas = notas
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del ítem"""
        if nuevo_estado in self.ESTADOS:
            self.estado = nuevo_estado
            return True
        return False
    
    def calcular_subtotal(self):
        """Recalcula el subtotal basado en precio y cantidad"""
        self.subtotal = self.precio_unitario * self.cantidad
        return self.subtotal
    
    def to_dict(self):
        """Convierte el ítem a un diccionario"""
        result = to_dict(self)
        result['menu_nombre'] = self.menu.nombre if self.menu else "Desconocido"
        return result
    
    def __repr__(self):
        return f"<ItemPedido {self.cantidad} x {self.menu.nombre if self.menu else 'Desconocido'} - ${self.subtotal}>"
