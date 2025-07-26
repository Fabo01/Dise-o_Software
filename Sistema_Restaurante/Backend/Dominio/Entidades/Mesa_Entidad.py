from datetime import datetime
from typing import Optional
from enum import Enum
from .EntidadBase import EntidadBase
from .Cliente_Entidad import ClienteEntidad
from ..Excepciones.DominioExcepcion import ValidacionExcepcion, OperacionInvalidaExcepcion


class EstadoMesa(Enum):
    """Estados posibles de una mesa"""
    LIBRE = "libre"
    OCUPADA = "ocupada"
    RESERVADA = "reservada"
    LIMPIEZA = "limpieza"
    FUERA_SERVICIO = "fuera_servicio"


class TipoMesa(Enum):
    """Tipos de mesa según capacidad y características"""
    INDIVIDUAL = "individual"      # 1-2 personas
    PEQUEÑA = "pequeña"           # 3-4 personas
    MEDIANA = "mediana"           # 5-6 personas
    GRANDE = "grande"             # 7-8 personas
    FAMILIAR = "familiar"         # 9+ personas
    VIP = "vip"                   # Mesa especial


class Mesa(EntidadBase):
    """
    Entidad que representa una mesa en el restaurante.
    """
    
    def __init__(self, numero: str, capacidad: int, tipo_mesa: TipoMesa, ubicacion: str = "", caracteristicas: str = ""):
        """
        Constructor para la entidad Mesa
        
        Args:
            numero (str): Número o identificador de la mesa
            capacidad (int): Cantidad máxima de personas que pueden sentarse
            tipo_mesa (TipoMesa): Tipo de mesa según capacidad
            ubicacion (str, opcional): Zona del restaurante donde está ubicada
            caracteristicas (str, opcional): Características especiales de la mesa
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        super().__init__()
        
        if not numero:
            raise ValidacionExcepcion("El número de mesa es obligatorio")
        if capacidad <= 0:
            raise ValidacionExcepcion("La capacidad debe ser mayor que cero")
        if capacidad > 20:
            raise ValidacionExcepcion("La capacidad no puede ser mayor a 20 personas")
        
        self._numero = numero
        self._capacidad = capacidad
        self._tipo_mesa = tipo_mesa
        self._ubicacion = ubicacion
        self._caracteristicas = caracteristicas
        self._estado = EstadoMesa.LIBRE  # Estado inicial
        self._cliente_actual = None
        self._hora_ocupacion = None
        self._cantidad_personas = 0
        self._activa = True
        self._tiempo_servicio_promedio = None  # en minutos
        self._pedido_id_actual = None
        
        self._validar_tipo_capacidad()
    
    def _validar_tipo_capacidad(self) -> None:
        """Valida que el tipo de mesa sea consistente con la capacidad"""
        rangos_capacidad = {
            TipoMesa.INDIVIDUAL: (1, 2),
            TipoMesa.PEQUEÑA: (3, 4),
            TipoMesa.MEDIANA: (5, 6),
            TipoMesa.GRANDE: (7, 8),
            TipoMesa.FAMILIAR: (9, 20),
            TipoMesa.VIP: (1, 20)  # VIP puede tener cualquier capacidad
        }
        
        min_cap, max_cap = rangos_capacidad[self._tipo_mesa]
        if not (min_cap <= self._capacidad <= max_cap):
            raise ValidacionExcepcion(
                f"Una mesa {self._tipo_mesa.value} debe tener entre {min_cap} y {max_cap} personas"
            )
    
    # Getters
    @property
    def numero(self):
        return self._numero
    
    @property
    def capacidad(self):
        return self._capacidad
    
    @property
    def tipo_mesa(self):
        return self._tipo_mesa
    
    @property
    def ubicacion(self):
        return self._ubicacion
    
    @property
    def caracteristicas(self):
        return self._caracteristicas
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def cliente_actual(self) -> Optional[ClienteEntidad]:
        return self._cliente_actual
    
    @property
    def hora_ocupacion(self) -> Optional[datetime]:
        return self._hora_ocupacion
    
    @property
    def cantidad_personas(self):
        return self._cantidad_personas
    
    @property
    def activa(self):
        return self._activa
    
    @property
    def tiempo_servicio_promedio(self):
        return self._tiempo_servicio_promedio
    
    @property
    def pedido_id_actual(self):
        return self._pedido_id_actual
    
    @property
    def esta_libre(self) -> bool:
        """Determina si la mesa está libre para ser ocupada"""
        return self._estado == EstadoMesa.LIBRE and self._activa
    
    @property
    def esta_ocupada(self) -> bool:
        """Determina si la mesa está ocupada"""
        return self._estado == EstadoMesa.OCUPADA
    
    @property
    def puede_reservarse(self) -> bool:
        """Determina si la mesa puede ser reservada"""
        return self._estado == EstadoMesa.LIBRE and self._activa
    
    @property
    def tiempo_ocupacion(self) -> Optional[int]:
        """
        Calcula el tiempo que lleva ocupada la mesa en minutos
        
        Returns:
            int: Tiempo en minutos, None si la mesa no está ocupada
        """
        if self._estado != "ocupada" or self._hora_ocupacion is None:
            return None
            
        tiempo = datetime.now() - self._hora_ocupacion
        return int(tiempo.total_seconds() / 60)
    
    # Métodos de negocio
    def ocupar(self, cliente: ClienteEntidad, cantidad_personas: int, pedido_id: Optional[int] = None):
        """
        Marca la mesa como ocupada con un cliente
        
        Args:
            cliente (Cliente): Cliente que ocupará la mesa
            cantidad_personas (int): Cantidad de personas en la mesa
            pedido_id (int, opcional): ID del pedido asociado
            
        Raises:
            ValidacionExcepcion: Si los datos no son válidos
            OperacionInvalidaExcepcion: Si la mesa no está libre o reservada
        """
        if not cliente:
            raise ValidacionExcepcion("El cliente es obligatorio")
        if cantidad_personas <= 0:
            raise ValidacionExcepcion("La cantidad de personas debe ser mayor que cero")
        if cantidad_personas > self._capacidad:
            raise ValidacionExcepcion(f"La mesa solo tiene capacidad para {self._capacidad} personas")
        if not self.esta_libre and self._estado != EstadoMesa.RESERVADA:
            raise OperacionInvalidaExcepcion(f"No se puede ocupar una mesa en estado: {self._estado.value}")
        if not self._activa:
            raise OperacionInvalidaExcepcion("No se puede ocupar una mesa inactiva")
        
        self._estado = EstadoMesa.OCUPADA
        self._cliente_actual = cliente
        self._cantidad_personas = cantidad_personas
        self._hora_ocupacion = datetime.now()
        self._pedido_id_actual = pedido_id
        self.actualizar_fecha()
    
    def liberar(self, actualizar_tiempo_promedio: bool = True) -> int:
        """
        Marca la mesa como libre y calcula tiempo de servicio
        
        Args:
            actualizar_tiempo_promedio: Si debe actualizar el tiempo promedio
            
        Returns:
            int: Tiempo de servicio en minutos
            
        Raises:
            OperacionInvalidaExcepcion: Si la mesa no está ocupada o reservada
        """
        if self._estado not in [EstadoMesa.OCUPADA, EstadoMesa.RESERVADA]:
            raise OperacionInvalidaExcepcion(f"No se puede liberar una mesa en estado: {self._estado.value}")
        
        tiempo_servicio = 0
        if self._estado == EstadoMesa.OCUPADA and self._hora_ocupacion:
            tiempo_servicio = int((datetime.now() - self._hora_ocupacion).total_seconds() / 60)
            
            # Actualizar tiempo promedio si se solicita
            if actualizar_tiempo_promedio:
                if self._tiempo_servicio_promedio is None:
                    self._tiempo_servicio_promedio = tiempo_servicio
                else:
                    # Promedio ponderado (70% histórico, 30% actual)
                    self._tiempo_servicio_promedio = int(
                        (self._tiempo_servicio_promedio * 0.7) + (tiempo_servicio * 0.3)
                    )
        
        self._estado = EstadoMesa.LIMPIEZA  # Requiere limpieza antes de estar libre
        self._cliente_actual = None
        self._hora_ocupacion = None
        self._cantidad_personas = 0
        self._pedido_id_actual = None
        self.actualizar_fecha()
        
        return tiempo_servicio
    
    def reservar(self, cliente: ClienteEntidad):
        """
        Marca la mesa como reservada
        
        Args:
            cliente (Cliente): Cliente que reserva la mesa
            
        Raises:
            ValidacionExcepcion: Si el cliente no es válido
            OperacionInvalidaExcepcion: Si la mesa no está libre
        """
        if not cliente:
            raise ValidacionExcepcion("El cliente es obligatorio")
        if not self.puede_reservarse:
            raise OperacionInvalidaExcepcion(f"No se puede reservar una mesa en estado: {self._estado.value}")
        
        self._estado = EstadoMesa.RESERVADA
        self._cliente_actual = cliente
        self.actualizar_fecha()
    
    def cancelar_reserva(self):
        """
        Cancela la reserva de la mesa
        
        Raises:
            OperacionInvalidaExcepcion: Si la mesa no está reservada
        """
        if self._estado != EstadoMesa.RESERVADA:
            raise OperacionInvalidaExcepcion(f"La mesa no está reservada")
        
        self._estado = EstadoMesa.LIBRE
        self._cliente_actual = None
        self.actualizar_fecha()
    
    def marcar_en_limpieza(self):
        """
        Marca la mesa como en limpieza
        
        Raises:
            OperacionInvalidaExcepcion: Si la mesa está ocupada
        """
        if self._estado == EstadoMesa.OCUPADA:
            raise OperacionInvalidaExcepcion("No se puede marcar para limpieza una mesa ocupada")
        
        self._estado = EstadoMesa.LIMPIEZA
        self._cliente_actual = None
        self._hora_ocupacion = None
        self._cantidad_personas = 0
        self._pedido_id_actual = None
        self.actualizar_fecha()
    
    def marcar_como_libre(self):
        """
        Marca la mesa como libre después de limpieza
        
        Raises:
            OperacionInvalidaExcepcion: Si la mesa no está en limpieza
        """
        if self._estado != EstadoMesa.LIMPIEZA:
            raise OperacionInvalidaExcepcion("La mesa debe estar en limpieza para marcarla como libre")
        
        self._estado = EstadoMesa.LIBRE
        self.actualizar_fecha()
    
    def activar_mesa(self):
        """Activa la mesa para servicio"""
        self._activa = True
        if self._estado == EstadoMesa.FUERA_SERVICIO:
            self._estado = EstadoMesa.LIBRE
        self.actualizar_fecha()
    
    def desactivar_mesa(self, motivo: Optional[str] = None):
        """
        Desactiva la mesa (fuera de servicio)
        
        Args:
            motivo: Motivo de la desactivación (opcional)
            
        Raises:
            OperacionInvalidaExcepcion: Si la mesa está ocupada
        """
        if self.esta_ocupada:
            raise OperacionInvalidaExcepcion("No se puede desactivar una mesa ocupada")
        
        self._activa = False
        self._estado = EstadoMesa.FUERA_SERVICIO
        self._cliente_actual = None
        self._pedido_id_actual = None
        
        if motivo:
            self._caracteristicas = f"Fuera de servicio: {motivo}"
        
        self.actualizar_fecha()
    
    def asignar_pedido(self, pedido_id: int):
        """
        Asigna un pedido a la mesa
        
        Args:
            pedido_id: ID del pedido a asignar
            
        Raises:
            OperacionInvalidaExcepcion: Si la mesa no está ocupada
        """
        if not self.esta_ocupada:
            raise OperacionInvalidaExcepcion("La mesa debe estar ocupada para asignar un pedido")
        
        self._pedido_id_actual = pedido_id
        self.actualizar_fecha()
    
    def obtener_tiempo_ocupacion_actual(self) -> Optional[int]:
        """
        Obtiene el tiempo actual de ocupación en minutos
        
        Returns:
            int: Tiempo de ocupación en minutos, None si no está ocupada
        """
        if not self.esta_ocupada or not self._hora_ocupacion:
            return None

        tiempo_ocupacion = datetime.now() - self._hora_ocupacion
        return int(tiempo_ocupacion.total_seconds() / 60)
    
    def esta_excediendo_tiempo_promedio(self, margen_porcentaje: int = 20) -> bool:
        """
        Determina si la mesa está excediendo el tiempo promedio de servicio
        
        Args:
            margen_porcentaje: Margen de tolerancia en porcentaje
            
        Returns:
            bool: True si está excediendo el tiempo promedio
        """
        if not self.esta_ocupada or not self._tiempo_servicio_promedio:
            return False

        tiempo_actual = self.obtener_tiempo_ocupacion_actual()
        if not tiempo_actual:
            return False

        tiempo_limite = self._tiempo_servicio_promedio * (1 + margen_porcentaje / 100)
        return tiempo_actual > tiempo_limite
    
    def es_adecuada_para(self, cantidad_personas: int) -> bool:
        """
        Verifica si la mesa es adecuada para una cantidad de personas
        
        Args:
            cantidad_personas (int): Cantidad de personas a ubicar
            
        Returns:
            bool: True si la mesa es adecuada, False en caso contrario
        """
        # Una mesa es adecuada si tiene capacidad suficiente sin desperdiciar demasiado espacio
        # La heurística es: capacidad >= cantidad_personas y capacidad <= cantidad_personas + 2
        return (self._capacidad >= cantidad_personas and self._capacidad <= cantidad_personas + 2)
    
    def obtener_resumen_estado(self) -> str:
        """Retorna un resumen del estado actual de la mesa"""
        estado_base = f"Mesa {self._numero} ({self._capacidad} personas) - {self._estado.value}"
        
        if self.esta_ocupada and self._hora_ocupacion:
            tiempo_ocupacion = self.obtener_tiempo_ocupacion_actual()
            estado_base += f" - {tiempo_ocupacion} min"
        
        if not self._activa:
            estado_base += " - INACTIVA"
            
        return estado_base
    
    def __str__(self):
        return f"Mesa {self._numero} ({self._capacidad} personas) - {self._estado.value}"
