# Objeto de Valor para Ingrediente (opcional, para atributos compuestos o validaciones)
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class IngredienteVO:
    nombre: str
    cantidad: float
    unidad_medida: str
    categoria: str
    fecha_vencimiento: Optional[date]
    nivel_critico: Optional[float]
    tipo: Optional[str]
