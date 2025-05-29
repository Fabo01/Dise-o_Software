from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Backend.Presentacion.Views.Cliente_Views import ClienteViewSet
from Backend.Presentacion.Views.Usuario_Views import UsuarioViewSet
from Backend.Presentacion.Controladores.Ingrediente_Controlador import IngredienteViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'ingredientes', IngredienteViewSet, basename='ingrediente')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "clientes": request.build_absolute_uri('clientes/'),
        "usuarios": request.build_absolute_uri('usuarios/'),
        "ingredientes": request.build_absolute_uri('ingredientes/'),
    })

urlpatterns = [
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
