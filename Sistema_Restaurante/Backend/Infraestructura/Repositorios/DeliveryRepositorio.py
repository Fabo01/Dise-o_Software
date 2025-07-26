# Backend/Infraestructura/Repositorios/DeliveryRepositorio.py
from typing import List, Optional
from decimal import Decimal
from Backend.Dominio.Interfaces.IDeliveryRepositorio import IDeliveryRepositorio
from Backend.Dominio.Entidades.DeliveryPedido_Entidad import DeliveryPedidoEntidad
from Backend.Infraestructura.Modelos.DeliveryPedido_Modelo import DeliveryPedidoModelo
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo
from django.db import transaction

class DeliveryRepositorio(IDeliveryRepositorio):
    """
    Implementación concreta del repositorio de delivery.
    Maneja la persistencia de datos relacionados con delivery.
    """
    
    def crear_pedido_delivery(self, delivery_pedido: DeliveryPedidoEntidad) -> DeliveryPedidoEntidad:
        """Crea un nuevo pedido de delivery"""
        with transaction.atomic():
            modelo = DeliveryPedidoModelo(
                pedido_id=delivery_pedido.pedido_id,
                direccion_entrega=delivery_pedido.direccion_entrega,
                telefono_contacto=delivery_pedido.telefono_contacto,
                coordenadas_lat=delivery_pedido.coordenadas_lat,
                coordenadas_lng=delivery_pedido.coordenadas_lng,
                tiempo_estimado=delivery_pedido.tiempo_estimado,
                costo_delivery=delivery_pedido.costo_delivery,
                estado=delivery_pedido.estado,
                repartidor_id=delivery_pedido.repartidor_id,
                notas_especiales=delivery_pedido.notas_especiales
            )
            modelo.save()
            
            # Convertir de modelo a entidad
            return self._modelo_a_entidad(modelo)
    
    def obtener_por_id(self, delivery_id: int) -> Optional[DeliveryPedidoEntidad]:
        """Obtiene un pedido de delivery por ID"""
        try:
            modelo = DeliveryPedidoModelo.objects.get(id=delivery_id)
            return self._modelo_a_entidad(modelo)
        except DeliveryPedidoModelo.DoesNotExist:
            return None
    
    def listar_pedidos_activos(self) -> List[DeliveryPedidoEntidad]:
        """Lista todos los pedidos de delivery activos"""
        estados_activos = ['pendiente', 'en_preparacion', 'en_camino']
        modelos = DeliveryPedidoModelo.objects.filter(estado__in=estados_activos)
        return [self._modelo_a_entidad(modelo) for modelo in modelos]
    
    def asignar_repartidor(self, delivery_id: int, repartidor_id: int) -> bool:
        """Asigna un repartidor a un pedido de delivery"""
        try:
            with transaction.atomic():
                modelo = DeliveryPedidoModelo.objects.get(id=delivery_id)
                modelo.repartidor_id = repartidor_id
                modelo.estado = 'asignado'
                modelo.save()
                return True
        except DeliveryPedidoModelo.DoesNotExist:
            return False
    
    def actualizar_estado(self, delivery_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de un pedido de delivery"""
        try:
            with transaction.atomic():
                modelo = DeliveryPedidoModelo.objects.get(id=delivery_id)
                modelo.estado = nuevo_estado
                modelo.save()
                return True
        except DeliveryPedidoModelo.DoesNotExist:
            return False
    
    def obtener_repartidores_disponibles(self) -> List:
        """Obtiene lista de repartidores disponibles"""
        # Buscar usuarios con rol de repartidor que estén disponibles
        from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
        
        repartidores_ocupados = DeliveryPedidoModelo.objects.filter(
            estado__in=['asignado', 'en_camino']
        ).values_list('repartidor_id', flat=True)
        
        repartidores_disponibles = UsuarioModelo.objects.filter(
            rol='repartidor',
            activo=True
        ).exclude(id__in=repartidores_ocupados)
        
        return [
            {
                'id': repartidor.id,
                'nombre': f"{repartidor.first_name} {repartidor.last_name}",
                'email': repartidor.email,
                'telefono': getattr(repartidor, 'telefono', None)
            }
            for repartidor in repartidores_disponibles
        ]
    
    def actualizar_ubicacion_repartidor(self, delivery_id: int, latitud: Decimal, longitud: Decimal) -> bool:
        """Actualiza la ubicación actual del repartidor"""
        try:
            with transaction.atomic():
                modelo = DeliveryPedidoModelo.objects.get(id=delivery_id)
                modelo.ubicacion_actual_lat = latitud
                modelo.ubicacion_actual_lng = longitud
                modelo.save()
                return True
        except DeliveryPedidoModelo.DoesNotExist:
            return False
    
    def listar_por_estado(self, estado: str) -> List[DeliveryPedidoEntidad]:
        """Lista pedidos de delivery por estado específico"""
        modelos = DeliveryPedidoModelo.objects.filter(estado=estado)
        return [self._modelo_a_entidad(modelo) for modelo in modelos]
    
    def _modelo_a_entidad(self, modelo: DeliveryPedidoModelo) -> DeliveryPedidoEntidad:
        """Convierte un modelo de Django a entidad de dominio"""
        return DeliveryPedidoEntidad(
            id=modelo.id,
            pedido_id=modelo.pedido_id,
            direccion_entrega=modelo.direccion_entrega,
            telefono_contacto=modelo.telefono_contacto,
            coordenadas_lat=modelo.coordenadas_lat,
            coordenadas_lng=modelo.coordenadas_lng,
            tiempo_estimado=modelo.tiempo_estimado,
            costo_delivery=modelo.costo_delivery,
            estado=modelo.estado,
            repartidor_id=modelo.repartidor_id,
            ubicacion_actual_lat=getattr(modelo, 'ubicacion_actual_lat', None),
            ubicacion_actual_lng=getattr(modelo, 'ubicacion_actual_lng', None),
            fecha_creacion=modelo.fecha_creacion,
            fecha_entrega=getattr(modelo, 'fecha_entrega', None),
            notas_especiales=modelo.notas_especiales
        )
