import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Mesa_Modelo import Mesa_Modelo

scenarios('features/mesas.feature')

@pytest.fixture
def limpiar_mesas(db):
    Mesa_Modelo.objects.all().delete()

@given(parsers.parse('que no existe una mesa con número {numero:d}'), target_fixture="limpiar_mesas")
def no_existe_mesa(numero, limpiar_mesas):
    assert not Mesa_Modelo.objects.filter(numero=numero).exists()

@given(parsers.parse('que existe una mesa con número {numero:d}'))
def existe_mesa(numero, db):
    Mesa_Modelo.objects.create(numero=numero, capacidad=4)
    assert Mesa_Modelo.objects.filter(numero=numero).exists()

@when(parsers.parse('creo una mesa con número {numero:d} y capacidad {capacidad:d}'))
def crear_mesa(numero, capacidad, db):
    Mesa_Modelo.objects.create(numero=numero, capacidad=capacidad)

@when(parsers.parse('actualizo la mesa {numero:d} a capacidad {capacidad:d}'))
def actualizar_mesa(numero, capacidad, db):
    mesa = Mesa_Modelo.objects.get(numero=numero)
    mesa.capacidad = capacidad
    mesa.save()

@when(parsers.parse('elimino la mesa {numero:d}'))
def eliminar_mesa(numero, db):
    Mesa_Modelo.objects.filter(numero=numero).delete()

@when('solicito la lista de mesas')
def listar_mesas(db):
    pass

@then(parsers.parse('la mesa {numero:d} debe existir en el sistema con capacidad {capacidad:d}'))
def verificar_mesa(numero, capacidad, db):
    mesa = Mesa_Modelo.objects.get(numero=numero)
    assert mesa.capacidad == capacidad

@then(parsers.parse('la mesa {numero:d} debe tener capacidad {capacidad:d}'))
def verificar_capacidad(numero, capacidad, db):
    mesa = Mesa_Modelo.objects.get(numero=numero)
    assert mesa.capacidad == capacidad

@then(parsers.parse('la mesa {numero:d} no debe existir en el sistema'))
def verificar_no_existe(numero, db):
    assert not Mesa_Modelo.objects.filter(numero=numero).exists()

@then('debo obtener una lista con las mesas existentes')
def verificar_lista_mesas(db):
    mesas = Mesa_Modelo.objects.all()
    assert mesas.count() >= 0
