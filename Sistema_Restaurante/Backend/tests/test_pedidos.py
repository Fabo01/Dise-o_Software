# import pytest
# from pytest_bdd import scenarios, given, when, then, parsers
# from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
# from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

# scenarios('features/pedidos.feature')

# @pytest.fixture
# def limpiar_pedidos(db):
#     PedidoModelo.objects.all().delete()

# @given(parsers.parse('que no existe un pedido con número {numero:d}'), target_fixture="limpiar_pedidos")
# def no_existe_pedido(numero, limpiar_pedidos):
#     assert not PedidoModelo.objects.filter(id=numero).exists()

# @given(parsers.parse('que existe un pedido con número {numero:d}'))
# def existe_pedido(numero, db):
#     cliente = ClienteModelo.objects.create(nombre="TestCliente", email="test@cliente.com")
#     PedidoModelo.objects.create(id=numero, cliente=cliente)
#     assert PedidoModelo.objects.filter(id=numero).exists()

# @when(parsers.parse('creo un pedido con número {numero:d} y cliente "{cliente_nombre}"'))
# def crear_pedido(numero, cliente_nombre, db):
#     cliente, _ = ClienteModelo.objects.get_or_create(nombre=cliente_nombre, email=f"{cliente_nombre}@mail.com")
#     PedidoModelo.objects.create(id=numero, cliente=cliente)

# @when(parsers.parse('actualizo el pedido {numero:d} a cliente "{cliente_nombre}"'))
# def actualizar_pedido(numero, cliente_nombre, db):
#     pedido = PedidoModelo.objects.get(id=numero)
#     cliente, _ = ClienteModelo.objects.get_or_create(nombre=cliente_nombre, email=f"{cliente_nombre}@mail.com")
#     pedido.cliente = cliente
#     pedido.save()

# @when(parsers.parse('elimino el pedido {numero:d}'))
# def eliminar_pedido(numero, db):
#     PedidoModelo.objects.filter(id=numero).delete()

# @when('solicito la lista de pedidos')
# def listar_pedidos(db):
#     pass

# @then(parsers.parse('el pedido {numero:d} debe existir en el sistema con cliente "{cliente_nombre}"'))
# def verificar_pedido(numero, cliente_nombre, db):
#     pedido = PedidoModelo.objects.get(id=numero)
#     assert pedido.cliente.nombre == cliente_nombre

# @then(parsers.parse('el pedido {numero:d} debe tener cliente "{cliente_nombre}"'))
# def verificar_cliente(numero, cliente_nombre, db):
#     pedido = PedidoModelo.objects.get(id=numero)
#     assert pedido.cliente.nombre == cliente_nombre

# @then(parsers.parse('el pedido {numero:d} no debe existir en el sistema'))
# def verificar_no_existe(numero, db):
#     assert not PedidoModelo.objects.filter(id=numero).exists()

# @then('debo obtener una lista con los pedidos existentes')
# def verificar_lista_pedidos(db):
#     pedidos = PedidoModelo.objects.all()
#     assert pedidos.count() >= 0

# @given('que existen pedidos registrados')
# def existen_pedidos_registrados(db, PedidoModelo):
#     PedidoModelo.objects.create(numero=1)
#     PedidoModelo.objects.create(numero=2)
#     assert PedidoModelo.objects.count() >= 2
