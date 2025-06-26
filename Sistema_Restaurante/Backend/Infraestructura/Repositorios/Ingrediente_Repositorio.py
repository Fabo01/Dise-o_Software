from django.db.models import F, Q

from Backend.Aplicacion.Interfaces.IIngrediente_Repositorio import IIngredienteRepositorio
from Backend.Dominio.Entidades.Ingrediente_Entidad import IngredienteEntidad
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo


class IngredienteRepositorio(IIngredienteRepositorio):
    '''
        nombre (str): Nombre del ingrediente.
        cantidad (float): Cantidad disponible del ingrediente.
        unidad_medida (str): Unidad de medida del ingrediente (ej. kg, g, l).
        fecha_vencimiento (datetime): Fecha de vencimiento del ingrediente.
        estado (str): Estado del ingrediente (ej. activo, inactivo).
        nivel_critico (float): Nivel mínimo de stock antes de generar alertas.
        tipo (str): Categoría del ingrediente (ej. proteína, vegetal, lácteo)
    '''
    def guardar(self, ingrediente):
        
        if ingrediente.id:
            ingrediente_modelo = IngredienteModelo.objects.get(id=ingrediente.id)
            ingrediente_modelo.nombre = ingrediente.nombre
            ingrediente_modelo.cantidad = ingrediente.cantidad
            ingrediente_modelo.unidad_medida = ingrediente.unidad_medida
            ingrediente_modelo.fecha_vencimiento = ingrediente.fecha_vencimiento
            ingrediente_modelo.estado = ingrediente.estado
            ingrediente_modelo.nivel_critico = ingrediente.nivel_critico
            ingrediente_modelo.tipo = ingrediente.tipo
        else:
            ingrediente_modelo = IngredienteModelo.objects.create(
                nombre=ingrediente.nombre,
                cantidad=ingrediente.cantidad,
                unidad_medida=ingrediente.unidad_medida,
                fecha_vencimiento=ingrediente.fecha_vencimiento,
                estado=ingrediente.estado,
                nivel_critico=ingrediente.nivel_critico,
                tipo=ingrediente.tipo
            )
            ingrediente.id = ingrediente_modelo.id
        return self._convertir_a_entidad(ingrediente_modelo)
    
    def buscar_por_id(self, id):
        """
        Busca un ingrediente por su ID
        """
        try:
            ingrediente_modelo = IngredienteModelo.objects.get(id=id)
            return self._convertir_a_entidad(ingrediente_modelo)
        except IngredienteModelo.DoesNotExist:
            return None
        
    def buscar_por_nombre(self, nombre):
        """
        Busca un ingrediente por su nombre
        """
        try:
            ingrediente_modelo = IngredienteModelo.objects.get(nombre=nombre)
            return self._convertir_a_entidad(ingrediente_modelo)
        except IngredienteModelo.DoesNotExist:
            return None
        
    def listar_todos(self):
        """
        Lista todos los ingredientes
        """
        ingredientes_modelo = IngredienteModelo.objects.all()
        return [self._convertir_a_entidad(ingrediente) for ingrediente in ingredientes_modelo]
    
    def listar_activos(self):
        """
        Lista todos los ingredientes activos
        """
        ingredientes_modelo = IngredienteModelo.objects.filter(estado="activo")
        return [self._convertir_a_entidad(ingrediente) for ingrediente in ingredientes_modelo]
    
    def crear(self, ingrediente):
        """
        Crea un nuevo ingrediente
        """
        return self.guardar(ingrediente)

    def actualizar(self, ingrediente):
        """
        Actualiza un ingrediente existente
        """
        return self.guardar(ingrediente)

    def obtener_por_id(self, id):
        """
        Obtiene un ingrediente por su ID
        """
        return self.buscar_por_id(id)

    def listar(self):
        """
        Lista todos los ingredientes
        """
        return self.listar_todos()

    def eliminar(self, id):
        """
        Elimina un ingrediente por su ID
        """
        return super().eliminar(id)
        
    def actualizar_stock(self, id, cantidad):
        """
        Actualiza la cantidad de stock de un ingrediente
        """
        try:
            ingrediente_modelo = IngredienteModelo.objects.get(id=id)
            ingrediente_modelo.cantidad += cantidad
            ingrediente_modelo.save()
            return self._convertir_a_entidad(ingrediente_modelo)
        except IngredienteModelo.DoesNotExist:
            return None
        
    def buscar_por_categoria(self, categoria):
        """
        Busca ingredientes por su categoría
        """
        ingredientes_modelo = IngredienteModelo.objects.filter(tipo=categoria)
        return [self._convertir_a_entidad(ingrediente) for ingrediente in ingredientes_modelo]
    
    def listar_por_estado(self, estado):
        """
        Lista ingredientes por su estado
        """
        ingredientes_modelo = IngredienteModelo.objects.filter(estado=estado)
        return [self._convertir_a_entidad(ingrediente) for ingrediente in ingredientes_modelo]
    
    def listar_bajo_nivel_critico(self):
        """
        Lista ingredientes que están por debajo del nivel crítico
        """
        ingredientes_modelo = IngredienteModelo.objects.filter(cantidad__lte=F('nivel_critico'))
        return [self._convertir_a_entidad(ingrediente) for ingrediente in ingredientes_modelo]
    
    def actualizar_estado(self, id, nuevo_estado):
        """
        Actualiza el estado de un ingrediente
        """
        try:
            ingrediente_modelo = IngredienteModelo.objects.get(id=id)
            ingrediente_modelo.estado = nuevo_estado
            ingrediente_modelo.save()
            return self._convertir_a_entidad(ingrediente_modelo)
        except IngredienteModelo.DoesNotExist:
            return None
        
    def _convertir_a_entidad(self, ingrediente_modelo):
        """
        Convierte un modelo de ingrediente a una entidad de dominio
        """
        return IngredienteEntidad(
            nombre=ingrediente_modelo.nombre,
            cantidad=float(ingrediente_modelo.cantidad),
            unidad_medida=ingrediente_modelo.unidad_medida,
            fecha_vencimiento=ingrediente_modelo.fecha_vencimiento,
            nivel_critico=float(ingrediente_modelo.nivel_critico) if ingrediente_modelo.nivel_critico else None,
            tipo=ingrediente_modelo.tipo,
            imagen=str(ingrediente_modelo.imagen) if ingrediente_modelo.imagen else None
        )
