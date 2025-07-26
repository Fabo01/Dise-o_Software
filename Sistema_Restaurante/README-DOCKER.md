# 🐳 Docker Setup - Sistema de Gestión de Restaurante

## Prerrequisitos

1. **Docker Desktop** instalado y ejecutándose
2. **Git** para clonar el repositorio
3. **PowerShell** (Windows) o **Terminal** (macOS/Linux)

## 🚀 Inicio Rápido

### 1. Verificar Docker
```bash
docker --version
docker-compose --version
```

### 2. Clonar y navegar al proyecto
```bash
cd "c:\Users\fabo\Documents\Git Universidad\Dise-o_Software\Sistema_Restaurante"
```

### 3. Construir las imágenes
```bash
# Windows PowerShell
.\docker-scripts.ps1 build

# Linux/macOS
make build
```

### 4. Levantar los servicios
```bash
# Windows PowerShell
.\docker-scripts.ps1 up

# Linux/macOS
make up
```

### 5. Acceder a la aplicación
- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:80/api/
- **Django Admin**: http://localhost:80/admin/
- **Swagger API**: http://localhost:80/swagger/
- **Adminer (DB)**: http://localhost:8080

## 📋 Comandos Disponibles

### Windows (PowerShell)
```powershell
# Mostrar ayuda
.\docker-scripts.ps1 help

# Construcción y servicios
.\docker-scripts.ps1 build          # Construir imágenes
.\docker-scripts.ps1 up             # Levantar servicios
.\docker-scripts.ps1 up-dev         # Modo desarrollo
.\docker-scripts.ps1 down           # Detener servicios
.\docker-scripts.ps1 restart        # Reiniciar servicios

# Logs y monitoreo
.\docker-scripts.ps1 logs           # Ver todos los logs
.\docker-scripts.ps1 logs-backend   # Logs del backend
.\docker-scripts.ps1 logs-frontend  # Logs del frontend
.\docker-scripts.ps1 status         # Estado de servicios
.\docker-scripts.ps1 health         # Verificar salud

# Acceso a contenedores
.\docker-scripts.ps1 shell-backend  # Shell del backend
.\docker-scripts.ps1 shell-frontend # Shell del frontend
.\docker-scripts.ps1 shell-db       # Shell de PostgreSQL

# Django específico
.\docker-scripts.ps1 migrate        # Ejecutar migraciones
.\docker-scripts.ps1 makemigrations # Crear migraciones
.\docker-scripts.ps1 collectstatic  # Archivos estáticos
.\docker-scripts.ps1 superuser      # Crear superusuario

# Pruebas y limpieza
.\docker-scripts.ps1 test           # Ejecutar pruebas
.\docker-scripts.ps1 clean          # Limpiar todo
```

### Linux/macOS (Makefile)
```bash
# Mostrar ayuda
make help

# Mismos comandos pero con make
make build
make up
make down
# ... etc
```

## 🏗️ Arquitectura Docker

```
┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │    Frontend     │
│   (Port 80)     │◄──►│   (React/Node)  │
│                 │    │   (Port 3000)   │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│     Backend     │    │   PostgreSQL    │
│    (Django)     │◄──►│   (Port 5432)   │
│   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│      Redis      │    │     Adminer     │
│   (Port 6379)   │    │   (Port 8080)   │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
```

## 🔧 Configuración

### Variables de Entorno
Las variables se configuran automáticamente en Docker, pero puedes personalizarlas en:
- `Backend/Config/Settings/docker.py`
- `docker-compose.yml`

### Base de Datos
- **Host**: postgres (interno), localhost:5432 (externo)
- **Database**: restaurant_db
- **User**: restaurant_user
- **Password**: Note12pro.

### Redis
- **Host**: redis (interno), localhost:6379 (externo)
- **Usado para**: Caché y sesiones

## 🐛 Resolución de Problemas

### Error: Puerto en uso
```bash
# Detener servicios que usen los puertos
.\docker-scripts.ps1 down
netstat -ano | findstr :80
# Cambiar puertos en docker-compose.yml si es necesario
```

### Error: Permiso denegado
```bash
# En PowerShell como administrador
Set-ExecutionPolicy RemoteSigned
```

### Error: Base de datos no conecta
```bash
# Verificar estado de PostgreSQL
.\docker-scripts.ps1 logs-db
.\docker-scripts.ps1 shell-db
```

### Error: Módulo no encontrado
```bash
# Reconstruir imágenes
.\docker-scripts.ps1 down
.\docker-scripts.ps1 build
.\docker-scripts.ps1 up
```

## 📊 Monitoreo y Logs

### Ver logs en tiempo real
```bash
# Todos los servicios
.\docker-scripts.ps1 logs

# Servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Verificar recursos
```bash
# Estado de contenedores
docker ps

# Uso de recursos
docker stats

# Espacio usado
docker system df
```

## 🧪 Desarrollo y Pruebas

### Modo Desarrollo
```bash
# Usar configuración de desarrollo
.\docker-scripts.ps1 up-dev

# Acceso:
# Frontend: http://localhost:3001
# Backend: http://localhost:8001
```

### Ejecutar Pruebas
```bash
# Todas las pruebas
.\docker-scripts.ps1 test

# Pruebas específicas
docker-compose exec backend python manage.py test Backend.tests
docker-compose exec backend pytest Backend/tests/
```

### Hot Reload
- **Backend**: Los cambios se reflejan automáticamente
- **Frontend**: Hot Module Replacement habilitado

## 🔒 Seguridad

### Producción
1. Cambiar SECRET_KEY en settings
2. Configurar ALLOWED_HOSTS específicos
3. Usar HTTPS con certificados
4. Configurar firewall para puertos específicos

### Credenciales por defecto
- **Admin DB**: restaurant_user / Note12pro.
- **Django Admin**: Crear con `.\docker-scripts.ps1 superuser`

## 📁 Estructura de Archivos Docker

```
Sistema_Restaurante/
├── docker-compose.yml          # Configuración principal
├── docker-compose.dev.yml      # Configuración desarrollo
├── Dockerfile.backend          # Imagen del backend
├── Dockerfile.frontend         # Imagen del frontend
├── .dockerignore              # Archivos a ignorar
├── Makefile                   # Comandos para Linux/macOS
├── docker-scripts.ps1         # Scripts para Windows
└── docker/
    ├── nginx/                 # Configuración Nginx
    ├── postgres/              # Scripts de PostgreSQL
    ├── redis/                 # Configuración Redis
    └── scripts/               # Scripts auxiliares
```

## 🆘 Soporte

Si encuentras problemas:

1. Verificar logs: `.\docker-scripts.ps1 logs`
2. Verificar salud: `.\docker-scripts.ps1 health`
3. Reiniciar servicios: `.\docker-scripts.ps1 restart`
4. Limpiar y reconstruir: `.\docker-scripts.ps1 clean` + `.\docker-scripts.ps1 build`

Para más ayuda, consulta la documentación de Docker Desktop o el equipo de desarrollo.
