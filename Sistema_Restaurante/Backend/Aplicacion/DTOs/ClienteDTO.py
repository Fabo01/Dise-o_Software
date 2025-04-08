from pydantic import BaseModel
from typing import Optional

class ClienteDTO(BaseModel):
    """
    DTO para transferir datos de clientes entre capas
    """
    id: Optional[int] = None
    rut: str
    nombre: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    correo: Optional[str] = None
    estado: str = "activo"
    
    class Config:
        """Configuración del modelo Pydantic"""
        orm_mode = True
