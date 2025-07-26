# Backend/Aplicacion/Servicios/DeliveryServicio.py
from typing import List, Optional
from decimal import Decimal
from Backend.Dominio.Interfaces.IDeliveryRepositorio import IDeliveryRepositorio
from Backend.Dominio.Entidades.DeliveryPedido_Entidad import DeliveryPedidoEntidad
from Backend.Aplicacion.DTOs.DeliveryDTO import DeliveryPedidoDTO, CrearDeliveryDTO
from Backend.Aplicacion.Excepciones.DeliveryExcepciones import (
    DeliveryNoEncontradoError,
    RepartidorNoDisponibleError,
    EstadoInvalidoError
)

class DeliveryServicio:
    """
    Servicio de aplicación para la gestión de delivery.
    Implementa los casos de uso relacionados con delivery.
    """
    
    def __init__(self, delivery_repositorio: IDeliveryRepositorio):
        self._delivery_repositorio = delivery_repositorio
    
    def crear_pedido_delivery(self, datos: CrearDeliveryDTO) -> DeliveryPedidoDTO:
        """
        Caso de uso: Crear nuevo pedido de delivery
        """
        # Validar datos de entrada
        self._validar_datos_delivery(datos)
        
        # Crear entidad de dominio
        delivery_entidad = DeliveryPedidoEntidad(
            pedido_id=datos.pedido_id,
            direccion_entrega=datos.direccion_entrega,
            telefono_contacto=datos.telefono_contacto,
            coordenadas_lat=datos.coordenadas_lat,
            coordenadas_lng=datos.coordenadas_lng,
            tiempo_estimado=datos.tiempo_estimado,
            costo_delivery=datos.costo_delivery,
            estado='pendiente',
            notas_especiales=datos.notas_especiales
        )
        
        # Guardar en repositorio
        delivery_creado = self._delivery_repositorio.crear_pedido_delivery(delivery_entidad)
        
        # Convertir a DTO de respuesta
        return self._entidad_a_dto(delivery_creado)
    
    def obtener_delivery_por_id(self, delivery_id: int) -> DeliveryPedidoDTO:
        """
        Caso de uso: Obtener información de un delivery por ID
        """
        delivery = self._delivery_repositorio.obtener_por_id(delivery_id)
        
        if not delivery:
            raise DeliveryNoEncontradoError(f"Delivery con ID {delivery_id} no encontrado")
        
        return self._entidad_a_dto(delivery)
    
    def listar_deliveries_activos(self) -> List[DeliveryPedidoDTO]:
        """
        Caso de uso: Listar todos los deliveries activos
        """
        deliveries = self._delivery_repositorio.listar_pedidos_activos()
        return [self._entidad_a_dto(delivery) for delivery in deliveries]
    
    def asignar_repartidor(self, delivery_id: int, repartidor_id: int) -> bool:
        """
        Caso de uso: Asignar repartidor a un delivery
        """
        # Verificar que el delivery existe
        delivery = self._delivery_repositorio.obtener_por_id(delivery_id)
        if not delivery:
            raise DeliveryNoEncontradoError(f"Delivery con ID {delivery_id} no encontrado")
        
        # Verificar que el repartidor está disponible
        repartidores_disponibles = self._delivery_repositorio.obtener_repartidores_disponibles()
        repartidor_disponible = any(
            rep['id'] == repartidor_id for rep in repartidores_disponibles
        )
        
        if not repartidor_disponible:
            raise RepartidorNoDisponibleError(f"Repartidor con ID {repartidor_id} no está disponible")
        
        # Asignar repartidor
        resultado = self._delivery_repositorio.asignar_repartidor(delivery_id, repartidor_id)
        
        if not resultado:
            raise DeliveryNoEncontradoError("No se pudo asignar el repartidor")
        
        return resultado
    
    def actualizar_estado_delivery(self, delivery_id: int, nuevo_estado: str) -> bool:
        """
        Caso de uso: Actualizar estado de un delivery
        """
        # Validar estado
        estados_validos = ['pendiente', 'asignado', 'en_preparacion', 'en_camino', 'entregado', 'cancelado']
        if nuevo_estado not in estados_validos:
            raise EstadoInvalidoError(f"Estado '{nuevo_estado}' no es válido")
        
        # Verificar que el delivery existe
        delivery = self._delivery_repositorio.obtener_por_id(delivery_id)
        if not delivery:
            raise DeliveryNoEncontradoError(f"Delivery con ID {delivery_id} no encontrado")
        
        # Actualizar estado
        resultado = self._delivery_repositorio.actualizar_estado(delivery_id, nuevo_estado)
        
        if not resultado:
            raise DeliveryNoEncontradoError("No se pudo actualizar el estado del delivery")
        
        return resultado
    
    def obtener_repartidores_disponibles(self) -> List[dict]:
        """
        Caso de uso: Obtener lista de repartidores disponibles
        """
        return self._delivery_repositorio.obtener_repartidores_disponibles()
    
    def actualizar_ubicacion_repartidor(self, delivery_id: int, latitud: Decimal, longitud: Decimal) -> bool:
        """
        Caso de uso: Actualizar ubicación del repartidor
        """
        # Verificar que el delivery existe y está en curso
        delivery = self._delivery_repositorio.obtener_por_id(delivery_id)
        if not delivery:
            raise DeliveryNoEncontradoError(f"Delivery con ID {delivery_id} no encontrado")
        
        if delivery.estado not in ['en_camino', 'asignado']:
            raise EstadoInvalidoError("Solo se puede actualizar ubicación para deliveries en camino o asignados")
        
        # Actualizar ubicación
        resultado = self._delivery_repositorio.actualizar_ubicacion_repartidor(delivery_id, latitud, longitud)
        
        if not resultado:
            raise DeliveryNoEncontradoError("No se pudo actualizar la ubicación del repartidor")
        
        return resultado
    
    def listar_deliveries_por_estado(self, estado: str) -> List[DeliveryPedidoDTO]:
        """
        Caso de uso: Listar deliveries por estado específico
        """
        deliveries = self._delivery_repositorio.listar_por_estado(estado)
        return [self._entidad_a_dto(delivery) for delivery in deliveries]
    
    def _validar_datos_delivery(self, datos: CrearDeliveryDTO):
        """Valida los datos de entrada para crear un delivery"""
        if not datos.direccion_entrega or len(datos.direccion_entrega.strip()) < 10:
            raise ValueError("La dirección de entrega debe tener al menos 10 caracteres")
        
        if not datos.telefono_contacto or len(datos.telefono_contacto) < 8:
            raise ValueError("El teléfono de contacto debe tener al menos 8 dígitos")
        
        if datos.coordenadas_lat is None or datos.coordenadas_lng is None:
            raise ValueError("Las coordenadas de latitud y longitud son obligatorias")
        
        if datos.costo_delivery < 0:
            raise ValueError("El costo de delivery no puede ser negativo")
    
    def _entidad_a_dto(self, entidad: DeliveryPedidoEntidad) -> DeliveryPedidoDTO:
        """Convierte una entidad de dominio a DTO"""
        return DeliveryPedidoDTO(
            id=entidad.id,
            pedido_id=entidad.pedido_id,
            direccion_entrega=entidad.direccion_entrega,
            telefono_contacto=entidad.telefono_contacto,
            coordenadas_lat=entidad.coordenadas_lat,
            coordenadas_lng=entidad.coordenadas_lng,
            tiempo_estimado=entidad.tiempo_estimado,
            costo_delivery=entidad.costo_delivery,
            estado=entidad.estado,
            repartidor_id=entidad.repartidor_id,
            ubicacion_actual_lat=entidad.ubicacion_actual_lat,
            ubicacion_actual_lng=entidad.ubicacion_actual_lng,
            fecha_creacion=entidad.fecha_creacion,
            fecha_entrega=entidad.fecha_entrega,
            notas_especiales=entidad.notas_especiales
        )
