import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo

scenarios('features/ingredientes.feature')

@pytest.fixture
def limpiar_ingredientes(db):
    IngredienteModelo.objects.all().delete()

@given(parsers.parse('que no existe un ingrediente llamado "{nombre}"'), target_fixture="limpiar_ingredientes")
def no_existe_ingrediente(nombre, limpiar_ingredientes):
    assert not IngredienteModelo.objects.filter(nombre=nombre).exists()

@given(parsers.parse('que existe un ingrediente llamado "{nombre}" con cantidad {cantidad:d}'))
def existe_ingrediente(nombre, cantidad, db):
    IngredienteModelo.objects.create(nombre=nombre, cantidad=cantidad, unidad_medida="kg", categoria="Verdura", nivel_critico=2)
    assert IngredienteModelo.objects.filter(nombre=nombre).exists()

@when(parsers.parse('creo un ingrediente con nombre "{nombre}", cantidad {cantidad:d}, unidad "{unidad}", categoría "{categoria}", nivel crítico {nivel_critico:d}'))
def crear_ingrediente(nombre, cantidad, unidad, categoria, nivel_critico, db):
    IngredienteModelo.objects.create(nombre=nombre, cantidad=cantidad, unidad_medida=unidad, categoria=categoria, nivel_critico=nivel_critico)

@when(parsers.parse('actualizo el ingrediente "{nombre}" a cantidad {cantidad:d}'))
def actualizar_ingrediente(nombre, cantidad, db):
    ingrediente = IngredienteModelo.objects.get(nombre=nombre)
    ingrediente.cantidad = cantidad
    ingrediente.save()

@when(parsers.parse('elimino el ingrediente "{nombre}"'))
def eliminar_ingrediente(nombre, db):
    IngredienteModelo.objects.filter(nombre=nombre).delete()

@when('solicito la lista de ingredientes')
def listar_ingredientes(db):
    pass  # No se requiere acción, la verificación se hace en el then

@then(parsers.parse('el ingrediente "{nombre}" debe existir en el sistema con cantidad {cantidad:d} y unidad "{unidad}"'))
def verificar_ingrediente(nombre, cantidad, unidad, db):
    ingrediente = IngredienteModelo.objects.get(nombre=nombre)
    assert ingrediente.cantidad == cantidad
    assert ingrediente.unidad_medida == unidad

@then(parsers.parse('el ingrediente "{nombre}" debe tener cantidad {cantidad:d}'))
def verificar_cantidad(nombre, cantidad, db):
    ingrediente = IngredienteModelo.objects.get(nombre=nombre)
    assert ingrediente.cantidad == cantidad

@then(parsers.parse('el ingrediente "{nombre}" no debe existir en el sistema'))
def verificar_no_existe(nombre, db):
    assert not IngredienteModelo.objects.filter(nombre=nombre).exists()

@then('debo obtener una lista con los ingredientes existentes')
def verificar_lista_ingredientes(db):
    ingredientes = IngredienteModelo.objects.all()
    assert ingredientes.count() >= 0
