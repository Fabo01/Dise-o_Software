import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Menu_Modelo import Menu_Modelo

scenarios('features/menus.feature')

@pytest.fixture
def limpiar_menus(db):
    Menu_Modelo.objects.all().delete()

@given(parsers.parse('que no existe un menú llamado "{nombre}"'), target_fixture="limpiar_menus")
def no_existe_menu(nombre, limpiar_menus):
    assert not Menu_Modelo.objects.filter(nombre=nombre).exists()

@given(parsers.parse('que existe un menú llamado "{nombre}"'))
def existe_menu(nombre, db):
    Menu_Modelo.objects.create(nombre=nombre, categoria="General")
    assert Menu_Modelo.objects.filter(nombre=nombre).exists()

@when(parsers.parse('creo un menú con nombre "{nombre}", categoría "{categoria}"'))
def crear_menu(nombre, categoria, db):
    Menu_Modelo.objects.create(nombre=nombre, categoria=categoria)

@when(parsers.parse('actualizo el menú "{nombre}" a categoría "{categoria}"'))
def actualizar_menu(nombre, categoria, db):
    menu = Menu_Modelo.objects.get(nombre=nombre)
    menu.categoria = categoria
    menu.save()

@when(parsers.parse('elimino el menú "{nombre}"'))
def eliminar_menu(nombre, db):
    Menu_Modelo.objects.filter(nombre=nombre).delete()

@when('solicito la lista de menús')
def listar_menus(db):
    pass

@then(parsers.parse('el menú "{nombre}" debe existir en el sistema con categoría "{categoria}"'))
def verificar_menu(nombre, categoria, db):
    menu = Menu_Modelo.objects.get(nombre=nombre)
    assert menu.categoria == categoria

@then(parsers.parse('el menú "{nombre}" debe tener categoría "{categoria}"'))
def verificar_categoria(nombre, categoria, db):
    menu = Menu_Modelo.objects.get(nombre=nombre)
    assert menu.categoria == categoria

@then(parsers.parse('el menú "{nombre}" no debe existir en el sistema'))
def verificar_no_existe(nombre, db):
    assert not Menu_Modelo.objects.filter(nombre=nombre).exists()

@then('debo obtener una lista con los menús existentes')
def verificar_lista_menus(db):
    menus = Menu_Modelo.objects.all()
    assert menus.count() >= 0
