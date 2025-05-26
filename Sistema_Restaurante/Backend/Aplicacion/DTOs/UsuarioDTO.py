from pydantic import BaseModel
from typing import Optional

class UsuarioDTO(BaseModel):
    id: Optional[int]
    username: Optional[str] = None  # Ahora es opcional, se autogenera
    password: str
    email: str
    nombre: str
    apellido: str
    rol: Optional[str] = None
    telefono: str
    estado: Optional[str] = 'Activo'

    class Config:
        orm_mode = True