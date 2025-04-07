from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, to_dict, db_session

class Menu(Base):
    """
    Modelo para los platos y productos que ofrece el restaurante.
    """
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Integer, nullable=False)  # Precio en la moneda local (ej. CLP)
    costo = Column(Integer, default=0)  # Costo estimado basado en ingredientes
    tiempo_preparacion = Column(Integer, default=15)  # Tiempo en minutos
    categoria = Column(String(50), nullable=False)
    imagen = Column(String(255), nullable=True)  # URL o path a imagen
    disponible = Column(Boolean, default=True)
    disponible_delivery = Column(Boolean, default=True)
    
    # Relaciones
    menu_ingredientes = relationship("MenuIngrediente", back_populates="menu", cascade="all, delete-orphan")
    items_pedido = relationship("ItemPedido", back_populates="menu")
    
    def __init__(self, nombre, precio, categoria, **kwargs):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calcular_costo(self):
        """Calcula el costo total basado en los ingredientes y sus cantidades"""
        total = 0
        for rel in self.menu_ingredientes:
            ingrediente_costo = rel.calcular_costo()
            if ingrediente_costo is not None:
                total += ingrediente_costo
        
        # Actualizar el costo almacenado
        self.costo = total
        return total
    
    def calcular_margen(self):
        """Calcula el margen de beneficio en porcentaje"""
        if self.costo == 0:
            return None
        return ((self.precio - self.costo) / self.precio) * 100
    
    def verificar_disponibilidad(self):
        """Verifica si hay suficientes ingredientes para preparar este menú"""
        for rel in self.menu_ingredientes:
            if not rel.hay_suficiente():
                return False
        return True
    
    def calcular_disponibles(self):
        """Calcula cuántas porciones se pueden preparar con el stock actual"""
        if not self.menu_ingredientes:
            return 0
            
        porciones = float('inf')
        for rel in self.menu_ingredientes:
            if rel.ingrediente.cantidad <= 0:
                return 0
            posibles = rel.ingrediente.cantidad / rel.cantidad
            porciones = min(porciones, posibles)
        return int(porciones)
    
    def agregar_ingrediente(self, ingrediente, cantidad):
        """Agrega un ingrediente al menú o actualiza su cantidad si ya existe"""
        from .menu_ingrediente import MenuIngrediente
        
        # Buscar si ya existe la relación
        for rel in self.menu_ingredientes:
            if rel.ingrediente_id == ingrediente.id:
                rel.cantidad = cantidad
                return rel
        
        # Crear nueva relación
        rel = MenuIngrediente(
            menu=self,
            ingrediente=ingrediente,
            cantidad=cantidad
        )
        self.menu_ingredientes.append(rel)
        return rel
    
    def eliminar_ingrediente(self, ingrediente_id):
        """Elimina un ingrediente del menú"""
        for i, rel in enumerate(self.menu_ingredientes):
            if rel.ingrediente_id == ingrediente_id:
                del self.menu_ingredientes[i]
                return True
        return False
    
    def actualizar_disponibilidad(self):
        """Actualiza el estado de disponibilidad según los ingredientes"""
        self.disponible = self.verificar_disponibilidad()
        return self.disponible
    
    def get_ingredientes(self):
        """Retorna la lista de ingredientes con sus cantidades"""
        return [
            {
                "ingrediente": rel.ingrediente,
                "cantidad": rel.cantidad,
                "unidad": rel.ingrediente.unidad
            } 
            for rel in self.menu_ingredientes
        ]
    
    def to_dict(self, incluir_ingredientes=False):
        """Convierte el menú a un diccionario"""
        result = to_dict(self)
        
        if incluir_ingredientes:
            result['ingredientes'] = [rel.to_dict() for rel in self.menu_ingredientes]
            result['disponibles'] = self.calcular_disponibles()
            
        return result
    
    def __repr__(self):
        return f"<Menu {self.nombre} (${self.precio})>"


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
