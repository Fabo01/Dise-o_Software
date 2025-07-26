# Backend/tests/test_delivery.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from decimal import Decimal
from django.utils import timezone
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.DeliveryPedido_Modelo import DeliveryPedidoModelo
from Backend.Infraestructura.Modelos.DeliveryApp_Modelo import DeliveryAppModelo
from Backend.Infraestructura.Modelos.DeliveryRepartidor_Modelo import DeliveryRepartidorModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Aplicacion.Servicios.Delivery_Servicio import DeliveryServicio

scenarios('features/delivery.feature')

@pytest.fixture
def delivery_servicio():
    return DeliveryServicio()

@pytest.fixture
def limpiar_delivery(db):
    DeliveryPedidoModelo.objects.all().delete()
    DeliveryAppModelo.objects.all().delete()
    DeliveryRepartidorModelo.objects.all().delete()
    PedidoModelo.objects.all().delete()
    ClienteModelo.objects.all().delete()

@pytest.fixture
def cliente_test(limpiar_delivery):
    return ClienteModelo.objects.create(
        rut='12345678-9',
        nombre='Juan Pérez',
        correo='juan@test.com',
        telefono='987654321'
    )

@pytest.fixture
def app_delivery_test(limpiar_delivery):
    return DeliveryAppModelo.objects.create(
        nombre='UberEats',
        comision=Decimal('15.0'),
        url_api='https://api.ubereats.com',
        activa=True
    )

@pytest.fixture
def repartidor_test(limpiar_delivery):
    return DeliveryRepartidorModelo.objects.create(
        nombre='Carlos Repartidor',
        telefono='912345678',
        vehiculo='Moto',
        estado='disponible',
        activo=True
    )

# Given steps
@given('que existe un cliente con rut "12345678-9"')
def cliente_existe(cliente_test):
    assert ClienteModelo.objects.filter(rut='12345678-9').exists()

@given('que existe una app de delivery llamada "UberEats"')
def app_delivery_existe(app_delivery_test):
    assert DeliveryAppModelo.objects.filter(nombre='UberEats').exists()

@given('que existe un repartidor disponible')
def repartidor_disponible_existe(repartidor_test):
    assert DeliveryRepartidorModelo.objects.filter(estado='disponible').exists()

@given('que no existen pedidos delivery pendientes')
def no_pedidos_delivery_pendientes(limpiar_delivery):
    assert DeliveryPedidoModelo.objects.filter(estado_delivery='pendiente').count() == 0

# When steps
@when('creo un pedido delivery directo con dirección "Av. Principal 123"')
def crear_pedido_delivery_directo(delivery_servicio, cliente_test):
    datos_pedido = {
        'cliente_rut': '12345678-9',
        'direccion_entrega': 'Av. Principal 123',
        'telefono_contacto': '987654321',
        'observaciones': 'Timbre azul',
        'total': 15000
    }
    resultado = delivery_servicio.crear_pedido_delivery_directo(datos_pedido)
    return resultado

@when('registro un pedido desde UberEats con código "UE12345"')
def registrar_pedido_desde_app_externa(delivery_servicio, app_delivery_test):
    datos_pedido = {
        'app_nombre': 'UberEats',
        'codigo_externo': 'UE12345',
        'direccion_entrega': 'Calle Secundaria 456',
        'total': 20000,
        'cliente': {
            'rut': 'EXT-UE12345',
            'nombre': 'Cliente Externo',
            'telefono': '956789123'
        }
    }
    resultado = delivery_servicio.crear_pedido_desde_app_externa(datos_pedido)
    return resultado

@when(parsers.parse('asigno el repartidor al pedido "{pedido_id:d}"'))
def asignar_repartidor_a_pedido(delivery_servicio, repartidor_test, pedido_id):
    resultado = delivery_servicio.asignar_repartidor(pedido_id, repartidor_test.id)
    return resultado

@when(parsers.parse('marco como entregado el pedido "{pedido_id:d}"'))
def marcar_pedido_entregado(delivery_servicio, pedido_id):
    datos_entrega = {
        'comentarios': 'Entregado correctamente'
    }
    resultado = delivery_servicio.completar_entrega(pedido_id, datos_entrega)
    return resultado

# Then steps
@then('el pedido delivery se crea exitosamente')
def pedido_delivery_creado_exitosamente():
    assert DeliveryPedidoModelo.objects.filter(estado_delivery='pendiente').exists()

@then('el pedido debe tener estado "pendiente"')
def pedido_estado_pendiente():
    pedido = DeliveryPedidoModelo.objects.last()
    assert pedido.estado_delivery == 'pendiente'

@then('el pedido debe tener dirección "Av. Principal 123"')
def pedido_direccion_correcta():
    pedido = DeliveryPedidoModelo.objects.last()
    assert pedido.direccion_entrega == 'Av. Principal 123'

@then('el pedido debe estar marcado como delivery externo')
def pedido_delivery_externo():
    pedido = DeliveryPedidoModelo.objects.last()
    assert pedido.es_delivery_externo == True

@then('el pedido debe tener código externo "UE12345"')
def pedido_codigo_externo_correcto():
    pedido = DeliveryPedidoModelo.objects.last()
    assert pedido.codigo_externo == 'UE12345'

@then('el repartidor debe estar asignado al pedido')
def repartidor_asignado():
    pedido = DeliveryPedidoModelo.objects.last()
    assert pedido.repartidor is not None
    assert pedido.estado_delivery == 'asignado'

@then('el repartidor debe tener estado "en_ruta"')
def repartidor_en_ruta():
    repartidor = DeliveryRepartidorModelo.objects.last()
    assert repartidor.estado == 'en_ruta'

@then('el pedido debe estar marcado como entregado')
def pedido_entregado():
    pedido = DeliveryPedidoModelo.objects.last()
    assert pedido.estado_delivery == 'entregado'
    assert pedido.hora_entrega is not None

@then('el repartidor debe estar disponible nuevamente')
def repartidor_disponible_nuevamente():
    repartidor = DeliveryRepartidorModelo.objects.last()
    assert repartidor.estado == 'disponible'
    assert repartidor.pedido_actual is None

@then('puedo obtener la lista de repartidores disponibles')
def obtener_repartidores_disponibles(delivery_servicio):
    repartidores = delivery_servicio.obtener_repartidores_disponibles()
    assert len(repartidores) > 0
    assert all(r['id'] for r in repartidores)

@then('puedo obtener la lista de pedidos pendientes de asignación')
def obtener_pedidos_pendientes_asignacion(delivery_servicio):
    pedidos = delivery_servicio.obtener_pedidos_pendientes_asignacion()
    assert isinstance(pedidos, list)

@then('puedo seguir el estado de la entrega')
def seguir_estado_entrega(delivery_servicio):
    pedido = DeliveryPedidoModelo.objects.last()
    estado = delivery_servicio.seguir_estado_entrega(pedido.pedido.id)
    assert estado['pedido_id'] == pedido.pedido.id
    assert 'estado' in estado
    assert 'direccion' in estado

@then('las estadísticas de delivery se actualizan correctamente')
def estadisticas_delivery_actualizadas(delivery_servicio):
    from datetime import datetime, timedelta
    fecha_inicio = datetime.now() - timedelta(days=1)
    fecha_fin = datetime.now() + timedelta(days=1)
    
    estadisticas = delivery_servicio.obtener_estadisticas_delivery(fecha_inicio, fecha_fin)
    assert 'total_pedidos_delivery' in estadisticas
    assert 'pedidos_entregados' in estadisticas
    assert estadisticas['total_pedidos_delivery'] >= 0
