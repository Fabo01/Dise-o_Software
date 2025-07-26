"""
URLs para el Dashboard analítico
"""

from django.urls import path
from Backend.Presentacion.Controladores.Dashboard_Controlador import (
    DashboardMetricasView,
    VentasPorFechaView,
    MenusPopularesView,
    IngredientesCriticosView,
    EstadoMesasView
)

urlpatterns = [
    path('metricas/', DashboardMetricasView.as_view(), name='dashboard-metricas'),
    path('ventas-por-fecha/', VentasPorFechaView.as_view(), name='ventas-por-fecha'),
    path('menus-populares/', MenusPopularesView.as_view(), name='menus-populares'),
    path('ingredientes-criticos/', IngredientesCriticosView.as_view(), name='ingredientes-criticos'),
    path('estado-mesas/', EstadoMesasView.as_view(), name='estado-mesas'),
]
