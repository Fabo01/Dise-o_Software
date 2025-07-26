from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from Backend.Dominio.Entidades.Pedido_Entidad import PedidoEntidad, EstadoPedido, TipoPedido


class IPedidoRepositorio(ABC):
    """Interfaz para el repositorio de pedidos"""

    @abstractmethod
    def crear(self, pedido: PedidoEntidad) -> PedidoEntidad:
        """
        Crea un nuevo pedido en el repositorio
        
        Args:
            pedido: Entidad de pedido a crear
            
        Returns:
            PedidoEntidad: Pedido creado con ID asignado
            
        Raises:
            RepositorioExcepcion: Si hay error en la creación
        """
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[PedidoEntidad]:
        """
        Obtiene un pedido por su ID
        
        Args:
            id: ID del pedido a buscar
            
        Returns:
            PedidoEntidad o None si no existe
        """
        pass

    @abstractmethod
    def obtener_todos(self, limite: Optional[int] = None, desplazamiento: int = 0) -> List[PedidoEntidad]:
        """
        Obtiene todos los pedidos con paginación opcional
        
        Args:
            limite: Límite de resultados (None para sin límite)
            desplazamiento: Offset para paginación
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos
        """
        pass

    @abstractmethod
    def actualizar(self, pedido: PedidoEntidad) -> PedidoEntidad:
        """
        Actualiza un pedido existente
        
        Args:
            pedido: Entidad de pedido con datos actualizados
            
        Returns:
            PedidoEntidad: Pedido actualizado
            
        Raises:
            RepositorioExcepcion: Si el pedido no existe o hay error
        """
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina un pedido por su ID
        
        Args:
            id: ID del pedido a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        pass

    @abstractmethod
    def buscar_por_cliente(self, cliente_id: int) -> List[PedidoEntidad]:
        """
        Busca pedidos por ID de cliente
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos del cliente
        """
        pass

    @abstractmethod
    def buscar_por_estado(self, estado: EstadoPedido) -> List[PedidoEntidad]:
        """
        Busca pedidos por estado
        
        Args:
            estado: Estado de los pedidos a buscar
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos con el estado especificado
        """
        pass

    @abstractmethod
    def buscar_por_mesa(self, mesa_id: int) -> List[PedidoEntidad]:
        """
        Busca pedidos por ID de mesa
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos de la mesa
        """
        pass

    @abstractmethod
    def buscar_por_tipo(self, tipo_pedido: TipoPedido) -> List[PedidoEntidad]:
        """
        Busca pedidos por tipo
        
        Args:
            tipo_pedido: Tipo de pedido a buscar
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos del tipo especificado
        """
        pass

    @abstractmethod
    def buscar_por_fecha(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> List[PedidoEntidad]:
        """
        Busca pedidos por rango de fechas
        
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango (opcional, por defecto fecha_inicio)
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos en el rango de fechas
        """
        pass

    @abstractmethod
    def buscar_pendientes_por_tiempo(self, minutos_limite: int) -> List[PedidoEntidad]:
        """
        Busca pedidos que están atrasados según el tiempo límite
        
        Args:
            minutos_limite: Tiempo límite en minutos
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos atrasados
        """
        pass

    @abstractmethod
    def obtener_estadisticas_por_fecha(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> Dict[str, Any]:
        """
        Obtiene estadísticas de pedidos para un rango de fechas
        
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango (opcional)
            
        Returns:
            Dict con estadísticas:
            - total_pedidos: Número total de pedidos
            - total_ventas: Suma total de ventas
            - pedidos_por_estado: Conteo por estado
            - pedidos_por_tipo: Conteo por tipo
            - tiempo_promedio_preparacion: Tiempo promedio en minutos
        """
        pass

    @abstractmethod
    def obtener_ventas_por_periodo(self, fecha_inicio: date, fecha_fin: Optional[date] = None) -> Dict[str, float]:
        """
        Obtiene las ventas agrupadas por período
        
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango (opcional)
            
        Returns:
            Dict con ventas por fecha
        """
        pass

    @abstractmethod
    def contar_por_estado(self) -> Dict[str, int]:
        """
        Cuenta pedidos agrupados por estado
        
        Returns:
            Dict con conteo por estado
        """
        pass

    @abstractmethod
    def obtener_pedidos_activos(self) -> List[PedidoEntidad]:
        """
        Obtiene pedidos que están activos (no entregados ni cancelados)
        
        Returns:
            List[PedidoEntidad]: Lista de pedidos activos
        """
        pass

    @abstractmethod
    def obtener_historial_cliente(self, cliente_id: int, limite: Optional[int] = None) -> List[PedidoEntidad]:
        """
        Obtiene el historial de pedidos de un cliente
        
        Args:
            cliente_id: ID del cliente
            limite: Límite de resultados (opcional)
            
        Returns:
            List[PedidoEntidad]: Lista de pedidos del cliente ordenados por fecha
        """
        pass

    @abstractmethod
    def buscar_por_filtros(self, filtros: Dict[str, Any]) -> List[PedidoEntidad]:
        """
        Busca pedidos usando múltiples filtros
        
        Args:
            filtros: Diccionario con criterios de búsqueda:
                - cliente_id: ID del cliente
                - estado: Estado del pedido
                - tipo_pedido: Tipo de pedido
                - mesa_id: ID de la mesa
                - fecha_inicio: Fecha de inicio
                - fecha_fin: Fecha de fin
                - texto: Búsqueda en observaciones
                
        Returns:
            List[PedidoEntidad]: Lista de pedidos que cumplen los filtros
        """
        pass

    @abstractmethod
    def existe(self, id: int) -> bool:
        """
        Verifica si existe un pedido con el ID especificado
        
        Args:
            id: ID del pedido a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """
        Cuenta el total de pedidos en el repositorio
        
        Returns:
            int: Número total de pedidos
        """
        pass
