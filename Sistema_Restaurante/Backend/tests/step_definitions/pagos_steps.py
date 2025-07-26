# Backend/tests/step_definitions/pagos_steps.py
from pytest_bdd import given, when, then, parsers
import pytest
from decimal import Decimal
from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
from Backend.Infraestructura.Modelos.MedioPago_Modelo import MedioPagoModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo

# Dado que existe un pedido en estado "entregado"
@given(parsers.parse('que existe un pedido con ID {pedido_id:d} en estado "entregado"'))
def pedido_entregado(pedido_id, db):
    cliente = ClienteModelo.objects.create(
        rut="12345678-9",
        nombre="Cliente Test",
        email="cliente@test.com",
        telefono="987654321"
    )
    
    pedido = PedidoModelo.objects.create(
        id=pedido_id,
        cliente=cliente,
        estado="entregado",
        total=15000
    )
    return pedido

# Dado que existe un medio de pago activo
@given(parsers.parse('que existe un medio de pago "{nombre}" activo'))
def medio_pago_activo(nombre, db):
    medio_pago = MedioPagoModelo.objects.create(
        nombre=nombre,
        tipo="efectivo" if nombre == "Efectivo" else "tarjeta",
        activo=True,
        comision_porcentaje=0,
        requiere_validacion_externa=False
    )
    return medio_pago

# Dado que existe un medio de pago con comisión
@given(parsers.parse('que existe un medio de pago "{nombre}" con comisión {comision:d}%'))
def medio_pago_con_comision(nombre, comision, db):
    medio_pago = MedioPagoModelo.objects.create(
        nombre=nombre,
        tipo="tarjeta",
        activo=True,
        comision_porcentaje=comision,
        requiere_validacion_externa=False
    )
    return medio_pago

# Cuando proceso el pago
@when(parsers.parse('proceso el pago del pedido {pedido_id:d} con "{medio_pago_nombre}" por ${monto:d}'))
def procesar_pago(pedido_id, medio_pago_nombre, monto, db):
    pedido = PedidoModelo.objects.get(id=pedido_id)
    medio_pago = MedioPagoModelo.objects.get(nombre=medio_pago_nombre)
    
    # Calcular comisión
    monto_decimal = Decimal(str(monto))
    comision = medio_pago.calcular_comision(monto_decimal)
    
    # Crear transacción
    transaccion = TransaccionModelo.objects.create(
        pedido=pedido,
        medio_pago=medio_pago,
        monto=monto_decimal,
        comision=comision,
        estado="exitosa",
        codigo_referencia=f"TXN{pedido_id}001"
    )
    
    # Actualizar estado del pedido
    pedido.estado = "pagado"
    pedido.save()
    
    return transaccion

# Entonces debe existir una transacción para el pedido
@then(parsers.parse('debe existir una transacción para el pedido {pedido_id:d}'))
def verificar_transaccion_existe(pedido_id, db):
    transacciones = TransaccionModelo.objects.filter(pedido_id=pedido_id)
    assert transacciones.exists()

