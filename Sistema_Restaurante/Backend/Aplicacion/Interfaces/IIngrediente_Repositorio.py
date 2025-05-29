from abc import ABC, abstractmethod

class IIngredienteRepositorio(ABC):
    @abstractmethod
    def guardar(self, ingrediente):
        pass

    @abstractmethod
    def buscar_por_id(self, id):
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre):
        pass

    @abstractmethod
    def listar_todos(self):
        pass

    @abstractmethod
    def listar_activos(self):
        pass

    @abstractmethod
    def eliminar(self, id):
        pass

    @abstractmethod
    def actualizar_stock(self, id, cantidad):
        pass

    @abstractmethod
    def buscar_por_categoria(self, categoria):
        pass

    @abstractmethod
    def listar_por_estado(self, estado):
        pass

    @abstractmethod
    def listar_bajo_nivel_critico(self):
        pass

    @abstractmethod
    def actualizar_estado(self, id, nuevo_estado):
        pass
