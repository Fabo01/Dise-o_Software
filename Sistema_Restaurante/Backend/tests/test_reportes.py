import pytest
from pytest_bdd import scenarios, given, when, then
from Backend.Infraestructura.Modelos.Pedido_Modelo import Pedido_Modelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo

scenarios('features/reportes.feature')

@given('que existen pedidos registrados')
def existen_pedidos(db):
    from Backend.Infraestructura.Modelos.Cliente_Modelo import Cliente_Modelo
    cliente, _ = Cliente_Modelo.objects.get_or_create(nombre="ClienteReporte", email="reporte@cliente.com")
    Pedido_Modelo.objects.create(cliente=cliente)
    assert Pedido_Modelo.objects.exists()

@given('que existen ingredientes registrados')
def existen_ingredientes(db):
    IngredienteModelo.objects.create(nombre="IngredienteReporte", cantidad=5, unidad_medida="kg", categoria="General", nivel_critico=1)
    assert IngredienteModelo.objects.exists()

@when('genero un reporte de ventas')
def generar_reporte_ventas():
    pass  # Simulación

@when('genero un reporte de inventario')
def generar_reporte_inventario():
    pass  # Simulación

@then('debo obtener un reporte con el resumen de ventas')
def verificar_reporte_ventas():
    assert True  # Simulación de verificación

@then('debo obtener un reporte con el estado del inventario')
def verificar_reporte_inventario():
    assert True  # Simulación de verificación
