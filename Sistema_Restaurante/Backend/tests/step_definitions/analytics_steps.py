# Backend/tests/step_definitions/analytics_steps.py
from pytest_bdd import given, when, then, parsers
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
from Backend.Infraestructura.Modelos.MedioPago_Modelo import MedioPagoModelo
from Backend.Aplicacion.Servicios.Analytics_Servicio import AnalyticsServicio

# Dado que existen pedidos en el sistema
@given(parsers.parse('que existen {cantidad:d} pedidos realizados en los últimos {dias:d} días'))
def pedidos_en_sistema(cantidad, dias, db):
    clientes = []
    for i in range(min(cantidad, 5)):  # Crear máximo 5 clientes
        cliente = ClienteModelo.objects.create(
            rut=f"1234567{i}-{i}",
            nombre=f"Cliente {i+1}",
            email=f"cliente{i+1}@test.com",
            telefono=f"98765432{i}"
        )
        clientes.append(cliente)
    
    fecha_inicio = datetime.now() - timedelta(days=dias)
    
    for i in range(cantidad):
        cliente = clientes[i % len(clientes)]
        fecha_pedido = fecha_inicio + timedelta(
            days=i * dias // cantidad,
            hours=(i * 3) % 24
        )
        
        pedido = PedidoModelo.objects.create(
            cliente=cliente,
            estado="pagado",
            total=5000 + (i * 1000),
            fecha_creacion=fecha_pedido
        )
        
        # Crear transacción asociada
        medio_pago = MedioPagoModelo.objects.get_or_create(
            nombre="Efectivo Test",
            defaults={
                'tipo': 'efectivo',
                'activo': True,
                'comision_porcentaje': 0
            }
        )[0]
        
        TransaccionModelo.objects.create(
            pedido=pedido,
            medio_pago=medio_pago,
            monto=pedido.total,
            comision=0,
            estado="exitosa",
            fecha_creacion=fecha_pedido
        )

# Dado que existen ingredientes con movimientos de stock
@given(parsers.parse('que existen {cantidad:d} ingredientes con movimientos de stock'))
def ingredientes_con_stock(cantidad, db):
    for i in range(cantidad):
        IngredienteModelo.objects.create(
            nombre=f"Ingrediente {i+1}",
            cantidad_disponible=100 - (i * 10),
            unidad_medida="kg",
            precio_unitario=1000 + (i * 500),
            stock_critico=10 + i,
            categoria="categoria_test"
        )

# Cuando solicito los KPIs de ventas del último mes
@when('solicito los KPIs de ventas del último mes')
def solicitar_kpis_ventas(db):
    analytics_service = AnalyticsServicio()
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    # Guardar los KPIs en el contexto de la prueba
    pytest.kpis_ventas = analytics_service.obtener_kpis_ventas(fecha_inicio, fecha_fin)

# Entonces debo recibir las métricas de ventas totales
@then('debo recibir las métricas de ventas totales')
def verificar_metricas_ventas(db):
    assert hasattr(pytest, 'kpis_ventas')
    kpis = pytest.kpis_ventas
    
    assert 'ventas_totales' in kpis
    assert 'cantidad_pedidos' in kpis
    assert 'ticket_promedio' in kpis
    assert isinstance(kpis['ventas_totales'], (int, float, Decimal))
    assert kpis['cantidad_pedidos'] >= 0

# Entonces debo recibir las métricas de crecimiento
@then('debo recibir las métricas de crecimiento')
def verificar_metricas_crecimiento(db):
    kpis = pytest.kpis_ventas
    
    assert 'crecimiento_ventas' in kpis
    assert 'crecimiento_pedidos' in kpis
    # Los valores de crecimiento pueden ser None si no hay datos del período anterior

# Cuando solicito el análisis de inventario
@when('solicito el análisis de inventario')
def solicitar_analisis_inventario(db):
    analytics_service = AnalyticsServicio()
    pytest.analisis_inventario = analytics_service.obtener_analisis_inventario()

# Entonces debo recibir la lista de ingredientes con stock crítico
@then('debo recibir la lista de ingredientes con stock crítico')
def verificar_stock_critico(db):
    assert hasattr(pytest, 'analisis_inventario')
    analisis = pytest.analisis_inventario
    
    assert 'ingredientes_stock_critico' in analisis
    assert isinstance(analisis['ingredientes_stock_critico'], list)

# Entonces debo recibir las métricas de rotación de inventario
@then('debo recibir las métricas de rotación de inventario')
def verificar_rotacion_inventario(db):
    analisis = pytest.analisis_inventario
    
    assert 'rotacion_inventario' in analisis
    assert 'valor_total_inventario' in analisis
    assert isinstance(analisis['valor_total_inventario'], (int, float, Decimal))

