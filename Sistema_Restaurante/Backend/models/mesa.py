from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict

class Mesa(Base):
    """
    Modelo para gestionar las mesas del restaurante.
    """
    __tablename__ = 'mesas'
    
    # Estados disponibles para una mesa
    ESTADOS = ['libre', 'ocupada', 'reservada', 'limpieza']
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidad = Column(Integer, default=4)
    estado = Column(String(15), default='libre')
    ubicacion = Column(String(50), nullable=True)  # ej: terraza, interior
    caracteristicas = Column(String(255), nullable=True)  # ej: vista, privada
    hora_inicio = Column(DateTime, nullable=True)  # Para tracking de tiempo de ocupación
    mesero_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    posicion_x = Column(Integer, nullable=True)  # Posición en el mapa del restaurante
    posicion_y = Column(Integer, nullable=True)  # Posición en el mapa del restaurante
    
    # Relaciones
    mesero_asignado = relationship("Usuario", back_populates="mesas_asignadas")
    pedidos = relationship("Pedido", back_populates="mesa")
    
    def __init__(self, numero, capacidad=4, **kwargs):
        self.numero = numero
        self.capacidad = capacidad
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def ocupar(self, mesero=None):
        """Cambia el estado de la mesa a ocupada y registra la hora"""
        if self.estado != 'ocupada':
            self.estado = 'ocupada'
            self.hora_inicio = datetime.now()
            self.mesero_asignado = mesero
            return True
        return False
    
    def liberar(self):
        """Cambia el estado de la mesa a libre y calcula tiempo de ocupación"""
        if self.estado == 'ocupada' and self.hora_inicio:
            tiempo_ocupacion = datetime.now() - self.hora_inicio
            self.estado = 'limpieza'
            self.hora_inicio = None
            self.mesero_asignado = None
            return tiempo_ocupacion.total_seconds() / 60  # Retorna minutos de ocupación
        return 0
    
    def marcar_limpia(self):
        """Cambia el estado de la mesa de limpieza a libre"""
        if self.estado == 'limpieza':
            self.estado = 'libre'
            return True
        return False
    
    def reservar(self, hora=None):
        """Reserva la mesa para una hora específica"""
        if self.estado == 'libre':
            self.estado = 'reservada'
            if hora:
                # Aquí se podría guardar la hora de reserva en otra tabla o campo
                pass
            return True
        return False
    
    def calcular_tiempo_ocupacion(self):
        """Calcula el tiempo que lleva ocupada la mesa en minutos"""
        if self.estado == 'ocupada' and self.hora_inicio:
            return (datetime.now() - self.hora_inicio).total_seconds() / 60
        return 0
    
    def get_pedido_actual(self):
        """Obtiene el pedido actual de la mesa si existe"""
        pedidos_activos = [p for p in self.pedidos 
                          if p.estado in ['recibido', 'en_preparacion', 'listo', 'entregado']]
        
        if pedidos_activos:
            return pedidos_activos[0]
        return None
    
    def to_dict(self, incluir_tiempo=True):
        """Convierte la mesa a un diccionario"""
        result = to_dict(self)
        
        if incluir_tiempo and self.estado == 'ocupada':
            result['tiempo_ocupacion'] = self.calcular_tiempo_ocupacion()
            
        if self.mesero_asignado:
            result['mesero_nombre'] = self.mesero_asignado.nombre
            
        return result
    
    def __repr__(self):
        return f"<Mesa {self.numero} ({self.capacidad} personas) - {self.estado}>"
