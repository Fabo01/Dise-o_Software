from datetime import datetime
from .EntidadBase import EntidadBase
from ..Objetos_Valor.Correo_VO import CorreoVO
from ..Objetos_Valor.RutVO import RutVO
from ..Objetos_Valor.TelefonoVO import TelefonoVO
from ..Excepciones.DominioExcepcion import ValidacionExcepcion

class ClienteEntidad(EntidadBase):
    """
    Entidad de dominio que representa un cliente del restaurante.
    Contiene las reglas de negocio y validaciones.
    """
    def __init__(self, nombre, correo, rut, telefono="", direccion=""):
        """
        Constructor de la entidad Cliente.
        
        Args:
            nombre (str): Nombre del cliente, no puede ser vacío
            correo (str): Correo del cliente, debe ser válido
            rut (str): RUT del cliente, debe tener un formato válido
            telefono (str, opcional): Teléfono del cliente
            direccion (str, opcional): Dirección del cliente
            estado (str, opcional): Estado del cliente, por defecto "activo"
            ultima_visita (str): Fecha de la ultima visita del cliente
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        super().__init__()
        
        if not nombre:
            raise ValidacionExcepcion("El nombre del cliente es obligatorio")
        
        self._nombre = nombre
        self._direccion = direccion
        self._ultima_visita = datetime.now()
        self._estado = "activo"  # Estado inicial
        
        # Usar objetos de valor para validación y encapsulación
        try:
            self._correo = CorreoVO(correo)
            self._rut = RutVO(rut)  # RUT como objeto de valor, inmutable
            self._telefono = TelefonoVO(telefono)
        except Exception as e:
            raise ValidacionExcepcion(str(e))

    # Getters
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def correo(self):
        return self._correo.valor
    
    @property
    def rut(self):
        return self._rut.valor
    
    @property
    def telefono(self):
        return self._telefono.valor
    
    @property
    def direccion(self):
        return self._direccion
    
    @property
    def ultima_visita(self):
        return self._ultima_visita
    
    @ultima_visita.setter
    def ultima_visita(self, valor):
        self._ultima_visita = valor
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        self._estado = valor
    
    # Métodos de negocio
    def actualizar_datos(self, nombre, correo, telefono=None, direccion=None):
        """
        Actualiza los datos del cliente
        
        Args:
            nombre (str): Nuevo nombre
            correo (str): Nuevo correo
            telefono (str, opcional): Nuevo teléfono
            direccion (str, opcional): Nueva dirección
            
        Raises:
            ValidacionExcepcion: Si los datos proporcionados no son válidos
        """
        if not nombre:
            raise ValidacionExcepcion("El nombre es obligatorio")
        
        self._nombre = nombre
        
        try:
            # Permitir que 'correo' sea str o CorreoVO
            if isinstance(correo, CorreoVO):
                correo_valor = correo.valor
            else:
                correo_valor = correo
            self._correo = CorreoVO(correo_valor)
            
            if telefono is not None:
                self._telefono = TelefonoVO(telefono)
            
            if direccion is not None:
                self._direccion = direccion
                
            self.actualizar_fecha()
        except ValueError as e:
            raise ValidacionExcepcion(str(e))
    
    def registrar_visita(self, fecha=None):
        """
        Registra una nueva visita del cliente
        
        Args:
            fecha (datetime, opcional): Fecha de la visita. Si es None, se usa la fecha actual.
        """
        if fecha is None:
            fecha = datetime.now()
        self._ultima_visita = fecha
        self.actualizar_fecha()

    def __str__(self):
        return f"{self._nombre} ({self._rut})"