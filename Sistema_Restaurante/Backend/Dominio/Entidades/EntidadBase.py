from datetime import datetime
from typing import Optional
from ..Interfaces.IEntidad import IEntidad

class EntidadBase(IEntidad):
    """
    Clase base para todas las entidades del dominio.
    Implementa la interfaz IEntidad y proporciona funcionalidad común.
    """
    
    def __init__(self):
        self._id = None
        self._fecha_creacion = datetime.now()
        self._fecha_actualizacion = self._fecha_creacion
        self._activo = True
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion
    
    @property
    def fecha_actualizacion(self) -> datetime:
        return self._fecha_actualizacion
    
    @property
    def activo(self) -> bool:
        """Indica si la entidad está activa."""
        return self._activo
    
    def actualizar_fecha(self):
        """Actualiza la fecha de modificación al momento actual."""
        self._fecha_actualizacion = datetime.now()
    
    def activar(self):
        """Activa la entidad."""
        self._activo = True
        self.actualizar_fecha()
    
    def desactivar(self):
        """Desactiva la entidad."""
        self._activo = False
        self.actualizar_fecha()
    
    def es_igual(self, otra_entidad) -> bool:
        """
        Compara si dos entidades son iguales basándose en su ID.
        Si los IDs son None, se consideran diferentes.
        
        Args:
            otra_entidad: Otra entidad para comparar
            
        Returns:
            bool: True si son iguales, False en caso contrario
        """
        if not isinstance(otra_entidad, IEntidad):
            return False
        
        # Si ambas tienen ID, comparar por ID
        if self._id is not None and otra_entidad.id is not None:
            return self._id == otra_entidad.id
        
        # Si alguna no tiene ID, no son iguales
        return False