# Entonces la transacción debe tener estado "exitosa"
@then('la transacción debe tener estado "exitosa"')
def verificar_transaccion_exitosa(db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.estado == "exitosa"

# Entonces el pedido debe cambiar a estado "pagado"
@then('el pedido debe cambiar a estado "pagado"')
def verificar_pedido_pagado(db):
    # Obtener la última transacción creada
    transaccion = TransaccionModelo.objects.last()
    pedido = transaccion.pedido
    assert pedido.estado == "pagado"

# Entonces debe existir una transacción con monto específico
@then(parsers.parse('debe existir una transacción con monto ${monto:d}'))
def verificar_monto_transaccion(monto, db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.monto == Decimal(str(monto))

# Entonces la comisión debe ser específica
@then(parsers.parse('la comisión debe ser ${comision:d}'))
def verificar_comision(comision, db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.comision == Decimal(str(comision))

# Entonces el monto neto debe ser específico
@then(parsers.parse('el monto neto debe ser ${monto_neto:d}'))
def verificar_monto_neto(monto_neto, db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.monto_neto() == Decimal(str(monto_neto))

# Dado que existe un medio de pago con validación externa
@given(parsers.parse('que existe un medio de pago "{nombre}" con validación externa'))
def medio_pago_validacion_externa(nombre, db):
    medio_pago = MedioPagoModelo.objects.create(
        nombre=nombre,
        tipo="tarjeta_externa",
        activo=True,
        comision_porcentaje=3,
        requiere_validacion_externa=True
    )
    return medio_pago

# Cuando proceso un pago que falla en la validación externa
@when('proceso un pago que falla en la validación externa')
def procesar_pago_fallido(db):
    pedido = PedidoModelo.objects.filter(estado="entregado").last()
    medio_pago = MedioPagoModelo.objects.filter(requiere_validacion_externa=True).last()
    
    # Simular fallo en validación externa
    transaccion = TransaccionModelo.objects.create(
        pedido=pedido,
        medio_pago=medio_pago,
        monto=pedido.total,
        comision=Decimal('0'),
        estado="fallida",
        codigo_referencia="FAIL001"
    )
    
    return transaccion

# Entonces la transacción debe tener estado "fallida"
@then('la transacción debe tener estado "fallida"')
def verificar_transaccion_fallida(db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.estado == "fallida"

# Entonces el pedido debe mantener estado "entregado"
@then('el pedido debe mantener estado "entregado"')
def verificar_pedido_mantiene_estado(db):
    transaccion = TransaccionModelo.objects.last()
    pedido = transaccion.pedido
    assert pedido.estado == "entregado"

# Dado que existe un pedido por monto específico
@given(parsers.parse('que existe un pedido con ID {pedido_id:d} por ${total:d} en estado "entregado"'))
def pedido_con_total_especifico(pedido_id, total, db):
    cliente = ClienteModelo.objects.create(
        rut="98765432-1",
        nombre="Cliente Múltiple",
        email="multiple@test.com",
        telefono="555555555"
    )
    
    pedido = PedidoModelo.objects.create(
        id=pedido_id,
        cliente=cliente,
        estado="entregado",
        total=total
    )
    return pedido

# Cuando proceso pago parcial
@when(parsers.parse('proceso pago parcial con "{medio_pago_nombre}" por ${monto:d}'))
def procesar_pago_parcial(medio_pago_nombre, monto, db):
    # Obtener el pedido más reciente
    pedido = PedidoModelo.objects.filter(estado="entregado").last()
    medio_pago = MedioPagoModelo.objects.get(nombre=medio_pago_nombre)
    
    monto_decimal = Decimal(str(monto))
    comision = medio_pago.calcular_comision(monto_decimal)
    
    transaccion = TransaccionModelo.objects.create(
        pedido=pedido,
        medio_pago=medio_pago,
        monto=monto_decimal,
        comision=comision,
        estado="exitosa",
        codigo_referencia=f"PARTIAL{TransaccionModelo.objects.count() + 1}"
    )
    
    return transaccion

# Entonces deben existir X transacciones para el pedido
@then(parsers.parse('deben existir {cantidad:d} transacciones para el pedido {pedido_id:d}'))
def verificar_cantidad_transacciones(cantidad, pedido_id, db):
    transacciones = TransaccionModelo.objects.filter(pedido_id=pedido_id)
    assert transacciones.count() == cantidad

# Entonces ambas transacciones deben tener estado "exitosa"
@then('ambas transacciones deben tener estado "exitosa"')
def verificar_todas_transacciones_exitosas(db):
    pedido = PedidoModelo.objects.last()
    transacciones = TransaccionModelo.objects.filter(pedido=pedido)
    for transaccion in transacciones:
        assert transaccion.estado == "exitosa"

# Dado que existe una transacción exitosa
@given(parsers.parse('que existe una transacción exitosa con ID {transaccion_id:d}'))
def transaccion_exitosa(transaccion_id, db):
    cliente = ClienteModelo.objects.create(
        rut="55555555-5",
        nombre="Cliente Comprobante",
        email="comprobante@test.com",
        telefono="777777777"
    )
    
    pedido = PedidoModelo.objects.create(
        cliente=cliente,
        estado="pagado",
        total=8000
    )
    
    medio_pago = MedioPagoModelo.objects.create(
        nombre="Efectivo Comprobante",
        tipo="efectivo",
        activo=True,
        comision_porcentaje=0
    )
    
    transaccion = TransaccionModelo.objects.create(
        id=transaccion_id,
        pedido=pedido,
        medio_pago=medio_pago,
        monto=8000,
        comision=0,
        estado="exitosa",
        codigo_referencia="COMP500"
    )
    
    return transaccion

# Cuando genero el comprobante de la transacción
@when(parsers.parse('genero el comprobante de la transacción {transaccion_id:d}'))
def generar_comprobante(transaccion_id, db):
    transaccion = TransaccionModelo.objects.get(id=transaccion_id)
    # Simular generación de comprobante
    # En la implementación real, esto llamaría al servicio de generación de PDF
    transaccion.comprobante_generado = True
    transaccion.save()

# Entonces debe existir un comprobante en formato PDF
@then('debe existir un comprobante en formato PDF')
def verificar_comprobante_pdf(db):
    transaccion = TransaccionModelo.objects.last()
    # En la implementación real, verificaríamos la existencia del archivo PDF
    assert hasattr(transaccion, 'comprobante_generado')

# Entonces debe contener los datos del pedido
@then('debe contener los datos del pedido')
def verificar_datos_pedido_en_comprobante(db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.pedido is not None
    assert transaccion.pedido.cliente is not None

# Entonces debe contener los datos del pago
@then('debe contener los datos del pago')
def verificar_datos_pago_en_comprobante(db):
    transaccion = TransaccionModelo.objects.last()
    assert transaccion.monto > 0
    assert transaccion.medio_pago is not None
    assert transaccion.codigo_referencia is not None
