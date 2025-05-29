from pydantic import BaseModel
from typing import Optional

class UsuarioDTO(BaseModel):
    rut: str  # RUT chileno, identificador único e inmutable
    username: Optional[str] = None  # Ahora es opcional, se autogenera
    password: str
    email: str
    nombre: str
    apellido: str
    rol: Optional[str] = None
    telefono: str
    estado: Optional[str] = 'Activo'
    direccion: Optional[str] = None

    class Config:
        orm_mode = True