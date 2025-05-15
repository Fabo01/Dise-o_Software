from pydantic import BaseModel
from typing import Optional

class IngredienteDTO(BaseModel):
    id: Optional[int] = None
    nombre: str
    cantidad: float
    unidad_medida: str
    estado: str = "activo"
    fecha_vencimiento: Optional[str] = None

    class Config:
        orm_mode = True

