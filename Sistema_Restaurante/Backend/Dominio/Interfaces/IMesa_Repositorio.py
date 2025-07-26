from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from Backend.Dominio.Entidades.Mesa_Entidad import Mesa, EstadoMesa, TipoMesa


class IMesaRepositorio(ABC):
    """
    Interfaz para el repositorio de mesas.
    Define todas las operaciones de acceso a datos para las mesas del restaurante.
    """
    
    # Operaciones CRUD básicas
    @abstractmethod
    def crear(self, mesa: Mesa) -> Mesa:
        """
        Crea una nueva mesa en el sistema.
        
        Args:
            mesa: Entidad Mesa a crear
            
        Returns:
            Mesa: Mesa creada con ID asignado
            
        Raises:
            RepositorioExcepcion: Si ocurre un error en la creación
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, mesa_id: int) -> Optional[Mesa]:
        """
        Obtiene una mesa por su ID.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa: Mesa encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def obtener_por_numero(self, numero: str) -> Optional[Mesa]:
        """
        Obtiene una mesa por su número.
        
        Args:
            numero: Número de la mesa
            
        Returns:
            Mesa: Mesa encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def obtener_todas(self) -> List[Mesa]:
        """
        Obtiene todas las mesas del sistema.
        
        Returns:
            List[Mesa]: Lista de todas las mesas
        """
        pass
    
    @abstractmethod
    def actualizar(self, mesa: Mesa) -> Mesa:
        """
        Actualiza una mesa existente.
        
        Args:
            mesa: Mesa con datos actualizados
            
        Returns:
            Mesa: Mesa actualizada
            
        Raises:
            RepositorioExcepcion: Si la mesa no existe o hay error en actualización
        """
        pass
    
    @abstractmethod
    def eliminar(self, mesa_id: int) -> bool:
        """
        Elimina una mesa del sistema.
        
        Args:
            mesa_id: ID de la mesa a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            RepositorioExcepcion: Si la mesa no puede ser eliminada
        """
        pass
    
    # Consultas por estado
    @abstractmethod
    def obtener_por_estado(self, estado: EstadoMesa) -> List[Mesa]:
        """
        Obtiene todas las mesas con un estado específico.
        
        Args:
            estado: Estado de las mesas a buscar
            
        Returns:
            List[Mesa]: Lista de mesas con el estado especificado
        """
        pass
    
    @abstractmethod
    def obtener_libres(self) -> List[Mesa]:
        """
        Obtiene todas las mesas libres y activas.
        
        Returns:
            List[Mesa]: Lista de mesas disponibles
        """
        pass
    
    @abstractmethod
    def obtener_ocupadas(self) -> List[Mesa]:
        """
        Obtiene todas las mesas ocupadas.
        
        Returns:
            List[Mesa]: Lista de mesas ocupadas
        """
        pass
    
    @abstractmethod
    def obtener_reservadas(self) -> List[Mesa]:
        """
        Obtiene todas las mesas reservadas.
        
        Returns:
            List[Mesa]: Lista de mesas reservadas
        """
        pass
    
    # Consultas por capacidad y tipo
    @abstractmethod
    def obtener_por_capacidad(self, capacidad_minima: int, capacidad_maxima: Optional[int] = None) -> List[Mesa]:
        """
        Obtiene mesas por rango de capacidad.
        
        Args:
            capacidad_minima: Capacidad mínima requerida
            capacidad_maxima: Capacidad máxima (opcional)
            
        Returns:
            List[Mesa]: Lista de mesas que cumplen el criterio
        """
        pass
    
    @abstractmethod
    def obtener_por_tipo(self, tipo_mesa: TipoMesa) -> List[Mesa]:
        """
        Obtiene mesas por tipo.
        
        Args:
            tipo_mesa: Tipo de mesa a buscar
            
        Returns:
            List[Mesa]: Lista de mesas del tipo especificado
        """
        pass
    
    @abstractmethod
    def obtener_adecuadas_para(self, cantidad_personas: int) -> List[Mesa]:
        """
        Obtiene mesas adecuadas para una cantidad específica de personas.
        
        Args:
            cantidad_personas: Cantidad de personas
            
        Returns:
            List[Mesa]: Lista de mesas adecuadas y disponibles
        """
        pass
    
    # Consultas por ubicación
    @abstractmethod
    def obtener_por_ubicacion(self, ubicacion: str) -> List[Mesa]:
        """
        Obtiene mesas por ubicación.
        
        Args:
            ubicacion: Ubicación a buscar
            
        Returns:
            List[Mesa]: Lista de mesas en la ubicación especificada
        """
        pass
    
    # Consultas por cliente
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> Optional[Mesa]:
        """
        Obtiene la mesa actualmente ocupada por un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Mesa: Mesa ocupada por el cliente o None
        """
        pass
    
    @abstractmethod
    def obtener_historial_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de mesas utilizadas por un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            List[Dict]: Lista con información del historial
        """
        pass
    
    # Operaciones de ocupación y liberación
    @abstractmethod
    def ocupar_mesa(self, mesa_id: int, cliente_id: int, cantidad_personas: int, 
                   pedido_id: Optional[int] = None) -> Mesa:
        """
        Ocupa una mesa para un cliente.
        
        Args:
            mesa_id: ID de la mesa
            cliente_id: ID del cliente
            cantidad_personas: Cantidad de personas
            pedido_id: ID del pedido (opcional)
            
        Returns:
            Mesa: Mesa ocupada
            
        Raises:
            RepositorioExcepcion: Si la mesa no puede ser ocupada
        """
        pass
    
    @abstractmethod
    def liberar_mesa(self, mesa_id: int) -> Dict[str, Any]:
        """
        Libera una mesa ocupada.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Dict: Información sobre la liberación (tiempo de servicio, etc.)
            
        Raises:
            RepositorioExcepcion: Si la mesa no puede ser liberada
        """
        pass
    
    @abstractmethod
    def reservar_mesa(self, mesa_id: int, cliente_id: int) -> Mesa:
        """
        Reserva una mesa para un cliente.
        
        Args:
            mesa_id: ID de la mesa
            cliente_id: ID del cliente
            
        Returns:
            Mesa: Mesa reservada
            
        Raises:
            RepositorioExcepcion: Si la mesa no puede ser reservada
        """
        pass
    
    @abstractmethod
    def cancelar_reserva(self, mesa_id: int) -> Mesa:
        """
        Cancela la reserva de una mesa.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa: Mesa con reserva cancelada
            
        Raises:
            RepositorioExcepcion: Si la mesa no tiene reserva
        """
        pass
    
    # Gestión de estado
    @abstractmethod
    def marcar_en_limpieza(self, mesa_id: int) -> Mesa:
        """
        Marca una mesa como en limpieza.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa: Mesa marcada para limpieza
        """
        pass
    
    @abstractmethod
    def marcar_como_libre(self, mesa_id: int) -> Mesa:
        """
        Marca una mesa como libre después de limpieza.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa: Mesa marcada como libre
        """
        pass
    
    @abstractmethod
    def activar_mesa(self, mesa_id: int) -> Mesa:
        """
        Activa una mesa para servicio.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa: Mesa activada
        """
        pass
    
    @abstractmethod
    def desactivar_mesa(self, mesa_id: int, motivo: Optional[str] = None) -> Mesa:
        """
        Desactiva una mesa (fuera de servicio).
        
        Args:
            mesa_id: ID de la mesa
            motivo: Motivo de la desactivación
            
        Returns:
            Mesa: Mesa desactivada
        """
        pass
    
    # Estadísticas y métricas
    @abstractmethod
    def obtener_estadisticas_ocupacion(self, fecha_inicio: Optional[datetime] = None,
                                     fecha_fin: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Obtiene estadísticas de ocupación de mesas.
        
        Args:
            fecha_inicio: Fecha de inicio del período (opcional)
            fecha_fin: Fecha de fin del período (opcional)
            
        Returns:
            Dict: Estadísticas de ocupación
        """
        pass
    
    @abstractmethod
    def obtener_tiempo_promedio_por_mesa(self, mesa_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtiene tiempo promedio de servicio por mesa.
        
        Args:
            mesa_id: ID de mesa específica (opcional)
            
        Returns:
            Dict: Información de tiempos promedio
        """
        pass
    
    @abstractmethod
    def obtener_mesas_con_mayor_rotacion(self, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene las mesas con mayor rotación de clientes.
        
        Args:
            limite: Número máximo de mesas a retornar
            
        Returns:
            List[Dict]: Lista de mesas con estadísticas de rotación
        """
        pass
    
    @abstractmethod
    def obtener_mesas_excediendo_tiempo_promedio(self, margen_porcentaje: int = 20) -> List[Mesa]:
        """
        Obtiene mesas que están excediendo el tiempo promedio de servicio.
        
        Args:
            margen_porcentaje: Margen de tolerancia en porcentaje
            
        Returns:
            List[Mesa]: Lista de mesas excediendo tiempo
        """
        pass
    
    # Búsquedas y filtros avanzados
    @abstractmethod
    def buscar_mesas(self, filtros: Dict[str, Any]) -> List[Mesa]:
        """
        Busca mesas según múltiples criterios.
        
        Args:
            filtros: Diccionario con criterios de búsqueda
            
        Returns:
            List[Mesa]: Lista de mesas que cumplen los criterios
        """
        pass
    
    @abstractmethod
    def contar_mesas_por_estado(self) -> Dict[str, int]:
        """
        Cuenta mesas agrupadas por estado.
        
        Returns:
            Dict: Cantidad de mesas por cada estado
        """
        pass
    
    @abstractmethod
    def obtener_disponibilidad_por_horario(self, fecha: datetime) -> Dict[str, Any]:
        """
        Obtiene disponibilidad de mesas para una fecha/horario específico.
        
        Args:
            fecha: Fecha y hora a consultar
            
        Returns:
            Dict: Información de disponibilidad
        """
        pass
