# Servicio de aplicación para la gestión de ingredientes
from typing import List, Optional
from Backend.Dominio.Entidades.Ingrediente_Entidad import Ingrediente
from Backend.Dominio.Interfaces.IIngredienteRepositorio import IIngredienteRepositorio
from Backend.Aplicacion.DTOs.IngredienteDTO import IngredienteDTO

class IngredienteServicio:
    """
    Servicio de aplicación para casos de uso de ingredientes.
    """
    def __init__(self, repositorio: IIngredienteRepositorio):
        self.repositorio = repositorio

    def crear_ingrediente(self, dto: IngredienteDTO) -> Ingrediente:
        ingrediente = Ingrediente(**dto.__dict__)
        return self.repositorio.crear(ingrediente)

    def editar_ingrediente(self, id: int, dto: IngredienteDTO) -> Ingrediente:
        ingrediente = self.repositorio.obtener_por_id(id)
        if not ingrediente:
            raise ValueError("Ingrediente no encontrado")
        for key, value in dto.__dict__.items():
            setattr(ingrediente, key, value)
        return self.repositorio.actualizar(ingrediente)

    def eliminar_ingrediente(self, id: int) -> None:
        self.repositorio.eliminar(id)

    def actualizar_stock(self, id: int, cantidad: float) -> Ingrediente:
        ingrediente = self.repositorio.obtener_por_id(id)
        if not ingrediente:
            raise ValueError("Ingrediente no encontrado")
        ingrediente.cantidad = cantidad
        return self.repositorio.actualizar(ingrediente)

    def listar_ingredientes(self) -> List[Ingrediente]:
        return self.repositorio.listar()

    def obtener_ingrediente(self, id: int) -> Optional[Ingrediente]:
        return self.repositorio.obtener_por_id(id)
