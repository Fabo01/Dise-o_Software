# Interfaz de repositorio para Ingrediente
from abc import ABC, abstractmethod
from typing import List, Optional
from ..Entidades.Ingrediente_Entidad import IngredienteEntidad

class IIngredienteRepositorio(ABC):
    """
    Interfaz para el repositorio de ingredientes.
    """
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[IngredienteEntidad]:
        pass

    @abstractmethod
    def listar(self) -> List[IngredienteEntidad]:
        pass

    @abstractmethod
    def crear(self, ingrediente: IngredienteEntidad) -> IngredienteEntidad:
        pass

    @abstractmethod
    def actualizar(self, ingrediente: IngredienteEntidad) -> IngredienteEntidad:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> None:
        pass
