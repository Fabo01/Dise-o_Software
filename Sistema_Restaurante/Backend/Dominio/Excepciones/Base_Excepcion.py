"""
Excepción base para el dominio.
Define la excepción raíz de todas las excepciones de dominio.
"""


class DominioExcepcion(Exception):
    """
    Excepción base para errores de dominio.
    
    Todas las excepciones específicas del dominio deben heredar de esta clase.
    """
    
    def __init__(self, mensaje: str = "Error en el dominio"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class ValidacionExcepcion(DominioExcepcion):
    """Excepción para errores de validación de datos."""
    
    def __init__(self, mensaje: str = "Error de validación"):
        super().__init__(mensaje)


class ReglaDeNegocioExcepcion(DominioExcepcion):
    """Excepción para violaciones de reglas de negocio."""
    
    def __init__(self, mensaje: str = "Violación de regla de negocio"):
        super().__init__(mensaje)


class EntidadNoEncontradaExcepcion(DominioExcepcion):
    """Excepción para cuando una entidad no se encuentra."""
    
    def __init__(self, mensaje: str = "Entidad no encontrada"):
        super().__init__(mensaje)


class ConflictoExcepcion(DominioExcepcion):
    """Excepción para conflictos de integridad de datos."""
    
    def __init__(self, mensaje: str = "Conflicto de datos"):
        super().__init__(mensaje)
