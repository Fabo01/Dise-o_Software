# Backend/tests/step_definitions/delivery_steps.py
from pytest_bdd import given, when, then, parsers
import pytest
from Backend.Infraestructura.Modelos.DeliveryPedido_Modelo import DeliveryPedidoModelo
from Backend.Infraestructura.Modelos.DeliveryRepartidor_Modelo import DeliveryRepartidorModelo
from Backend.Infraestructura.Modelos.DeliveryApp_Modelo import DeliveryAppModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

# Dado que existe un repartidor disponible
@given(parsers.parse('que existe un repartidor "{nombre}" disponible'))
def repartidor_disponible(nombre, db):
    app_delivery = DeliveryAppModelo.objects.create(
        nombre="App Propia",
        activa=True,
        comision_porcentaje=0
    )
    
    repartidor = DeliveryRepartidorModelo.objects.create(
        nombre=nombre,
        telefono="123456789",
        email=f"{nombre.lower()}@delivery.com",
        delivery_app=app_delivery,
        activo=True,
        ubicacion_latitud=-33.4489,
        ubicacion_longitud=-70.6693
    )
    return repartidor

# Dado que existe un pedido delivery pendiente
@given(parsers.parse('que existe un pedido delivery pendiente con ID {pedido_id:d}'))
def pedido_delivery_pendiente(pedido_id, db):
    cliente = ClienteModelo.objects.create(
        rut="12345678-9",
        nombre="Cliente Test",
        email="cliente@test.com",
        telefono="987654321"
    )
    
    pedido = PedidoModelo.objects.create(
        id=pedido_id,
        cliente=cliente,
        estado="pendiente",
        total=15000
    )
    
    delivery_pedido = DeliveryPedidoModelo.objects.create(
        pedido=pedido,
        direccion_entrega="Av. Providencia 123, Santiago",
        telefono_contacto="987654321",
        tiempo_estimado_minutos=30,
        costo_envio=2000,
        estado_delivery="pendiente"
    )
    
    return delivery_pedido

# Cuando asigno el repartidor al pedido
@when(parsers.parse('asigno el repartidor "{nombre}" al pedido {pedido_id:d}'))
def asignar_repartidor(nombre, pedido_id, db):
    repartidor = DeliveryRepartidorModelo.objects.get(nombre=nombre)
    delivery_pedido = DeliveryPedidoModelo.objects.get(pedido_id=pedido_id)
    
    delivery_pedido.repartidor = repartidor
    delivery_pedido.estado_delivery = "asignado"
    delivery_pedido.save()

# Entonces el pedido debe tener repartidor asignado
@then(parsers.parse('el pedido {pedido_id:d} debe tener repartidor asignado'))
def verificar_repartidor_asignado(pedido_id, db):
    delivery_pedido = DeliveryPedidoModelo.objects.get(pedido_id=pedido_id)
    assert delivery_pedido.repartidor is not None
    assert delivery_pedido.estado_delivery == "asignado"

# Entonces el repartidor debe estar ocupado
@then(parsers.parse('el repartidor "{nombre}" debe estar ocupado'))
def verificar_repartidor_ocupado(nombre, db):
    repartidor = DeliveryRepartidorModelo.objects.get(nombre=nombre)
    assert not repartidor.esta_disponible()

# Dado que existe un pedido en estado "en_ruta"
@given(parsers.parse('que existe un pedido en estado "en_ruta" con ID {pedido_id:d}'))
def pedido_en_ruta(pedido_id, db, repartidor_disponible):
    cliente = ClienteModelo.objects.create(
        rut="87654321-0",
        nombre="Cliente Ruta",
        email="ruta@test.com",
        telefono="123123123"
    )
    
    pedido = PedidoModelo.objects.create(
        id=pedido_id,
        cliente=cliente,
        estado="preparando",
        total=12000
    )
    
    delivery_pedido = DeliveryPedidoModelo.objects.create(
        pedido=pedido,
        direccion_entrega="Av. Las Condes 456, Santiago",
        telefono_contacto="123123123",
        tiempo_estimado_minutos=25,
        costo_envio=1500,
        estado_delivery="en_ruta",
        repartidor=repartidor_disponible
    )
    
    return delivery_pedido

