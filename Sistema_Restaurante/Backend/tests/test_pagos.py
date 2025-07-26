# Backend/tests/test_pagos.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from decimal import Decimal
from django.utils import timezone
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.MedioPago_Modelo import MedioPagoModelo
from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
from Backend.Aplicacion.Servicios.Pagos_Servicio import PagosServicio

scenarios('features/pagos.feature')

@pytest.fixture
def pagos_servicio():
    return PagosServicio()

@pytest.fixture
def limpiar_pagos(db):
    TransaccionModelo.objects.all().delete()
    MedioPagoModelo.objects.all().delete()
    PedidoModelo.objects.all().delete()
    ClienteModelo.objects.all().delete()

@pytest.fixture
def cliente_test(limpiar_pagos):
    return ClienteModelo.objects.create(
        rut='12345678-9',
        nombre='Juan Pérez',
        correo='juan@test.com',
        telefono='987654321'
    )

@pytest.fixture
def pedido_test(cliente_test):
    return PedidoModelo.objects.create(
        cliente=cliente_test,
        estado='pendiente',
        tipo='presencial',
        total=Decimal('15000.00'),
        observaciones='Pedido de prueba'
    )

@pytest.fixture
def medio_pago_efectivo(limpiar_pagos):
    return MedioPagoModelo.objects.create(
        nombre='Efectivo',
        tipo='efectivo',
        comision_porcentaje=Decimal('0.0'),
        comision_fija=Decimal('0.0'),
        requiere_validacion_externa=False,
        activo=True
    )

@pytest.fixture
def medio_pago_tarjeta(limpiar_pagos):
    return MedioPagoModelo.objects.create(
        nombre='Tarjeta de Crédito',
        tipo='tarjeta_credito',
        comision_porcentaje=Decimal('2.5'),
        comision_fija=Decimal('100.0'),
        requiere_validacion_externa=True,
        activo=True
    )

# Given steps
@given('que existe un pedido con total $15.000')
def pedido_con_total_existe(pedido_test):
    assert pedido_test.total == Decimal('15000.00')

@given('que existe un medio de pago "Efectivo"')
def medio_pago_efectivo_existe(medio_pago_efectivo):
    assert MedioPagoModelo.objects.filter(nombre='Efectivo').exists()

@given('que existe un medio de pago "Tarjeta de Crédito"')
def medio_pago_tarjeta_existe(medio_pago_tarjeta):
    assert MedioPagoModelo.objects.filter(nombre='Tarjeta de Crédito').exists()

@given('que no existen transacciones para el pedido')
def no_transacciones_pedido(pedido_test):
    assert TransaccionModelo.objects.filter(pedido=pedido_test).count() == 0

@given('que existe una transacción pendiente')
def transaccion_pendiente_existe(pedido_test, medio_pago_tarjeta):
    return TransaccionModelo.objects.create(
        pedido=pedido_test,
        medio_pago=medio_pago_tarjeta,
        monto=Decimal('15000.00'),
        comision=Decimal('475.00'),  # 2.5% + $100
        estado='pendiente',
        codigo_referencia='TXN-TEST123'
    )

# When steps
@when('proceso un pago único de $15.000 en efectivo')
def procesar_pago_unico_efectivo(pagos_servicio, pedido_test, medio_pago_efectivo):
    datos_pago = {
        'pedido_id': pedido_test.id,
        'medio_pago_id': medio_pago_efectivo.id,
        'monto': 15000
    }
    resultado = pagos_servicio.procesar_pago_unico(datos_pago)
    return resultado

@when('proceso un pago único de $15.000 con tarjeta')
def procesar_pago_unico_tarjeta(pagos_servicio, pedido_test, medio_pago_tarjeta):
    datos_pago = {
        'pedido_id': pedido_test.id,
        'medio_pago_id': medio_pago_tarjeta.id,
        'monto': 15000
    }
    resultado = pagos_servicio.procesar_pago_unico(datos_pago)
    return resultado

@when('proceso un pago dividido: $10.000 efectivo y $5.000 tarjeta')
def procesar_pago_dividido(pagos_servicio, pedido_test, medio_pago_efectivo, medio_pago_tarjeta):
    datos_pago = {
        'pedido_id': pedido_test.id,
        'pagos': [
            {
                'medio_pago_id': medio_pago_efectivo.id,
                'monto': 10000
            },
            {
                'medio_pago_id': medio_pago_tarjeta.id,
                'monto': 5000
            }
        ]
    }
    resultado = pagos_servicio.procesar_pago_dividido(datos_pago)
    return resultado

@when('confirmo la transacción pendiente')
def confirmar_transaccion_pendiente(pagos_servicio, transaccion_pendiente_existe):
    transaccion = transaccion_pendiente_existe
    datos_confirmacion = {
        'codigo_autorizacion': 'AUTH123456',
        'datos_adicionales': {'banco': 'Banco Test'}
    }
    resultado = pagos_servicio.confirmar_pago_pendiente(transaccion.id, datos_confirmacion)
    return resultado

