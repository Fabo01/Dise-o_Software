from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Backend.Presentacion.Views.Cliente_Views import ClienteViewSet
from Backend.Presentacion.Views.Usuario_Views import UsuarioViewSet
from Backend.Presentacion.Controladores.Ingrediente_Controlador import IngredienteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'ingredientes', IngredienteViewSet, basename='ingrediente')

urlpatterns = [
    path('api/', include(router.urls)),
]
