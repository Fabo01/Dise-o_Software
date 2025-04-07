from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, to_dict, db_session

class Pedido(Base):
    """
    Modelo para los pedidos realizados por los clientes.
    """
    __tablename__ = 'pedidos'
    
    # Estados disponibles para un pedido
    ESTADOS = ['recibido', 'en_preparacion', 'listo', 'entregado', 'pagado', 'cancelado']
    
    # Tipos de pedido
    TIPOS = ['local', 'delivery', 'para_llevar']
    
    id = Column(Integer, primary_key=True)
    cliente_rut = Column(String(12), ForeignKey('clientes.rut'), nullable=False)
    mesa_id = Column(Integer, ForeignKey('mesas.id'), nullable=True)
    fecha = Column(DateTime, default=datetime.now)
    estado = Column(String(15), default='recibido')
    total = Column(Integer, default=0)
    notas = Column(Text, nullable=True)
    creado_por_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    tipo = Column(String(15), default='local')
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="pedidos")
    mesa = relationship("Mesa", back_populates="pedidos")
    creado_por = relationship("Usuario", foreign_keys=[creado_por_id], back_populates="pedidos_creados")
    items = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    transacciones = relationship("Transaccion", back_populates="pedido")
    historial_estados = relationship("HistorialEstadoPedido", back_populates="pedido", order_by="HistorialEstadoPedido.fecha")
    delivery = relationship("DeliveryPedido", back_populates="pedido", uselist=False, cascade="all, delete-orphan")
    
    def __init__(self, cliente, **kwargs):
        self.cliente = cliente
        self.cliente_rut = cliente.rut
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calcular_total(self):
        """Calcula el total del pedido basado en los ítems"""
        total = sum(item.subtotal for item in self.items)
        self.total = total
        return total
    
    def agregar_item(self, menu, cantidad, notas=None):
        """Agrega un ítem al pedido o actualiza su cantidad si ya existe"""
        from .item_pedido import ItemPedido
        
        # Buscar si ya existe el ítem
        for item in self.items:
            if item.menu_id == menu.id:
                item.cantidad += cantidad
                item.subtotal = item.precio_unitario * item.cantidad
                if notas:
                    item.notas = notas
                    
                # Actualizar el total del pedido
                self.calcular_total()
                return item
        
        # Crear nuevo ítem
        item = ItemPedido(
            pedido=self,
            menu=menu,
            cantidad=cantidad,
            precio_unitario=menu.precio,
            subtotal=menu.precio * cantidad,
            notas=notas
        )
        self.items.append(item)
        
        # Actualizar el total del pedido
        self.calcular_total()
        return item
    
    def eliminar_item(self, item_id):
        """Elimina un ítem del pedido"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                # Actualizar el total del pedido
                self.calcular_total()
                return True
        return False
    
    def cambiar_estado(self, nuevo_estado, usuario=None, comentario=None):
        """Cambia el estado del pedido y registra en historial"""
        from .historial_estado_pedido import HistorialEstadoPedido
        
        if nuevo_estado not in self.ESTADOS:
            return False
            
        estado_anterior = self.estado
        self.estado = nuevo_estado
        
        # Registrar en historial
        historial = HistorialEstadoPedido(
            pedido=self,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=usuario,
            comentario=comentario
        )
        db_session.add(historial)
        
        # Acciones adicionales según el nuevo estado
        if nuevo_estado == 'en_preparacion' and estado_anterior == 'recibido':
            self.reservar_ingredientes()
            
        return True
    
    def reservar_ingredientes(self):
        """Reserva los ingredientes necesarios para este pedido"""
        if self.estado != 'recibido':
            return False
        
        # Verificar disponibilidad primero
        for item in self.items:
            for rel in item.menu.menu_ingredientes:
                cantidad_necesaria = rel.cantidad * item.cantidad
                if rel.ingrediente.cantidad < cantidad_necesaria:
                    return False
        
        # Si hay suficientes ingredientes, descontarlos
        for item in self.items:
            for rel in item.menu.menu_ingredientes:
                cantidad_necesaria = rel.cantidad * item.cantidad
                motivo = f"Pedido #{self.id} - {item.menu.nombre} x{item.cantidad}"
                rel.ingrediente.actualizar_stock(
                    -cantidad_necesaria, 
                    motivo,
                    self.creado_por
                )
        
        return True
    
    def get_tiempo_estimado(self):
        """Calcula el tiempo estimado total para el pedido en minutos"""
        if not self.items:
            return 0
            
        # Encontrar el ítem con mayor tiempo de preparación
        max_tiempo = max(item.menu.tiempo_preparacion for item in self.items)
        
        # Considerar la cantidad de ítems para el tiempo total
        factor_cantidad = sum(item.cantidad for item in self.items) * 0.5
        
        return max_tiempo + factor_cantidad
    
    def puede_editarse(self):
        """Determina si el pedido aún puede ser editado"""
        return self.estado in ['recibido']
    
    def puede_cancelarse(self):
        """Determina si el pedido aún puede ser cancelado"""
        return self.estado in ['recibido', 'en_preparacion']
    
    def to_dict(self, incluir_items=False):
        """Convierte el pedido a un diccionario"""
        result = to_dict(self)
        
        # Agregar información adicional
        result['cliente_nombre'] = self.cliente.nombre if self.cliente else None
        
        if self.mesa:
            result['mesa_numero'] = self.mesa.numero
            
        if self.creado_por:
            result['creado_por_nombre'] = self.creado_por.nombre
            
        if incluir_items:
            result['items'] = [item.to_dict() for item in self.items]
            
        return result
    
    def __repr__(self):
        return f"<Pedido #{self.id} - {self.cliente.nombre if self.cliente else 'Sin cliente'} ({self.estado})>"


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


class DeliveryApp(Base):
    """
    Configuración de las aplicaciones de delivery externas.
    """
    __tablename__ = 'delivery_apps'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    comision = Column(Float, default=0)  # Porcentaje de comisión (0.1 = 10%)
    activa = Column(Boolean, default=True)
    api_key = Column(String(255), nullable=True)
    api_secret = Column(String(255), nullable=True)
    
    # Relaciones
    pedidos = relationship("DeliveryPedido", back_populates="app")
    
    def __init__(self, nombre, **kwargs):
        self.nombre = nombre
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def calcular_comision(self, monto):
        """Calcula la comisión para un monto específico"""
        return round(monto * self.comision)
    
    def to_dict(self):
        """Convierte la app a un diccionario"""
        # Excluir datos sensibles
        return to_dict(self, exclude=['api_key', 'api_secret'])
    
    def __repr__(self):
        return f"<DeliveryApp {self.nombre} ({self.comision*100}%)>"
