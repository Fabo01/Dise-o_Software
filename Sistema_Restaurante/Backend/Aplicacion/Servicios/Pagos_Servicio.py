# Backend/Aplicacion/Servicios/Pagos_Servicio.py
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
from Backend.Infraestructura.Modelos.MedioPago_Modelo import MedioPagoModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo

class PagosServicio:
    """
    Servicio para gestionar pagos y transacciones
    """
    
    def procesar_pago_unico(self, datos_pago: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un pago único completo de un pedido
        """
        try:
            with transaction.atomic():
                # Validar pedido
                pedido = PedidoModelo.objects.get(
                    id=datos_pago['pedido_id'],
                    estado__in=['pendiente', 'preparando', 'listo']
                )
                
                # Validar medio de pago
                medio_pago = MedioPagoModelo.objects.get(
                    id=datos_pago['medio_pago_id'],
                    activo=True
                )
                
                # Validar monto
                monto_pago = Decimal(str(datos_pago['monto']))
                if monto_pago != pedido.total:
                    raise ValueError(f"El monto del pago ({monto_pago}) no coincide con el total del pedido ({pedido.total})")
                
                # Calcular comisión
                comision = medio_pago.calcular_comision(monto_pago)
                monto_neto = monto_pago - comision
                
                # Crear transacción
                transaccion_data = {
                    'pedido': pedido,
                    'medio_pago': medio_pago,
                    'monto': monto_pago,
                    'comision': comision,
                    'estado': 'pendiente',
                    'codigo_referencia': self._generar_codigo_referencia(),
                    'datos_externos': datos_pago.get('datos_externos', {})
                }
                
                # Procesar según el tipo de medio de pago
                if medio_pago.requiere_validacion_externa:
                    # Para medios de pago que requieren validación externa (tarjetas, etc.)
                    resultado_validacion = self._procesar_pago_externo(transaccion_data, datos_pago)
                    transaccion_data.update(resultado_validacion)
                else:
                    # Para efectivo y otros medios directos
                    transaccion_data['estado'] = 'completada'
                    transaccion_data['fecha_procesamiento'] = timezone.now()
                
                transaccion = TransaccionModelo.objects.create(**transaccion_data)
                
                # Actualizar estado del pedido si el pago fue exitoso
                if transaccion.es_exitosa():
                    pedido.estado = 'pagado'
                    pedido.save()
                
                return {
                    'transaccion_id': transaccion.id,
                    'codigo_referencia': transaccion.codigo_referencia,
                    'estado': transaccion.estado,
                    'monto': float(monto_pago),
                    'comision': float(comision),
                    'monto_neto': float(monto_neto),
                    'medio_pago': medio_pago.nombre,
                    'fecha_procesamiento': transaccion.fecha_procesamiento.isoformat() if transaccion.fecha_procesamiento else None,
                    'pedido_estado': pedido.estado
                }
                
        except PedidoModelo.DoesNotExist:
            raise ValueError(f"Pedido {datos_pago['pedido_id']} no encontrado o no disponible para pago")
        except MedioPagoModelo.DoesNotExist:
            raise ValueError(f"Medio de pago {datos_pago['medio_pago_id']} no encontrado o inactivo")
        except Exception as e:
            raise Exception(f"Error al procesar pago: {str(e)}")
    
    def procesar_pago_dividido(self, datos_pago: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un pago dividido en múltiples medios de pago
        """
        try:
            with transaction.atomic():
                # Validar pedido
                pedido = PedidoModelo.objects.get(
                    id=datos_pago['pedido_id'],
                    estado__in=['pendiente', 'preparando', 'listo']
                )
                
                pagos = datos_pago['pagos']  # Lista de pagos
                total_pagos = sum(Decimal(str(pago['monto'])) for pago in pagos)
                
                # Validar que la suma de pagos coincida con el total
                if total_pagos != pedido.total:
                    raise ValueError(f"La suma de pagos ({total_pagos}) no coincide con el total del pedido ({pedido.total})")
                
                transacciones = []
                total_comisiones = Decimal('0')
                
                # Procesar cada pago
                for pago_data in pagos:
                    # Validar medio de pago
                    medio_pago = MedioPagoModelo.objects.get(
                        id=pago_data['medio_pago_id'],
                        activo=True
                    )
                    
                    monto = Decimal(str(pago_data['monto']))
                    comision = medio_pago.calcular_comision(monto)
                    total_comisiones += comision
                    
                    # Crear transacción
                    transaccion_data = {
                        'pedido': pedido,
                        'medio_pago': medio_pago,
                        'monto': monto,
                        'comision': comision,
                        'estado': 'pendiente',
                        'codigo_referencia': self._generar_codigo_referencia(),
                        'datos_externos': pago_data.get('datos_externos', {}),
                        'es_pago_dividido': True
                    }
                    
                    # Procesar según el tipo de medio de pago
                    if medio_pago.requiere_validacion_externa:
                        resultado_validacion = self._procesar_pago_externo(transaccion_data, pago_data)
                        transaccion_data.update(resultado_validacion)
                    else:
                        transaccion_data['estado'] = 'completada'
                        transaccion_data['fecha_procesamiento'] = timezone.now()
                    
                    transaccion = TransaccionModelo.objects.create(**transaccion_data)
                    transacciones.append(transaccion)
                
                # Verificar que todas las transacciones fueron exitosas
                transacciones_exitosas = [t for t in transacciones if t.es_exitosa()]
                
                if len(transacciones_exitosas) == len(transacciones):
                    # Todos los pagos exitosos
                    pedido.estado = 'pagado'
                    pedido.save()
                    estado_general = 'completado'
                else:
                    # Algunos pagos fallaron
                    estado_general = 'parcial'
                
                return {
                    'estado_general': estado_general,
                    'total_transacciones': len(transacciones),
                    'transacciones_exitosas': len(transacciones_exitosas),
                    'total_pagado': float(sum(t.monto for t in transacciones_exitosas)),
                    'total_comisiones': float(total_comisiones),
                    'monto_neto_total': float(sum(t.monto_neto() for t in transacciones_exitosas)),
                    'detalle_transacciones': [
                        {
                            'id': t.id,
                            'codigo_referencia': t.codigo_referencia,
                            'medio_pago': t.medio_pago.nombre,
                            'monto': float(t.monto),
                            'estado': t.estado
                        }
                        for t in transacciones
                    ],
                    'pedido_estado': pedido.estado
                }
                
        except PedidoModelo.DoesNotExist:
            raise ValueError(f"Pedido {datos_pago['pedido_id']} no encontrado")
        except MedioPagoModelo.DoesNotExist as e:
            raise ValueError(f"Medio de pago no encontrado: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al procesar pago dividido: {str(e)}")
    
    def confirmar_pago_pendiente(self, transaccion_id: int, datos_confirmacion: Dict[str, Any]) -> Dict[str, Any]:
        """
        Confirma un pago que estaba pendiente de validación externa
        """
        try:
            with transaction.atomic():
                transaccion = TransaccionModelo.objects.select_related('pedido').get(
                    id=transaccion_id,
                    estado='pendiente'
                )
                
                # Actualizar transacción
                transaccion.estado = 'completada'
                transaccion.fecha_procesamiento = timezone.now()
                transaccion.codigo_autorizacion = datos_confirmacion.get('codigo_autorizacion', '')
                transaccion.datos_externos.update(datos_confirmacion.get('datos_adicionales', {}))
                transaccion.save()
                
                # Verificar si es el último pago pendiente del pedido
                pagos_pendientes = TransaccionModelo.objects.filter(
                    pedido=transaccion.pedido,
                    estado='pendiente'
                ).count()
                
                if pagos_pendientes == 0:
                    # Todas las transacciones completadas, marcar pedido como pagado
                    transaccion.pedido.estado = 'pagado'
                    transaccion.pedido.save()
                
                return {
                    'transaccion_id': transaccion.id,
                    'estado': transaccion.estado,
                    'codigo_autorizacion': transaccion.codigo_autorizacion,
                    'fecha_procesamiento': transaccion.fecha_procesamiento.isoformat(),
                    'pedido_estado': transaccion.pedido.estado,
                    'monto_neto': float(transaccion.monto_neto())
                }
                
        except TransaccionModelo.DoesNotExist:
            raise ValueError(f"Transacción {transaccion_id} no encontrada o no está pendiente")
        except Exception as e:
            raise Exception(f"Error al confirmar pago: {str(e)}")
    
    def rechazar_pago_pendiente(self, transaccion_id: int, motivo: str) -> Dict[str, Any]:
        """
        Rechaza un pago que estaba pendiente de validación
        """
        try:
            with transaction.atomic():
                transaccion = TransaccionModelo.objects.select_related('pedido').get(
                    id=transaccion_id,
                    estado='pendiente'
                )
                
                # Actualizar transacción
                transaccion.estado = 'fallida'
                transaccion.motivo_rechazo = motivo
                transaccion.fecha_procesamiento = timezone.now()
                transaccion.save()
                
                return {
                    'transaccion_id': transaccion.id,
                    'estado': transaccion.estado,
                    'motivo_rechazo': motivo,
                    'fecha_procesamiento': transaccion.fecha_procesamiento.isoformat()
                }
                
        except TransaccionModelo.DoesNotExist:
            raise ValueError(f"Transacción {transaccion_id} no encontrada o no está pendiente")
        except Exception as e:
            raise Exception(f"Error al rechazar pago: {str(e)}")
    
    def obtener_medios_pago_disponibles(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de medios de pago disponibles
        """
        try:
            medios_pago = MedioPagoModelo.objects.filter(activo=True).order_by('nombre')
            
            return [
                {
                    'id': mp.id,
                    'nombre': mp.nombre,
                    'tipo': mp.tipo,
                    'comision_porcentaje': float(mp.comision_porcentaje),
                    'comision_fija': float(mp.comision_fija),
                    'requiere_validacion_externa': mp.requiere_validacion_externa,
                    'descripcion': mp.descripcion
                }
                for mp in medios_pago
            ]
            
        except Exception as e:
            raise Exception(f"Error al obtener medios de pago: {str(e)}")
    
    def obtener_historial_pagos_pedido(self, pedido_id: int) -> Dict[str, Any]:
        """
        Obtiene el historial completo de pagos de un pedido
        """
        try:
            pedido = PedidoModelo.objects.get(id=pedido_id)
            transacciones = TransaccionModelo.objects.select_related('medio_pago').filter(
                pedido=pedido
            ).order_by('fecha_creacion')
            
            total_pagado = sum(t.monto for t in transacciones if t.es_exitosa())
            total_comisiones = sum(t.comision for t in transacciones if t.es_exitosa())
            
            return {
                'pedido_id': pedido_id,
                'total_pedido': float(pedido.total),
                'total_pagado': float(total_pagado),
                'saldo_pendiente': float(pedido.total - total_pagado),
                'total_comisiones': float(total_comisiones),
                'transacciones': [
                    {
                        'id': t.id,
                        'codigo_referencia': t.codigo_referencia,
                        'medio_pago': t.medio_pago.nombre,
                        'monto': float(t.monto),
                        'comision': float(t.comision),
                        'monto_neto': float(t.monto_neto()),
                        'estado': t.estado,
                        'fecha_creacion': t.fecha_creacion.isoformat(),
                        'fecha_procesamiento': t.fecha_procesamiento.isoformat() if t.fecha_procesamiento else None,
                        'codigo_autorizacion': t.codigo_autorizacion
                    }
                    for t in transacciones
                ]
            }
            
        except PedidoModelo.DoesNotExist:
            raise ValueError(f"Pedido {pedido_id} no encontrado")
        except Exception as e:
            raise Exception(f"Error al obtener historial de pagos: {str(e)}")
    
    def obtener_reporte_ventas_por_medio_pago(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Genera reporte de ventas agrupado por medio de pago
        """
        try:
            transacciones = TransaccionModelo.objects.select_related('medio_pago').filter(
                fecha_creacion__range=[fecha_inicio, fecha_fin],
                estado='completada'
            )
            
            reporte_por_medio = {}
            total_ventas = Decimal('0')
            total_comisiones = Decimal('0')
            
            for transaccion in transacciones:
                medio = transaccion.medio_pago.nombre
                
                if medio not in reporte_por_medio:
                    reporte_por_medio[medio] = {
                        'cantidad_transacciones': 0,
                        'monto_total': Decimal('0'),
                        'comisiones_total': Decimal('0'),
                        'monto_neto_total': Decimal('0')
                    }
                
                reporte_por_medio[medio]['cantidad_transacciones'] += 1
                reporte_por_medio[medio]['monto_total'] += transaccion.monto
                reporte_por_medio[medio]['comisiones_total'] += transaccion.comision
                reporte_por_medio[medio]['monto_neto_total'] += transaccion.monto_neto()
                
                total_ventas += transaccion.monto
                total_comisiones += transaccion.comision
            
            # Convertir a formato JSON serializable
            reporte_final = {}
            for medio, datos in reporte_por_medio.items():
                reporte_final[medio] = {
                    'cantidad_transacciones': datos['cantidad_transacciones'],
                    'monto_total': float(datos['monto_total']),
                    'comisiones_total': float(datos['comisiones_total']),
                    'monto_neto_total': float(datos['monto_neto_total']),
                    'porcentaje_del_total': float(datos['monto_total'] / total_ventas * 100) if total_ventas > 0 else 0
                }
            
            return {
                'periodo': {
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat()
                },
                'resumen_general': {
                    'total_transacciones': len(transacciones),
                    'total_ventas': float(total_ventas),
                    'total_comisiones': float(total_comisiones),
                    'total_neto': float(total_ventas - total_comisiones)
                },
                'detalle_por_medio_pago': reporte_final
            }
            
        except Exception as e:
            raise Exception(f"Error al generar reporte de ventas: {str(e)}")
    
    def obtener_transacciones_pendientes(self) -> List[Dict[str, Any]]:
        """
        Obtiene las transacciones que están pendientes de confirmación
        """
        try:
            transacciones = TransaccionModelo.objects.select_related('pedido', 'medio_pago').filter(
                estado='pendiente'
            ).order_by('fecha_creacion')
            
            return [
                {
                    'id': t.id,
                    'codigo_referencia': t.codigo_referencia,
                    'pedido_id': t.pedido.id,
                    'medio_pago': t.medio_pago.nombre,
                    'monto': float(t.monto),
                    'fecha_creacion': t.fecha_creacion.isoformat(),
                    'tiempo_espera_minutos': int((timezone.now() - t.fecha_creacion).total_seconds() / 60)
                }
                for t in transacciones
            ]
            
        except Exception as e:
            raise Exception(f"Error al obtener transacciones pendientes: {str(e)}")
    
    # Métodos auxiliares privados
    def _generar_codigo_referencia(self) -> str:
        """Genera un código de referencia único para la transacción"""
        import uuid
        return f"TXN-{uuid.uuid4().hex[:8].upper()}"
    
    def _procesar_pago_externo(self, transaccion_data: Dict[str, Any], datos_pago: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simula el procesamiento con un proveedor de pagos externo
        En un sistema real, aquí se haría la integración con APIs de pago
        """
        # Simulación de procesamiento externo
        # En producción esto sería una llamada a la API del proveedor de pagos
        
        # Por ahora, simulamos que el 95% de los pagos son exitosos
        import random
        if random.random() < 0.95:
            return {
                'estado': 'completada',
                'fecha_procesamiento': timezone.now(),
                'codigo_autorizacion': f"AUTH-{random.randint(100000, 999999)}"
            }
        else:
            return {
                'estado': 'fallida',
                'fecha_procesamiento': timezone.now(),
                'motivo_rechazo': 'Rechazo simulado del proveedor'
            }
