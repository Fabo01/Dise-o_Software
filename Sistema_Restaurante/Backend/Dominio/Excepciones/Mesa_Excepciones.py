"""
Excepciones específicas para el dominio de Mesas.
Define las excepciones de negocio relacionadas con la gestión de mesas.
"""

from Backend.Dominio.Excepciones.Base_Excepcion import DominioExcepcion


class MesaExcepcion(DominioExcepcion):
    """Excepción base para errores relacionados con mesas."""
    pass


class MesaNoEncontradaExcepcion(MesaExcepcion):
    """Excepción lanzada cuando una mesa no se encuentra."""
    def __init__(self, mensaje: str = "Mesa no encontrada"):
        super().__init__(mensaje)


class MesaEstadoInvalidoExcepcion(MesaExcepcion):
    """Excepción lanzada cuando se intenta asignar un estado inválido a una mesa."""
    def __init__(self, mensaje: str = "Estado de mesa inválido"):
        super().__init__(mensaje)


class MesaOcupadaExcepcion(MesaExcepcion):
    """Excepción lanzada cuando se intenta realizar una operación en una mesa ocupada."""
    def __init__(self, mensaje: str = "La mesa está ocupada"):
        super().__init__(mensaje)


class MesaNoDisponibleExcepcion(MesaExcepcion):
    """Excepción lanzada cuando se intenta usar una mesa que no está disponible."""
    def __init__(self, mensaje: str = "La mesa no está disponible"):
        super().__init__(mensaje)


class NumeroMesaDuplicadoExcepcion(MesaExcepcion):
    """Excepción lanzada cuando se intenta crear una mesa con un número ya existente."""
    def __init__(self, mensaje: str = "El número de mesa ya existe"):
        super().__init__(mensaje)


class CapacidadInsuficienteExcepcion(MesaExcepcion):
    """Excepción lanzada cuando la capacidad de una mesa es insuficiente."""
    def __init__(self, mensaje: str = "La capacidad de la mesa es insuficiente"):
        super().__init__(mensaje)


class MesaFueraServicioExcepcion(MesaExcepcion):
    """Excepción lanzada cuando se intenta usar una mesa que está fuera de servicio."""
    def __init__(self, mensaje: str = "La mesa está fuera de servicio"):
        super().__init__(mensaje)
