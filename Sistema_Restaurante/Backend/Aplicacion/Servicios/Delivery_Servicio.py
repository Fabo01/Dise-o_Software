# Backend/Aplicacion/Servicios/Delivery_Servicio.py
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from django.db import transaction
from django.utils import timezone

from Backend.Infraestructura.Modelos.DeliveryPedido_Modelo import DeliveryPedidoModelo
from Backend.Infraestructura.Modelos.DeliveryApp_Modelo import DeliveryAppModelo
from Backend.Infraestructura.Modelos.DeliveryRepartidor_Modelo import DeliveryRepartidorModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

class DeliveryServicio:
    """
    Servicio para gestionar pedidos de delivery y repartidores
    """
    
    def crear_pedido_delivery_directo(self, datos_pedido: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un pedido delivery directo (no desde app externa)
        """
        try:
            with transaction.atomic():
                # Validar cliente
                cliente = ClienteModelo.objects.get(rut=datos_pedido['cliente_rut'])
                
                # Crear pedido base
                pedido_data = {
                    'cliente': cliente,
                    'estado': 'pendiente',
                    'tipo': 'delivery',
                    'observaciones': datos_pedido.get('observaciones', ''),
                    'total': datos_pedido.get('total', 0)
                }
                pedido = PedidoModelo.objects.create(**pedido_data)
                
                # Crear información específica de delivery
                delivery_data = {
                    'pedido': pedido,
                    'direccion_entrega': datos_pedido['direccion_entrega'],
                    'telefono_contacto': datos_pedido.get('telefono_contacto', ''),
                    'tiempo_estimado_minutos': self._calcular_tiempo_estimado(datos_pedido['direccion_entrega']),
                    'costo_envio': self._calcular_costo_envio(datos_pedido['direccion_entrega']),
                    'es_delivery_externo': False,
                    'estado_delivery': 'pendiente'
                }
                delivery_pedido = DeliveryPedidoModelo.objects.create(**delivery_data)
                
                return {
                    'id': pedido.id,
                    'delivery_id': delivery_pedido.pedido_id,
                    'estado': pedido.estado,
                    'tiempo_estimado': delivery_data['tiempo_estimado_minutos'],
                    'costo_envio': delivery_data['costo_envio'],
                    'direccion': delivery_data['direccion_entrega']
                }
                
        except ClienteModelo.DoesNotExist:
            raise ValueError(f"Cliente con RUT {datos_pedido['cliente_rut']} no encontrado")
        except Exception as e:
            raise Exception(f"Error al crear pedido delivery: {str(e)}")
    
    def crear_pedido_desde_app_externa(self, datos_pedido: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registra un pedido recibido desde una app externa (Rappi, Uber Eats, etc.)
        """
        try:
            with transaction.atomic():
                # Validar app de delivery
                app_delivery = DeliveryAppModelo.objects.get(
                    nombre=datos_pedido['app_nombre'],
                    activa=True
                )
                
                # Crear o buscar cliente
                cliente_data = datos_pedido.get('cliente', {})
                cliente, created = ClienteModelo.objects.get_or_create(
                    rut=cliente_data.get('rut', f"EXT-{datos_pedido['codigo_externo']}"),
                    defaults={
                        'nombre': cliente_data.get('nombre', 'Cliente Externo'),
                        'correo': cliente_data.get('correo', ''),
                        'telefono': cliente_data.get('telefono', '')
                    }
                )
                
                # Crear pedido base
                total_bruto = datos_pedido['total']
                comision = app_delivery.calcular_comision(total_bruto)
                
                pedido_data = {
                    'cliente': cliente,
                    'estado': 'pendiente',
                    'tipo': 'delivery',
                    'total': total_bruto,
                    'observaciones': f"Pedido desde {app_delivery.nombre} - Código: {datos_pedido['codigo_externo']}"
                }
                pedido = PedidoModelo.objects.create(**pedido_data)
                
                # Crear información específica de delivery
                delivery_data = {
                    'pedido': pedido,
                    'direccion_entrega': datos_pedido['direccion_entrega'],
                    'telefono_contacto': cliente_data.get('telefono', ''),
                    'delivery_app': app_delivery,
                    'codigo_externo': datos_pedido['codigo_externo'],
                    'tiempo_estimado_minutos': datos_pedido.get('tiempo_estimado', 45),
                    'costo_envio': datos_pedido.get('costo_envio', 0),
                    'comision_app': comision,
                    'es_delivery_externo': True,
                    'estado_delivery': 'pendiente'
                }
                delivery_pedido = DeliveryPedidoModelo.objects.create(**delivery_data)
                
                return {
                    'id': pedido.id,
                    'delivery_id': delivery_pedido.pedido_id,
                    'app': app_delivery.nombre,
                    'codigo_externo': datos_pedido['codigo_externo'],
                    'comision': comision,
                    'total_neto': total_bruto - comision,
                    'estado': pedido.estado
                }
                
        except DeliveryAppModelo.DoesNotExist:
            raise ValueError(f"App de delivery '{datos_pedido['app_nombre']}' no encontrada o inactiva")
        except Exception as e:
            raise Exception(f"Error al crear pedido desde app externa: {str(e)}")
    
    def asignar_repartidor(self, pedido_id: int, repartidor_id: int) -> Dict[str, Any]:
        """
        Asigna un repartidor a un pedido delivery
        """
        try:
            with transaction.atomic():
                # Validar pedido delivery
                delivery_pedido = DeliveryPedidoModelo.objects.select_related('pedido').get(
                    pedido_id=pedido_id,
                    estado_delivery__in=['pendiente', 'listo']
                )
                
                # Validar repartidor
                repartidor = DeliveryRepartidorModelo.objects.get(
                    id=repartidor_id,
                    activo=True
                )
                
                if not repartidor.esta_disponible():
                    raise ValueError(f"Repartidor {repartidor.nombre} no está disponible")
                
                # Asignar repartidor
                delivery_pedido.repartidor = repartidor
                delivery_pedido.estado_delivery = 'asignado'
                delivery_pedido.hora_asignacion = timezone.now()
                delivery_pedido.save()
                
                # Actualizar estado del repartidor
                repartidor.estado = 'en_ruta'
                repartidor.pedido_actual = delivery_pedido
                repartidor.save()
                
                # Actualizar pedido base
                delivery_pedido.pedido.estado = 'en_ruta'
                delivery_pedido.pedido.save()
                
                return {
                    'pedido_id': pedido_id,
                    'repartidor': {
                        'id': repartidor.id,
                        'nombre': repartidor.nombre,
                        'telefono': repartidor.telefono,
                        'vehiculo': repartidor.vehiculo
                    },
                    'estado': delivery_pedido.estado_delivery,
                    'hora_asignacion': delivery_pedido.hora_asignacion.isoformat()
                }
                
        except DeliveryPedidoModelo.DoesNotExist:
            raise ValueError(f"Pedido delivery {pedido_id} no encontrado o no disponible para asignación")
        except DeliveryRepartidorModelo.DoesNotExist:
            raise ValueError(f"Repartidor {repartidor_id} no encontrado")
        except Exception as e:
            raise Exception(f"Error al asignar repartidor: {str(e)}")
    
    def obtener_repartidores_disponibles(self) -> List[Dict[str, Any]]:
        """
        Obtiene lista de repartidores disponibles para asignación
        """
        try:
            repartidores = DeliveryRepartidorModelo.objects.filter(
                estado='disponible',
                activo=True
            ).order_by('nombre')
            
            return [
                {
                    'id': r.id,
                    'nombre': r.nombre,
                    'telefono': r.telefono,
                    'vehiculo': r.vehiculo,
                    'ubicacion': {
                        'lat': float(r.ubicacion_lat) if r.ubicacion_lat else None,
                        'lng': float(r.ubicacion_lng) if r.ubicacion_lng else None
                    } if r.ubicacion_lat and r.ubicacion_lng else None
                }
                for r in repartidores
            ]
            
        except Exception as e:
            raise Exception(f"Error al obtener repartidores disponibles: {str(e)}")
    
    def obtener_pedidos_pendientes_asignacion(self) -> List[Dict[str, Any]]:
        """
        Obtiene pedidos delivery listos para asignar repartidor
        """
        try:
            pedidos = DeliveryPedidoModelo.objects.select_related('pedido', 'delivery_app').filter(
                estado_delivery__in=['pendiente', 'listo'],
                repartidor__isnull=True
            ).order_by('pedido__fecha_creacion')
            
            return [
                {
                    'id': p.pedido.id,
                    'cliente': p.pedido.cliente.nombre,
                    'direccion': p.direccion_entrega,
                    'total': float(p.pedido.total),
                    'tiempo_estimado': p.tiempo_estimado_minutos,
                    'app_externa': p.delivery_app.nombre if p.es_delivery_externo else None,
                    'hora_creacion': p.pedido.fecha_creacion.isoformat(),
                    'prioridad': self._calcular_prioridad_entrega(p)
                }
                for p in pedidos
            ]
            
        except Exception as e:
            raise Exception(f"Error al obtener pedidos pendientes: {str(e)}")
    
    def seguir_estado_entrega(self, pedido_id: int) -> Dict[str, Any]:
        """
        Obtiene el estado actual de una entrega
        """
        try:
            delivery_pedido = DeliveryPedidoModelo.objects.select_related(
                'pedido', 'repartidor', 'delivery_app'
            ).get(pedido_id=pedido_id)
            
            resultado = {
                'pedido_id': pedido_id,
                'estado': delivery_pedido.estado_delivery,
                'direccion': delivery_pedido.direccion_entrega,
                'tiempo_estimado': delivery_pedido.tiempo_estimado_minutos,
                'costo_envio': float(delivery_pedido.costo_envio),
                'hora_creacion': delivery_pedido.pedido.fecha_creacion.isoformat()
            }
            
            # Información del repartidor si está asignado
            if delivery_pedido.repartidor:
                resultado['repartidor'] = {
                    'nombre': delivery_pedido.repartidor.nombre,
                    'telefono': delivery_pedido.repartidor.telefono,
                    'vehiculo': delivery_pedido.repartidor.vehiculo,
                    'ubicacion': {
                        'lat': float(delivery_pedido.repartidor.ubicacion_lat) if delivery_pedido.repartidor.ubicacion_lat else None,
                        'lng': float(delivery_pedido.repartidor.ubicacion_lng) if delivery_pedido.repartidor.ubicacion_lng else None
                    } if delivery_pedido.repartidor.ubicacion_lat else None
                }
                resultado['hora_asignacion'] = delivery_pedido.hora_asignacion.isoformat() if delivery_pedido.hora_asignacion else None
            
            # Información de app externa si aplica
            if delivery_pedido.es_delivery_externo and delivery_pedido.delivery_app:
                resultado['app_externa'] = {
                    'nombre': delivery_pedido.delivery_app.nombre,
                    'codigo_externo': delivery_pedido.codigo_externo,
                    'comision': float(delivery_pedido.comision_app)
                }
            
            # Calcular tiempo transcurrido y tiempo restante estimado
            tiempo_transcurrido = (timezone.now() - delivery_pedido.pedido.fecha_creacion).total_seconds() / 60
            tiempo_restante = max(0, delivery_pedido.tiempo_estimado_minutos - tiempo_transcurrido)
            
            resultado['tiempo_transcurrido_minutos'] = int(tiempo_transcurrido)
            resultado['tiempo_restante_estimado'] = int(tiempo_restante)
            
            return resultado
            
        except DeliveryPedidoModelo.DoesNotExist:
            raise ValueError(f"Pedido delivery {pedido_id} no encontrado")
        except Exception as e:
            raise Exception(f"Error al seguir estado de entrega: {str(e)}")
    
    def completar_entrega(self, pedido_id: int, datos_entrega: Dict[str, Any]) -> Dict[str, Any]:
        """
        Marca un pedido como entregado
        """
        try:
            with transaction.atomic():
                delivery_pedido = DeliveryPedidoModelo.objects.select_related('pedido', 'repartidor').get(
                    pedido_id=pedido_id,
                    estado_delivery='en_ruta'
                )
                
                # Actualizar delivery
                delivery_pedido.estado_delivery = 'entregado'
                delivery_pedido.hora_entrega = timezone.now()
                delivery_pedido.comentarios_entrega = datos_entrega.get('comentarios', '')
                delivery_pedido.save()
                
                # Actualizar pedido base
                delivery_pedido.pedido.estado = 'entregado'
                delivery_pedido.pedido.save()
                
                # Liberar repartidor
                if delivery_pedido.repartidor:
                    delivery_pedido.repartidor.estado = 'disponible'
                    delivery_pedido.repartidor.pedido_actual = None
                    delivery_pedido.repartidor.save()
                
                # Calcular métricas de entrega
                tiempo_total = (delivery_pedido.hora_entrega - delivery_pedido.pedido.fecha_creacion).total_seconds() / 60
                
                return {
                    'pedido_id': pedido_id,
                    'estado': 'entregado',
                    'hora_entrega': delivery_pedido.hora_entrega.isoformat(),
                    'tiempo_total_minutos': int(tiempo_total),
                    'tiempo_estimado_vs_real': {
                        'estimado': delivery_pedido.tiempo_estimado_minutos,
                        'real': int(tiempo_total),
                        'diferencia': int(tiempo_total - delivery_pedido.tiempo_estimado_minutos)
                    }
                }
                
        except DeliveryPedidoModelo.DoesNotExist:
            raise ValueError(f"Pedido delivery {pedido_id} no encontrado o no está en ruta")
        except Exception as e:
            raise Exception(f"Error al completar entrega: {str(e)}")
    
    def obtener_estadisticas_delivery(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Obtiene estadísticas de delivery para un período
        """
        try:
            pedidos_delivery = DeliveryPedidoModelo.objects.select_related('pedido', 'delivery_app').filter(
                pedido__fecha_creacion__range=[fecha_inicio, fecha_fin]
            )
            
            total_pedidos = pedidos_delivery.count()
            pedidos_entregados = pedidos_delivery.filter(estado_delivery='entregado').count()
            
            # Estadísticas por app
            stats_por_app = {}
            for pedido in pedidos_delivery.filter(es_delivery_externo=True):
                app_nombre = pedido.delivery_app.nombre
                if app_nombre not in stats_por_app:
                    stats_por_app[app_nombre] = {
                        'pedidos': 0,
                        'comision_total': 0,
                        'ventas_brutas': 0
                    }
                stats_por_app[app_nombre]['pedidos'] += 1
                stats_por_app[app_nombre]['comision_total'] += float(pedido.comision_app)
                stats_por_app[app_nombre]['ventas_brutas'] += float(pedido.pedido.total)
            
            return {
                'total_pedidos_delivery': total_pedidos,
                'pedidos_entregados': pedidos_entregados,
                'tasa_entrega': (pedidos_entregados / total_pedidos * 100) if total_pedidos > 0 else 0,
                'pedidos_directos': pedidos_delivery.filter(es_delivery_externo=False).count(),
                'pedidos_apps_externas': pedidos_delivery.filter(es_delivery_externo=True).count(),
                'estadisticas_por_app': stats_por_app,
                'ingresos_delivery': sum(float(p.pedido.total) for p in pedidos_delivery),
                'comisiones_pagadas': sum(float(p.comision_app) for p in pedidos_delivery.filter(es_delivery_externo=True))
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener estadísticas de delivery: {str(e)}")
    
    # Métodos auxiliares privados
    def _calcular_tiempo_estimado(self, direccion: str) -> int:
        """Calcula tiempo estimado de entrega basado en la dirección"""
        # Implementación simplificada - en un sistema real usaría APIs de mapas
        return 45  # 45 minutos por defecto
    
    def _calcular_costo_envio(self, direccion: str) -> float:
        """Calcula costo de envío basado en la dirección"""
        # Implementación simplificada - en un sistema real usaría APIs de mapas
        return 2500.0  # $2500 por defecto
    
    def _calcular_prioridad_entrega(self, delivery_pedido: DeliveryPedidoModelo) -> str:
        """Calcula la prioridad de un pedido para asignación"""
        tiempo_espera = (timezone.now() - delivery_pedido.pedido.fecha_creacion).total_seconds() / 60
        
        if tiempo_espera > 60:
            return 'alta'
        elif tiempo_espera > 30:
            return 'media'
        else:
            return 'baja'
