from django.urls import path
from Backend.Presentacion.Controladores.Cliente_Controlador import ClienteAPI, ClienteEstadoAPI, ClienteVisitaAPI

urlpatterns = [
    # URLs para operaciones CRUD básicas de clientes
    path('clientes/', ClienteAPI.as_view(), name='cliente-lista'),
    path('clientes/<int:id>/', ClienteAPI.as_view(), name='cliente-detalle'),
    
    # URLs para operaciones específicas
    path('clientes/<int:id>/estado/', ClienteEstadoAPI.as_view(), name='cliente-estado'),
    path('clientes/<int:id>/visita/', ClienteVisitaAPI.as_view(), name='cliente-visita'),
]