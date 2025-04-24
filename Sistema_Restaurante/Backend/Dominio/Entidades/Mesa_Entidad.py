from datetime import datetime
from typing import Optional
from .EntidadBase import EntidadBase
from .Cliente_Entidad import Cliente
from ..Excepciones.DominioExcepcion import ValidacionExcepcion, OperacionInvalidaExcepcion

class Mesa(EntidadBase):
    """
    Entidad que representa una mesa en el restaurante.
    """
    
    # Estados posibles para una mesa
    ESTADOS = ["libre", "ocupada", "reservada", "en_limpieza"]
    
    def __init__(self, numero: str, capacidad: int, ubicacion: str = "", caracteristicas: str = ""):
        """
        Constructor para la entidad Mesa
        
        Args:
            numero (str): Número o identificador de la mesa
            capacidad (int): Cantidad máxima de personas que pueden sentarse
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
        
        self._numero = numero
        self._capacidad = capacidad
        self._ubicacion = ubicacion
        self._caracteristicas = caracteristicas
        self._estado = "libre"  # Estado inicial
        self._cliente_actual = None
        self._hora_ocupacion = None
        self._cantidad_personas = 0
    
    # Getters
    @property
    def numero(self):
        return self._numero
    
    @property
    def capacidad(self):
        return self._capacidad
    
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
    def cliente_actual(self) -> Optional[Cliente]:
        return self._cliente_actual
    
    @property
    def hora_ocupacion(self) -> Optional[datetime]:
        return self._hora_ocupacion
    
    @property
    def cantidad_personas(self):
        return self._cantidad_personas
    
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
    def ocupar(self, cliente: Cliente, cantidad_personas: int):
        """
        Marca la mesa como ocupada con un cliente
        
        Args:
            cliente (Cliente): Cliente que ocupará la mesa
            cantidad_personas (int): Cantidad de personas en la mesa
            
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
        if self._estado not in ["libre", "reservada"]:
            raise OperacionInvalidaExcepcion(f"No se puede ocupar una mesa en estado: {self._estado}")
        
        self._estado = "ocupada"
        self._cliente_actual = cliente
        self._cantidad_personas = cantidad_personas
        self._hora_ocupacion = datetime.now()
        self.actualizar_fecha()
    
    def liberar(self):
        """
        Marca la mesa como libre
        
        Raises:
            OperacionInvalidaExcepcion: Si la mesa no está ocupada o reservada
        """
        if self._estado not in ["ocupada", "reservada"]:
            raise OperacionInvalidaExcepcion(f"No se puede liberar una mesa en estado: {self._estado}")
        
        self._estado = "libre"
        self._cliente_actual = None
        self._hora_ocupacion = None
        self._cantidad_personas = 0
        self.actualizar_fecha()
    
    def reservar(self, cliente: Cliente):
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
        if self._estado != "libre":
            raise OperacionInvalidaExcepcion(f"No se puede reservar una mesa en estado: {self._estado}")
        
        self._estado = "reservada"
        self._cliente_actual = cliente
        self.actualizar_fecha()
    
    def marcar_en_limpieza(self):
        """
        Marca la mesa como en limpieza
        
        Raises:
            OperacionInvalidaExcepcion: Si la mesa no está libre u ocupada
        """
        if self._estado not in ["libre", "ocupada"]:
            raise OperacionInvalidaExcepcion(f"No se puede marcar para limpieza una mesa en estado: {self._estado}")
        
        self._estado = "en_limpieza"
        self._cliente_actual = None
        self._hora_ocupacion = None
        self._cantidad_personas = 0
        self.actualizar_fecha()
    
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
        return (self._capacidad >= cantidad_personas and 
                self._capacidad <= cantidad_personas + 2)
    
    def __str__(self):
        return f"Mesa {self._numero} ({self._capacidad} personas) - {self._estado}"
