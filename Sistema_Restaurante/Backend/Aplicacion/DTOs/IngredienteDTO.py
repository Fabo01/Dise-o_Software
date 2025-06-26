from pydantic import BaseModel
from typing import Optional

class IngredienteDTO(BaseModel):
    id: Optional[int] = None
    nombre: str
    cantidad: float
    categoria: Optional[str] = None
    imagen: Optional[str] = None
    unidad_medida: str
    fecha_vencimiento: Optional[str] = None
    estado: str = "activo"
    fecha_registro: Optional[str] = None
    nivel_critico: Optional[float] = None
    tipo: Optional[str] = None

    class Config:
        orm_mode = True

