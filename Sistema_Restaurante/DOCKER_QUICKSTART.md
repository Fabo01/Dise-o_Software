# 🐳 Guía de Inicio Rápido - Docker

## Prerrequisitos

1. **Docker Desktop** instalado y ejecutándose
   - Windows: [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Asegúrate de que Docker esté ejecutándose (ícono en la bandeja del sistema)

2. **Git** (para clonar el repositorio)

## 🚀 Inicio Rápido

### Opción 1: Script Automatizado (Recomendado)

```bash
# En Windows (PowerShell o CMD)
.\docker-manager.bat up

# En Linux/Mac
./docker-manager.sh up
```

### Opción 2: Comandos Manuales

```bash
# 1. Construir las imágenes
docker-compose build

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Ver logs (opcional)
docker-compose logs -f
```

## 📱 Acceso a la Aplicación

Una vez que todos los servicios estén ejecutándose:

- **🌐 Frontend (React)**: http://localhost:3000
- **🔧 Backend API**: http://localhost:8000
- **📖 Documentación API (Swagger)**: http://localhost:8000/swagger/
- **👑 Panel de Administración**: http://localhost:8000/admin/
  - Usuario: `admin`
  - Contraseña: `admin123`

## 🛠️ Comandos Útiles

### Gestión de Servicios

```bash
# Iniciar servicios
docker-manager.bat up

# Detener servicios
docker-manager.bat down

# Reiniciar servicios
docker-manager.bat restart

# Ver estado de servicios
docker-manager.bat status

# Ver logs en tiempo real
docker-manager.bat logs
```

### Desarrollo

```bash
# Conectar al contenedor del backend
docker-manager.bat backend

# Conectar al contenedor del frontend
docker-manager.bat frontend

# Ejecutar migraciones
docker-manager.bat migrate

# Ejecutar tests
docker-manager.bat test

# Conectar a la base de datos
docker-manager.bat db
```

### Mantenimiento

```bash
# Construir imágenes desde cero
docker-manager.bat build

# Limpiar todo (contenedores, imágenes, volúmenes)
docker-manager.bat clean

# Reset completo del sistema
docker-manager.bat reset
```

## 🗄️ Servicios Incluidos

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Frontend | 3000 | Aplicación React |
| Backend | 8000 | API Django REST |
| PostgreSQL | 5432 | Base de datos |
| Redis | 6379 | Caché y sesiones |
| Nginx | 80, 443 | Proxy reverso (producción) |

## 📁 Estructura de Volúmenes

```
docker-volumes/
├── postgres_data/      # Datos de PostgreSQL
├── redis_data/         # Datos de Redis
├── backend_static/     # Archivos estáticos Django
├── backend_media/      # Archivos multimedia
└── frontend_node_modules/  # Dependencias Node.js
```

## 🔧 Configuración

### Variables de Entorno

Las variables están configuradas en `.env.docker`:

```env
# Base de datos
POSTGRES_DB=restaurant_db
POSTGRES_USER=restaurant_user
POSTGRES_PASSWORD=Note12pro.

# Django
DEBUG=True
SECRET_KEY=your-secret-key-here

# URLs
REACT_APP_API_URL=http://localhost:8000
```

### Personalización

Para modificar la configuración:

1. Edita `.env.docker`
2. Reinicia los servicios: `docker-manager.bat restart`

## 🐛 Solución de Problemas

### Error: "Docker no está ejecutándose"
```bash
# Solución: Inicia Docker Desktop
# Windows: Busca "Docker Desktop" en el menú inicio
```

### Error: Puerto ya en uso
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Detener servicios Docker
docker-manager.bat down
```

### Error: Problemas con volúmenes
```bash
# Limpiar volúmenes
docker-manager.bat clean

# Reconstruir todo
docker-manager.bat reset
```

### Error: Dependencias frontend
```bash
# Conectar al frontend y reinstalar
docker-manager.bat frontend
npm install
exit
docker-manager.bat restart
```

## 📊 Monitoreo

### Ver logs específicos
```bash
# Logs del backend
docker-compose logs -f backend

# Logs del frontend
docker-compose logs -f frontend

# Logs de la base de datos
docker-compose logs -f postgres
```

### Verificar salud de servicios
```bash
# Estado general
docker-compose ps

# Recursos utilizados
docker stats

# Espacio en disco
docker system df
```

## 🔄 Flujo de Desarrollo

1. **Modificar código**: Los cambios se reflejan automáticamente
   - Backend: Hot reload con Django
   - Frontend: Hot reload con React

2. **Migraciones de base de datos**:
   ```bash
   docker-manager.bat backend
   python manage.py makemigrations
   python manage.py migrate
   exit
   ```

3. **Instalar nuevas dependencias**:
   ```bash
   # Backend
   docker-manager.bat backend
   pip install nueva-dependencia
   pip freeze > requirements.txt
   exit
   
   # Frontend
   docker-manager.bat frontend
   npm install nueva-dependencia
   exit
   ```

4. **Reconstruir después de cambios**:
   ```bash
   docker-manager.bat build
   docker-manager.bat up
   ```

## 🚀 Despliegue a Producción

Para producción, usa el archivo `docker-compose.prod.yml`:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-manager.bat logs`
2. Verifica el estado: `docker-manager.bat status`
3. Reinicia: `docker-manager.bat restart`
4. Como último recurso: `docker-manager.bat reset`
