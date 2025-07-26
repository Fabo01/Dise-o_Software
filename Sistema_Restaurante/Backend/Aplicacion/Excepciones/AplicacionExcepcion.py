class AplicacionExcepcion(Exception):
    """
    Clase base para excepciones de la capa de aplicación.
    """
    def __init__(self, message: str, codigo: str = None):
        """
        Constructor de la excepción de aplicación.
        
        Args:
            message (str): Mensaje de error
            codigo (str, opcional): Código de error específico
        """
        super().__init__(message)
        self.message = message
        self.codigo = codigo


class ServicioExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando ocurre un error en un servicio de aplicación.
    """
    pass


class EntidadNoEncontradaExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando no se encuentra una entidad solicitada.
    """
    def __init__(self, entidad: str, identificador: str):
        """
        Constructor para entidad no encontrada.
        
        Args:
            entidad (str): Tipo de entidad
            identificador (str): Identificador de la entidad
        """
        message = f"No se encontró {entidad} con identificador: {identificador}"
        super().__init__(message, "ENTIDAD_NO_ENCONTRADA")
        self.entidad = entidad
        self.identificador = identificador


class ConflictoExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando hay un conflicto en la operación (ej: duplicados).
    """
    pass


class AutorizacionExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando el usuario no tiene permisos para realizar una operación.
    """
    pass


class ValidacionAplicacionExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando fallan las validaciones a nivel de aplicación.
    """
    def __init__(self, errores: dict):
        """
        Constructor para errores de validación.
        
        Args:
            errores (dict): Diccionario con los errores de validación
        """
        message = "Errores de validación en la aplicación"
        super().__init__(message, "VALIDACION_APLICACION")
        self.errores = errores


class RecursoNoDisponibleExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando un recurso no está disponible.
    """
    pass


class OperacionNoPermitidaExcepcion(AplicacionExcepcion):
    """
    Excepción lanzada cuando se intenta realizar una operación no permitida.
    """
    pass