@when('rechazo la transacción pendiente')
def rechazar_transaccion_pendiente(pagos_servicio, transaccion_pendiente_existe):
    transaccion = transaccion_pendiente_existe
    resultado = pagos_servicio.rechazar_pago_pendiente(transaccion.id, 'Fondos insuficientes')
    return resultado

# Then steps
@then('la transacción se crea exitosamente')
def transaccion_creada_exitosamente(pedido_test):
    assert TransaccionModelo.objects.filter(pedido=pedido_test).exists()

@then('la transacción tiene estado "completada"')
def transaccion_estado_completada(pedido_test):
    transaccion = TransaccionModelo.objects.filter(pedido=pedido_test).last()
    assert transaccion.estado == 'completada'

@then('la transacción tiene estado "pendiente"')
def transaccion_estado_pendiente(pedido_test):
    transaccion = TransaccionModelo.objects.filter(pedido=pedido_test).last()
    assert transaccion.estado == 'pendiente'

@then('el pedido cambia a estado "pagado"')
def pedido_estado_pagado(pedido_test):
    pedido_test.refresh_from_db()
    assert pedido_test.estado == 'pagado'

@then('la comisión calculada es $0')
def comision_cero(pedido_test):
    transaccion = TransaccionModelo.objects.filter(pedido=pedido_test).last()
    assert transaccion.comision == Decimal('0.00')

@then('la comisión calculada es mayor a $0')
def comision_mayor_cero(pedido_test):
    transaccion = TransaccionModelo.objects.filter(pedido=pedido_test).last()
    assert transaccion.comision > Decimal('0.00')

@then('se crean múltiples transacciones')
def multiples_transacciones_creadas(pedido_test):
    transacciones = TransaccionModelo.objects.filter(pedido=pedido_test)
    assert transacciones.count() > 1

@then('la suma de montos coincide con el total del pedido')
def suma_montos_coincide_total(pedido_test):
    transacciones = TransaccionModelo.objects.filter(pedido=pedido_test, estado='completada')
    total_pagado = sum(t.monto for t in transacciones)
    assert total_pagado == pedido_test.total

@then('la transacción se confirma exitosamente')
def transaccion_confirmada_exitosamente():
    transaccion = TransaccionModelo.objects.filter(estado='completada').last()
    assert transaccion is not None
    assert transaccion.codigo_autorizacion is not None

@then('la transacción se rechaza correctamente')
def transaccion_rechazada_correctamente():
    transaccion = TransaccionModelo.objects.filter(estado='fallida').last()
    assert transaccion is not None
    assert transaccion.motivo_rechazo == 'Fondos insuficientes'

@then('puedo obtener el historial de pagos del pedido')
def obtener_historial_pagos(pagos_servicio, pedido_test):
    historial = pagos_servicio.obtener_historial_pagos_pedido(pedido_test.id)
    assert historial['pedido_id'] == pedido_test.id
    assert 'total_pedido' in historial
    assert 'transacciones' in historial

@then('puedo obtener la lista de medios de pago disponibles')
def obtener_medios_pago_disponibles(pagos_servicio):
    medios_pago = pagos_servicio.obtener_medios_pago_disponibles()
    assert len(medios_pago) > 0
    assert all('id' in mp for mp in medios_pago)

@then('puedo obtener las transacciones pendientes')
def obtener_transacciones_pendientes(pagos_servicio):
    transacciones = pagos_servicio.obtener_transacciones_pendientes()
    assert isinstance(transacciones, list)

@then('puedo generar reporte de ventas por medio de pago')
def generar_reporte_ventas(pagos_servicio):
    from datetime import datetime, timedelta
    fecha_inicio = datetime.now() - timedelta(days=1)
    fecha_fin = datetime.now() + timedelta(days=1)
    
    reporte = pagos_servicio.obtener_reporte_ventas_por_medio_pago(fecha_inicio, fecha_fin)
    assert 'resumen_general' in reporte
    assert 'detalle_por_medio_pago' in reporte

@then('el monto neto se calcula correctamente')
def monto_neto_calculado_correctamente(pedido_test):
    transacciones = TransaccionModelo.objects.filter(pedido=pedido_test)
    for transaccion in transacciones:
        monto_neto_esperado = transaccion.monto - transaccion.comision
        assert transaccion.monto_neto() == monto_neto_esperado

@then('los códigos de referencia son únicos')
def codigos_referencia_unicos():
    transacciones = TransaccionModelo.objects.all()
    codigos = [t.codigo_referencia for t in transacciones]
    assert len(codigos) == len(set(codigos))  # Sin duplicados
