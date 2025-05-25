from abc import ABC, abstractmethod

class IEntidadFactory(ABC):
    @abstractmethod
    def crear(self, *args, **kwargs):
        """
        Método abstracto para crear una entidad.
        Debe ser implementado por las subclases.
        """
        pass