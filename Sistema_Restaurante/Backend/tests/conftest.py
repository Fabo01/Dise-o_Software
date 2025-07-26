# Backend/tests/conftest.py
import pytest
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import execute_from_command_line
import os
import sys

def pytest_configure():
    """Configure Django settings for pytest."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.Config.Settings.test')
    
    if not settings.configured:
        settings.configure(
            SECRET_KEY='test-secret-key-for-testing-only',
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'rest_framework',
                'Backend.Infraestructura',
            ],
            USE_TZ=True,
            ROOT_URLCONF='Backend.Presentacion.urls',
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ],
            CACHES={
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                }
            },
            REST_FRAMEWORK={
                'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework.authentication.SessionAuthentication',
                ],
                'DEFAULT_PERMISSION_CLASSES': [
                    'rest_framework.permissions.IsAuthenticated',
                ],
            }
        )
    
    django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    """Set up the test database."""
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])

@pytest.fixture
def performance_data():
    """Fixture para crear datos de prueba para tests de rendimiento"""
    from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
    from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
    from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
    
    # Crear clientes de prueba
    clientes = []
    for i in range(100):
        cliente = ClienteModelo.objects.create(
            rut=f"1234567{i:02d}",
            nombre=f"Cliente {i}",
            email=f"cliente{i}@test.com",
            telefono=f"9876543{i:02d}"
        )
        clientes.append(cliente)
    
    # Crear ingredientes de prueba
    ingredientes = []
    for i in range(50):
        ingrediente = IngredienteModelo.objects.create(
            nombre=f"Ingrediente {i}",
            stock_actual=100 + i,
            stock_minimo=10,
            precio_unitario=1000 + (i * 100)
        )
        ingredientes.append(ingrediente)
    
    # Crear menús de prueba
    menus = []
    for i in range(30):
        menu = MenuModelo.objects.create(
            nombre=f"Menu {i}",
            descripcion=f"Descripción del menu {i}",
            precio=5000 + (i * 500),
            categoria="Plato Principal",
            disponible=True
        )
        menus.append(menu)
    
    return {
        'clientes': clientes,
        'ingredientes': ingredientes,
        'menus': menus
    }

@pytest.fixture
def api_client():
    """Provide Django REST framework test client."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, django_user_model):
    """Provide authenticated API client."""
    user = django_user_model.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    api_client.force_authenticate(user=user)
    return api_client