# Cuando genero un reporte de ventas para el período
@when(parsers.parse('genero un reporte de ventas para el período de {dias:d} días'))
def generar_reporte_ventas(dias, db):
    analytics_service = AnalyticsServicio()
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=dias)
    
    pytest.reporte_ventas = analytics_service.generar_reporte_ventas(fecha_inicio, fecha_fin)

# Entonces el reporte debe contener un resumen de ventas
@then('el reporte debe contener un resumen de ventas')
def verificar_resumen_ventas(db):
    assert hasattr(pytest, 'reporte_ventas')
    reporte = pytest.reporte_ventas
    
    assert 'resumen' in reporte
    resumen = reporte['resumen']
    
    assert 'total_ventas' in resumen
    assert 'total_pedidos' in resumen
    assert 'ticket_promedio' in resumen

# Entonces el reporte debe contener un desglose por día
@then('el reporte debe contener un desglose por día')
def verificar_desglose_diario(db):
    reporte = pytest.reporte_ventas
    
    assert 'ventas_por_dia' in reporte
    assert isinstance(reporte['ventas_por_dia'], list)

# Entonces el reporte debe contener los métodos de pago utilizados
@then('el reporte debe contener los métodos de pago utilizados')
def verificar_metodos_pago(db):
    reporte = pytest.reporte_ventas
    
    assert 'metodos_pago' in reporte
    assert isinstance(reporte['metodos_pago'], dict)

# Dado que existe un período de comparación
@given(parsers.parse('que existe un período de comparación de {dias:d} días'))
def periodo_comparacion(dias, db):
    # Crear pedidos para el período anterior
    fecha_fin_anterior = datetime.now() - timedelta(days=dias)
    fecha_inicio_anterior = fecha_fin_anterior - timedelta(days=dias)
    
    cliente = ClienteModelo.objects.create(
        rut="99999999-9",
        nombre="Cliente Comparación",
        email="comparacion@test.com",
        telefono="111111111"
    )
    
    medio_pago = MedioPagoModelo.objects.get_or_create(
        nombre="Tarjeta Test",
        defaults={
            'tipo': 'tarjeta',
            'activo': True,
            'comision_porcentaje': 2
        }
    )[0]
    
    # Crear algunos pedidos en el período anterior
    for i in range(5):
        fecha_pedido = fecha_inicio_anterior + timedelta(days=i)
        
        pedido = PedidoModelo.objects.create(
            cliente=cliente,
            estado="pagado",
            total=3000 + (i * 500),
            fecha_creacion=fecha_pedido
        )
        
        TransaccionModelo.objects.create(
            pedido=pedido,
            medio_pago=medio_pago,
            monto=pedido.total,
            comision=pedido.total * Decimal('0.02'),
            estado="exitosa",
            fecha_creacion=fecha_pedido
        )

# Cuando solicito el análisis comparativo
@when('solicito el análisis comparativo')
def solicitar_analisis_comparativo(db):
    analytics_service = AnalyticsServicio()
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    pytest.analisis_comparativo = analytics_service.obtener_analisis_comparativo(fecha_inicio, fecha_fin)

# Entonces debo recibir las métricas comparativas
@then('debo recibir las métricas comparativas')
def verificar_metricas_comparativas(db):
    assert hasattr(pytest, 'analisis_comparativo')
    analisis = pytest.analisis_comparativo
    
    assert 'periodo_actual' in analisis
    assert 'periodo_anterior' in analisis
    assert 'comparacion' in analisis
    
    comparacion = analisis['comparacion']
    assert 'variacion_ventas' in comparacion
    assert 'variacion_pedidos' in comparacion

# Entonces debo recibir el porcentaje de crecimiento
@then('debo recibir el porcentaje de crecimiento')
def verificar_porcentaje_crecimiento(db):
    analisis = pytest.analisis_comparativo
    comparacion = analisis['comparacion']
    
    # Los porcentajes pueden ser None o números
    assert 'porcentaje_crecimiento_ventas' in comparacion
    assert 'porcentaje_crecimiento_pedidos' in comparacion

# Cuando solicito exportar el reporte en formato JSON
@when('solicito exportar el reporte en formato JSON')
def exportar_reporte_json(db):
    analytics_service = AnalyticsServicio()
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=7)
    
    pytest.reporte_exportado = analytics_service.exportar_reporte(
        fecha_inicio, fecha_fin, formato='json'
    )

# Entonces debo recibir un archivo JSON válido
@then('debo recibir un archivo JSON válido')
def verificar_json_valido(db):
    assert hasattr(pytest, 'reporte_exportado')
    reporte = pytest.reporte_exportado
    
    # Verificar que es un diccionario válido (JSON serializable)
    assert isinstance(reporte, dict)
    assert 'metadata' in reporte
    assert 'datos' in reporte
    
    metadata = reporte['metadata']
    assert 'fecha_generacion' in metadata
    assert 'formato' in metadata
    assert metadata['formato'] == 'json'
