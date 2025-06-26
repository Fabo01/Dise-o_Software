from django.contrib import admin
from django.urls import path, include
from Backend.Presentacion.Views.Index_View import IndexHtmlView
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from Backend.Presentacion.Views.Cliente_Views import ClienteViewSet
from Backend.Presentacion.Views.Usuario_Views import UsuarioViewSet
from Backend.Presentacion.Controladores.Ingrediente_Controlador import IngredienteViewSet
import os
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'ingredientes', IngredienteViewSet, basename='ingrediente')

schema_view = get_schema_view(
    openapi.Info(
        title="API Restaurante",
        default_version='v1',
        description="Documentación interactiva de la API del sistema de restaurante",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', IndexHtmlView.as_view(), name='index'),  # <-- Esto sirve index.html en la raíz
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'Frontend'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
