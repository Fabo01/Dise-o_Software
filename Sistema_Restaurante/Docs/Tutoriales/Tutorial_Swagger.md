# Tutorial: Uso y conexión a Swagger en el Sistema de Gestión de Restaurante

Este tutorial explica cómo habilitar, acceder y utilizar Swagger (OpenAPI) para documentar y probar la API RESTful del sistema.

---

## 1. ¿Qué es Swagger?
Swagger (ahora conocido como OpenAPI) es una herramienta que permite documentar, visualizar y probar de forma interactiva los endpoints de una API REST. Facilita la colaboración entre backend, frontend y QA, y permite a cualquier usuario autorizado explorar y consumir la API desde el navegador.

---

## 2. Requisitos previos
- Tener el proyecto Django configurado y funcionando.
- Haber instalado la dependencia `drf-yasg` (Yet Another Swagger Generator) en el entorno virtual:

```bash
pip install drf-yasg
```

Asegúrate de que esté incluida en `requirements.txt`:
```
drf-yasg>=1.21
```

---

## 3. Configuración de Swagger en Django

### a) Agrega `drf_yasg` a `INSTALLED_APPS` en tu archivo de settings:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_yasg',
    ...
]
```

### b) Configura las rutas de Swagger en tu archivo principal de URLs (por ejemplo, `Backend/Config/urls.py`):

```python
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Restaurante",
      default_version='v1',
      description="Documentación interactiva de la API del sistema de gestión de restaurante",
      contact=openapi.Contact(email="soporte@restaurante.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    ... # tus otras rutas
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

---

## 4. Levantar el servidor y acceder a Swagger

1. Asegúrate de tener el entorno virtual activado y las migraciones aplicadas.
2. Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

3. Abre tu navegador y accede a:
- [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  ← Interfaz Swagger UI
- [http://localhost:8000/redoc/](http://localhost:8000/redoc/)    ← Interfaz Redoc (alternativa)
- [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json) ← Esquema JSON

---

## 5. ¿Cómo usar Swagger?
- Explora todos los endpoints disponibles, sus métodos, parámetros y respuestas.
- Haz pruebas de endpoints directamente desde la interfaz (botón "Try it out").
- Visualiza los modelos de datos y ejemplos de request/response.
- Si tu API requiere autenticación, puedes ingresar el token JWT o credenciales en el botón "Authorize".

---

## 6. Consejos y buenas prácticas
- Mantén actualizada la documentación de tus endpoints y modelos.
- Usa descripciones claras en tus serializers y views para que Swagger las muestre.
- Protege el acceso a Swagger en producción (por ejemplo, solo para administradores).
- Puedes personalizar el título, descripción y branding en la configuración de `get_schema_view`.

---

**¡Listo! Ahora puedes documentar, probar y compartir tu API de forma profesional usando Swagger.**
