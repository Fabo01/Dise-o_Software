class DominioExcepcion(Exception):
    """Clase base para excepciones del dominio."""
    pass

class ValidacionExcepcion(DominioExcepcion):
    """Excepción lanzada cuando falla la validación de una entidad."""
    pass

class OperacionInvalidaExcepcion(DominioExcepcion):
    """Excepción lanzada cuando se intenta realizar una operación no válida."""
    pass

class EntidadNoEncontradaExcepcion(DominioExcepcion):
    """Excepción lanzada cuando no se encuentra una entidad."""
    pass
