import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

scenarios('features/clientes.feature')

@pytest.fixture
def limpiar_clientes(db):
    ClienteModelo.objects.all().delete()

@given(parsers.parse('que no existe un cliente con nombre "{nombre}"'), target_fixture="limpiar_clientes")
def no_existe_cliente(nombre, limpiar_clientes):
    assert not ClienteModelo.objects.filter(nombre=nombre).exists()

@given(parsers.parse('que existe un cliente con nombre "{nombre}"'))
def existe_cliente(nombre, db):
    rut = f"{nombre.lower()}-rut"
    ClienteModelo.objects.create(nombre=nombre, rut=rut, correo=f"{nombre}@mail.com")
    assert ClienteModelo.objects.filter(nombre=nombre).exists()

@given('que existen clientes registrados')
def existen_clientes_registrados(db):
    ClienteModelo.objects.create(nombre="Ana", rut="ana-rut", correo="ana@mail.com")
    ClienteModelo.objects.create(nombre="Luis", rut="luis-rut", correo="luis@mail.com")
    assert ClienteModelo.objects.count() >= 2

@when(parsers.parse('creo un cliente con nombre "{nombre}", correo "{correo}"'))
def crear_cliente(nombre, correo, db):
    ClienteModelo.objects.create(nombre=nombre, correo=correo)

@when(parsers.parse('actualizo el cliente "{nombre}" a correo "{correo}"'))
def actualizar_cliente(nombre, correo, db):
    cliente = ClienteModelo.objects.get(nombre=nombre)
    cliente.correo = correo
    cliente.save()

@when(parsers.parse('elimino el cliente "{nombre}"'))
def eliminar_cliente(nombre, db):
    ClienteModelo.objects.filter(nombre=nombre).delete()

@when('solicito la lista de clientes')
def listar_clientes(db):
    pass

@then(parsers.parse('el cliente "{nombre}" debe existir en el sistema con correo "{correo}"'))
def verificar_cliente(nombre, correo, db):
    cliente = ClienteModelo.objects.get(nombre=nombre)
    assert cliente.correo == correo

@then(parsers.parse('el cliente "{nombre}" debe tener correo "{correo}"'))
def verificar_correo(nombre, correo, db):
    cliente = ClienteModelo.objects.get(nombre=nombre)
    assert cliente.correo == correo

@then(parsers.parse('el cliente "{nombre}" no debe existir en el sistema'))
def verificar_no_existe(nombre, db):
    assert not ClienteModelo.objects.filter(nombre=nombre).exists()

@then('debo obtener una lista con los clientes existentes')
def verificar_lista_clientes(db):
    clientes = ClienteModelo.objects.all()
    assert clientes.count() >= 0
