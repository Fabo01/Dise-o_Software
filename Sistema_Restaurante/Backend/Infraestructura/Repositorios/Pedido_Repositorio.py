from typing import List, Optional, Dict, Any
from datetime import datetime, date
from django.db import transaction
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone

from Backend.Dominio.Interfaces.IPedido_Repositorio import IPedidoRepositorio
from Backend.Dominio.Entidades.Pedido_Entidad import PedidoEntidad, EstadoPedido, TipoPedido, ItemPedido
from Backend.Dominio.Objetos_Valor.PrecioVO import PrecioVO
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo, ItemPedidoModelo
from Backend.Dominio.Excepciones.DominioExcepcion import DominioExcepcion


class RepositorioExcepcion(DominioExcepcion):
    """Excepción específica para errores de repositorio"""
    pass


class PedidoRepositorio(IPedidoRepositorio):
    """Implementación del repositorio de pedidos usando Django ORM"""

    def crear(self, pedido: PedidoEntidad) -> PedidoEntidad:
        """Crea un nuevo pedido en la base de datos"""
        try:
            with transaction.atomic():
                # Crear el modelo de pedido
                pedido_modelo = PedidoModelo(
                    cliente_id=pedido.cliente_id,
                    tipo_pedido=pedido.tipo_pedido.value,
                    mesa_id=pedido.mesa_id,
                    direccion_entrega=pedido.direccion_entrega,
                    telefono_contacto=pedido.telefono_contacto,
                    observaciones_generales=pedido.observaciones_generales,
                    estado=pedido.estado.value,
                    tiempo_preparacion_estimado=pedido.tiempo_preparacion_estimado,
                )
                
                if pedido.fecha_confirmacion:
                    pedido_modelo.fecha_confirmacion = pedido.fecha_confirmacion
                if pedido.fecha_entrega:
                    pedido_modelo.fecha_entrega = pedido.fecha_entrega
                
                pedido_modelo.save()
                
                # Crear los items del pedido
                for item in pedido.items:
                    ItemPedidoModelo.objects.create(
                        pedido=pedido_modelo,
                        menu_id=item.menu_id,
                        cantidad=item.cantidad,
                        precio_unitario=item.precio_unitario.valor,
                        observaciones=item.observaciones
                    )
                
                # Recalcular total
                pedido_modelo._recalcular_total()
                
                return self._modelo_a_entidad(pedido_modelo)
                
        except Exception as e:
            raise RepositorioExcepcion(f"Error al crear pedido: {str(e)}")

    def obtener_por_id(self, id: int) -> Optional[PedidoEntidad]:
        """Obtiene un pedido por su ID"""
        try:
            pedido_modelo = PedidoModelo.objects.prefetch_related('items__menu').get(pk=id)
            return self._modelo_a_entidad(pedido_modelo)
        except PedidoModelo.DoesNotExist:
            return None
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener pedido {id}: {str(e)}")

    def obtener_todos(self, limite: Optional[int] = None, desplazamiento: int = 0) -> List[PedidoEntidad]:
        """Obtiene todos los pedidos con paginación opcional"""
        try:
            queryset = PedidoModelo.objects.prefetch_related('items__menu').order_by('-fecha_creacion')
            
            if limite is not None:
                queryset = queryset[desplazamiento:desplazamiento + limite]
            elif desplazamiento > 0:
                queryset = queryset[desplazamiento:]
            
            return [self._modelo_a_entidad(pedido) for pedido in queryset]
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener pedidos: {str(e)}")

    def actualizar(self, pedido: PedidoEntidad) -> PedidoEntidad:
        """Actualiza un pedido existente"""
        try:
            with transaction.atomic():
                pedido_modelo = PedidoModelo.objects.get(pk=pedido.id)
                
                # Actualizar campos del pedido
                pedido_modelo.cliente_id = pedido.cliente_id
                pedido_modelo.tipo_pedido = pedido.tipo_pedido.value
                pedido_modelo.mesa_id = pedido.mesa_id
                pedido_modelo.direccion_entrega = pedido.direccion_entrega
                pedido_modelo.telefono_contacto = pedido.telefono_contacto
                pedido_modelo.observaciones_generales = pedido.observaciones_generales
                pedido_modelo.estado = pedido.estado.value
                pedido_modelo.tiempo_preparacion_estimado = pedido.tiempo_preparacion_estimado
                pedido_modelo.fecha_confirmacion = pedido.fecha_confirmacion
                pedido_modelo.fecha_entrega = pedido.fecha_entrega
                
                pedido_modelo.save()
                
                # Actualizar items (eliminar existentes y crear nuevos)
                pedido_modelo.items.all().delete()
                
                for item in pedido.items:
                    ItemPedidoModelo.objects.create(
                        pedido=pedido_modelo,
                        menu_id=item.menu_id,
                        cantidad=item.cantidad,
                        precio_unitario=item.precio_unitario.valor,
                        observaciones=item.observaciones
                    )
                
                # Recalcular total
                pedido_modelo._recalcular_total()
                
                return self._modelo_a_entidad(pedido_modelo)
                
        except PedidoModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Pedido con ID {pedido.id} no encontrado")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al actualizar pedido: {str(e)}")

    def eliminar(self, id: int) -> bool:
        """Elimina un pedido por su ID"""
        try:
            pedidos_eliminados, _ = PedidoModelo.objects.filter(pk=id).delete()
            return pedidos_eliminados > 0
        except Exception as e:
            raise RepositorioExcepcion(f"Error al eliminar pedido {id}: {str(e)}")

    def buscar_por_cliente(self, cliente_id: int) -> List[PedidoEntidad]:
        """Busca pedidos por ID de cliente"""
        try:
            pedidos = PedidoModelo.objects.filter(cliente_id=cliente_id).prefetch_related('items__menu').order_by('-fecha_creacion')
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar pedidos del cliente {cliente_id}: {str(e)}")

    def buscar_por_estado(self, estado: EstadoPedido) -> List[PedidoEntidad]:
        """Busca pedidos por estado"""
        try:
            pedidos = PedidoModelo.objects.filter(estado=estado.value).prefetch_related('items__menu').order_by('-fecha_creacion')
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar pedidos por estado {estado.value}: {str(e)}")

    def buscar_por_mesa(self, mesa_id: int) -> List[PedidoEntidad]:
        """Busca pedidos por ID de mesa"""
        try:
            pedidos = PedidoModelo.objects.filter(mesa_id=mesa_id).prefetch_related('items__menu').order_by('-fecha_creacion')
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar pedidos de la mesa {mesa_id}: {str(e)}")

    def buscar_por_tipo(self, tipo_pedido: TipoPedido) -> List[PedidoEntidad]:
        """Busca pedidos por tipo"""
        try:
            pedidos = PedidoModelo.objects.filter(tipo_pedido=tipo_pedido.value).prefetch_related('items__menu').order_by('-fecha_creacion')
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar pedidos por tipo {tipo_pedido.value}: {str(e)}")

    def buscar_por_fecha(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> List[PedidoEntidad]:
        """Busca pedidos por rango de fechas"""
        try:
            if fecha_fin is None:
                fecha_fin = fecha_inicio
            
            pedidos = PedidoModelo.objects.filter(
                fecha_creacion__date__range=[fecha_inicio, fecha_fin]
            ).prefetch_related('items__menu').order_by('-fecha_creacion')
            
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar pedidos por fecha: {str(e)}")

    def buscar_pendientes_por_tiempo(self, minutos_limite: int) -> List[PedidoEntidad]:
        """Busca pedidos que están atrasados según el tiempo límite"""
        try:
            tiempo_limite = timezone.now() - timezone.timedelta(minutes=minutos_limite)
            
            pedidos = PedidoModelo.objects.filter(
                Q(estado__in=['confirmado', 'en_preparacion']) &
                Q(fecha_confirmacion__lt=tiempo_limite)
            ).prefetch_related('items__menu').order_by('fecha_confirmacion')
            
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar pedidos atrasados: {str(e)}")

    def obtener_estadisticas_por_fecha(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> Dict[str, Any]:
        """Obtiene estadísticas de pedidos para un rango de fechas"""
        try:
            if fecha_fin is None:
                fecha_fin = fecha_inicio
            
            pedidos = PedidoModelo.objects.filter(
                fecha_creacion__date__range=[fecha_inicio, fecha_fin]
            )
            
            estadisticas = pedidos.aggregate(
                total_pedidos=Count('id'),
                total_ventas=Sum('total'),
                tiempo_promedio=Avg('tiempo_preparacion_estimado')
            )
            
            # Conteo por estado
            pedidos_por_estado = dict(
                pedidos.values('estado').annotate(count=Count('id')).values_list('estado', 'count')
            )
            
            # Conteo por tipo
            pedidos_por_tipo = dict(
                pedidos.values('tipo_pedido').annotate(count=Count('id')).values_list('tipo_pedido', 'count')
            )
            
            return {
                'total_pedidos': estadisticas['total_pedidos'] or 0,
                'total_ventas': float(estadisticas['total_ventas'] or 0),
                'pedidos_por_estado': pedidos_por_estado,
                'pedidos_por_tipo': pedidos_por_tipo,
                'tiempo_promedio_preparacion': float(estadisticas['tiempo_promedio'] or 0),
            }
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener estadísticas: {str(e)}")

    def obtener_ventas_por_periodo(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> Dict[str, float]:
        """Obtiene las ventas agrupadas por período"""
        try:
            if fecha_fin is None:
                fecha_fin = fecha_inicio
            
            ventas = PedidoModelo.objects.filter(
                fecha_creacion__date__range=[fecha_inicio, fecha_fin],
                estado='entregado'
            ).extra(
                select={'fecha': 'DATE(fecha_creacion)'}
            ).values('fecha').annotate(
                total=Sum('total')
            ).order_by('fecha')
            
            return {venta['fecha'].strftime('%Y-%m-%d'): float(venta['total']) for venta in ventas}
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener ventas por período: {str(e)}")

    def contar_por_estado(self) -> Dict[str, int]:
        """Cuenta pedidos agrupados por estado"""
        try:
            conteos = PedidoModelo.objects.values('estado').annotate(count=Count('id'))
            return {conteo['estado']: conteo['count'] for conteo in conteos}
        except Exception as e:
            raise RepositorioExcepcion(f"Error al contar por estado: {str(e)}")

    def obtener_pedidos_activos(self) -> List[PedidoEntidad]:
        """Obtiene pedidos que están activos (no entregados ni cancelados)"""
        try:
            pedidos = PedidoModelo.objects.filter(
                estado__in=['pendiente', 'confirmado', 'en_preparacion', 'listo']
            ).prefetch_related('items__menu').order_by('fecha_creacion')
            
            return [self._modelo_a_entidad(pedido) for pedido in pedidos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener pedidos activos: {str(e)}")

    def obtener_historial_cliente(self, cliente_id: int, limite: Optional[int] = None) -> List[PedidoEntidad]:
        """Obtiene el historial de pedidos de un cliente"""
        try:
            queryset = PedidoModelo.objects.filter(cliente_id=cliente_id).prefetch_related('items__menu').order_by('-fecha_creacion')
            
            if limite is not None:
                queryset = queryset[:limite]
            
            return [self._modelo_a_entidad(pedido) for pedido in queryset]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener historial del cliente {cliente_id}: {str(e)}")

    def buscar_por_filtros(self, filtros: Dict[str, Any]) -> List[PedidoEntidad]:
        """Busca pedidos usando múltiples filtros"""
        try:
            queryset = PedidoModelo.objects.prefetch_related('items__menu')
            
            if 'cliente_id' in filtros:
                queryset = queryset.filter(cliente_id=filtros['cliente_id'])
            
            if 'estado' in filtros:
                queryset = queryset.filter(estado=filtros['estado'])
            
            if 'tipo_pedido' in filtros:
                queryset = queryset.filter(tipo_pedido=filtros['tipo_pedido'])
            
            if 'mesa_id' in filtros:
                queryset = queryset.filter(mesa_id=filtros['mesa_id'])
            
            if 'fecha_inicio' in filtros:
                fecha_inicio = filtros['fecha_inicio']
                fecha_fin = filtros.get('fecha_fin', fecha_inicio)
                queryset = queryset.filter(fecha_creacion__date__range=[fecha_inicio, fecha_fin])
            
            if 'texto' in filtros:
                texto = filtros['texto']
                queryset = queryset.filter(
                    Q(observaciones_generales__icontains=texto) |
                    Q(items__observaciones__icontains=texto)
                ).distinct()
            
            return [self._modelo_a_entidad(pedido) for pedido in queryset.order_by('-fecha_creacion')]
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al buscar con filtros: {str(e)}")

    def existe(self, id: int) -> bool:
        """Verifica si existe un pedido con el ID especificado"""
        try:
            return PedidoModelo.objects.filter(pk=id).exists()
        except Exception as e:
            raise RepositorioExcepcion(f"Error al verificar existencia del pedido {id}: {str(e)}")

    def contar_total(self) -> int:
        """Cuenta el total de pedidos en el repositorio"""
        try:
            return PedidoModelo.objects.count()
        except Exception as e:
            raise RepositorioExcepcion(f"Error al contar pedidos: {str(e)}")

    def _modelo_a_entidad(self, pedido_modelo: PedidoModelo) -> PedidoEntidad:
        """Convierte un modelo Django a entidad de dominio"""
        
        # Convertir items
        items = []
        for item_modelo in pedido_modelo.items.all():
            item = ItemPedido(
                menu_id=item_modelo.menu.id,
                nombre_menu=item_modelo.menu.nombre,
                precio_unitario=PrecioVO(float(item_modelo.precio_unitario)),
                cantidad=item_modelo.cantidad,
                observaciones=item_modelo.observaciones
            )
            items.append(item)
        
        # Crear entidad de pedido
        pedido = PedidoEntidad(
            cliente_id=pedido_modelo.cliente.id,
            tipo_pedido=TipoPedido(pedido_modelo.tipo_pedido),
            items=items,
            mesa_id=pedido_modelo.mesa.id if pedido_modelo.mesa else None,
            direccion_entrega=pedido_modelo.direccion_entrega,
            telefono_contacto=pedido_modelo.telefono_contacto,
            observaciones_generales=pedido_modelo.observaciones_generales,
            id=pedido_modelo.id,
            fecha_creacion=pedido_modelo.fecha_creacion
        )
        
        # Establecer estado y fechas
        pedido._estado = EstadoPedido(pedido_modelo.estado)
        pedido._fecha_confirmacion = pedido_modelo.fecha_confirmacion
        pedido._fecha_entrega = pedido_modelo.fecha_entrega
        pedido._tiempo_preparacion_estimado = pedido_modelo.tiempo_preparacion_estimado
        
        return pedido
