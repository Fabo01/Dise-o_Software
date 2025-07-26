# 🐳 Documentación de Docker para el Sistema de Restaurante

## ¿Qué es Docker y para qué serviría en este proyecto?

Docker es una plataforma de contenedorización que permite empaquetar aplicaciones y sus dependencias en contenedores ligeros y portables. Para nuestro sistema de restaurante, Docker proporcionaría los siguientes beneficios:

### 🎯 Beneficios de Docker

1. **Consistencia de Entorno**
   - Mismo entorno en desarrollo, testing y producción
   - Elimina problemas de "funciona en mi máquina"
   - Versiones exactas de Python, Node.js, y dependencias

2. **Facilidad de Despliegue**
   - Un solo comando para levantar todo el sistema
   - Escalabilidad automática
   - Rollbacks instantáneos

3. **Aislamiento de Servicios**
   - Backend Django en un contenedor
   - Frontend React en otro contenedor
   - Base de datos PostgreSQL en contenedor separado
   - Redis para caché en su propio contenedor

4. **Gestión de Dependencias**
   - No necesidad de instalar Python, Node.js localmente
   - Versiones específicas garantizadas
   - Dependencias del sistema incluidas

## 📁 Estructura Docker Propuesta

```
Sistema_Restaurante/
├── docker-compose.yml          # Orquestación de servicios
├── Dockerfile.backend          # Imagen del backend Django
├── Dockerfile.frontend         # Imagen del frontend React
├── docker/
│   ├── nginx/
│   │   └── default.conf       # Configuración del proxy
│   ├── postgres/
│   │   └── init.sql          # Scripts de inicialización DB
│   └── redis/
│       └── redis.conf        # Configuración de Redis
└── .dockerignore              # Archivos a ignorar
```

## 🚀 Implementación Docker

### 1. Dockerfile para Backend Django

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

# Configurar entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=Backend.Config.Settings.production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Backend.Config.wsgi:application"]
```

### 2. Dockerfile para Frontend React

```dockerfile
# Dockerfile.frontend
FROM node:18-alpine AS builder

# Directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY . .

# Build de producción
RUN npm run build

# Etapa de producción con Nginx
FROM nginx:alpine

# Copiar archivos build
COPY --from=builder /app/build /usr/share/nginx/html

# Copiar configuración personalizada de nginx
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 80

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose - Orquestación Completa

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Base de datos PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: restaurante_db
    environment:
      POSTGRES_DB: restaurante_db
      POSTGRES_USER: restaurante_user
      POSTGRES_PASSWORD: restaurante_pass123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U restaurante_user -d restaurante_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis para caché y sesiones
  redis:
    image: redis:7-alpine
    container_name: restaurante_redis
    command: redis-server /etc/redis/redis.conf
    volumes:
      - redis_data:/data
      - ./docker/redis/redis.conf:/etc/redis/redis.conf
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Backend Django
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: restaurante_backend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://restaurante_user:restaurante_pass123@postgres:5432/restaurante_db
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=False
      - ALLOWED_HOSTS=localhost,127.0.0.1,backend
    volumes:
      - ./media:/app/media
      - ./static:/app/static
    ports:
      - "8000:8000"
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py loaddata fixtures/datos_iniciales.json &&
             gunicorn --bind 0.0.0.0:8000 Backend.Config.wsgi:application"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend React
  frontend:
    build:
      context: ../Frontend
      dockerfile: Dockerfile.frontend
    container_name: restaurante_frontend
    depends_on:
      - backend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx como proxy reverso (opcional)
  nginx:
    image: nginx:alpine
    container_name: restaurante_proxy
    depends_on:
      - backend
      - frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
      - ./static:/static
      - ./media:/media
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: restaurante_network
```

### 4. Configuración de Nginx

```nginx
# docker/nginx/default.conf
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:80;
}

server {
    listen 80;
    server_name localhost;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Swagger Documentation
    location /swagger/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /static/;
    }

    # Media files
    location /media/ {
        alias /media/;
    }
}
```

## 🚀 Comandos de Uso

### Desarrollo
```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# Iniciar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v
```

### Producción
```bash
# Usar archivo de producción
docker-compose -f docker-compose.prod.yml up -d

# Escalar servicios
docker-compose up --scale backend=3

# Actualizar servicios
docker-compose pull
docker-compose up -d
```

### Mantenimiento
```bash
# Ejecutar migraciones
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Backup de base de datos
docker-compose exec postgres pg_dump -U restaurante_user restaurante_db > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U restaurante_user restaurante_db < backup.sql
```

## 🔧 Configuración de Entorno

### Variables de Entorno (.env)
```env
# Base de datos
DATABASE_URL=postgresql://restaurante_user:restaurante_pass123@postgres:5432/restaurante_db
POSTGRES_DB=restaurante_db
POSTGRES_USER=restaurante_user
POSTGRES_PASSWORD=restaurante_pass123

# Redis
REDIS_URL=redis://redis:6379/0

# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com

# API URLs
REACT_APP_API_URL=http://localhost:8000/api
```

## 📊 Monitoreo y Logs

### Configuración de Logging
```yaml
# Añadir al docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Healthchecks
Cada servicio incluye healthchecks para monitoreo automático:
- PostgreSQL: verificación de conexión
- Redis: comando ping
- Backend: endpoint de salud
- Frontend: verificación HTTP
- Nginx: verificación de proxy

## 🔒 Seguridad

### Mejores Prácticas Implementadas
1. **Usuarios no-root** en contenedores
2. **Variables de entorno** para credenciales
3. **Redes isoladas** entre servicios
4. **Volúmenes persistentes** para datos
5. **Healthchecks** para monitoreo
6. **Secrets management** para producción

## 🚀 Despliegue en Producción

### Con Docker Swarm
```bash
# Inicializar swarm
docker swarm init

# Deploy del stack
docker stack deploy -c docker-compose.prod.yml restaurante

# Escalar servicios
docker service scale restaurante_backend=3
```

### Con Kubernetes (Helm Chart)
```yaml
# values.yaml para Helm
replicaCount: 3
image:
  repository: tu-registry/restaurante-backend
  tag: latest
service:
  type: LoadBalancer
  port: 80
```

## 📈 Ventajas vs. Instalación Manual

| Aspecto | Instalación Manual | Docker |
|---------|-------------------|---------|
| **Tiempo de setup** | 30-60 minutos | 5-10 minutos |
| **Dependencias** | Instalar Python, Node, DB | Solo Docker |
| **Consistencia** | Variable entre entornos | 100% consistente |
| **Escalabilidad** | Manual y compleja | Automática |
| **Backup/Restore** | Múltiples pasos | Un comando |
| **Rollback** | Manual | Instantáneo |
| **Monitoreo** | Configuración manual | Integrado |

## 🎯 Casos de Uso Ideales para Docker

1. **Equipos de Desarrollo**: Entorno consistente para todos
2. **Staging/Testing**: Réplica exacta de producción
3. **Despliegue Cloud**: AWS ECS, Google Cloud Run, Azure Container Instances
4. **CI/CD**: Integración con Jenkins, GitLab CI, GitHub Actions
5. **Microservicios**: Escalabilidad independiente de componentes

Docker transformaría este proyecto de restaurante en una solución empresarial lista para producción, con capacidades de escalabilidad, monitoreo y despliegue automatizado que facilitarían enormemente su mantenimiento y evolución.
