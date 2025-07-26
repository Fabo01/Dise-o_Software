"""
Servicio de aplicación para la gestión de Mesas.
Implementa la lógica de negocio y orquesta las operaciones entre repositorios.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from Backend.Dominio.Entidades.Mesa_Entidad import Mesa
from Backend.Dominio.Interfaces.Mesa_Repositorio_Interface import MesaRepositorioInterface
from Backend.Infraestructura.Repositorios.Mesa_Repositorio import MesaRepositorio
from Backend.Aplicacion.DTOs.Mesa_DTO import (
    MesaDTO, 
    CrearMesaDTO, 
    ActualizarMesaDTO,
    EstadisticasMesasDTO
)
from Backend.Dominio.Excepciones.Mesa_Excepciones import (
    MesaNoEncontradaExcepcion,
    MesaEstadoInvalidoExcepcion,
    MesaOcupadaExcepcion,
    NumeroMesaDuplicadoExcepcion
)


class MesaServicio:
    """
    Servicio de aplicación para mesas.
    Maneja la lógica de negocio y coordina operaciones de mesas.
    """
    
    def __init__(self, mesa_repositorio: Optional[MesaRepositorioInterface] = None):
        self.mesa_repositorio = mesa_repositorio or MesaRepositorio()
    
    def obtener_todas_las_mesas(self, filtros: Optional[Dict[str, Any]] = None) -> List[Mesa]:
        """
        Obtiene todas las mesas con filtros opcionales.
        
        Args:
            filtros: Diccionario con filtros a aplicar
            
        Returns:
            Lista de mesas
        """
        if filtros is None:
            filtros = {}
            
        return self.mesa_repositorio.obtener_todas(filtros)
    
    def obtener_mesa_por_id(self, mesa_id: int) -> Mesa:
        """
        Obtiene una mesa por su ID.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa encontrada
            
        Raises:
            MesaNoEncontradaExcepcion: Si la mesa no existe
        """
        mesa = self.mesa_repositorio.obtener_por_id(mesa_id)
        if not mesa:
            raise MesaNoEncontradaExcepcion(f"Mesa con ID {mesa_id} no encontrada")
        return mesa
    
    def obtener_mesa_por_numero(self, numero: int) -> Optional[Mesa]:
        """
        Obtiene una mesa por su número.
        
        Args:
            numero: Número de la mesa
            
        Returns:
            Mesa encontrada o None si no existe
        """
        return self.mesa_repositorio.obtener_por_numero(numero)
    
    def crear_mesa(self, crear_mesa_dto: CrearMesaDTO) -> Mesa:
        """
        Crea una nueva mesa.
        
        Args:
            crear_mesa_dto: DTO con datos para crear la mesa
            
        Returns:
            Mesa creada
            
        Raises:
            NumeroMesaDuplicadoExcepcion: Si ya existe una mesa con ese número
        """
        # Validar que no exista una mesa con el mismo número
        mesa_existente = self.obtener_mesa_por_numero(crear_mesa_dto.numero)
        if mesa_existente:
            raise NumeroMesaDuplicadoExcepcion(
                f"Ya existe una mesa con el número {crear_mesa_dto.numero}"
            )
        
        # Validar capacidad
        if crear_mesa_dto.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        
        # Validar estado
        estados_validos = ['disponible', 'ocupada', 'reservada', 'fuera_servicio']
        if crear_mesa_dto.estado not in estados_validos:
            raise MesaEstadoInvalidoExcepcion(
                f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
            )
        
        # Crear entidad Mesa
        mesa = Mesa(
            numero=crear_mesa_dto.numero,
            capacidad=crear_mesa_dto.capacidad,
            estado=crear_mesa_dto.estado,
            ubicacion=crear_mesa_dto.ubicacion,
            observaciones=crear_mesa_dto.observaciones
        )
        
        return self.mesa_repositorio.crear(mesa)
    
    def actualizar_mesa(self, mesa_id: int, actualizar_mesa_dto: ActualizarMesaDTO) -> Mesa:
        """
        Actualiza una mesa existente.
        
        Args:
            mesa_id: ID de la mesa a actualizar
            actualizar_mesa_dto: DTO con datos a actualizar
            
        Returns:
            Mesa actualizada
            
        Raises:
            MesaNoEncontradaExcepcion: Si la mesa no existe
            NumeroMesaDuplicadoExcepcion: Si el nuevo número ya existe
        """
        mesa = self.obtener_mesa_por_id(mesa_id)
        
        # Validar número único si se está cambiando
        if (actualizar_mesa_dto.numero is not None and 
            actualizar_mesa_dto.numero != mesa.numero):
            mesa_existente = self.obtener_mesa_por_numero(actualizar_mesa_dto.numero)
            if mesa_existente:
                raise NumeroMesaDuplicadoExcepcion(
                    f"Ya existe una mesa con el número {actualizar_mesa_dto.numero}"
                )
        
        # Validar capacidad si se está cambiando
        if (actualizar_mesa_dto.capacidad is not None and 
            actualizar_mesa_dto.capacidad <= 0):
            raise ValueError("La capacidad debe ser mayor a 0")
        
        # Validar estado si se está cambiando
        if actualizar_mesa_dto.estado is not None:
            estados_validos = ['disponible', 'ocupada', 'reservada', 'fuera_servicio']
            if actualizar_mesa_dto.estado not in estados_validos:
                raise MesaEstadoInvalidoExcepcion(
                    f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
                )
        
        # Actualizar campos que no son None
        if actualizar_mesa_dto.numero is not None:
            mesa.numero = actualizar_mesa_dto.numero
        if actualizar_mesa_dto.capacidad is not None:
            mesa.capacidad = actualizar_mesa_dto.capacidad
        if actualizar_mesa_dto.estado is not None:
            mesa.estado = actualizar_mesa_dto.estado
        if actualizar_mesa_dto.ubicacion is not None:
            mesa.ubicacion = actualizar_mesa_dto.ubicacion
        if actualizar_mesa_dto.observaciones is not None:
            mesa.observaciones = actualizar_mesa_dto.observaciones
        
        return self.mesa_repositorio.actualizar(mesa)
    
    def eliminar_mesa(self, mesa_id: int) -> bool:
        """
        Elimina una mesa.
        
        Args:
            mesa_id: ID de la mesa a eliminar
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            MesaNoEncontradaExcepcion: Si la mesa no existe
            MesaOcupadaExcepcion: Si la mesa está ocupada
        """
        mesa = self.obtener_mesa_por_id(mesa_id)
        
        # No permitir eliminar mesas ocupadas
        if mesa.estado == 'ocupada':
            raise MesaOcupadaExcepcion("No se puede eliminar una mesa ocupada")
        
        return self.mesa_repositorio.eliminar(mesa_id)
    
    def cambiar_estado_mesa(self, mesa_id: int, nuevo_estado: str) -> Mesa:
        """
        Cambia el estado de una mesa.
        
        Args:
            mesa_id: ID de la mesa
            nuevo_estado: Nuevo estado de la mesa
            
        Returns:
            Mesa con estado actualizado
            
        Raises:
            MesaNoEncontradaExcepcion: Si la mesa no existe
            MesaEstadoInvalidoExcepcion: Si el estado es inválido
        """
        mesa = self.obtener_mesa_por_id(mesa_id)
        
        estados_validos = ['disponible', 'ocupada', 'reservada', 'fuera_servicio']
        if nuevo_estado not in estados_validos:
            raise MesaEstadoInvalidoExcepcion(
                f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
            )
        
        # Validaciones de transición de estado
        if mesa.estado == 'ocupada' and nuevo_estado == 'disponible':
            # Permitir liberar mesa ocupada
            pass
        elif mesa.estado == 'disponible' and nuevo_estado in ['ocupada', 'reservada']:
            # Permitir ocupar o reservar mesa disponible
            pass
        elif nuevo_estado == 'fuera_servicio':
            # Siempre permitir poner fuera de servicio
            pass
        elif mesa.estado == 'fuera_servicio' and nuevo_estado == 'disponible':
            # Permitir volver a servicio
            pass
        
        mesa.estado = nuevo_estado
        return self.mesa_repositorio.actualizar(mesa)
    
    def obtener_mesas_disponibles(self, capacidad_min: Optional[int] = None) -> List[Mesa]:
        """
        Obtiene todas las mesas disponibles.
        
        Args:
            capacidad_min: Capacidad mínima requerida
            
        Returns:
            Lista de mesas disponibles
        """
        filtros = {'estado': 'disponible'}
        if capacidad_min:
            filtros['capacidad_min'] = capacidad_min
            
        return self.mesa_repositorio.obtener_todas(filtros)
    
    def obtener_mesas_ocupadas(self) -> List[Mesa]:
        """
        Obtiene todas las mesas ocupadas.
        
        Returns:
            Lista de mesas ocupadas
        """
        return self.mesa_repositorio.obtener_todas({'estado': 'ocupada'})
    
    def obtener_estadisticas_mesas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de ocupación de mesas.
        
        Returns:
            Diccionario con estadísticas
        """
        todas_las_mesas = self.obtener_todas_las_mesas()
        
        total_mesas = len(todas_las_mesas)
        mesas_disponibles = len([m for m in todas_las_mesas if m.estado == 'disponible'])
        mesas_ocupadas = len([m for m in todas_las_mesas if m.estado == 'ocupada'])
        mesas_reservadas = len([m for m in todas_las_mesas if m.estado == 'reservada'])
        mesas_fuera_servicio = len([m for m in todas_las_mesas if m.estado == 'fuera_servicio'])
        
        capacidad_total = sum(mesa.capacidad for mesa in todas_las_mesas)
        capacidad_disponible = sum(
            mesa.capacidad for mesa in todas_las_mesas 
            if mesa.estado == 'disponible'
        )
        
        porcentaje_ocupacion = (mesas_ocupadas / total_mesas * 100) if total_mesas > 0 else 0
        
        return {
            'total_mesas': total_mesas,
            'mesas_disponibles': mesas_disponibles,
            'mesas_ocupadas': mesas_ocupadas,
            'mesas_reservadas': mesas_reservadas,
            'mesas_fuera_servicio': mesas_fuera_servicio,
            'porcentaje_ocupacion': round(porcentaje_ocupacion, 2),
            'capacidad_total': capacidad_total,
            'capacidad_disponible': capacidad_disponible
        }
    
    def asignar_pedido_a_mesa(self, mesa_id: int, pedido_id: int) -> Mesa:
        """
        Asigna un pedido a una mesa y la marca como ocupada.
        
        Args:
            mesa_id: ID de la mesa
            pedido_id: ID del pedido
            
        Returns:
            Mesa actualizada
            
        Raises:
            MesaNoEncontradaExcepcion: Si la mesa no existe
            MesaOcupadaExcepcion: Si la mesa ya está ocupada
        """
        mesa = self.obtener_mesa_por_id(mesa_id)
        
        if mesa.estado != 'disponible':
            raise MesaOcupadaExcepcion("La mesa no está disponible para asignar un pedido")
        
        # Cambiar estado a ocupada
        mesa.estado = 'ocupada'
        return self.mesa_repositorio.actualizar(mesa)
    
    def liberar_mesa(self, mesa_id: int) -> Mesa:
        """
        Libera una mesa marcándola como disponible.
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            Mesa liberada
            
        Raises:
            MesaNoEncontradaExcepcion: Si la mesa no existe
        """
        mesa = self.obtener_mesa_por_id(mesa_id)
        mesa.estado = 'disponible'
        return self.mesa_repositorio.actualizar(mesa)
    
    def buscar_mesas_por_capacidad(self, capacidad: int, disponible_solo: bool = True) -> List[Mesa]:
        """
        Busca mesas por capacidad específica.
        
        Args:
            capacidad: Capacidad requerida
            disponible_solo: Si solo buscar en mesas disponibles
            
        Returns:
            Lista de mesas que cumplen el criterio
        """
        filtros = {'capacidad': capacidad}
        if disponible_solo:
            filtros['estado'] = 'disponible'
            
        return self.mesa_repositorio.obtener_todas(filtros)
