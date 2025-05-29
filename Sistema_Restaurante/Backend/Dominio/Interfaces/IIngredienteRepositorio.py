# Interfaz de repositorio para Ingrediente
from abc import ABC, abstractmethod
from typing import List, Optional
from Sistema_Restaurante.Backend.Dominio.Entidades.Ingrediente_Entidad import Ingrediente

class IIngredienteRepositorio(ABC):
    """
    Interfaz para el repositorio de ingredientes.
    """
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Ingrediente]:
        pass

    @abstractmethod
    def listar(self) -> List[Ingrediente]:
        pass

    @abstractmethod
    def crear(self, ingrediente: Ingrediente) -> Ingrediente:
        pass

    @abstractmethod
    def actualizar(self, ingrediente: Ingrediente) -> Ingrediente:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> None:
        pass
