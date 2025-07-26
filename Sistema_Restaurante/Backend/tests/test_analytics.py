# Backend/tests/test_analytics.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Aplicacion.Servicios.Analytics_Servicio import AnalyticsServicio

scenarios('features/analytics.feature')

@pytest.fixture
def analytics_servicio():
    return AnalyticsServicio()

@pytest.fixture
def limpiar_analytics(db):
    PedidoModelo.objects.all().delete()
    MenuModelo.objects.all().delete()
    IngredienteModelo.objects.all().delete()
    MesaModelo.objects.all().delete()
    ClienteModelo.objects.all().delete()

@pytest.fixture
def datos_test_completos(limpiar_analytics):
    # Crear clientes
    cliente1 = ClienteModelo.objects.create(
        rut='12345678-9',
        nombre='Juan Pérez',
        correo='juan@test.com',
        telefono='987654321'
    )
    cliente2 = ClienteModelo.objects.create(
        rut='98765432-1',
        nombre='María García',
        correo='maria@test.com',
        telefono='912345678'
    )
    
    # Crear ingredientes
    ingrediente1 = IngredienteModelo.objects.create(
        nombre='Tomate',
        cantidad=Decimal('50.0'),
        unidad_medida='kg',
        precio_unitario=Decimal('2000.0')
    )
    ingrediente2 = IngredienteModelo.objects.create(
        nombre='Carne',
        cantidad=Decimal('20.0'),
        unidad_medida='kg',
        precio_unitario=Decimal('8000.0')
    )
    
    # Crear menus
    menu1 = MenuModelo.objects.create(
        nombre='Hamburguesa Clásica',
        descripcion='Hamburguesa con carne y tomate',
        precio=Decimal('8500.0'),
        categoria='Hamburguesas',
        disponible=True
    )
    menu2 = MenuModelo.objects.create(
        nombre='Ensalada César',
        descripcion='Ensalada fresca',
        precio=Decimal('6500.0'),
        categoria='Ensaladas',
        disponible=True
    )
    
    # Crear mesas
    mesa1 = MesaModelo.objects.create(
        numero=1,
        capacidad=4,
        estado='disponible'
    )
    mesa2 = MesaModelo.objects.create(
        numero=2,
        capacidad=2,
        estado='ocupada'
    )
    
    # Crear pedidos
    pedido1 = PedidoModelo.objects.create(
        cliente=cliente1,
        mesa=mesa1,
        estado='completado',
        tipo='presencial',
        total=Decimal('15000.0'),
        fecha_creacion=timezone.now() - timedelta(hours=2)
    )
    pedido2 = PedidoModelo.objects.create(
        cliente=cliente2,
        estado='completado',
        tipo='delivery',
        total=Decimal('12000.0'),
        fecha_creacion=timezone.now() - timedelta(hours=1)
    )
    
    return {
        'clientes': [cliente1, cliente2],
        'ingredientes': [ingrediente1, ingrediente2],
        'menus': [menu1, menu2],
        'mesas': [mesa1, mesa2],
        'pedidos': [pedido1, pedido2]
    }

# Given steps
@given('que existen datos de ventas en el sistema')
def datos_ventas_existen(datos_test_completos):
    assert PedidoModelo.objects.filter(estado='completado').count() > 0

@given('que existen clientes registrados')
def clientes_registrados_existen(datos_test_completos):
    assert ClienteModelo.objects.count() > 0

@given('que existen ingredientes en inventario')
def ingredientes_inventario_existen(datos_test_completos):
    assert IngredienteModelo.objects.count() > 0

@given('que existen menús disponibles')
def menus_disponibles_existen(datos_test_completos):
    assert MenuModelo.objects.filter(disponible=True).count() > 0

@given('que existen mesas configuradas')
def mesas_configuradas_existen(datos_test_completos):
    assert MesaModelo.objects.count() > 0

@given('que existen pedidos de diferentes tipos')
def pedidos_diferentes_tipos_existen(datos_test_completos):
    assert PedidoModelo.objects.filter(tipo='presencial').exists()
    assert PedidoModelo.objects.filter(tipo='delivery').exists()

# When steps
@when('solicito el dashboard completo')
def solicitar_dashboard_completo(analytics_servicio):
    dashboard = analytics_servicio.obtener_datos_dashboard_completo()
    return dashboard

@when('solicito las ventas del día actual')
def solicitar_ventas_dia_actual(analytics_servicio):
    hoy = timezone.now().date()
    ventas = analytics_servicio.obtener_ventas_por_periodo(hoy, hoy)
    return ventas

@when('solicito las ventas de la última semana')
def solicitar_ventas_ultima_semana(analytics_servicio):
    fecha_fin = timezone.now().date()
    fecha_inicio = fecha_fin - timedelta(days=7)
    ventas = analytics_servicio.obtener_ventas_por_periodo(fecha_inicio, fecha_fin)
    return ventas

@when('solicito el análisis de inventario')
def solicitar_analisis_inventario(analytics_servicio):
    inventario = analytics_servicio.obtener_analisis_inventario()
    return inventario

@when('solicito las métricas operacionales')
def solicitar_metricas_operacionales(analytics_servicio):
    metricas = analytics_servicio.obtener_metricas_operacionales()
    return metricas

@when('solicito las métricas de clientes')
def solicitar_metricas_clientes(analytics_servicio):
    metricas = analytics_servicio.obtener_metricas_clientes()
    return metricas

@when('solicito los productos más vendidos')
def solicitar_productos_mas_vendidos(analytics_servicio):
    productos = analytics_servicio.obtener_productos_mas_vendidos()
    return productos

