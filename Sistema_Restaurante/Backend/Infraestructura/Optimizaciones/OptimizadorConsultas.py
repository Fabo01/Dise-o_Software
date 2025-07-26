# Backend/Infraestructura/Optimizaciones/OptimizadorConsultas.py
from django.db import models
from django.db.models import Prefetch, Q, F, Count, Sum, Avg
from django.core.cache import cache
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OptimizadorConsultas:
    """
    Clase para optimizar consultas de base de datos y mejorar rendimiento
    Implementa las tareas S3-21, S3-22, S3-23 del backlog
    """
    
    @staticmethod
    def optimizar_consulta_pedidos_con_items():
        """
        Optimiza la consulta de pedidos con sus items usando select_related y prefetch_related
        """
        from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
        from Backend.Infraestructura.Modelos.ItemPedido_Modelo import ItemPedidoModelo
        
        # Consulta optimizada que evita N+1 queries
        return PedidoModelo.objects.select_related(
            'cliente',
            'mesa'
        ).prefetch_related(
            Prefetch(
                'items',
                queryset=ItemPedidoModelo.objects.select_related('menu')
            )
        ).annotate(
            cantidad_items=Count('items'),
            total_calculado=Sum(F('items__cantidad') * F('items__precio_unitario'))
        )
    
    @staticmethod
    def optimizar_consulta_menu_con_ingredientes():
        """
        Optimiza la consulta de menús con ingredientes
        """
        from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
        
        return MenuModelo.objects.select_related().prefetch_related(
            'ingredientes'
        ).annotate(
            cantidad_ingredientes=Count('ingredientes'),
            costo_total=Sum('ingredientes__precio_unitario')
        )
    
    @staticmethod
    def obtener_estadisticas_ventas_optimizado(fecha_inicio: datetime, fecha_fin: datetime):
        """
        Obtiene estadísticas de ventas de forma optimizada usando agregaciones
        """
        from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
        
        cache_key = f"ventas_stats_{fecha_inicio.date()}_{fecha_fin.date()}"
        resultado = cache.get(cache_key)
        
        if resultado is None:
            resultado = TransaccionModelo.objects.filter(
                fecha_creacion__range=(fecha_inicio, fecha_fin),
                estado='exitosa'
            ).aggregate(
                total_ventas=Sum('monto'),
                total_transacciones=Count('id'),
                promedio_transaccion=Avg('monto'),
                total_comisiones=Sum('comision')
            )
            
            # Cachear por 30 minutos
            cache.set(cache_key, resultado, 30 * 60)
            logger.info(f"Estadísticas calculadas y cacheadas: {cache_key}")
        
        return resultado
    
    @staticmethod
    def obtener_ingredientes_criticos_optimizado():
        """
        Obtiene ingredientes con stock crítico de forma optimizada
        """
        from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
        
        cache_key = "ingredientes_criticos"
        resultado = cache.get(cache_key)
        
        if resultado is None:
            resultado = list(
                IngredienteModelo.objects.filter(
                    cantidad_disponible__lte=F('stock_critico')
                ).select_related().values(
                    'id', 'nombre', 'cantidad_disponible', 'stock_critico', 'categoria'
                )
            )
            
            # Cachear por 10 minutos
            cache.set(cache_key, resultado, 10 * 60)
            logger.info("Ingredientes críticos cacheados")
        
        return resultado
    
    @staticmethod
    def obtener_pedidos_delivery_optimizado():
        """
        Optimiza consultas de pedidos delivery con repartidores
        """
        from Backend.Infraestructura.Modelos.DeliveryPedido_Modelo import DeliveryPedidoModelo
        
        return DeliveryPedidoModelo.objects.select_related(
            'pedido',
            'pedido__cliente',
            'repartidor',
            'repartidor__delivery_app'
        ).annotate(
            tiempo_transcurrido=models.F('fecha_actualizacion') - models.F('fecha_creacion')
        )
    
    @staticmethod
    def limpiar_cache_relacionado(modulo: str):
        """
        Limpia cache relacionado a un módulo específico
        """
        patrones_cache = {
            'ventas': ['ventas_stats_*', 'dashboard_*'],
            'ingredientes': ['ingredientes_criticos', 'menu_*'],
            'pedidos': ['pedidos_*', 'dashboard_*'],
            'delivery': ['delivery_*']
        }
        
        if modulo in patrones_cache:
            for patron in patrones_cache[modulo]:
                cache.delete_pattern(patron)
            logger.info(f"Cache limpiado para módulo: {modulo}")

