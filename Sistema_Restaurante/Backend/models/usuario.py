from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .base import Base, to_dict

class Usuario(Base):
    """
    Modelo para los usuarios del sistema con manejo de roles y permisos.
    """
    __tablename__ = 'usuarios'
    
    # Roles disponibles en el sistema
    ROLES = {
        'admin': 'Administrador',
        'jefe_local': 'Jefe de Local',
        'jefe_turno': 'Jefe de Turno',
        'mesero': 'Mesero',
        'cocina': 'Cocina',
    }
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    rol = Column(String(20), default='mesero')
    telefono = Column(String(15), nullable=True)
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    pedidos_creados = relationship("Pedido", back_populates="creado_por", foreign_keys="Pedido.creado_por_id")
    pedidos_entrega = relationship("DeliveryPedido", back_populates="repartidor", foreign_keys="DeliveryPedido.repartidor_id")
    mesas_asignadas = relationship("Mesa", back_populates="mesero_asignado")
    cambios_estado = relationship("HistorialEstadoPedido", back_populates="usuario")
    movimientos_inventario = relationship("MovimientoInventario", back_populates="usuario")
    
    def __init__(self, username, password, nombre, rol='mesero', **kwargs):
        self.username = username
        self.set_password(password)
        self.nombre = nombre
        self.rol = rol
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        """Establece una contraseña encriptada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password_hash, password)
    
    def get_rol_display(self):
        """Retorna el nombre legible del rol"""
        return self.ROLES.get(self.rol, self.rol)
    
    def actualizar_ultimo_acceso(self):
        """Actualiza la fecha de último acceso al sistema"""
        self.ultimo_acceso = datetime.now()
    
    def has_permission(self, permission):
        """
        Verifica si el usuario tiene un permiso específico según su rol
        
        Implementar lógica específica según los requerimientos
        """
        # Ejemplo básico de permisos por rol
        permission_map = {
            'admin': ['all'],
            'jefe_local': ['all'],
            'jefe_turno': ['view_reports', 'manage_orders', 'manage_tables', 'manage_staff'],
            'mesero': ['create_order', 'manage_tables', 'manage_clients'],
            'cocina': ['view_orders', 'update_inventory'],
        }
        
        # El admin y jefe local tienen todos los permisos
        if 'all' in permission_map.get(self.rol, []):
            return True
            
        # Verificar permiso específico
        return permission in permission_map.get(self.rol, [])
    
    def to_dict(self, exclude_password=True):
        """Convierte el usuario a un diccionario, excluyendo la contraseña por defecto"""
        exclude = ['password_hash'] if exclude_password else []
        return to_dict(self, exclude)
    
    def __repr__(self):
        return f"<Usuario {self.username} ({self.get_rol_display()})>"