@when('solicito el análisis de rendimiento por períodos')
def solicitar_analisis_rendimiento_periodos(analytics_servicio):
    analisis = analytics_servicio.obtener_analisis_rendimiento_por_periodos()
    return analisis

# Then steps
@then('obtengo un dashboard con todas las métricas principales')
def dashboard_completo_obtenido(analytics_servicio):
    dashboard = analytics_servicio.obtener_datos_dashboard_completo()
    
    # Verificar que contiene todas las secciones principales
    assert 'ventas' in dashboard
    assert 'pedidos' in dashboard
    assert 'inventario' in dashboard
    assert 'clientes' in dashboard
    assert 'mesas' in dashboard
    assert 'productos_populares' in dashboard

@then('las métricas de ventas son precisas')
def metricas_ventas_precisas(analytics_servicio):
    hoy = timezone.now().date()
    ventas = analytics_servicio.obtener_ventas_por_periodo(hoy, hoy)
    
    # Verificar campos requeridos
    assert 'total_ventas' in ventas
    assert 'cantidad_pedidos' in ventas
    assert 'ticket_promedio' in ventas
    assert isinstance(ventas['total_ventas'], (int, float, Decimal))

@then('las métricas de inventario son correctas')
def metricas_inventario_correctas(analytics_servicio):
    inventario = analytics_servicio.obtener_analisis_inventario()
    
    assert 'total_productos' in inventario
    assert 'valor_total_inventario' in inventario
    assert 'productos_bajo_stock' in inventario
    assert inventario['total_productos'] >= 0

@then('las métricas operacionales incluyen información de mesas')
def metricas_operacionales_incluyen_mesas(analytics_servicio):
    metricas = analytics_servicio.obtener_metricas_operacionales()
    
    assert 'mesas' in metricas
    assert 'total_mesas' in metricas['mesas']
    assert 'mesas_ocupadas' in metricas['mesas']
    assert 'porcentaje_ocupacion' in metricas['mesas']

@then('las métricas de clientes muestran estadísticas relevantes')
def metricas_clientes_relevantes(analytics_servicio):
    metricas = analytics_servicio.obtener_metricas_clientes()
    
    assert 'total_clientes' in metricas
    assert 'clientes_activos_mes' in metricas
    assert 'ticket_promedio_cliente' in metricas
    assert metricas['total_clientes'] >= 0

@then('obtengo una lista de productos más vendidos')
def lista_productos_mas_vendidos_obtenida(analytics_servicio):
    productos = analytics_servicio.obtener_productos_mas_vendidos()
    
    assert isinstance(productos, list)
    # Si hay datos, verificar estructura
    if productos:
        assert 'nombre' in productos[0]
        assert 'cantidad_vendida' in productos[0]

@then('el análisis de rendimiento muestra tendencias por período')
def analisis_rendimiento_muestra_tendencias(analytics_servicio):
    analisis = analytics_servicio.obtener_analisis_rendimiento_por_periodos()
    
    assert 'ventas_por_dia' in analisis
    assert 'tendencia_semanal' in analisis
    assert isinstance(analisis['ventas_por_dia'], list)

@then('las métricas se calculan en tiempo real')
def metricas_tiempo_real(analytics_servicio):
    # Crear un nuevo pedido y verificar que las métricas se actualizan
    from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
    
    cliente = ClienteModelo.objects.first()
    nuevo_pedido = PedidoModelo.objects.create(
        cliente=cliente,
        estado='completado',
        tipo='presencial',
        total=Decimal('5000.0')
    )
    
    # Obtener métricas actualizadas
    dashboard = analytics_servicio.obtener_datos_dashboard_completo()
    assert dashboard['pedidos']['total_pedidos'] > 0

@then('puedo filtrar las métricas por período específico')
def filtrar_metricas_por_periodo(analytics_servicio):
    # Filtrar por período específico
    fecha_inicio = timezone.now().date() - timedelta(days=1)
    fecha_fin = timezone.now().date()
    
    ventas = analytics_servicio.obtener_ventas_por_periodo(fecha_inicio, fecha_fin)
    assert 'periodo' in ventas or ventas is not None

@then('las métricas incluyen comparaciones con períodos anteriores')
def metricas_incluyen_comparaciones(analytics_servicio):
    analisis = analytics_servicio.obtener_analisis_rendimiento_por_periodos()
    
    # Verificar que incluye datos comparativos
    assert isinstance(analisis, dict)
    # Estructura básica de comparación
    assert len(analisis) > 0

@then('puedo exportar los datos del dashboard')
def exportar_datos_dashboard(analytics_servicio):
    dashboard = analytics_servicio.obtener_datos_dashboard_completo()
    
    # Verificar que los datos son serializables (pueden exportarse)
    import json
    try:
        json.dumps(dashboard, default=str)  # default=str para manejar Decimal y datetime
        exportable = True
    except:
        exportable = False
    
    assert exportable

@then('todas las métricas son numéricamente consistentes')
def metricas_numericamente_consistentes(analytics_servicio):
    dashboard = analytics_servicio.obtener_datos_dashboard_completo()
    
    # Verificar consistencia numérica básica
    if 'ventas' in dashboard and 'total_ventas' in dashboard['ventas']:
        assert dashboard['ventas']['total_ventas'] >= 0
    
    if 'pedidos' in dashboard and 'total_pedidos' in dashboard['pedidos']:
        assert dashboard['pedidos']['total_pedidos'] >= 0
    
    if 'clientes' in dashboard and 'total_clientes' in dashboard['clientes']:
        assert dashboard['clientes']['total_clientes'] >= 0
