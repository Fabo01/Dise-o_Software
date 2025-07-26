from typing import List, Optional, Dict, Any
from datetime import datetime, date
from Backend.Dominio.Interfaces.IPedido_Repositorio import IPedidoRepositorio
from Backend.Dominio.Entidades.Pedido_Entidad import PedidoEntidad, EstadoPedido, TipoPedido, ItemPedido
from Backend.Dominio.Objetos_Valor.PrecioVO import PrecioVO
from Backend.Aplicacion.DTOs.PedidoDTO import *
from Backend.Aplicacion.Excepciones.AplicacionExcepcion import ServicioExcepcion, EntidadNoEncontradaExcepcion
from Backend.Dominio.Excepciones.DominioExcepcion import DominioExcepcion


class PedidoServicio:
    """Servicio de aplicación para la gestión de pedidos"""
    
    def __init__(self, pedido_repositorio: IPedidoRepositorio):
        self._pedido_repositorio = pedido_repositorio

    def crear_pedido(self, pedido_crear_dto: PedidoCrearDTO) -> PedidoDTO:
        """
        Caso de uso: Crear un nuevo pedido
        
        Args:
            pedido_crear_dto: DTO con datos para crear el pedido
            
        Returns:
            PedidoDTO: Pedido creado
            
        Raises:
            ServicioExcepcion: Si hay error en la creación
            DominioExcepcion: Si los datos no son válidos
        """
        try:
            # Validar tipo de pedido
            try:
                tipo_pedido = TipoPedido(pedido_crear_dto.tipo_pedido)
            except ValueError:
                raise DominioExcepcion(f"Tipo de pedido inválido: {pedido_crear_dto.tipo_pedido}")
            
            # Crear items del pedido
            items = []
            for item_data in pedido_crear_dto.items:
                # Aquí normalmente obtendrías los datos del menú desde su repositorio
                # Por simplicidad, asumo que vienen los datos necesarios
                item = ItemPedido(
                    menu_id=item_data['menu_id'],
                    nombre_menu=item_data.get('nombre_menu', f"Menu {item_data['menu_id']}"),
                    precio_unitario=PrecioVO(item_data['precio_unitario']),
                    cantidad=item_data['cantidad'],
                    observaciones=item_data.get('observaciones')
                )
                items.append(item)
            
            # Crear entidad de pedido
            pedido_entidad = PedidoEntidad(
                cliente_id=pedido_crear_dto.cliente_id,
                tipo_pedido=tipo_pedido,
                items=items,
                mesa_id=pedido_crear_dto.mesa_id,
                direccion_entrega=pedido_crear_dto.direccion_entrega,
                telefono_contacto=pedido_crear_dto.telefono_contacto,
                observaciones_generales=pedido_crear_dto.observaciones_generales
            )
            
            if pedido_crear_dto.tiempo_preparacion_estimado:
                pedido_entidad._tiempo_preparacion_estimado = pedido_crear_dto.tiempo_preparacion_estimado
            
            # Guardar en repositorio
            pedido_guardado = self._pedido_repositorio.crear(pedido_entidad)
            
            # Convertir a DTO y retornar
            return self._entidad_a_dto(pedido_guardado)
            
        except DominioExcepcion as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al crear pedido: {str(e)}")

    def obtener_pedido_por_id(self, pedido_id: int) -> Optional[PedidoDTO]:
        """
        Caso de uso: Obtener un pedido por su ID
        
        Args:
            pedido_id: ID del pedido a buscar
            
        Returns:
            PedidoDTO o None si no existe
        """
        try:
            pedido_entidad = self._pedido_repositorio.obtener_por_id(pedido_id)
            if pedido_entidad:
                return self._entidad_a_dto(pedido_entidad)
            return None
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener pedido {pedido_id}: {str(e)}")

    def obtener_todos_los_pedidos(self, limite: Optional[int] = None, desplazamiento: int = 0) -> List[PedidoDTO]:
        """
        Caso de uso: Obtener todos los pedidos con paginación
        
        Args:
            limite: Límite de resultados
            desplazamiento: Offset para paginación
            
        Returns:
            List[PedidoDTO]: Lista de pedidos
        """
        try:
            pedidos = self._pedido_repositorio.obtener_todos(limite, desplazamiento)
            return [self._entidad_a_dto(pedido) for pedido in pedidos]
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener pedidos: {str(e)}")

    def actualizar_pedido(self, pedido_actualizar_dto: PedidoActualizarDTO) -> PedidoDTO:
        """
        Caso de uso: Actualizar un pedido existente
        
        Args:
            pedido_actualizar_dto: DTO con datos actualizados
            
        Returns:
            PedidoDTO: Pedido actualizado
            
        Raises:
            EntidadNoEncontradaExcepcion: Si el pedido no existe
        """
        try:
            # Obtener pedido existente
            pedido_entidad = self._pedido_repositorio.obtener_por_id(pedido_actualizar_dto.id)
            if not pedido_entidad:
                raise EntidadNoEncontradaExcepcion(f"Pedido con ID {pedido_actualizar_dto.id} no encontrado")
            
            # Actualizar campos si se proporcionan
            if pedido_actualizar_dto.tipo_pedido:
                pedido_entidad._tipo_pedido = TipoPedido(pedido_actualizar_dto.tipo_pedido)
            
            if pedido_actualizar_dto.mesa_id is not None:
                pedido_entidad._mesa_id = pedido_actualizar_dto.mesa_id
            
            if pedido_actualizar_dto.direccion_entrega is not None:
                pedido_entidad._direccion_entrega = pedido_actualizar_dto.direccion_entrega
            
            if pedido_actualizar_dto.telefono_contacto is not None:
                pedido_entidad._telefono_contacto = pedido_actualizar_dto.telefono_contacto
            
            if pedido_actualizar_dto.observaciones_generales is not None:
                pedido_entidad._observaciones_generales = pedido_actualizar_dto.observaciones_generales
            
            if pedido_actualizar_dto.tiempo_preparacion_estimado is not None:
                pedido_entidad._tiempo_preparacion_estimado = pedido_actualizar_dto.tiempo_preparacion_estimado
            
            # Actualizar items si se proporcionan
            if pedido_actualizar_dto.items is not None:
                items = []
                for item_data in pedido_actualizar_dto.items:
                    item = ItemPedido(
                        menu_id=item_data['menu_id'],
                        nombre_menu=item_data.get('nombre_menu', f"Menu {item_data['menu_id']}"),
                        precio_unitario=PrecioVO(item_data['precio_unitario']),
                        cantidad=item_data['cantidad'],
                        observaciones=item_data.get('observaciones')
                    )
                    items.append(item)
                pedido_entidad._items = items
            
            # Guardar cambios
            pedido_actualizado = self._pedido_repositorio.actualizar(pedido_entidad)
            return self._entidad_a_dto(pedido_actualizado)
            
        except EntidadNoEncontradaExcepcion as e:
            raise e
        except DominioExcepcion as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al actualizar pedido: {str(e)}")

    def cambiar_estado_pedido(self, cambiar_estado_dto: PedidoCambiarEstadoDTO) -> PedidoDTO:
        """
        Caso de uso: Cambiar el estado de un pedido
        
        Args:
            cambiar_estado_dto: DTO con el nuevo estado
            
        Returns:
            PedidoDTO: Pedido con estado actualizado
        """
        try:
            # Obtener pedido existente
            pedido_entidad = self._pedido_repositorio.obtener_por_id(cambiar_estado_dto.id)
            if not pedido_entidad:
                raise EntidadNoEncontradaExcepcion(f"Pedido con ID {cambiar_estado_dto.id} no encontrado")
            
            # Cambiar estado según el valor solicitado
            nuevo_estado = EstadoPedido(cambiar_estado_dto.nuevo_estado)
            
            if nuevo_estado == EstadoPedido.CONFIRMADO:
                pedido_entidad.confirmar_pedido(cambiar_estado_dto.tiempo_preparacion)
            elif nuevo_estado == EstadoPedido.EN_PREPARACION:
                pedido_entidad.iniciar_preparacion()
            elif nuevo_estado == EstadoPedido.LISTO:
                pedido_entidad.marcar_listo()
            elif nuevo_estado == EstadoPedido.ENTREGADO:
                pedido_entidad.entregar_pedido()
            elif nuevo_estado == EstadoPedido.CANCELADO:
                pedido_entidad.cancelar_pedido(cambiar_estado_dto.motivo_cancelacion)
            
            # Guardar cambios
            pedido_actualizado = self._pedido_repositorio.actualizar(pedido_entidad)
            return self._entidad_a_dto(pedido_actualizado)
            
        except EntidadNoEncontradaExcepcion as e:
            raise e
        except DominioExcepcion as e:
            raise e
        except Exception as e:
            raise ServicioExcepcion(f"Error al cambiar estado del pedido: {str(e)}")

    def eliminar_pedido(self, pedido_id: int) -> bool:
        """
        Caso de uso: Eliminar un pedido
        
        Args:
            pedido_id: ID del pedido a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            return self._pedido_repositorio.eliminar(pedido_id)
        except Exception as e:
            raise ServicioExcepcion(f"Error al eliminar pedido {pedido_id}: {str(e)}")

    def buscar_pedidos(self, busqueda_dto: PedidoBusquedaDTO) -> List[PedidoDTO]:
        """
        Caso de uso: Buscar pedidos con múltiples filtros
        
        Args:
            busqueda_dto: DTO con criterios de búsqueda
            
        Returns:
            List[PedidoDTO]: Lista de pedidos que cumplen los criterios
        """
        try:
            # Crear diccionario de filtros
            filtros = {}
            
            if busqueda_dto.cliente_id:
                filtros['cliente_id'] = busqueda_dto.cliente_id
            
            if busqueda_dto.estado:
                filtros['estado'] = busqueda_dto.estado
            
            if busqueda_dto.tipo_pedido:
                filtros['tipo_pedido'] = busqueda_dto.tipo_pedido
            
            if busqueda_dto.mesa_id:
                filtros['mesa_id'] = busqueda_dto.mesa_id
            
            if busqueda_dto.fecha_inicio:
                filtros['fecha_inicio'] = busqueda_dto.fecha_inicio
            
            if busqueda_dto.fecha_fin:
                filtros['fecha_fin'] = busqueda_dto.fecha_fin
            
            if busqueda_dto.texto:
                filtros['texto'] = busqueda_dto.texto
            
            # Buscar usando filtros
            if busqueda_dto.solo_activos:
                pedidos = self._pedido_repositorio.obtener_pedidos_activos()
            else:
                pedidos = self._pedido_repositorio.buscar_por_filtros(filtros)
            
            # Aplicar paginación si es necesario
            if busqueda_dto.limite or busqueda_dto.desplazamiento > 0:
                inicio = busqueda_dto.desplazamiento
                fin = inicio + busqueda_dto.limite if busqueda_dto.limite else None
                pedidos = pedidos[inicio:fin]
            
            return [self._entidad_a_dto(pedido) for pedido in pedidos]
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al buscar pedidos: {str(e)}")

    def obtener_pedidos_por_cliente(self, cliente_id: int) -> List[PedidoDTO]:
        """
        Caso de uso: Obtener todos los pedidos de un cliente
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            List[PedidoDTO]: Lista de pedidos del cliente
        """
        try:
            pedidos = self._pedido_repositorio.buscar_por_cliente(cliente_id)
            return [self._entidad_a_dto(pedido) for pedido in pedidos]
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener pedidos del cliente {cliente_id}: {str(e)}")

    def obtener_pedidos_por_estado(self, estado: str) -> List[PedidoDTO]:
        """
        Caso de uso: Obtener pedidos por estado
        
        Args:
            estado: Estado de los pedidos a buscar
            
        Returns:
            List[PedidoDTO]: Lista de pedidos con el estado especificado
        """
        try:
            estado_enum = EstadoPedido(estado)
            pedidos = self._pedido_repositorio.buscar_por_estado(estado_enum)
            return [self._entidad_a_dto(pedido) for pedido in pedidos]
        except ValueError:
            raise DominioExcepcion(f"Estado inválido: {estado}")
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener pedidos por estado: {str(e)}")

    def obtener_pedidos_activos(self) -> List[PedidoDTO]:
        """
        Caso de uso: Obtener todos los pedidos activos (no entregados ni cancelados)
        
        Returns:
            List[PedidoDTO]: Lista de pedidos activos
        """
        try:
            pedidos = self._pedido_repositorio.obtener_pedidos_activos()
            return [self._entidad_a_dto(pedido) for pedido in pedidos]
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener pedidos activos: {str(e)}")

    def obtener_pedidos_cocina(self) -> List[PedidoCocinaDTO]:
        """
        Caso de uso: Obtener pedidos optimizados para mostrar en cocina
        
        Returns:
            List[PedidoCocinaDTO]: Lista de pedidos para cocina
        """
        try:
            # Obtener pedidos que están en preparación o confirmados
            estados_cocina = [EstadoPedido.CONFIRMADO, EstadoPedido.EN_PREPARACION]
            pedidos = []
            
            for estado in estados_cocina:
                pedidos.extend(self._pedido_repositorio.buscar_por_estado(estado))
            
            # Convertir a DTOs de cocina
            pedidos_cocina = []
            for pedido in pedidos:
                pedido_cocina = PedidoCocinaDTO(
                    id=pedido.id,
                    numero_mesa=f"Mesa {pedido.mesa_id}" if pedido.mesa_id else None,
                    tipo_pedido=pedido.tipo_pedido.value,
                    estado=pedido.estado.value,
                    tiempo_transcurrido=pedido.obtener_tiempo_transcurrido(),
                    tiempo_estimado=pedido.tiempo_preparacion_estimado,
                    esta_atrasado=pedido.esta_atrasado(),
                    items=[{
                        'nombre': item.nombre_menu,
                        'cantidad': item.cantidad,
                        'observaciones': item.observaciones
                    } for item in pedido.items],
                    observaciones=pedido.observaciones_generales,
                    prioridad='alta' if pedido.esta_atrasado() else 'media'
                )
                pedidos_cocina.append(pedido_cocina)
            
            # Ordenar por prioridad (atrasados primero)
            pedidos_cocina.sort(key=lambda p: (p.prioridad != 'alta', p.tiempo_transcurrido or 0))
            
            return pedidos_cocina
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener pedidos para cocina: {str(e)}")

    def obtener_estadisticas_pedidos(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> PedidoEstadisticasDTO:
        """
        Caso de uso: Obtener estadísticas de pedidos
        
        Args:
            fecha_inicio: Fecha de inicio del período
            fecha_fin: Fecha de fin del período (opcional)
            
        Returns:
            PedidoEstadisticasDTO: Estadísticas de pedidos
        """
        try:
            estadisticas = self._pedido_repositorio.obtener_estadisticas_por_fecha(fecha_inicio, fecha_fin)
            ventas_por_fecha = self._pedido_repositorio.obtener_ventas_por_periodo(fecha_inicio, fecha_fin)
            
            # Contar pedidos atrasados
            pedidos_atrasados = len(self._pedido_repositorio.buscar_pendientes_por_tiempo(60))  # 60 minutos
            
            return PedidoEstadisticasDTO(
                total_pedidos=estadisticas['total_pedidos'],
                total_ventas=estadisticas['total_ventas'],
                pedidos_por_estado=estadisticas['pedidos_por_estado'],
                pedidos_por_tipo=estadisticas['pedidos_por_tipo'],
                tiempo_promedio_preparacion=estadisticas['tiempo_promedio_preparacion'],
                pedidos_atrasados=pedidos_atrasados,
                ventas_por_fecha=ventas_por_fecha
            )
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener estadísticas: {str(e)}")

    def obtener_historial_cliente(self, cliente_id: int, limite: Optional[int] = None) -> PedidoHistorialDTO:
        """
        Caso de uso: Obtener historial de pedidos de un cliente
        
        Args:
            cliente_id: ID del cliente
            limite: Límite de pedidos a retornar
            
        Returns:
            PedidoHistorialDTO: Historial del cliente
        """
        try:
            pedidos = self._pedido_repositorio.obtener_historial_cliente(cliente_id, limite)
            
            if not pedidos:
                return PedidoHistorialDTO(
                    cliente_id=cliente_id,
                    cliente_nombre="Cliente no encontrado",
                    total_pedidos=0,
                    total_gastado=0.0,
                    ultimo_pedido=None,
                    pedidos=[]
                )
            
            # Calcular estadísticas
            total_gastado = sum(pedido.total.valor for pedido in pedidos if pedido.estado == EstadoPedido.ENTREGADO)
            ultimo_pedido = max(pedido.fecha_creacion for pedido in pedidos) if pedidos else None
            
            # Convertir a DTOs de resumen
            pedidos_resumen = []
            for pedido in pedidos:
                resumen = PedidoResumenDTO(
                    id=pedido.id,
                    cliente_nombre="",  # Se llenará con datos del cliente
                    tipo_pedido=pedido.tipo_pedido.value,
                    estado=pedido.estado.value,
                    mesa_numero=f"Mesa {pedido.mesa_id}" if pedido.mesa_id else None,
                    total=pedido.total.valor,
                    cantidad_items=pedido.cantidad_total_items,
                    fecha_creacion=pedido.fecha_creacion,
                    tiempo_transcurrido=pedido.obtener_tiempo_transcurrido(),
                    esta_atrasado=pedido.esta_atrasado()
                )
                pedidos_resumen.append(resumen)
            
            return PedidoHistorialDTO(
                cliente_id=cliente_id,
                cliente_nombre="",  # Se llenará con datos del cliente
                total_pedidos=len(pedidos),
                total_gastado=total_gastado,
                ultimo_pedido=ultimo_pedido,
                pedidos=pedidos_resumen
            )
            
        except Exception as e:
            raise ServicioExcepcion(f"Error al obtener historial del cliente: {str(e)}")

    def validar_pedido(self, pedido_crear_dto: PedidoCrearDTO) -> PedidoValidacionDTO:
        """
        Caso de uso: Validar un pedido antes de crearlo
        
        Args:
            pedido_crear_dto: DTO con datos del pedido a validar
            
        Returns:
            PedidoValidacionDTO: Resultado de la validación
        """
        errores = []
        advertencias = []
        total_estimado = 0.0
        tiempo_preparacion_total = 0
        
        try:
            # Validar tipo de pedido
            try:
                tipo_pedido = TipoPedido(pedido_crear_dto.tipo_pedido)
            except ValueError:
                errores.append(f"Tipo de pedido inválido: {pedido_crear_dto.tipo_pedido}")
            
            # Validar items
            if not pedido_crear_dto.items:
                errores.append("El pedido debe tener al menos un item")
            else:
                for i, item_data in enumerate(pedido_crear_dto.items):
                    if item_data.get('cantidad', 0) <= 0:
                        errores.append(f"Item {i+1}: La cantidad debe ser mayor a 0")
                    
                    if item_data.get('precio_unitario', 0) <= 0:
                        errores.append(f"Item {i+1}: El precio unitario debe ser mayor a 0")
                    
                    # Calcular totales
                    cantidad = item_data.get('cantidad', 0)
                    precio = item_data.get('precio_unitario', 0)
                    total_estimado += cantidad * precio
                    
                    # Tiempo de preparación estimado (ejemplo: 10 min base + 2 min por cantidad)
                    tiempo_item = 10 + (cantidad * 2)
                    tiempo_preparacion_total = max(tiempo_preparacion_total, tiempo_item)
            
            # Validaciones específicas por tipo
            if not errores:
                if tipo_pedido == TipoPedido.MESA and not pedido_crear_dto.mesa_id:
                    errores.append("Un pedido de mesa debe tener una mesa asignada")
                
                if tipo_pedido == TipoPedido.DELIVERY and not pedido_crear_dto.direccion_entrega:
                    errores.append("Un pedido de delivery debe tener dirección de entrega")
            
            # Advertencias
            if total_estimado > 100000:  # Ejemplo: pedidos muy grandes
                advertencias.append("Pedido con valor muy alto, confirme con el cliente")
            
            if tiempo_preparacion_total > 60:  # Más de 1 hora
                advertencias.append("Tiempo de preparación estimado muy largo")
            
            es_valido = len(errores) == 0
            
            return PedidoValidacionDTO(
                es_valido=es_valido,
                errores=errores,
                advertencias=advertencias,
                total_estimado=total_estimado,
                tiempo_preparacion_total=tiempo_preparacion_total if tiempo_preparacion_total > 0 else None
            )
            
        except Exception as e:
            return PedidoValidacionDTO(
                es_valido=False,
                errores=[f"Error en validación: {str(e)}"],
                advertencias=[],
                total_estimado=0.0,
                tiempo_preparacion_total=None
            )

    def _entidad_a_dto(self, pedido: PedidoEntidad) -> PedidoDTO:
        """Convierte una entidad de pedido a DTO"""
        items_dto = []
        for item in pedido.items:
            item_dto = ItemPedidoDTO(
                menu_id=item.menu_id,
                nombre_menu=item.nombre_menu,
                precio_unitario=item.precio_unitario.valor,
                cantidad=item.cantidad,
                observaciones=item.observaciones,
                subtotal=item.subtotal.valor
            )
            items_dto.append(item_dto)
        
        return PedidoDTO(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            cliente_nombre=None,  # Se llenará con datos del cliente si es necesario
            cliente_rut=None,
            tipo_pedido=pedido.tipo_pedido.value,
            estado=pedido.estado.value,
            mesa_id=pedido.mesa_id,
            mesa_numero=f"Mesa {pedido.mesa_id}" if pedido.mesa_id else None,
            direccion_entrega=pedido.direccion_entrega,
            telefono_contacto=pedido.telefono_contacto,
            observaciones_generales=pedido.observaciones_generales,
            fecha_creacion=pedido.fecha_creacion,
            fecha_confirmacion=pedido.fecha_confirmacion,
            fecha_entrega=pedido.fecha_entrega,
            tiempo_preparacion_estimado=pedido.tiempo_preparacion_estimado,
            total=pedido.total.valor,
            items=items_dto,
            cantidad_total_items=pedido.cantidad_total_items,
            tiempo_transcurrido=pedido.obtener_tiempo_transcurrido(),
            esta_atrasado=pedido.esta_atrasado()
        )
