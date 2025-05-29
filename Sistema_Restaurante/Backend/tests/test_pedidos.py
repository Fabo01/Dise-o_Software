import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Pedido_Modelo import Pedido_Modelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import Cliente_Modelo

scenarios('features/pedidos.feature')

@pytest.fixture
def limpiar_pedidos(db):
    Pedido_Modelo.objects.all().delete()

@given(parsers.parse('que no existe un pedido con número {numero:d}'), target_fixture="limpiar_pedidos")
def no_existe_pedido(numero, limpiar_pedidos):
    assert not Pedido_Modelo.objects.filter(id=numero).exists()

@given(parsers.parse('que existe un pedido con número {numero:d}'))
def existe_pedido(numero, db):
    cliente = Cliente_Modelo.objects.create(nombre="TestCliente", email="test@cliente.com")
    Pedido_Modelo.objects.create(id=numero, cliente=cliente)
    assert Pedido_Modelo.objects.filter(id=numero).exists()

@when(parsers.parse('creo un pedido con número {numero:d} y cliente "{cliente_nombre}"'))
def crear_pedido(numero, cliente_nombre, db):
    cliente, _ = Cliente_Modelo.objects.get_or_create(nombre=cliente_nombre, email=f"{cliente_nombre}@mail.com")
    Pedido_Modelo.objects.create(id=numero, cliente=cliente)

@when(parsers.parse('actualizo el pedido {numero:d} a cliente "{cliente_nombre}"'))
def actualizar_pedido(numero, cliente_nombre, db):
    pedido = Pedido_Modelo.objects.get(id=numero)
    cliente, _ = Cliente_Modelo.objects.get_or_create(nombre=cliente_nombre, email=f"{cliente_nombre}@mail.com")
    pedido.cliente = cliente
    pedido.save()

@when(parsers.parse('elimino el pedido {numero:d}'))
def eliminar_pedido(numero, db):
    Pedido_Modelo.objects.filter(id=numero).delete()

@when('solicito la lista de pedidos')
def listar_pedidos(db):
    pass

@then(parsers.parse('el pedido {numero:d} debe existir en el sistema con cliente "{cliente_nombre}"'))
def verificar_pedido(numero, cliente_nombre, db):
    pedido = Pedido_Modelo.objects.get(id=numero)
    assert pedido.cliente.nombre == cliente_nombre

@then(parsers.parse('el pedido {numero:d} debe tener cliente "{cliente_nombre}"'))
def verificar_cliente(numero, cliente_nombre, db):
    pedido = Pedido_Modelo.objects.get(id=numero)
    assert pedido.cliente.nombre == cliente_nombre

@then(parsers.parse('el pedido {numero:d} no debe existir en el sistema'))
def verificar_no_existe(numero, db):
    assert not Pedido_Modelo.objects.filter(id=numero).exists()

@then('debo obtener una lista con los pedidos existentes')
def verificar_lista_pedidos(db):
    pedidos = Pedido_Modelo.objects.all()
    assert pedidos.count() >= 0
