from sqlalchemy import Column, String, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from .base import Base, to_dict

class Cliente(Base):
    """
    Modelo para gestionar la información de los clientes del restaurante.
    """
    __tablename__ = 'clientes'
    
    # Estados disponibles para un cliente
    ESTADOS = ['activo', 'inactivo', 'bloqueado']
    
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=True)
    direccion = Column(Text, nullable=True)
    correo = Column(String(100), nullable=True)
    preferencias = Column(JSON, default=lambda: {})
    fecha_registro = Column(DateTime, default=datetime.now)
    ultima_visita = Column(DateTime, nullable=True)
    estado = Column(String(15), default='activo')
    
    # Relaciones
    pedidos = relationship("Pedido", back_populates="cliente")
    
    def __init__(self, rut, nombre, **kwargs):
        self.rut = rut
        self.nombre = nombre
        
        for key, value in kwargs.items():
            if key == 'preferencias' and isinstance(value, str):
                value = json.loads(value)
            setattr(self, key, value)
    
    def actualizar_visita(self):
        """Actualiza la fecha de última visita del cliente"""
        self.ultima_visita = datetime.now()
    
    def set_preferencia(self, key, value):
        """Establece una preferencia específica para el cliente"""
        preferencias = self.preferencias if self.preferencias else {}
        preferencias[key] = value
        self.preferencias = preferencias
    
    def get_preferencia(self, key, default=None):
        """Obtiene una preferencia específica del cliente"""
        if not self.preferencias:
            return default
        return self.preferencias.get(key, default)
    
    def add_direccion_alternativa(self, direccion, etiqueta="Alternativa"):
        """Agrega una dirección alternativa a las preferencias del cliente"""
        preferencias = self.preferencias if self.preferencias else {}
        
        if 'direcciones' not in preferencias:
            preferencias['direcciones'] = []
            
        preferencias['direcciones'].append({
            'direccion': direccion,
            'etiqueta': etiqueta
        })
        
        self.preferencias = preferencias
    
    def verificar_estado(self):
        """Verifica y actualiza el estado del cliente según reglas de negocio"""
        # Implementar reglas específicas según requisitos
        pass
    
    def get_historial_pedidos(self):
        """Retorna el historial completo de pedidos del cliente"""
        return sorted(self.pedidos, key=lambda p: p.fecha, reverse=True)
    
    def to_dict(self):
        """Convierte el cliente a un diccionario"""
        return to_dict(self)
    
    def __repr__(self):
        return f"<Cliente {self.nombre} ({self.rut})>"
