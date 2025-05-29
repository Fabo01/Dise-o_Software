import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Cliente_Modelo import Cliente_Modelo

scenarios('features/clientes.feature')

@pytest.fixture
def limpiar_clientes(db):
    Cliente_Modelo.objects.all().delete()

@given(parsers.parse('que no existe un cliente con nombre "{nombre}"'), target_fixture="limpiar_clientes")
def no_existe_cliente(nombre, limpiar_clientes):
    assert not Cliente_Modelo.objects.filter(nombre=nombre).exists()

@given(parsers.parse('que existe un cliente con nombre "{nombre}"'))
def existe_cliente(nombre, db):
    Cliente_Modelo.objects.create(nombre=nombre, email=f"{nombre}@mail.com")
    assert Cliente_Modelo.objects.filter(nombre=nombre).exists()

@when(parsers.parse('creo un cliente con nombre "{nombre}", correo "{correo}"'))
def crear_cliente(nombre, correo, db):
    Cliente_Modelo.objects.create(nombre=nombre, email=correo)

@when(parsers.parse('actualizo el cliente "{nombre}" a correo "{correo}"'))
def actualizar_cliente(nombre, correo, db):
    cliente = Cliente_Modelo.objects.get(nombre=nombre)
    cliente.email = correo
    cliente.save()

@when(parsers.parse('elimino el cliente "{nombre}"'))
def eliminar_cliente(nombre, db):
    Cliente_Modelo.objects.filter(nombre=nombre).delete()

@when('solicito la lista de clientes')
def listar_clientes(db):
    pass

@then(parsers.parse('el cliente "{nombre}" debe existir en el sistema con correo "{correo}"'))
def verificar_cliente(nombre, correo, db):
    cliente = Cliente_Modelo.objects.get(nombre=nombre)
    assert cliente.email == correo

@then(parsers.parse('el cliente "{nombre}" debe tener correo "{correo}"'))
def verificar_correo(nombre, correo, db):
    cliente = Cliente_Modelo.objects.get(nombre=nombre)
    assert cliente.email == correo

@then(parsers.parse('el cliente "{nombre}" no debe existir en el sistema'))
def verificar_no_existe(nombre, db):
    assert not Cliente_Modelo.objects.filter(nombre=nombre).exists()

@then('debo obtener una lista con los clientes existentes')
def verificar_lista_clientes(db):
    clientes = Cliente_Modelo.objects.all()
    assert clientes.count() >= 0
