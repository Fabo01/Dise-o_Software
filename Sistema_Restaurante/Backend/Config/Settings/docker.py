"""
Configuración específica para Docker del Sistema de Restaurante.
"""
import os
from .settings import *

# Configuración de base de datos para Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'restaurant_db'),
        'USER': os.getenv('POSTGRES_USER', 'restaurant_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'Note12pro.'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Configuración de Redis para caché
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Configuración de sesiones con Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Configuración de logs para Docker
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'Backend': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Configuración de archivos estáticos para Docker
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Configuración de seguridad para Docker
ALLOWED_HOSTS = ['*']  # En producción, especificar hosts específicos

# Configuración de CORS para Docker
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://frontend:3000",
    "http://localhost:80",
    "http://nginx:80",
]

# Configuración adicional para Docker
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Configuración de tiempo de zona
USE_TZ = True
TIME_ZONE = 'America/Santiago'
