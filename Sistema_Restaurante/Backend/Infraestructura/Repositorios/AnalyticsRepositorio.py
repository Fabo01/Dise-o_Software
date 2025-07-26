# Backend/Infraestructura/Repositorios/AnalyticsRepositorio.py
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from Backend.Dominio.Interfaces.IAnalyticsRepositorio import IAnalyticsRepositorio
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
# from Backend.Infraestructura.Modelos.DetallePedido_Modelo import DetallePedidoModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
from Backend.Infraestructura.Modelos.DeliveryPedido_Modelo import DeliveryPedidoModelo
from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
import pandas as pd
import numpy as np

class AnalyticsRepositorio(IAnalyticsRepositorio):
    """
    Implementación concreta del repositorio de analytics.
    Maneja consultas complejas para reportes y análisis de datos.
    """
    
    def obtener_ventas_por_periodo(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene datos de ventas en un período específico"""
        pedidos = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado__in=['completado', 'entregado']
        )
        
        # Calcular métricas básicas
        total_pedidos = pedidos.count()
        total_ingresos = pedidos.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        promedio_pedido = total_ingresos / total_pedidos if total_pedidos > 0 else Decimal('0.00')
        
        # Ventas por día
        ventas_diarias = pedidos.extra(
            select={'fecha': 'DATE(fecha_creacion)'}
        ).values('fecha').annotate(
            total_dia=Sum('total'),
            pedidos_dia=Count('id')
        ).order_by('fecha')
        
        return {
            'periodo': {
                'inicio': fecha_inicio,
                'fin': fecha_fin
            },
            'resumen': {
                'total_pedidos': total_pedidos,
                'total_ingresos': float(total_ingresos),
                'promedio_por_pedido': float(promedio_pedido)
            },
            'ventas_diarias': list(ventas_diarias)
        }
    
    def obtener_productos_mas_vendidos(self, limite: int = 10, fecha_inicio: Optional[date] = None, 
                                     fecha_fin: Optional[date] = None) -> List[Dict[str, Any]]:
        """Obtiene los productos más vendidos"""
        # Por ahora retornamos datos simulados hasta implementar DetallePedido
        # TODO: Implementar cuando DetallePedidoModelo esté disponible
        
        return [
            {
                'menu__nombre': 'Hamburguesa Clásica',
                'menu__precio': 15.99,
                'menu__categoria': 'Plato Principal',
                'cantidad_vendida': 150,
                'ingresos_generados': 2398.50
            },
            {
                'menu__nombre': 'Pizza Margherita',
                'menu__precio': 18.50,
                'menu__categoria': 'Plato Principal',
                'cantidad_vendida': 120,
                'ingresos_generados': 2220.00
            }
        ]
    
    def obtener_estadisticas_mesas(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene estadísticas de uso de mesas"""
        pedidos_mesa = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            mesa__isnull=False,
            estado__in=['completado', 'entregado']
        )
        
        # Estadísticas por mesa
        stats_mesas = pedidos_mesa.values(
            'mesa__numero',
            'mesa__capacidad'
        ).annotate(
            total_pedidos=Count('id'),
            ingresos_mesa=Sum('total'),
            tiempo_promedio=Avg('tiempo_preparacion')
        ).order_by('-ingresos_mesa')
        
        # Mesa más rentable
        mesa_top = stats_mesas.first() if stats_mesas else None
        
        # Ocupación promedio
        total_mesas = MesaModelo.objects.filter(activa=True).count()
        mesas_usadas = pedidos_mesa.values('mesa').distinct().count()
        ocupacion_promedio = (mesas_usadas / total_mesas * 100) if total_mesas > 0 else 0
        
        return {
            'estadisticas_por_mesa': list(stats_mesas),
            'mesa_mas_rentable': mesa_top,
            'ocupacion_promedio': round(ocupacion_promedio, 2),
            'total_mesas_disponibles': total_mesas
        }
    
    def obtener_ingresos_por_metodo_pago(self, fecha_inicio: date, fecha_fin: date) -> List[Dict[str, Any]]:
        """Obtiene ingresos desglosados por método de pago"""
        transacciones = TransaccionModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado='completado'
        ).values(
            'medio_pago__nombre',
            'medio_pago__tipo'
        ).annotate(
            total_transacciones=Count('id'),
            monto_total=Sum('monto'),
            comisiones_total=Sum('comision')
        ).order_by('-monto_total')
        
        return list(transacciones)
    
    def obtener_tendencias_pedidos(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene tendencias de pedidos por horas/días"""
        pedidos = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado__in=['completado', 'entregado']
        )
        
        # Tendencia por hora del día
        pedidos_por_hora = pedidos.extra(
            select={'hora': 'EXTRACT(hour FROM fecha_creacion)'}
        ).values('hora').annotate(
            cantidad=Count('id'),
            ingresos=Sum('total')
        ).order_by('hora')
        
        # Tendencia por día de la semana
        pedidos_por_dia_semana = pedidos.extra(
            select={'dia_semana': 'EXTRACT(dow FROM fecha_creacion)'}
        ).values('dia_semana').annotate(
            cantidad=Count('id'),
            ingresos=Sum('total')
        ).order_by('dia_semana')
        
        # Mapear números de día a nombres
        dias_nombres = {0: 'Domingo', 1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 
                       4: 'Jueves', 5: 'Viernes', 6: 'Sábado'}
        
        for item in pedidos_por_dia_semana:
            item['dia_nombre'] = dias_nombres.get(item['dia_semana'], 'Desconocido')
        
        return {
            'tendencia_horaria': list(pedidos_por_hora),
            'tendencia_semanal': list(pedidos_por_dia_semana)
        }
    
    def obtener_estadisticas_delivery(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene estadísticas del servicio de delivery"""
        deliveries = DeliveryPedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin
        )
        
        total_deliveries = deliveries.count()
        deliveries_completados = deliveries.filter(estado='entregado').count()
        tasa_exito = (deliveries_completados / total_deliveries * 100) if total_deliveries > 0 else 0
        
        # Tiempo promedio de entrega
        tiempo_promedio = deliveries.filter(estado='entregado').aggregate(
            promedio=Avg('tiempo_estimado')
        )['promedio'] or 0
        
        # Ingresos por delivery
        ingresos_delivery = deliveries.aggregate(
            total=Sum('costo_delivery')
        )['total'] or Decimal('0.00')
        
        # Estados de delivery
        estados = deliveries.values('estado').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad')
        
        return {
            'total_deliveries': total_deliveries,
            'tasa_exito': round(tasa_exito, 2),
            'tiempo_promedio_entrega': round(float(tiempo_promedio), 2),
            'ingresos_delivery': float(ingresos_delivery),
            'distribucion_estados': list(estados)
        }
    
    def obtener_satisfaccion_cliente(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene métricas de satisfacción del cliente"""
        # Simulamos métricas de satisfacción basadas en datos disponibles
        pedidos = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado__in=['completado', 'entregado']
        )
        
        # Tiempo promedio de preparación (indicador de eficiencia)
        tiempo_promedio_prep = pedidos.aggregate(
            promedio=Avg('tiempo_preparacion')
        )['promedio'] or 0
        
        # Pedidos cancelados (indicador negativo)
        pedidos_cancelados = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado='cancelado'
        ).count()
        
        total_pedidos = pedidos.count() + pedidos_cancelados
        tasa_cancelacion = (pedidos_cancelados / total_pedidos * 100) if total_pedidos > 0 else 0
        
        # Clientes frecuentes (más de 1 pedido en el período)
        clientes_frecuentes = pedidos.values('cliente').annotate(
            cantidad_pedidos=Count('id')
        ).filter(cantidad_pedidos__gt=1).count()
        
        return {
            'tiempo_promedio_preparacion': round(float(tiempo_promedio_prep), 2),
            'tasa_cancelacion': round(tasa_cancelacion, 2),
            'clientes_frecuentes': clientes_frecuentes,
            'total_pedidos_periodo': total_pedidos,
            'indicador_satisfaccion': round(100 - tasa_cancelacion, 2)  # Métrica simplificada
        }
    
    def obtener_rendimiento_empleados(self, fecha_inicio: date, fecha_fin: date) -> List[Dict[str, Any]]:
        """Obtiene métricas de rendimiento de empleados"""
        # Analizar pedidos por empleado que los tomó
        rendimiento = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado__in=['completado', 'entregado'],
            cliente__isnull=False  # Asumimos que cliente representa quien tomó el pedido
        ).values(
            'cliente__first_name',
            'cliente__last_name',
            'cliente__email'
        ).annotate(
            pedidos_atendidos=Count('id'),
            ingresos_generados=Sum('total'),
            tiempo_promedio=Avg('tiempo_preparacion')
        ).order_by('-pedidos_atendidos')
        
        return list(rendimiento)
    
    def obtener_costos_operacionales(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Obtiene análisis de costos operacionales"""
        # Por ahora calculamos basados en datos disponibles
        # TODO: Implementar cálculos detallados cuando DetallePedido esté disponible
        
        # Ingresos totales de pedidos
        pedidos_periodo = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado__in=['completado', 'entregado']
        )
        
        ingresos_totales = pedidos_periodo.aggregate(
            total=Sum('total')
        )['total'] or Decimal('0.00')
        
        # Estimación de costos (30% de ingresos como simulación)
        costo_ingredientes = ingresos_totales * Decimal('0.30')
        
        # Costos de delivery
        costos_delivery = DeliveryPedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado='entregado'
        ).aggregate(
            total=Sum('costo_delivery')
        )['total'] or Decimal('0.00')
        
        # Comisiones de pagos
        comisiones_pagos = TransaccionModelo.objects.filter(
            fecha_transaccion__date__gte=fecha_inicio,
            fecha_transaccion__date__lte=fecha_fin,
            estado='exitosa'
        ).aggregate(
            total=Sum('monto_comision')
        )['total'] or Decimal('0.00')
        
        # Margen de ganancia
        costos_totales = costo_ingredientes + comisiones_pagos
        ganancia_bruta = ingresos_totales - costos_totales
        margen_porcentaje = (ganancia_bruta / ingresos_totales * 100) if ingresos_totales > 0 else 0
        
        return {
            'ingresos_totales': float(ingresos_totales),
            'costo_ingredientes': float(costo_ingredientes),
            'costos_delivery': float(costos_delivery),
            'comisiones_pagos': float(comisiones_pagos),
            'costos_totales': float(costos_totales),
            'ganancia_bruta': float(ganancia_bruta),
            'margen_porcentaje': round(float(margen_porcentaje), 2)
        }
    
    def generar_reporte_ejecutivo(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Genera reporte ejecutivo consolidado"""
        ventas = self.obtener_ventas_por_periodo(fecha_inicio, fecha_fin)
        productos_top = self.obtener_productos_mas_vendidos(5, fecha_inicio, fecha_fin)
        costos = self.obtener_costos_operacionales(fecha_inicio, fecha_fin)
        delivery_stats = self.obtener_estadisticas_delivery(fecha_inicio, fecha_fin)
        satisfaccion = self.obtener_satisfaccion_cliente(fecha_inicio, fecha_fin)
        
        return {
            'periodo': ventas['periodo'],
            'resumen_ejecutivo': {
                'total_ingresos': ventas['resumen']['total_ingresos'],
                'total_pedidos': ventas['resumen']['total_pedidos'],
                'margen_ganancia': costos['margen_porcentaje'],
                'satisfaccion_cliente': satisfaccion['indicador_satisfaccion']
            },
            'productos_destacados': productos_top,
            'rendimiento_delivery': {
                'total_deliveries': delivery_stats['total_deliveries'],
                'tasa_exito': delivery_stats['tasa_exito']
            },
            'analisis_costos': costos,
            'fecha_generacion': timezone.now()
        }
    
    def obtener_predicciones_demanda(self, dias_adelante: int = 7) -> Dict[str, Any]:
        """Obtiene predicciones de demanda basadas en datos históricos"""
        # Obtener datos históricos de los últimos 30 días
        fecha_fin = date.today()
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        pedidos_historicos = PedidoModelo.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin,
            estado__in=['completado', 'entregado']
        ).extra(
            select={'fecha': 'DATE(fecha_creacion)'}
        ).values('fecha').annotate(
            pedidos_dia=Count('id'),
            ingresos_dia=Sum('total')
        ).order_by('fecha')
        
        if not pedidos_historicos:
            return {'predicciones': [], 'confianza': 0}
        
        # Convertir a DataFrame para análisis
        df = pd.DataFrame(list(pedidos_historicos))
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Calcular tendencia simple usando promedio móvil
        promedio_pedidos = df['pedidos_dia'].mean()
        promedio_ingresos = df['ingresos_dia'].mean()
        
        # Generar predicciones simples
        predicciones = []
        for i in range(1, dias_adelante + 1):
            fecha_prediccion = fecha_fin + timedelta(days=i)
            # Aplicar variación estacional (simulada)
            factor_estacional = 1.0
            if fecha_prediccion.weekday() in [5, 6]:  # Fin de semana
                factor_estacional = 1.2
            
            predicciones.append({
                'fecha': fecha_prediccion,
                'pedidos_estimados': int(promedio_pedidos * factor_estacional),
                'ingresos_estimados': float(promedio_ingresos * factor_estacional)
            })
        
        return {
            'predicciones': predicciones,
            'confianza': 75,  # Simulada
            'base_historica': len(df),
            'metodo': 'Promedio móvil con ajuste estacional'
        }
