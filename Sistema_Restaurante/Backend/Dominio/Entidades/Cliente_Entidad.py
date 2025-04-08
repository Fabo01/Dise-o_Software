from datetime import datetime

class ClienteEntidad:
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
        """
        if not nombre:
            raise ValueError("El nombre del cliente es obligatorio")
        if not self._validar_rut(rut):
            raise ValueError(f"RUT inválido: {rut}")
            
        self.id = None
        self.nombre = nombre
        self.correo = correo
        self.rut = rut
        self.telefono = telefono
        self.direccion = direccion
        self.estado = "activo"
        self.fecha_registro = datetime.now()
        self.ultima_visita = datetime.now()

    def _validar_rut(self, rut):
        """
        Valida que el RUT tenga un formato correcto.
        
        Args:
            rut (str): RUT a validar
            
        Returns:
            bool: True si el RUT es válido, False en caso contrario
        """
        if not rut or len(rut) < 8 or len(rut) > 10:
            return False
        return '-' in rut
            
    def desactivar(self):
        """Desactiva al cliente"""
        self.estado = "inactivo"
        
    def activar(self):
        """Activa al cliente"""
        self.estado = "activo"
            
    def actualizar_datos(self, nombre, correo, telefono=None, direccion=None):
        """
        Actualiza los datos del cliente
        
        Args:
            nombre (str): Nuevo nombre
            correo (str): Nuevo correo
            telefono (str, opcional): Nuevo teléfono
            direccion (str, opcional): Nueva dirección
        """
        if not nombre:
            raise ValueError("El nombre es obligatorio")
        
        self.nombre = nombre
        self.correo = correo
        
        if telefono is not None:
            self.telefono = telefono
        
        if direccion is not None:
            self.direccion = direccion
    
    def registrar_visita(self, fecha=None):
        """
        Registra una nueva visita del cliente
        
        Args:
            fecha (datetime, opcional): Fecha de la visita. Si es None, se usa la fecha actual.
        """
        if fecha is None:
            fecha = datetime.now()
        self.ultima_visita = fecha

    def __str__(self):
        return f"{self.nombre} ({self.rut})"