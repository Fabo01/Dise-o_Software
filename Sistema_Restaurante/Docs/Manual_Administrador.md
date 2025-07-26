# Manual de Administrador - Sistema de Gestión de Restaurante
# S3-37: Documentación para administradores

## 📋 Índice

1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Gestión de Usuarios](#gestión-de-usuarios)
4. [Configuración del Sistema](#configuración-del-sistema)
5. [Gestión de Base de Datos](#gestión-de-base-de-datos)
6. [Monitoreo y Performance](#monitoreo-y-performance)
7. [Respaldos y Recuperación](#respaldos-y-recuperación)
8. [Seguridad](#seguridad)
9. [Mantenimiento](#mantenimiento)
10. [Troubleshooting](#troubleshooting)
11. [APIs y Integraciones](#apis-y-integraciones)

---

## 🚀 Introducción

Este manual está diseñado para administradores de sistema responsables del Sistema de Gestión de Restaurante. Incluye información técnica sobre instalación, configuración, mantenimiento y resolución de problemas.

### Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    ARQUITECTURA GENERAL                 │
├─────────────────┬─────────────────┬─────────────────────┤
│    Frontend     │     Backend     │    Base de Datos    │
│   React 18      │   Django 4.2    │   PostgreSQL 14     │
│   Tailwind CSS  │   Django REST   │   Redis (Cache)     │
│   Vite          │   Framework     │                     │
└─────────────────┴─────────────────┴─────────────────────┘
```

### Requisitos del Sistema

**Servidor de Producción:**
- CPU: 4 cores mínimo (8 cores recomendado)
- RAM: 8GB mínimo (16GB recomendado)
- Disco: 100GB SSD mínimo
- OS: Ubuntu 20.04 LTS o superior

**Dependencias:**
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Nginx 1.18+

---

## ⚙️ Instalación y Configuración

### Instalación del Backend

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd Sistema_Restaurante
```

2. **Configurar entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
# Crear archivo .env
cp .env.example .env

# Editar variables necesarias
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/restaurant_db
REDIS_URL=redis://localhost:6379/0
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

5. **Configurar base de datos:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Instalación del Frontend

1. **Navegar al directorio frontend:**
```bash
cd Frontend
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Configurar variables de entorno:**
```bash
# Crear archivo .env
cp .env.example .env

# Configurar URL del backend
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENVIRONMENT=production
```

4. **Build para producción:**
```bash
npm run build
```

### Configuración de Nginx

```nginx
# /etc/nginx/sites-available/restaurant-system
server {
    listen 80;
    server_name your-domain.com;

    # Frontend estático
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Archivos estáticos del backend
    location /static/ {
        alias /path/to/backend/staticfiles/;
    }

    location /media/ {
        alias /path/to/backend/media/;
    }
}
```

### Configuración de Systemd (Ubuntu/Debian)

```ini
# /etc/systemd/system/restaurant-backend.service
[Unit]
Description=Restaurant System Backend
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=www-data
WorkingDirectory=/path/to/Sistema_Restaurante/Backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn Backend.Config.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Activar el servicio:**
```bash
sudo systemctl enable restaurant-backend
sudo systemctl start restaurant-backend
sudo systemctl status restaurant-backend
```

---

## 👥 Gestión de Usuarios

### Tipos de Usuario

El sistema maneja diferentes niveles de acceso:

1. **Superadministrador**
   - Acceso completo al sistema
   - Gestión de usuarios
   - Configuración del sistema
   - Acceso a todos los módulos

2. **Administrador**
   - Gestión de operaciones diarias
   - Reportes y analytics
   - Configuración de menús y precios

3. **Supervisor**
   - Gestión de pedidos y delivery
   - Supervisión de personal
   - Reportes operacionales

4. **Empleado**
   - Gestión de pedidos
   - Actualización de estados
   - Acceso limitado a reportes

### Crear Usuarios

**Desde Django Admin:**
```bash
python manage.py createsuperuser
```

**Desde la interfaz:**
1. Acceder a "Administración" → "Usuarios"
2. Hacer clic en "Nuevo Usuario"
3. Completar información:
   - Username
   - Email
   - Contraseña temporal
   - Rol asignado
   - Permisos específicos

### Gestión de Permisos

**Permisos por módulo:**
```python
# Ejemplo de configuración de permisos
PERMISSIONS = {
    'clientes': ['view', 'add', 'change', 'delete'],
    'inventario': ['view', 'add', 'change'],
    'pedidos': ['view', 'add', 'change'],
    'reportes': ['view'],
    'configuracion': ['view', 'change']
}
```

**Asignar permisos específicos:**
1. Ir a Django Admin → Groups
2. Crear grupos por rol
3. Asignar permisos específicos
4. Agregar usuarios a grupos

---

## 🔧 Configuración del Sistema

### Variables de Configuración

**Settings principales:**
```python
# Backend/Config/Settings/production.py
import os
from .base import *

# Seguridad
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Cache con Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Configuración de Logging

```python
# Configuración de logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/restaurant-system/backend.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/restaurant-system/error.log',
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Configuración de CORS

```python
# Para permitir requests desde el frontend
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

---

## 🗄️ Gestión de Base de Datos

### Migraciones

**Crear migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Migración con datos:**
```bash
# Crear migración de datos
python manage.py makemigrations --empty app_name

# Ejemplo de migración de datos
def migrate_data(apps, schema_editor):
    Cliente = apps.get_model('Infraestructura', 'ClienteModel')
    # Lógica de migración
```

**Rollback de migraciones:**
```bash
# Volver a migración específica
python manage.py migrate app_name 0001

# Ver estado de migraciones
python manage.py showmigrations
```

### Optimización de Consultas

**Índices de base de datos:**
```python
# En los modelos
class ClienteModel(models.Model):
    rut = models.CharField(max_length=12, unique=True, db_index=True)
    email = models.EmailField(db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['rut']),
            models.Index(fields=['email']),
            models.Index(fields=['-fecha_creacion']),
        ]
```

**Monitoring de consultas lentas:**
```python
# En settings.py para desarrollo
if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
```

### Backup de Base de Datos

**Script de backup automático:**
```bash
#!/bin/bash
# backup_db.sh

DB_NAME="restaurant_db"
DB_USER="postgres"
BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Crear backup
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Comprimir
gzip $BACKUP_DIR/backup_$DATE.sql

# Limpiar backups antiguos (mantener 30 días)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completado: $BACKUP_DIR/backup_$DATE.sql.gz"
```

**Configurar cron para backups automáticos:**
```bash
# Ejecutar cada día a las 2:00 AM
0 2 * * * /path/to/backup_db.sh
```

---

## 📊 Monitoreo y Performance

### Métricas Clave

**Sistema operativo:**
- CPU usage
- Memory usage
- Disk I/O
- Network traffic

**Aplicación:**
- Response times
- Error rates
- Database query times
- Cache hit rates

**Negocio:**
- Pedidos por hora
- Revenue tracking
- Customer satisfaction
- Delivery performance

### Configuración de Monitoreo

**Con Prometheus y Grafana:**

1. **Instalar django-prometheus:**
```bash
pip install django-prometheus
```

2. **Configurar en settings:**
```python
INSTALLED_APPS = [
    'django_prometheus',
    # ... otras apps
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ... otros middlewares
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]
```

3. **URLs para métricas:**
```python
# urls.py
urlpatterns = [
    path('metrics/', include('django_prometheus.urls')),
]
```

### Health Checks

**Endpoint de salud:**
```python
# Backend/Presentacion/Views/health.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis

def health_check(request):
    """Health check endpoint para load balancers"""
    status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['checks']['database'] = 'healthy'
    except Exception as e:
        status['checks']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        cache.set('health_check', 'ok', 30)
        cache.get('health_check')
        status['checks']['cache'] = 'healthy'
    except Exception as e:
        status['checks']['cache'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    return JsonResponse(status)
```

### Performance Profiling

**Usar Django Debug Toolbar en desarrollo:**
```python
# settings/development.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

**Profile queries:**
```python
from django.db import connection
from django.conf import settings

if settings.DEBUG:
    print(f"Queries executed: {len(connection.queries)}")
    for query in connection.queries:
        print(f"Time: {query['time']}s - SQL: {query['sql']}")
```

---

## 💾 Respaldos y Recuperación

### Sistema de Backup Automático

El sistema incluye un módulo completo de backup:

**Uso del comando de backup:**
```bash
# Crear backup completo
python manage.py backup crear

# Listar backups disponibles
python manage.py backup listar

# Restaurar desde backup
python manage.py backup restaurar --backup-path=/path/to/backup.zip

# Validar integridad de backup
python manage.py backup validar --backup-path=/path/to/backup.zip
```

**Configuración de backup automático:**
```python
# settings.py
BACKUP_DIR = '/backups/sistema'
MAX_BACKUPS = 30  # Mantener 30 días
```

### Estrategia de Backup

**Frecuencia recomendada:**
- **Backup completo**: Diario a las 2:00 AM
- **Backup incremental**: Cada 6 horas
- **Backup de base de datos**: Cada hora durante horarios operativos

**Tipos de backup:**
1. **Backup de aplicación**: Código, configuración, datos
2. **Backup de base de datos**: Dump completo de PostgreSQL
3. **Backup de archivos**: Media files, logs, uploads

### Procedimiento de Recuperación

**Recuperación completa:**
1. Restaurar servidor desde imagen/snapshot
2. Restaurar backup de aplicación
3. Restaurar base de datos
4. Verificar integridad de datos
5. Reiniciar servicios

**Recuperación de datos específicos:**
```sql
-- Restaurar tabla específica
pg_restore -U postgres -d restaurant_db -t clientes backup.dump
```

---

## 🔒 Seguridad

### Configuración de Seguridad

**Settings de seguridad:**
```python
# Seguridad HTTP
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8,}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Gestión de Secrets

**Usando variables de entorno:**
```bash
# .env
SECRET_KEY=your-very-secret-key-here
DATABASE_PASSWORD=secure-db-password
EMAIL_PASSWORD=email-service-password
REDIS_PASSWORD=redis-password

# Payment gateway secrets
PAYMENT_API_KEY=payment-api-key
PAYMENT_SECRET=payment-secret
```

**En producción con systemd:**
```ini
[Service]
Environment="SECRET_KEY=your-secret-key"
Environment="DATABASE_PASSWORD=db-password"
EnvironmentFile=/etc/restaurant-system/secrets.env
```

### Auditoría y Logs

**Log de auditoría:**
```python
# Backend/Aplicacion/Servicios/AuditoriaService.py
class AuditoriaService:
    @staticmethod
    def log_action(user, action, model, object_id, changes=None):
        from Backend.Infraestructura.Modelos.AuditoriaModel import AuditoriaModel
        
        AuditoriaModel.objects.create(
            usuario=user,
            accion=action,
            modelo=model.__name__,
            objeto_id=object_id,
            cambios=changes,
            ip_address=get_client_ip(request),
            timestamp=timezone.now()
        )
```

### Firewall y Red

**Configuración UFW (Ubuntu):**
```bash
# Permitir solo puertos necesarios
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

**Fail2ban para protección contra ataques:**
```ini
# /etc/fail2ban/jail.local
[django]
enabled = true
port = http,https
filter = django
logpath = /var/log/restaurant-system/backend.log
maxretry = 5
bantime = 3600
```

---

## 🔧 Mantenimiento

### Tareas de Mantenimiento Rutinario

**Diarias:**
- Verificar logs de errores
- Comprobar backups automáticos
- Revisar métricas de performance
- Verificar espacio en disco

**Semanales:**
- Limpiar logs antiguos
- Actualizar dependencias de seguridad
- Revisar usuarios activos
- Optimizar base de datos

**Mensuales:**
- Actualizar sistema operativo
- Revisar configuración de seguridad
- Auditoría de accesos
- Planificación de capacidad

### Scripts de Mantenimiento

**Limpieza de logs:**
```bash
#!/bin/bash
# cleanup_logs.sh
LOG_DIR="/var/log/restaurant-system"
DAYS_TO_KEEP=30

find $LOG_DIR -name "*.log" -mtime +$DAYS_TO_KEEP -delete
find $LOG_DIR -name "*.log.*" -mtime +$DAYS_TO_KEEP -delete

# Comprimir logs de la semana pasada
find $LOG_DIR -name "*.log" -mtime +7 -exec gzip {} \;
```

**Optimización de base de datos:**
```bash
#!/bin/bash
# optimize_db.sh
psql -U postgres -d restaurant_db -c "VACUUM ANALYZE;"
psql -U postgres -d restaurant_db -c "REINDEX DATABASE restaurant_db;"
```

### Monitoreo de Recursos

**Script de monitoring:**
```bash
#!/bin/bash
# system_check.sh

# CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)

# Memory usage
MEM_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')

# Disk usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)

# Database connections
DB_CONNECTIONS=$(psql -U postgres -t -c "SELECT count(*) FROM pg_stat_activity;")

echo "CPU: ${CPU_USAGE}%"
echo "Memory: ${MEM_USAGE}%"
echo "Disk: ${DISK_USAGE}%"
echo "DB Connections: $DB_CONNECTIONS"

# Alertas
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "ALERT: High CPU usage"
fi

if (( $(echo "$MEM_USAGE > 90" | bc -l) )); then
    echo "ALERT: High memory usage"
fi
```

---

## 🚨 Troubleshooting

### Problemas Comunes

**1. Alto uso de CPU/Memoria**

*Síntomas:*
- Respuestas lentas
- Timeouts en requests
- Load promedio alto

*Diagnóstico:*
```bash
# Ver procesos que más CPU consumen
top -o %CPU

# Ver uso de memoria
free -h
ps aux --sort=-%mem | head

# Ver conexiones de red
netstat -tuln

# Ver consultas lentas en PostgreSQL
psql -U postgres -c "SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

*Soluciones:*
- Optimizar consultas SQL lentas
- Implementar cache adicional
- Aumentar recursos del servidor
- Optimizar código Python

**2. Errores de Base de Datos**

*Síntomas:*
- Errores de conexión
- Consultas que fallan
- Datos inconsistentes

*Diagnóstico:*
```bash
# Ver logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Verificar conexiones activas
psql -U postgres -c "SELECT * FROM pg_stat_activity;"

# Verificar integridad de datos
python manage.py check --database default
```

*Soluciones:*
- Reiniciar servicio PostgreSQL
- Verificar configuración de conexión
- Restaurar desde backup si hay corrupción
- Ejecutar VACUUM ANALYZE

**3. Problemas de Cache**

*Síntomas:*
- Datos desactualizados
- Errores de conexión a Redis
- Performance degradada

*Diagnóstico:*
```bash
# Verificar estado de Redis
redis-cli ping
redis-cli info

# Ver keys en cache
redis-cli keys "*"

# Monitorear operaciones
redis-cli monitor
```

*Soluciones:*
- Reiniciar Redis
- Limpiar cache específico
- Verificar configuración de conexión
- Implementar fallback sin cache

### Logs de Debugging

**Ubicación de logs:**
```
/var/log/restaurant-system/
├── backend.log          # Logs generales del backend
├── error.log           # Logs de errores
├── django.log          # Logs específicos de Django
├── nginx_access.log    # Logs de acceso Nginx
├── nginx_error.log     # Logs de errores Nginx
└── postgresql.log      # Logs de base de datos
```

**Comandos útiles para logs:**
```bash
# Ver errores recientes
tail -f /var/log/restaurant-system/error.log

# Buscar errores específicos
grep -i "error" /var/log/restaurant-system/backend.log

# Ver logs con timestamp
journalctl -u restaurant-backend -f

# Filtrar por nivel de log
grep "ERROR\|CRITICAL" /var/log/restaurant-system/*.log
```

---

## 🔌 APIs y Integraciones

### Documentación de API

**Swagger/OpenAPI:**
El sistema incluye documentación automática de API:
- URL: `https://your-domain.com/api/docs/`
- Formato interactivo con Swagger UI
- Descarga de especificación OpenAPI

**Endpoints principales:**
```
GET    /api/clientes/           # Lista de clientes
POST   /api/clientes/           # Crear cliente
GET    /api/clientes/{id}/      # Detalle de cliente
PUT    /api/clientes/{id}/      # Actualizar cliente
DELETE /api/clientes/{id}/      # Eliminar cliente

GET    /api/pedidos/            # Lista de pedidos
POST   /api/pedidos/            # Crear pedido
GET    /api/pedidos/{id}/       # Detalle de pedido
PATCH  /api/pedidos/{id}/       # Actualizar estado

GET    /api/analytics/dashboard/ # Métricas del dashboard
GET    /api/analytics/ventas/    # Reportes de ventas
```

### Autenticación API

**Token Authentication:**
```python
# Obtener token
POST /api/auth/login/
{
    "username": "usuario",
    "password": "contraseña"
}

# Respuesta
{
    "token": "abc123...",
    "user": {...}
}

# Usar token en requests
Authorization: Token abc123...
```

### Rate Limiting

**Configuración:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

### Webhooks

**Configurar webhooks para eventos:**
```python
# Backend/Aplicacion/Servicios/WebhookService.py
class WebhookService:
    @staticmethod
    def send_webhook(event, data, webhook_url):
        payload = {
            'event': event,
            'data': data,
            'timestamp': timezone.now().isoformat()
        }
        
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
```

---

## 📞 Contacto y Soporte

### Soporte Técnico

**Equipo de Desarrollo:**
- 📧 **Email**: dev-team@restaurant-system.com
- 💬 **Slack**: #restaurant-system-support
- 🎫 **Issue Tracker**: GitHub Issues

**Escalación:**
1. **Nivel 1**: Administrador local
2. **Nivel 2**: Equipo de desarrollo
3. **Nivel 3**: Arquitecto de sistemas

### Información para Reportes

**Incluir en reportes de problemas:**
- Versión del sistema
- Logs relevantes
- Pasos para reproducir
- Impacto en el negocio
- Configuración del entorno

### Recursos Adicionales

- 📚 **Documentación técnica**: `/docs/technical/`
- 🎥 **Videos de configuración**: Canal YouTube interno
- 📖 **Wiki del equipo**: Confluence/Notion
- 🔧 **Scripts de utilidad**: `/scripts/admin/`

---

**Documento actualizado: [Fecha actual]**
**Versión del sistema: 1.0**
**Mantenido por: Equipo de Desarrollo**
