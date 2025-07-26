from typing import List, Optional, Dict, Any
from datetime import datetime
from django.db import transaction, models
from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from Backend.Dominio.Interfaces.IMesa_Repositorio import IMesaRepositorio
from Backend.Dominio.Entidades.Mesa_Entidad import Mesa, EstadoMesa, TipoMesa
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Dominio.Excepciones.DominioExcepcion import RepositorioExcepcion


class MesaRepositorio(IMesaRepositorio):
    """
    Implementación del repositorio de mesas usando Django ORM.
    """
    
    def _convertir_modelo_a_entidad(self, modelo: MesaModelo) -> Mesa:
        """
        Convierte un modelo Django a entidad de dominio.
        
        Args:
            modelo: Modelo Django MesaModelo
            
        Returns:
            Mesa: Entidad de dominio
        """
        try:
            # Mapear tipo de mesa
            tipo_mapping = {
                'individual': TipoMesa.INDIVIDUAL,
                'pequeña': TipoMesa.PEQUEÑA,
                'mediana': TipoMesa.MEDIANA,
                'grande': TipoMesa.GRANDE,
                'familiar': TipoMesa.FAMILIAR,
                'vip': TipoMesa.VIP
            }
            
            tipo_mesa = tipo_mapping.get(modelo.tipo_mesa, TipoMesa.PEQUEÑA)
            
            mesa = Mesa(
                numero=modelo.numero,
                capacidad=modelo.capacidad,
                tipo_mesa=tipo_mesa,
                ubicacion=modelo.ubicacion or "",
                caracteristicas=modelo.caracteristicas or ""
            )
            
            # Establecer ID y fechas
            mesa._id = modelo.id
            mesa._fecha_creacion = modelo.fecha_creacion
            mesa._fecha_actualizacion = modelo.fecha_actualizacion
            
            # Establecer estado y datos de ocupación
            estado_mapping = {
                'libre': EstadoMesa.LIBRE,
                'ocupada': EstadoMesa.OCUPADA,
                'reservada': EstadoMesa.RESERVADA,
                'limpieza': EstadoMesa.LIMPIEZA,
                'fuera_servicio': EstadoMesa.FUERA_SERVICIO
            }
            
            mesa._estado = estado_mapping.get(modelo.estado, EstadoMesa.LIBRE)
            mesa._activa = modelo.activa
            mesa._hora_ocupacion = modelo.hora_ocupacion
            mesa._tiempo_servicio_promedio = modelo.tiempo_servicio_promedio
            mesa._pedido_id_actual = modelo.pedido_id_actual
            
            # Cliente actual (solo ID por ahora)
            if modelo.cliente_actual:
                mesa._cliente_id_actual = modelo.cliente_actual.id
            
            if modelo.cantidad_personas_actual:
                mesa._cantidad_personas = modelo.cantidad_personas_actual
            
            return mesa
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al convertir modelo a entidad: {str(e)}")
    
    def _convertir_entidad_a_modelo(self, mesa: Mesa, modelo: Optional[MesaModelo] = None) -> MesaModelo:
        """
        Convierte una entidad de dominio a modelo Django.
        
        Args:
            mesa: Entidad de dominio
            modelo: Modelo existente para actualizar (opcional)
            
        Returns:
            MesaModelo: Modelo Django
        """
        try:
            if modelo is None:
                modelo = MesaModelo()
            
            # Mapear tipo de mesa
            tipo_mapping = {
                TipoMesa.INDIVIDUAL: 'individual',
                TipoMesa.PEQUEÑA: 'pequeña',
                TipoMesa.MEDIANA: 'mediana',
                TipoMesa.GRANDE: 'grande',
                TipoMesa.FAMILIAR: 'familiar',
                TipoMesa.VIP: 'vip'
            }
            
            modelo.numero = mesa.numero
            modelo.capacidad = mesa.capacidad
            modelo.tipo_mesa = tipo_mapping[mesa.tipo_mesa]
            modelo.ubicacion = mesa.ubicacion
            modelo.caracteristicas = mesa.caracteristicas
            
            # Mapear estado
            estado_mapping = {
                EstadoMesa.LIBRE: 'libre',
                EstadoMesa.OCUPADA: 'ocupada',
                EstadoMesa.RESERVADA: 'reservada',
                EstadoMesa.LIMPIEZA: 'limpieza',
                EstadoMesa.FUERA_SERVICIO: 'fuera_servicio'
            }
            
            modelo.estado = estado_mapping[mesa.estado]
            modelo.activa = mesa.activa
            modelo.hora_ocupacion = mesa.hora_ocupacion
            modelo.tiempo_servicio_promedio = mesa.tiempo_servicio_promedio
            modelo.pedido_id_actual = mesa.pedido_id_actual
            
            # Cliente actual
            if hasattr(mesa, '_cliente_id_actual') and mesa._cliente_id_actual:
                try:
                    modelo.cliente_actual = ClienteModelo.objects.get(id=mesa._cliente_id_actual)
                except ClienteModelo.DoesNotExist:
                    modelo.cliente_actual = None
            else:
                modelo.cliente_actual = None
            
            if hasattr(mesa, '_cantidad_personas'):
                modelo.cantidad_personas_actual = mesa._cantidad_personas
            
            return modelo
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al convertir entidad a modelo: {str(e)}")
    
    # Operaciones CRUD básicas
    def crear(self, mesa: Mesa) -> Mesa:
        """Crea una nueva mesa en el sistema."""
        try:
            with transaction.atomic():
                modelo = self._convertir_entidad_a_modelo(mesa)
                modelo.save()
                return self._convertir_modelo_a_entidad(modelo)
        except ValidationError as e:
            raise RepositorioExcepcion(f"Error de validación al crear mesa: {str(e)}")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al crear mesa: {str(e)}")
    
    def obtener_por_id(self, mesa_id: int) -> Optional[Mesa]:
        """Obtiene una mesa por su ID."""
        try:
            modelo = MesaModelo.objects.get(id=mesa_id)
            return self._convertir_modelo_a_entidad(modelo)
        except MesaModelo.DoesNotExist:
            return None
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesa por ID: {str(e)}")
    
    def obtener_por_numero(self, numero: str) -> Optional[Mesa]:
        """Obtiene una mesa por su número."""
        try:
            modelo = MesaModelo.objects.get(numero=numero)
            return self._convertir_modelo_a_entidad(modelo)
        except MesaModelo.DoesNotExist:
            return None
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesa por número: {str(e)}")
    
    def obtener_todas(self) -> List[Mesa]:
        """Obtiene todas las mesas del sistema."""
        try:
            modelos = MesaModelo.objects.all().order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener todas las mesas: {str(e)}")
    
    def actualizar(self, mesa: Mesa) -> Mesa:
        """Actualiza una mesa existente."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.get(id=mesa.id)
                modelo = self._convertir_entidad_a_modelo(mesa, modelo)
                modelo.save()
                return self._convertir_modelo_a_entidad(modelo)
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa.id} no encontrada")
        except ValidationError as e:
            raise RepositorioExcepcion(f"Error de validación al actualizar mesa: {str(e)}")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al actualizar mesa: {str(e)}")
    
    def eliminar(self, mesa_id: int) -> bool:
        """Elimina una mesa del sistema."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.get(id=mesa_id)
                
                # Verificar que no esté ocupada
                if modelo.estado == 'ocupada':
                    raise RepositorioExcepcion("No se puede eliminar una mesa ocupada")
                
                modelo.delete()
                return True
        except MesaModelo.DoesNotExist:
            return False
        except Exception as e:
            raise RepositorioExcepcion(f"Error al eliminar mesa: {str(e)}")
    
    # Consultas por estado
    def obtener_por_estado(self, estado: EstadoMesa) -> List[Mesa]:
        """Obtiene todas las mesas con un estado específico."""
        try:
            estado_mapping = {
                EstadoMesa.LIBRE: 'libre',
                EstadoMesa.OCUPADA: 'ocupada',
                EstadoMesa.RESERVADA: 'reservada',
                EstadoMesa.LIMPIEZA: 'limpieza',
                EstadoMesa.FUERA_SERVICIO: 'fuera_servicio'
            }
            
            estado_str = estado_mapping[estado]
            modelos = MesaModelo.objects.filter(estado=estado_str).order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas por estado: {str(e)}")
    
    def obtener_libres(self) -> List[Mesa]:
        """Obtiene todas las mesas libres y activas."""
        try:
            modelos = MesaModelo.objects.filter(
                estado='libre',
                activa=True
            ).order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas libres: {str(e)}")
    
    def obtener_ocupadas(self) -> List[Mesa]:
        """Obtiene todas las mesas ocupadas."""
        try:
            modelos = MesaModelo.objects.filter(estado='ocupada').order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas ocupadas: {str(e)}")
    
    def obtener_reservadas(self) -> List[Mesa]:
        """Obtiene todas las mesas reservadas."""
        try:
            modelos = MesaModelo.objects.filter(estado='reservada').order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas reservadas: {str(e)}")
    
    # Consultas por capacidad y tipo
    def obtener_por_capacidad(self, capacidad_minima: int, capacidad_maxima: Optional[int] = None) -> List[Mesa]:
        """Obtiene mesas por rango de capacidad."""
        try:
            query = Q(capacidad__gte=capacidad_minima)
            if capacidad_maxima:
                query &= Q(capacidad__lte=capacidad_maxima)
            
            modelos = MesaModelo.objects.filter(query).order_by('capacidad', 'numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas por capacidad: {str(e)}")
    
    def obtener_por_tipo(self, tipo_mesa: TipoMesa) -> List[Mesa]:
        """Obtiene mesas por tipo."""
        try:
            tipo_mapping = {
                TipoMesa.INDIVIDUAL: 'individual',
                TipoMesa.PEQUEÑA: 'pequeña',
                TipoMesa.MEDIANA: 'mediana',
                TipoMesa.GRANDE: 'grande',
                TipoMesa.FAMILIAR: 'familiar',
                TipoMesa.VIP: 'vip'
            }
            
            tipo_str = tipo_mapping[tipo_mesa]
            modelos = MesaModelo.objects.filter(tipo_mesa=tipo_str).order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas por tipo: {str(e)}")
    
    def obtener_adecuadas_para(self, cantidad_personas: int) -> List[Mesa]:
        """Obtiene mesas adecuadas para una cantidad específica de personas."""
        try:
            # Mesas con capacidad suficiente sin desperdiciar demasiado espacio
            modelos = MesaModelo.objects.filter(
                capacidad__gte=cantidad_personas,
                capacidad__lte=cantidad_personas + 2,
                estado='libre',
                activa=True
            ).order_by('capacidad', 'numero')
            
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas adecuadas: {str(e)}")
    
    # Continúa en la siguiente parte...
    def obtener_por_ubicacion(self, ubicacion: str) -> List[Mesa]:
        """Obtiene mesas por ubicación."""
        try:
            modelos = MesaModelo.objects.filter(
                ubicacion__icontains=ubicacion
            ).order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas por ubicación: {str(e)}")
    
    def obtener_por_cliente(self, cliente_id: int) -> Optional[Mesa]:
        """Obtiene la mesa actualmente ocupada por un cliente."""
        try:
            modelo = MesaModelo.objects.filter(
                cliente_actual_id=cliente_id,
                estado__in=['ocupada', 'reservada']
            ).first()
            
            return self._convertir_modelo_a_entidad(modelo) if modelo else None
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesa por cliente: {str(e)}")
    
    def obtener_historial_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """Obtiene el historial de mesas utilizadas por un cliente."""
        try:
            # Este método requeriría una tabla de historial adicional
            # Por simplicidad, retornamos información básica
            return []
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener historial del cliente: {str(e)}")
    
    # Operaciones de ocupación y liberación
    def ocupar_mesa(self, mesa_id: int, cliente_id: int, cantidad_personas: int, 
                   pedido_id: Optional[int] = None) -> Mesa:
        """Ocupa una mesa para un cliente."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if not modelo.esta_libre and modelo.estado != 'reservada':
                    raise RepositorioExcepcion(f"La mesa {modelo.numero} no está disponible")
                
                if not modelo.activa:
                    raise RepositorioExcepcion(f"La mesa {modelo.numero} está fuera de servicio")
                
                if cantidad_personas > modelo.capacidad:
                    raise RepositorioExcepcion(
                        f"La mesa solo tiene capacidad para {modelo.capacidad} personas"
                    )
                
                # Obtener cliente
                cliente = ClienteModelo.objects.get(id=cliente_id)
                
                # Actualizar estado
                modelo.estado = 'ocupada'
                modelo.cliente_actual = cliente
                modelo.cantidad_personas_actual = cantidad_personas
                modelo.hora_ocupacion = timezone.now()
                modelo.pedido_id_actual = pedido_id
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except ClienteModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Cliente con ID {cliente_id} no encontrado")
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al ocupar mesa: {str(e)}")
    
    def liberar_mesa(self, mesa_id: int) -> Dict[str, Any]:
        """Libera una mesa ocupada."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if modelo.estado not in ['ocupada', 'reservada']:
                    raise RepositorioExcepcion(f"La mesa {modelo.numero} no está ocupada o reservada")
                
                tiempo_servicio = 0
                if modelo.estado == 'ocupada' and modelo.hora_ocupacion:
                    modelo.hora_liberacion = timezone.now()
                    tiempo_servicio = modelo.calcular_tiempo_servicio()
                    
                    # Actualizar tiempo promedio
                    if tiempo_servicio:
                        modelo.actualizar_tiempo_promedio(tiempo_servicio)
                    
                    # Incrementar servicios
                    modelo.incrementar_servicios()
                
                # Cambiar estado a limpieza
                modelo.estado = 'limpieza'
                modelo.cliente_actual = None
                modelo.cantidad_personas_actual = None
                modelo.pedido_id_actual = None
                modelo.save()
                
                return {
                    'mesa': self._convertir_modelo_a_entidad(modelo),
                    'tiempo_servicio': tiempo_servicio,
                    'hora_liberacion': modelo.hora_liberacion
                }
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al liberar mesa: {str(e)}")
    
    def reservar_mesa(self, mesa_id: int, cliente_id: int) -> Mesa:
        """Reserva una mesa para un cliente."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if not modelo.puede_reservarse:
                    raise RepositorioExcepcion(f"La mesa {modelo.numero} no puede ser reservada")
                
                cliente = ClienteModelo.objects.get(id=cliente_id)
                
                modelo.estado = 'reservada'
                modelo.cliente_actual = cliente
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except ClienteModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Cliente con ID {cliente_id} no encontrado")
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al reservar mesa: {str(e)}")
    
    def cancelar_reserva(self, mesa_id: int) -> Mesa:
        """Cancela la reserva de una mesa."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if modelo.estado != 'reservada':
                    raise RepositorioExcepcion(f"La mesa {modelo.numero} no está reservada")
                
                modelo.estado = 'libre'
                modelo.cliente_actual = None
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al cancelar reserva: {str(e)}")
    
    # Gestión de estado
    def marcar_en_limpieza(self, mesa_id: int) -> Mesa:
        """Marca una mesa como en limpieza."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if modelo.estado == 'ocupada':
                    raise RepositorioExcepcion("No se puede marcar para limpieza una mesa ocupada")
                
                modelo.estado = 'limpieza'
                modelo.cliente_actual = None
                modelo.cantidad_personas_actual = None
                modelo.pedido_id_actual = None
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al marcar mesa en limpieza: {str(e)}")
    
    def marcar_como_libre(self, mesa_id: int) -> Mesa:
        """Marca una mesa como libre después de limpieza."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if modelo.estado != 'limpieza':
                    raise RepositorioExcepcion("La mesa debe estar en limpieza para marcarla como libre")
                
                modelo.estado = 'libre'
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al marcar mesa como libre: {str(e)}")
    
    def activar_mesa(self, mesa_id: int) -> Mesa:
        """Activa una mesa para servicio."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                modelo.activa = True
                if modelo.estado == 'fuera_servicio':
                    modelo.estado = 'libre'
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al activar mesa: {str(e)}")
    
    def desactivar_mesa(self, mesa_id: int, motivo: Optional[str] = None) -> Mesa:
        """Desactiva una mesa (fuera de servicio)."""
        try:
            with transaction.atomic():
                modelo = MesaModelo.objects.select_for_update().get(id=mesa_id)
                
                if modelo.estado == 'ocupada':
                    raise RepositorioExcepcion("No se puede desactivar una mesa ocupada")
                
                modelo.activa = False
                modelo.estado = 'fuera_servicio'
                modelo.cliente_actual = None
                modelo.pedido_id_actual = None
                
                if motivo:
                    modelo.caracteristicas = f"Fuera de servicio: {motivo}"
                
                modelo.save()
                
                return self._convertir_modelo_a_entidad(modelo)
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al desactivar mesa: {str(e)}")
    
    # Estadísticas y métricas
    def obtener_estadisticas_ocupacion(self, fecha_inicio: Optional[datetime] = None,
                                     fecha_fin: Optional[datetime] = None) -> Dict[str, Any]:
        """Obtiene estadísticas de ocupación de mesas."""
        try:
            query = MesaModelo.objects.all()
            
            if fecha_inicio:
                query = query.filter(fecha_actualizacion__gte=fecha_inicio)
            if fecha_fin:
                query = query.filter(fecha_actualizacion__lte=fecha_fin)
            
            stats = query.aggregate(
                total_mesas=Count('id'),
                mesas_activas=Count('id', filter=Q(activa=True)),
                tiempo_promedio_global=Avg('tiempo_servicio_promedio'),
                servicios_totales=models.Sum('total_servicios')
            )
            
            # Contar por estado
            estados = query.values('estado').annotate(count=Count('id'))
            
            return {
                'estadisticas_generales': stats,
                'por_estado': {estado['estado']: estado['count'] for estado in estados},
                'fecha_consulta': timezone.now()
            }
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener estadísticas: {str(e)}")
    
    def obtener_tiempo_promedio_por_mesa(self, mesa_id: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene tiempo promedio de servicio por mesa."""
        try:
            if mesa_id:
                modelo = MesaModelo.objects.get(id=mesa_id)
                return {
                    'mesa': modelo.numero,
                    'tiempo_promedio': modelo.tiempo_servicio_promedio,
                    'total_servicios': modelo.total_servicios
                }
            else:
                modelos = MesaModelo.objects.filter(
                    tiempo_servicio_promedio__isnull=False
                ).order_by('numero')
                
                return {
                    'mesas': [
                        {
                            'mesa': modelo.numero,
                            'tiempo_promedio': modelo.tiempo_servicio_promedio,
                            'total_servicios': modelo.total_servicios
                        }
                        for modelo in modelos
                    ]
                }
                
        except MesaModelo.DoesNotExist:
            raise RepositorioExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener tiempos promedio: {str(e)}")
    
    def obtener_mesas_con_mayor_rotacion(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Obtiene las mesas con mayor rotación de clientes."""
        try:
            modelos = MesaModelo.objects.filter(
                total_servicios__gt=0
            ).order_by('-total_servicios')[:limite]
            
            return [
                {
                    'mesa': modelo.numero,
                    'total_servicios': modelo.total_servicios,
                    'tiempo_promedio': modelo.tiempo_servicio_promedio,
                    'capacidad': modelo.capacidad,
                    'tipo': modelo.get_tipo_mesa_display()
                }
                for modelo in modelos
            ]
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas con mayor rotación: {str(e)}")
    
    def obtener_mesas_excediendo_tiempo_promedio(self, margen_porcentaje: int = 20) -> List[Mesa]:
        """Obtiene mesas que están excediendo el tiempo promedio de servicio."""
        try:
            mesas_excediendo = []
            modelos_ocupados = MesaModelo.objects.filter(
                estado='ocupada',
                hora_ocupacion__isnull=False,
                tiempo_servicio_promedio__isnull=False
            )
            
            for modelo in modelos_ocupados:
                tiempo_actual = modelo.obtener_tiempo_ocupacion_actual()
                if tiempo_actual:
                    tiempo_limite = modelo.tiempo_servicio_promedio * (1 + margen_porcentaje / 100)
                    if tiempo_actual > tiempo_limite:
                        mesas_excediendo.append(self._convertir_modelo_a_entidad(modelo))
            
            return mesas_excediendo
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener mesas excediendo tiempo: {str(e)}")
    
    # Búsquedas y filtros avanzados
    def buscar_mesas(self, filtros: Dict[str, Any]) -> List[Mesa]:
        """Busca mesas según múltiples criterios."""
        try:
            query = MesaModelo.objects.all()
            
            if 'numero' in filtros:
                query = query.filter(numero__icontains=filtros['numero'])
            
            if 'estado' in filtros:
                query = query.filter(estado=filtros['estado'])
            
            if 'capacidad_min' in filtros:
                query = query.filter(capacidad__gte=filtros['capacidad_min'])
            
            if 'capacidad_max' in filtros:
                query = query.filter(capacidad__lte=filtros['capacidad_max'])
            
            if 'tipo_mesa' in filtros:
                query = query.filter(tipo_mesa=filtros['tipo_mesa'])
            
            if 'ubicacion' in filtros:
                query = query.filter(ubicacion__icontains=filtros['ubicacion'])
            
            if 'activa' in filtros:
                query = query.filter(activa=filtros['activa'])
            
            modelos = query.order_by('numero')
            return [self._convertir_modelo_a_entidad(modelo) for modelo in modelos]
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error en búsqueda de mesas: {str(e)}")
    
    def contar_mesas_por_estado(self) -> Dict[str, int]:
        """Cuenta mesas agrupadas por estado."""
        try:
            resultado = MesaModelo.objects.values('estado').annotate(
                count=Count('id')
            ).order_by('estado')
            
            return {item['estado']: item['count'] for item in resultado}
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al contar mesas por estado: {str(e)}")
    
    def obtener_disponibilidad_por_horario(self, fecha: datetime) -> Dict[str, Any]:
        """Obtiene disponibilidad de mesas para una fecha/horario específico."""
        try:
            # Por simplicidad, retornamos disponibilidad actual
            total_mesas = MesaModelo.objects.filter(activa=True).count()
            mesas_libres = MesaModelo.objects.filter(estado='libre', activa=True).count()
            mesas_ocupadas = MesaModelo.objects.filter(estado='ocupada').count()
            mesas_reservadas = MesaModelo.objects.filter(estado='reservada').count()
            
            return {
                'fecha_consulta': fecha,
                'total_mesas': total_mesas,
                'disponibles': mesas_libres,
                'ocupadas': mesas_ocupadas,
                'reservadas': mesas_reservadas,
                'porcentaje_ocupacion': round((mesas_ocupadas / total_mesas) * 100, 2) if total_mesas > 0 else 0
            }
            
        except Exception as e:
            raise RepositorioExcepcion(f"Error al obtener disponibilidad: {str(e)}")
