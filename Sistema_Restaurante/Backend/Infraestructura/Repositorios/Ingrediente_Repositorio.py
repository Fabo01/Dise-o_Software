from django.db.models import Q

from Backend.Dominio.Interfaces.IRepository import IRepository
from Backend.Dominio.Entidades.Ingrediente_Entidad import Ingrediente


class IngredienteRepositorio(IRepository):
    def __init__(self):
        self.model = Ingrediente

    def agregar(self, entidad):
        self.model.objects.create(**entidad)

    def obtener(self, id):
        return self.model.objects.get(id=id)

    def actualizar(self, id, entidad):
        self.model.objects.filter(id=id).update(**entidad)  

    def eliminar(self, id):
        self.model.objects.filter(id=id).delete()

    def buscar(self, **kwargs):
        return self.model.objects.filter(**kwargs)