class IndicesDB:
    """
    Gestiona la creación de índices optimizados para mejorar consultas
    Implementa tarea S3-22 del backlog
    """
    
    @staticmethod
    def crear_indices_pedidos():
        """
        Crea índices compuestos para optimizar consultas de pedidos
        """
        from django.db import connection
        
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_pedido_cliente_fecha ON pedido_modelo (cliente_id, fecha_creacion);",
            "CREATE INDEX IF NOT EXISTS idx_pedido_estado_fecha ON pedido_modelo (estado, fecha_creacion);",
            "CREATE INDEX IF NOT EXISTS idx_pedido_mesa_estado ON pedido_modelo (mesa_id, estado);",
        ]
        
        with connection.cursor() as cursor:
            for indice in indices:
                try:
                    cursor.execute(indice)
                    logger.info(f"Índice creado: {indice}")
                except Exception as e:
                    logger.error(f"Error creando índice: {e}")
    
    @staticmethod
    def crear_indices_transacciones():
        """
        Crea índices para optimizar consultas de transacciones
        """
        from django.db import connection
        
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_transaccion_pedido_estado ON transaccion_modelo (pedido_id, estado);",
            "CREATE INDEX IF NOT EXISTS idx_transaccion_fecha_estado ON transaccion_modelo (fecha_creacion, estado);",
            "CREATE INDEX IF NOT EXISTS idx_transaccion_medio_pago ON transaccion_modelo (medio_pago_id, estado);",
        ]
        
        with connection.cursor() as cursor:
            for indice in indices:
                try:
                    cursor.execute(indice)
                    logger.info(f"Índice creado: {indice}")
                except Exception as e:
                    logger.error(f"Error creando índice: {e}")
    
    @staticmethod
    def crear_indices_delivery():
        """
        Crea índices para optimizar consultas de delivery
        """
        from django.db import connection
        
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_delivery_estado_fecha ON deliverypedido_modelo (estado_delivery, fecha_creacion);",
            "CREATE INDEX IF NOT EXISTS idx_delivery_repartidor_estado ON deliverypedido_modelo (repartidor_id, estado_delivery);",
            "CREATE INDEX IF NOT EXISTS idx_repartidor_activo_disponible ON deliveryrepartidor_modelo (activo, ubicacion_latitud, ubicacion_longitud);",
        ]
        
        with connection.cursor() as cursor:
            for indice in indices:
                try:
                    cursor.execute(indice)
                    logger.info(f"Índice creado: {indice}")
                except Exception as e:
                    logger.error(f"Error creando índice: {e}")

class CacheManager:
    """
    Gestiona estrategias de cache para mejorar rendimiento
    Implementa tarea S3-23 del backlog
    """
    
    TIMEOUTS = {
        'menus': 60 * 60,  # 1 hora
        'ingredientes': 30 * 60,  # 30 minutos
        'estadisticas': 15 * 60,  # 15 minutos
        'configuracion': 24 * 60 * 60,  # 24 horas
    }
    
    @staticmethod
    def cache_menus_disponibles():
        """
        Cachea la lista de menús disponibles
        """
        from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
        
        cache_key = "menus_disponibles"
        menus = cache.get(cache_key)
        
        if menus is None:
            menus = list(
                MenuModelo.objects.filter(
                    disponible=True
                ).select_related().values(
                    'id', 'nombre', 'precio', 'categoria', 'tiempo_preparacion'
                )
            )
            cache.set(cache_key, menus, CacheManager.TIMEOUTS['menus'])
            logger.info("Menús disponibles cacheados")
        
        return menus
    
    @staticmethod
    def cache_configuracion_sistema():
        """
        Cachea configuraciones del sistema
        """
        cache_key = "config_sistema"
        config = cache.get(cache_key)
        
        if config is None:
            config = {
                'hora_apertura': '09:00',
                'hora_cierre': '23:00',
                'tiempo_max_mesa': 120,  # minutos
                'comision_delivery': 10,  # porcentaje
                'areas_delivery_activas': True,
            }
            cache.set(cache_key, config, CacheManager.TIMEOUTS['configuracion'])
            logger.info("Configuración del sistema cacheada")
        
        return config
    
    @staticmethod
    def invalidar_cache_menu():
        """
        Invalida cache relacionado con menús cuando hay cambios
        """
        cache.delete_many([
            'menus_disponibles',
            'menus_por_categoria',
            'ingredientes_menu'
        ])
        logger.info("Cache de menús invalidado")
    
    @staticmethod
    def invalidar_cache_estadisticas():
        """
        Invalida cache de estadísticas cuando hay nuevas transacciones
        """
        # Obtener todas las claves de cache de estadísticas del día
        from django.core.cache.utils import make_key
        today = datetime.now().date()
        
        keys_to_delete = [
            f'ventas_stats_{today}*',
            'dashboard_kpis',
            'estadisticas_diarias'
        ]
        
        for pattern in keys_to_delete:
            cache.delete_pattern(pattern)
        
        logger.info("Cache de estadísticas invalidado")
