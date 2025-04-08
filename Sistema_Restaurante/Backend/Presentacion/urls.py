from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Backend.Presentacion.Views.Cliente_Views import ClienteViewSet
from Backend.Presentacion.Controladores.Cliente_Controlador import ClienteEstadoAPI, ClienteVisitaAPI

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/clientes/<int:id>/estado/', ClienteEstadoAPI.as_view(), name='cliente-estado'),
    path('api/clientes/<int:id>/visita/', ClienteVisitaAPI.as_view(), name='cliente-visita'),
]
