"""
Controlador para el Dashboard analítico del sistema
Maneja las visualizaciones y métricas de negocio
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo


class DashboardMetricasView(APIView):
    """
    Vista para obtener métricas principales del dashboard
    """
    
    def get(self, request):
        """Obtiene las métricas principales del dashboard"""
        try:
            # Métricas generales
            total_clientes = ClienteModelo.objects.count()
            total_mesas = MesaModelo.objects.count()
            mesas_ocupadas = MesaModelo.objects.filter(estado='ocupada').count()
            total_menus = MenuModelo.objects.filter(disponible=True).count()
            
            # Pedidos del día
            hoy = timezone.now().date()
            pedidos_hoy = PedidoModelo.objects.filter(
                fecha_creacion__date=hoy
            ).count()
            
            # Ingresos del día
            ingresos_hoy = PedidoModelo.objects.filter(
                fecha_creacion__date=hoy,
                estado='entregado'
            ).aggregate(total=Sum('total'))['total'] or Decimal('0')
            
            # Tiempo promedio de servicio
            tiempo_promedio = MesaModelo.objects.filter(
                tiempo_servicio_promedio__isnull=False
            ).aggregate(promedio=Avg('tiempo_servicio_promedio'))['promedio'] or 0
            
            metricas = {
                'clientes_total': total_clientes,
                'mesas_total': total_mesas,
                'mesas_ocupadas': mesas_ocupadas,
                'mesas_libres': total_mesas - mesas_ocupadas,
                'menus_disponibles': total_menus,
                'pedidos_hoy': pedidos_hoy,
                'ingresos_hoy': float(ingresos_hoy),
                'tiempo_promedio_servicio': round(tiempo_promedio, 1) if tiempo_promedio else 0,
                'ocupacion_mesas': round((mesas_ocupadas / total_mesas * 100), 1) if total_mesas > 0 else 0
            }
            
            return Response(metricas, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener métricas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VentasPorFechaView(APIView):
    """
    Vista para obtener datos de ventas por fecha
    """
    
    def get(self, request):
        """Obtiene datos de ventas de los últimos 7 días"""
        try:
            # Últimos 7 días
            fecha_fin = timezone.now().date()
            fecha_inicio = fecha_fin - timedelta(days=6)
            
            # Consultar ventas por día
            ventas_diarias = []
            fecha_actual = fecha_inicio
            
            while fecha_actual <= fecha_fin:
                pedidos_dia = PedidoModelo.objects.filter(
                    fecha_creacion__date=fecha_actual,
                    estado='entregado'
                )
                
                total_dia = pedidos_dia.aggregate(total=Sum('total'))['total'] or Decimal('0')
                cantidad_pedidos = pedidos_dia.count()
                
                ventas_diarias.append({
                    'fecha': fecha_actual.strftime('%Y-%m-%d'),
                    'fecha_formateada': fecha_actual.strftime('%d/%m'),
                    'total_ventas': float(total_dia),
                    'cantidad_pedidos': cantidad_pedidos
                })
                
                fecha_actual += timedelta(days=1)
            
            return Response({
                'ventas_diarias': ventas_diarias,
                'periodo': f'{fecha_inicio.strftime("%d/%m/%Y")} - {fecha_fin.strftime("%d/%m/%Y")}'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener ventas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MenusPopularesView(APIView):
    """
    Vista para obtener los menús más populares
    """
    
    def get(self, request):
        """Obtiene los menús más ordenados"""
        try:
            # Top 5 menús más populares
            menus_populares = MenuModelo.objects.filter(
                disponible=True,
                veces_ordenado__gt=0
            ).order_by('-veces_ordenado')[:5]
            
            datos_menus = []
            for menu in menus_populares:
                datos_menus.append({
                    'id': menu.id,
                    'nombre': menu.nombre,
                    'categoria': menu.categoria,
                    'precio': float(menu.precio),
                    'veces_ordenado': menu.veces_ordenado,
                    'tiempo_preparacion': menu.tiempo_preparacion
                })
            
            return Response({
                'menus_populares': datos_menus
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener menús populares: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IngredientesCriticosView(APIView):
    """
    Vista para obtener ingredientes con stock crítico
    """
    
    def get(self, request):
        """Obtiene ingredientes con cantidad menor al nivel crítico"""
        try:
            from django.db.models import F
            
            ingredientes_criticos = IngredienteModelo.objects.filter(
                cantidad__lte=F('nivel_critico'),
                activo=True
            ).order_by('cantidad')
            
            datos_ingredientes = []
            for ingrediente in ingredientes_criticos:
                datos_ingredientes.append({
                    'id': ingrediente.id,
                    'nombre': ingrediente.nombre,
                    'categoria': ingrediente.categoria,
                    'cantidad_actual': float(ingrediente.cantidad),
                    'nivel_critico': float(ingrediente.nivel_critico),
                    'unidad_medida': ingrediente.unidad_medida,
                    'porcentaje_stock': round((ingrediente.cantidad / ingrediente.nivel_critico * 100), 1) if ingrediente.nivel_critico > 0 else 0
                })
            
            return Response({
                'ingredientes_criticos': datos_ingredientes,
                'total_criticos': len(datos_ingredientes)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener ingredientes críticos: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EstadoMesasView(APIView):
    """
    Vista para obtener el estado actual de todas las mesas
    """
    
    def get(self, request):
        """Obtiene el estado de todas las mesas"""
        try:
            mesas = MesaModelo.objects.all().order_by('numero')
            
            datos_mesas = []
            for mesa in mesas:
                tiempo_ocupacion = None
                if mesa.estado == 'ocupada' and mesa.hora_ocupacion:
                    tiempo_ocupacion = mesa.obtener_tiempo_ocupacion_actual()
                
                datos_mesas.append({
                    'id': mesa.id,
                    'numero': mesa.numero,
                    'capacidad': mesa.capacidad,
                    'estado': mesa.estado,
                    'estado_display': mesa.get_estado_display(),
                    'ubicacion': mesa.ubicacion,
                    'activa': mesa.activa,
                    'cantidad_personas_actual': mesa.cantidad_personas_actual,
                    'tiempo_ocupacion': tiempo_ocupacion,
                    'cliente_actual': mesa.cliente_actual.nombre if mesa.cliente_actual else None,
                    'tipo_mesa': mesa.tipo_mesa
                })
            
            # Resumen por estado
            resumen_estados = {
                'libre': mesas.filter(estado='libre', activa=True).count(),
                'ocupada': mesas.filter(estado='ocupada').count(),
                'reservada': mesas.filter(estado='reservada').count(),
                'limpieza': mesas.filter(estado='limpieza').count(),
                'fuera_servicio': mesas.filter(estado='fuera_servicio').count() + mesas.filter(activa=False).count()
            }
            
            return Response({
                'mesas': datos_mesas,
                'resumen_estados': resumen_estados,
                'total_mesas': mesas.count()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener estado de mesas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
