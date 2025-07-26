# Backend/Aplicacion/Servicios/Analytics_Servicio.py
from typing import Dict, List, Any
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Avg, Q, F
from django.db import models
from django.utils import timezone

from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo

class AnalyticsServicio:
    """
    Servicio para generar analytics y KPIs del restaurante
    """
    
    def obtener_kpis_ventas(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Obtiene KPIs relacionados con ventas
        """
        pedidos = PedidoModelo.objects.filter(
            fecha_creacion__range=[fecha_inicio, fecha_fin],
            estado__in=['entregado', 'pagado']
        )
        
        transacciones = TransaccionModelo.objects.filter(
            pedido__in=pedidos,
            estado='exitosa'
        )
        
        return {
            'total_ventas': transacciones.aggregate(Sum('monto'))['monto__sum'] or 0,
            'total_pedidos': pedidos.count(),
            'ticket_promedio': transacciones.aggregate(Avg('monto'))['monto__avg'] or 0,
            'comisiones_totales': transacciones.aggregate(Sum('monto_comision'))['monto_comision__sum'] or 0,
            'ventas_por_dia': self._obtener_ventas_por_dia(fecha_inicio, fecha_fin),
            'metodos_pago_mas_usados': self._obtener_metodos_pago_populares(transacciones)
        }
    
    def obtener_kpis_inventario(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Obtiene KPIs relacionados con inventario
        """
        ingredientes = IngredienteModelo.objects.all()
        ingredientes_criticos = ingredientes.filter(cantidad__lte=F('nivel_critico'))
        
        return {
            'total_ingredientes': ingredientes.count(),
            'ingredientes_criticos': ingredientes_criticos.count(),
            'valor_total_inventario': ingredientes.aggregate(
                total=Sum(F('cantidad') * F('precio_unitario'), output_field=models.DecimalField())
            )['total'] or 0,
            'ingredientes_mas_usados': self._obtener_ingredientes_mas_usados(fecha_inicio, fecha_fin),
            'rotacion_inventario': self._calcular_rotacion_inventario(fecha_inicio, fecha_fin)
        }
    
    def obtener_kpis_operacionales(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Obtiene KPIs operacionales
        """
        mesas = MesaModelo.objects.all()
        pedidos = PedidoModelo.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
        
        return {
            'ocupacion_promedio_mesas': self._calcular_ocupacion_mesas(fecha_inicio, fecha_fin),
            'tiempo_promedio_servicio': self._calcular_tiempo_promedio_servicio(pedidos),
            'pedidos_por_hora': self._obtener_pedidos_por_hora(fecha_inicio, fecha_fin),
            'eficiencia_cocina': self._calcular_eficiencia_cocina(pedidos),
            'total_mesas': mesas.count(),
            'capacidad_total': mesas.aggregate(Sum('capacidad'))['capacidad__sum'] or 0
        }
    
    def obtener_kpis_clientes(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Obtiene KPIs relacionados con clientes
        """
        clientes = ClienteModelo.objects.all()
        pedidos = PedidoModelo.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
        
        clientes_activos = clientes.filter(
            pedidos__fecha_creacion__range=[fecha_inicio, fecha_fin]
        ).distinct()
        
        return {
            'total_clientes': clientes.count(),
            'clientes_activos': clientes_activos.count(),
            'clientes_nuevos': self._obtener_clientes_nuevos(fecha_inicio, fecha_fin),
            'clientes_frecuentes': self._obtener_clientes_frecuentes(fecha_inicio, fecha_fin),
            'valor_promedio_cliente': self._calcular_valor_promedio_cliente(fecha_inicio, fecha_fin)
        }
    
    def obtener_datos_dashboard_completo(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """
        Obtiene todos los datos necesarios para el dashboard
        """
        return {
            'periodo': {
                'inicio': fecha_inicio.isoformat(),
                'fin': fecha_fin.isoformat()
            },
            'ventas': self.obtener_kpis_ventas(fecha_inicio, fecha_fin),
            'inventario': self.obtener_kpis_inventario(fecha_inicio, fecha_fin),
            'operacional': self.obtener_kpis_operacionales(fecha_inicio, fecha_fin),
            'clientes': self.obtener_kpis_clientes(fecha_inicio, fecha_fin),
            'menus_populares': self._obtener_menus_populares(fecha_inicio, fecha_fin),
            'tendencias': self._calcular_tendencias(fecha_inicio, fecha_fin)
        }
    
    # Métodos auxiliares privados
    def _obtener_ventas_por_dia(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Dict]:
        """Obtiene ventas agrupadas por día"""
        from django.db.models import TruncDate
        return list(
            TransaccionModelo.objects.filter(
                fecha_transaccion__range=[fecha_inicio, fecha_fin],
                estado='exitosa'
            ).extra({
                'fecha': "DATE(fecha_transaccion)"
            }).values('fecha').annotate(
                total=Sum('monto'),
                cantidad=Count('id')
            ).order_by('fecha')
        )
    
    def _obtener_metodos_pago_populares(self, transacciones) -> List[Dict]:
        """Obtiene métodos de pago más utilizados"""
        return list(
            transacciones.values('medio_pago__nombre', 'medio_pago__tipo')
            .annotate(
                total_transacciones=Count('id'),
                monto_total=Sum('monto')
            ).order_by('-total_transacciones')[:5]
        )
    
    def _obtener_ingredientes_mas_usados(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Dict]:
        """Obtiene ingredientes más utilizados en el periodo"""
        # Esta lógica dependería de un modelo de MovimientoStock o similar
        # Por ahora retornamos estructura base
        return []
    
    def _calcular_rotacion_inventario(self, fecha_inicio: datetime, fecha_fin: datetime) -> float:
        """Calcula la rotación del inventario"""
        # Implementación simplificada
        return 0.0
    
    def _calcular_ocupacion_mesas(self, fecha_inicio: datetime, fecha_fin: datetime) -> float:
        """Calcula ocupación promedio de mesas"""
        # Implementación simplificada
        return 0.0
    
    def _calcular_tiempo_promedio_servicio(self, pedidos) -> float:
        """Calcula tiempo promedio de servicio"""
        # Implementación simplificada basada en timestamps de pedidos
        return 0.0
    
    def _obtener_pedidos_por_hora(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Dict]:
        """Obtiene distribución de pedidos por hora"""
        from django.db.models import Extract
        return list(
            PedidoModelo.objects.filter(
                fecha_creacion__range=[fecha_inicio, fecha_fin]
            ).extra({
                'hora': "EXTRACT(hour FROM fecha_creacion)"
            }).values('hora').annotate(
                cantidad=Count('id')
            ).order_by('hora')
        )
    
    def _calcular_eficiencia_cocina(self, pedidos) -> Dict[str, float]:
        """Calcula métricas de eficiencia de cocina"""
        return {
            'tiempo_preparacion_promedio': 0.0,
            'pedidos_a_tiempo': 0.0,
            'pedidos_retrasados': 0.0
        }
    
    def _obtener_clientes_nuevos(self, fecha_inicio: datetime, fecha_fin: datetime) -> int:
        """Obtiene cantidad de clientes nuevos en el periodo"""
        return ClienteModelo.objects.filter(
            fecha_registro__range=[fecha_inicio, fecha_fin]
        ).count()
    
    def _obtener_clientes_frecuentes(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Dict]:
        """Obtiene clientes más frecuentes"""
        return list(
            ClienteModelo.objects.filter(
                pedidos__fecha_creacion__range=[fecha_inicio, fecha_fin]
            ).annotate(
                total_pedidos=Count('pedidos')
            ).order_by('-total_pedidos')[:10]
            .values('nombre', 'email', 'total_pedidos')
        )
    
    def _calcular_valor_promedio_cliente(self, fecha_inicio: datetime, fecha_fin: datetime) -> float:
        """Calcula valor promedio por cliente"""
        return 0.0
    
    def _obtener_menus_populares(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Dict]:
        """Obtiene menús más populares"""
        return list(
            MenuModelo.objects.filter(
                items_pedido__pedido__fecha_creacion__range=[fecha_inicio, fecha_fin]
            ).annotate(
                total_pedidos=Count('items_pedido')
            ).order_by('-total_pedidos')[:10]
            .values('nombre', 'categoria', 'total_pedidos')
        )
    
    def _calcular_tendencias(self, fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, Any]:
        """Calcula tendencias comparando con periodo anterior"""
        periodo_anterior_inicio = fecha_inicio - (fecha_fin - fecha_inicio)
        periodo_anterior_fin = fecha_inicio
        
        kpis_actual = self.obtener_kpis_ventas(fecha_inicio, fecha_fin)
        kpis_anterior = self.obtener_kpis_ventas(periodo_anterior_inicio, periodo_anterior_fin)
        
        return {
            'crecimiento_ventas': self._calcular_porcentaje_crecimiento(
                kpis_anterior['total_ventas'], kpis_actual['total_ventas']
            ),
            'crecimiento_pedidos': self._calcular_porcentaje_crecimiento(
                kpis_anterior['total_pedidos'], kpis_actual['total_pedidos']
            )
        }
    
    def _calcular_porcentaje_crecimiento(self, valor_anterior: float, valor_actual: float) -> float:
        """Calcula porcentaje de crecimiento entre dos valores"""
        if valor_anterior == 0:
            return 100.0 if valor_actual > 0 else 0.0
        return ((valor_actual - valor_anterior) / valor_anterior) * 100
