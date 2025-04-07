from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, to_dict

class MenuIngrediente(Base):
    """
    Relación entre Menú e Ingrediente, con la cantidad necesaria.
    """
    __tablename__ = 'menu_ingredientes'
    
    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id'), primary_key=True)
    cantidad = Column(Float, nullable=False)  # Cantidad necesaria por porción
    
    # Relaciones
    menu = relationship("Menu", back_populates="menu_ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="menu_ingredientes")
    
    def __init__(self, menu, ingrediente, cantidad):
        self.menu = menu
        self.ingrediente = ingrediente
        self.cantidad = cantidad
    
    def hay_suficiente(self):
        """Verifica si hay suficiente cantidad del ingrediente"""
        return self.ingrediente.cantidad >= self.cantidad
    
    def calcular_costo(self):
        """Calcula el costo de este ingrediente para el menú"""
        if hasattr(self.ingrediente, 'costo_unitario') and self.ingrediente.costo_unitario:
            return self.cantidad * self.ingrediente.costo_unitario
        return None
    
    def to_dict(self):
        """Convierte la relación a un diccionario"""
        return {
            "menu_id": self.menu_id,
            "ingrediente_id": self.ingrediente_id,
            "ingrediente_nombre": self.ingrediente.nombre,
            "cantidad": self.cantidad,
            "unidad": self.ingrediente.unidad,
            "hay_suficiente": self.hay_suficiente()
        }
    
    def __repr__(self):
        return f"<MenuIngrediente {self.menu.nombre} - {self.ingrediente.nombre} ({self.cantidad} {self.ingrediente.unidad})>"