# Cuando marco el pedido como entregado
@when(parsers.parse('marco el pedido {pedido_id:d} como entregado'))
def marcar_entregado(pedido_id, db):
    delivery_pedido = DeliveryPedidoModelo.objects.get(pedido_id=pedido_id)
    delivery_pedido.estado_delivery = "entregado"
    delivery_pedido.save()
    
    # También actualizar el pedido principal
    pedido = delivery_pedido.pedido
    pedido.estado = "entregado"
    pedido.save()

# Entonces el pedido debe estar en estado "entregado"
@then(parsers.parse('el pedido {pedido_id:d} debe estar en estado "entregado"'))
def verificar_pedido_entregado(pedido_id, db):
    delivery_pedido = DeliveryPedidoModelo.objects.get(pedido_id=pedido_id)
    assert delivery_pedido.estado_delivery == "entregado"
    assert delivery_pedido.pedido.estado == "entregado"

# Entonces el repartidor debe estar disponible nuevamente
@then(parsers.parse('el repartidor debe estar disponible nuevamente'))
def verificar_repartidor_disponible(db):
    # Buscar cualquier repartidor que debería estar disponible
    repartidores = DeliveryRepartidorModelo.objects.filter(activo=True)
    disponibles = [r for r in repartidores if r.esta_disponible()]
    assert len(disponibles) > 0

# Dado que no hay repartidores disponibles
@given('que no hay repartidores disponibles')
def no_repartidores_disponibles(db):
    # Crear repartidores ocupados
    app_delivery = DeliveryAppModelo.objects.create(
        nombre="App Test",
        activa=True,
        comision_porcentaje=0
    )
    
    cliente = ClienteModelo.objects.create(
        rut="11111111-1",
        nombre="Cliente Ocupado",
        email="ocupado@test.com",
        telefono="111111111"
    )
    
    pedido = PedidoModelo.objects.create(
        cliente=cliente,
        estado="preparando",
        total=10000
    )
    
    repartidor = DeliveryRepartidorModelo.objects.create(
        nombre="Repartidor Ocupado",
        telefono="999999999",
        email="ocupado@delivery.com",
        delivery_app=app_delivery,
        activo=True,
        ubicacion_latitud=-33.4489,
        ubicacion_longitud=-70.6693
    )
    
    # Asignar pedido para que esté ocupado
    DeliveryPedidoModelo.objects.create(
        pedido=pedido,
        direccion_entrega="Dirección ocupada",
        telefono_contacto="999999999",
        tiempo_estimado_minutos=30,
        costo_envio=2000,
        estado_delivery="en_ruta",
        repartidor=repartidor
    )

# Cuando intento asignar un repartidor
@when(parsers.parse('intento asignar un repartidor al pedido {pedido_id:d}'))
def intentar_asignar_repartidor(pedido_id, db):
    # Simular intento de asignación
    delivery_pedido = DeliveryPedidoModelo.objects.get(pedido_id=pedido_id)
    repartidores_disponibles = [r for r in DeliveryRepartidorModelo.objects.filter(activo=True) if r.esta_disponible()]
    
    if not repartidores_disponibles:
        # No hacer nada si no hay repartidores disponibles
        pass
    else:
        delivery_pedido.repartidor = repartidores_disponibles[0]
        delivery_pedido.estado_delivery = "asignado"
        delivery_pedido.save()

# Entonces el pedido debe permanecer sin asignar
@then(parsers.parse('el pedido {pedido_id:d} debe permanecer sin asignar'))
def verificar_pedido_sin_asignar(pedido_id, db):
    delivery_pedido = DeliveryPedidoModelo.objects.get(pedido_id=pedido_id)
    assert delivery_pedido.repartidor is None
    assert delivery_pedido.estado_delivery == "pendiente"
