"""
Controlador para el Dashboard y Analytics
Proporciona métricas y KPIs del restaurante
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo


class DashboardController(viewsets.ViewSet):
    """
    Controlador para métricas y analytics del dashboard
    """
    
    @action(detail=False, methods=['get'])
    def resumen_general(self, request):
        """Obtener resumen general del restaurante"""
        hoy = timezone.now().date()
        
        # Métricas básicas
        total_clientes = ClienteModelo.objects.count()
        total_mesas = MesaModelo.objects.filter(activa=True).count()
        mesas_ocupadas = MesaModelo.objects.filter(estado='ocupada').count()
        total_ingredientes = IngredienteModelo.objects.filter(activo=True).count()
        ingredientes_stock_bajo = IngredienteModelo.objects.filter(
            cantidad__lte=F('nivel_critico'),
            activo=True
        ).count()
        
        # Métricas de pedidos de hoy
        pedidos_hoy = PedidoModelo.objects.filter(fecha_creacion__date=hoy)
        ventas_hoy = pedidos_hoy.aggregate(
            total=Sum('total')
        )['total'] or Decimal('0')
        
        # Pedidos por estado
        pedidos_por_estado = pedidos_hoy.values('estado').annotate(
            cantidad=Count('id')
        )
        
        # Ocupación de mesas
        ocupacion_mesas = {
            'total': total_mesas,
            'ocupadas': mesas_ocupadas,
            'libres': total_mesas - mesas_ocupadas,
            'porcentaje_ocupacion': round((mesas_ocupadas / total_mesas * 100), 2) if total_mesas > 0 else 0
        }
        
        return Response({
            'status': 'success',
            'data': {
                'metricas_generales': {
                    'total_clientes': total_clientes,
                    'total_mesas': total_mesas,
                    'total_ingredientes': total_ingredientes,
                    'ingredientes_stock_bajo': ingredientes_stock_bajo
                },
                'ventas_hoy': {
                    'total_pedidos': pedidos_hoy.count(),
                    'total_ventas': str(ventas_hoy),
                    'promedio_por_pedido': str(round(ventas_hoy / pedidos_hoy.count(), 2)) if pedidos_hoy.count() > 0 else '0'
                },
                'pedidos_por_estado': list(pedidos_por_estado),
                'ocupacion_mesas': ocupacion_mesas,
                'fecha_consulta': hoy.strftime('%Y-%m-%d')
            }
        })
    
    @action(detail=False, methods=['get'])
    def ventas_periodo(self, request):
        """Obtener ventas por período"""
        # Parámetros de consulta
        dias = int(request.query_params.get('dias', 7))
        fecha_fin = timezone.now().date()
        fecha_inicio = fecha_fin - timedelta(days=dias-1)
        
        # Consulta de ventas por día
        ventas_por_dia = PedidoModelo.objects.filter(
            fecha_creacion__date__range=[fecha_inicio, fecha_fin],
            estado__in=['entregado', 'listo']
        ).extra(
            select={'fecha': 'date(fecha_creacion)'}
        ).values('fecha').annotate(
            total_ventas=Sum('total'),
            cantidad_pedidos=Count('id')
        ).order_by('fecha')
        
        # Métricas del período
        total_ventas = sum(item['total_ventas'] or 0 for item in ventas_por_dia)
        total_pedidos = sum(item['cantidad_pedidos'] for item in ventas_por_dia)
        promedio_diario = total_ventas / dias if dias > 0 else 0
        
        return Response({
            'status': 'success',
            'data': {
                'periodo': {
                    'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
                    'dias': dias
                },
                'resumen': {
                    'total_ventas': str(total_ventas),
                    'total_pedidos': total_pedidos,
                    'promedio_diario': str(round(promedio_diario, 2)),
                    'promedio_por_pedido': str(round(total_ventas / total_pedidos, 2)) if total_pedidos > 0 else '0'
                },
                'ventas_por_dia': [
                    {
                        'fecha': item['fecha'],
                        'total_ventas': str(item['total_ventas'] or 0),
                        'cantidad_pedidos': item['cantidad_pedidos']
                    }
                    for item in ventas_por_dia
                ]
            }
        })
    
    @action(detail=False, methods=['get'])
    def menus_populares(self, request):
        """Obtener menús más populares"""
        dias = int(request.query_params.get('dias', 30))
        fecha_inicio = timezone.now().date() - timedelta(days=dias)
        
        # Consultar items de pedidos más populares
        from Backend.Infraestructura.Modelos.Pedido_Modelo import ItemPedidoModelo
        
        items_populares = ItemPedidoModelo.objects.filter(
            pedido__fecha_creacion__date__gte=fecha_inicio,
            pedido__estado__in=['entregado', 'listo']
        ).values(
            'menu__nombre',
            'menu__categoria',
            'menu__precio'
        ).annotate(
            total_pedidos=Count('id'),
            total_cantidad=Sum('cantidad'),
            total_ventas=Sum('subtotal')
        ).order_by('-total_cantidad')[:10]
        
        return Response({
            'status': 'success',
            'data': {
                'periodo_dias': dias,
                'menus_populares': [
                    {
                        'nombre': item['menu__nombre'],
                        'categoria': item['menu__categoria'],
                        'precio': str(item['menu__precio']),
                        'total_pedidos': item['total_pedidos'],
                        'total_cantidad': item['total_cantidad'],
                        'total_ventas': str(item['total_ventas'] or 0)
                    }
                    for item in items_populares
                ]
            }
        })
    
    @action(detail=False, methods=['get'])
    def estado_inventario(self, request):
        """Obtener estado del inventario"""
        # Ingredientes por categoría
        ingredientes_por_categoria = IngredienteModelo.objects.filter(
            activo=True
        ).values('categoria').annotate(
            total=Count('id'),
            stock_bajo=Count('id', filter=Q(cantidad__lte=F('nivel_critico'))),
            stock_agotado=Count('id', filter=Q(cantidad=0))
        )
        
        # Ingredientes próximos a vencer
        fecha_limite = timezone.now().date() + timedelta(days=7)
        ingredientes_vencimiento = IngredienteModelo.objects.filter(
            activo=True,
            fecha_vencimiento__lte=fecha_limite,
            fecha_vencimiento__gte=timezone.now().date()
        ).values(
            'nombre', 'fecha_vencimiento', 'cantidad', 'unidad_medida'
        )
        
        # Top ingredientes con stock bajo
        stock_critico = IngredienteModelo.objects.filter(
            activo=True,
            cantidad__lte=models.F('nivel_critico')
        ).values(
            'nombre', 'cantidad', 'nivel_critico', 'unidad_medida', 'categoria'
        )[:10]
        
        return Response({
            'status': 'success',
            'data': {
                'resumen_por_categoria': list(ingredientes_por_categoria),
                'ingredientes_vencimiento': [
                    {
                        'nombre': item['nombre'],
                        'fecha_vencimiento': item['fecha_vencimiento'].strftime('%Y-%m-%d'),
                        'cantidad': str(item['cantidad']),
                        'unidad_medida': item['unidad_medida'],
                        'dias_restantes': (item['fecha_vencimiento'] - timezone.now().date()).days
                    }
                    for item in ingredientes_vencimiento
                ],
                'stock_critico': list(stock_critico)
            }
        })
    
    @action(detail=False, methods=['get'])
    def rendimiento_mesas(self, request):
        """Obtener métricas de rendimiento de mesas"""
        dias = int(request.query_params.get('dias', 7))
        fecha_inicio = timezone.now().date() - timedelta(days=dias)
        
        # Métricas por mesa
        mesas_rendimiento = MesaModelo.objects.filter(
            activa=True
        ).annotate(
            pedidos_periodo=Count(
                'pedidos',
                filter=Q(pedidos__fecha_creacion__date__gte=fecha_inicio)
            ),
            ventas_periodo=Sum(
                'pedidos__total',
                filter=Q(
                    pedidos__fecha_creacion__date__gte=fecha_inicio,
                    pedidos__estado__in=['entregado', 'listo']
                )
            )
        ).values(
            'numero', 'capacidad', 'ubicacion', 'pedidos_periodo', 'ventas_periodo'
        ).order_by('-ventas_periodo')
        
        return Response({
            'status': 'success',
            'data': {
                'periodo_dias': dias,
                'rendimiento_mesas': [
                    {
                        'numero': mesa['numero'],
                        'capacidad': mesa['capacidad'],
                        'ubicacion': mesa['ubicacion'],
                        'pedidos_periodo': mesa['pedidos_periodo'],
                        'ventas_periodo': str(mesa['ventas_periodo'] or 0)
                    }
                    for mesa in mesas_rendimiento
                ]
            }
        })
    
    @action(detail=False, methods=['get'])
    def alertas(self, request):
        """Obtener alertas del sistema"""
        alertas = []
        
        # Ingredientes con stock bajo
        ingredientes_stock_bajo = IngredienteModelo.objects.filter(
            activo=True,
            cantidad__lte=models.F('nivel_critico')
        ).count()
        
        if ingredientes_stock_bajo > 0:
            alertas.append({
                'tipo': 'stock_bajo',
                'severidad': 'alta' if ingredientes_stock_bajo > 5 else 'media',
                'mensaje': f'{ingredientes_stock_bajo} ingrediente(s) con stock bajo',
                'cantidad': ingredientes_stock_bajo
            })
        
        # Ingredientes próximos a vencer
        ingredientes_vencimiento = IngredienteModelo.objects.filter(
            activo=True,
            fecha_vencimiento__lte=timezone.now().date() + timedelta(days=3),
            fecha_vencimiento__gte=timezone.now().date()
        ).count()
        
        if ingredientes_vencimiento > 0:
            alertas.append({
                'tipo': 'vencimiento',
                'severidad': 'alta',
                'mensaje': f'{ingredientes_vencimiento} ingrediente(s) próximo(s) a vencer',
                'cantidad': ingredientes_vencimiento
            })
        
        # Pedidos pendientes por mucho tiempo
        pedidos_atrasados = PedidoModelo.objects.filter(
            estado='en_preparacion',
            fecha_confirmacion__lt=timezone.now() - timedelta(hours=1)
        ).count()
        
        if pedidos_atrasados > 0:
            alertas.append({
                'tipo': 'pedidos_atrasados',
                'severidad': 'media',
                'mensaje': f'{pedidos_atrasados} pedido(s) en preparación por más de 1 hora',
                'cantidad': pedidos_atrasados
            })
        
        return Response({
            'status': 'success',
            'data': {
                'total_alertas': len(alertas),
                'alertas': alertas
            }
        })
