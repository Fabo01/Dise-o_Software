# Entidad Ingrediente para la capa de Dominio
from datetime import date
from typing import Optional

class Ingrediente:
    """
    Entidad de dominio que representa un ingrediente en el sistema.
    """
    def __init__(self, id: int, nombre: str, cantidad: float, categoria: str, imagen: Optional[str], unidad_medida: str,
                 fecha_vencimiento: Optional[date], estado: str, fecha_registro: date, nivel_critico: Optional[float], tipo: Optional[str]):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.categoria = categoria
        self.imagen = imagen
        self.unidad_medida = unidad_medida
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.fecha_registro = fecha_registro
        self.nivel_critico = nivel_critico
        self.tipo = tipo

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} {self.unidad_medida})"
