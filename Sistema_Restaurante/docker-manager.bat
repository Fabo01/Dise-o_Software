@echo off
REM Script de gestión Docker para Windows
REM Sistema de Gestión de Restaurante

setlocal enabledelayedexpansion

REM Colores para CMD (limitados)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

if "%1"=="" goto :show_help
if "%1"=="help" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

REM Verificar que Docker esté ejecutándose
docker info >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Error: Docker no está ejecutándose%NC%
    echo Por favor, inicia Docker Desktop y vuelve a intentar.
    exit /b 1
)

if "%1"=="build" goto :build_images
if "%1"=="up" goto :start_services
if "%1"=="down" goto :stop_services
if "%1"=="restart" goto :restart_services
if "%1"=="logs" goto :show_logs
if "%1"=="status" goto :show_status
if "%1"=="clean" goto :clean_all
if "%1"=="reset" goto :reset_all
if "%1"=="backend" goto :connect_backend
if "%1"=="frontend" goto :connect_frontend
if "%1"=="db" goto :connect_db
if "%1"=="migrate" goto :run_migrations
if "%1"=="test" goto :run_tests

echo %RED%❌ Comando desconocido: %1%NC%
echo.
goto :show_help

:show_help
echo %BLUE%🐳 Sistema de Gestión de Restaurante - Docker Manager%NC%
echo.
echo Uso: %0 [COMANDO]
echo.
echo Comandos disponibles:
echo   build     - Construir todas las imágenes
echo   up        - Levantar todos los servicios
echo   down      - Detener todos los servicios
echo   restart   - Reiniciar todos los servicios
echo   logs      - Mostrar logs de todos los servicios
echo   status    - Mostrar estado de los servicios
echo   clean     - Limpiar contenedores, imágenes y volúmenes
echo   reset     - Reiniciar completamente (down + clean + build + up)
echo   backend   - Conectar al contenedor del backend
echo   frontend  - Conectar al contenedor del frontend
echo   db        - Conectar a la base de datos PostgreSQL
echo   migrate   - Ejecutar migraciones de Django
echo   test      - Ejecutar tests
echo   help      - Mostrar esta ayuda
echo.
echo %YELLOW%📋 URLs disponibles después de 'up':%NC%
echo   🌐 Frontend: http://localhost:3000
echo   🔧 Backend API: http://localhost:8000
echo   📖 Swagger/API Docs: http://localhost:8000/swagger/
echo   👑 Django Admin: http://localhost:8000/admin/
exit /b 0

:build_images
echo %BLUE%🔨 Construyendo imágenes Docker...%NC%
docker-compose build --no-cache
if errorlevel 1 (
    echo %RED%❌ Error al construir las imágenes%NC%
    exit /b 1
)
echo %GREEN%✅ Imágenes construidas exitosamente%NC%
exit /b 0

:start_services
echo %BLUE%🚀 Iniciando servicios...%NC%
docker-compose up -d
if errorlevel 1 (
    echo %RED%❌ Error al iniciar servicios%NC%
    exit /b 1
)
echo %GREEN%✅ Servicios iniciados%NC%
echo.
echo %YELLOW%📋 URLs disponibles:%NC%
echo   🌐 Frontend: http://localhost:3000
echo   🔧 Backend API: http://localhost:8000
echo   📖 Swagger/API Docs: http://localhost:8000/swagger/
echo   👑 Django Admin: http://localhost:8000/admin/
echo   🗄️  PostgreSQL: localhost:5432
echo   🗃️  Redis: localhost:6379
exit /b 0

:stop_services
echo %BLUE%🛑 Deteniendo servicios...%NC%
docker-compose down
echo %GREEN%✅ Servicios detenidos%NC%
exit /b 0

:restart_services
call :stop_services
call :start_services
exit /b 0

:show_logs
echo %BLUE%📜 Mostrando logs...%NC%
docker-compose logs -f
exit /b 0

:show_status
echo %BLUE%📊 Estado de los servicios:%NC%
docker-compose ps
echo.
echo %BLUE%💾 Uso de volúmenes:%NC%
docker system df
exit /b 0

:clean_all
echo %YELLOW%⚠️  Esto eliminará todos los contenedores, imágenes y volúmenes%NC%
set /p answer="¿Estás seguro? (y/N): "
if /i "!answer!"=="y" (
    echo %BLUE%🧹 Limpiando...%NC%
    docker-compose down -v --rmi all --remove-orphans
    docker system prune -af --volumes
    echo %GREEN%✅ Limpieza completada%NC%
) else (
    echo %YELLOW%❌ Limpieza cancelada%NC%
)
exit /b 0

:reset_all
echo %YELLOW%⚠️  Esto reiniciará completamente el sistema%NC%
set /p answer="¿Estás seguro? (y/N): "
if /i "!answer!"=="y" (
    call :stop_services
    call :clean_all
    call :build_images
    call :start_services
    echo %GREEN%✅ Reset completado%NC%
) else (
    echo %YELLOW%❌ Reset cancelado%NC%
)
exit /b 0

:connect_backend
echo %BLUE%🔗 Conectando al contenedor del backend...%NC%
docker-compose exec backend bash
exit /b 0

:connect_frontend
echo %BLUE%🔗 Conectando al contenedor del frontend...%NC%
docker-compose exec frontend sh
exit /b 0

:connect_db
echo %BLUE%🔗 Conectando a PostgreSQL...%NC%
docker-compose exec postgres psql -U restaurant_user -d restaurant_db
exit /b 0

:run_migrations
echo %BLUE%🔄 Ejecutando migraciones...%NC%
docker-compose exec backend python manage.py migrate
echo %GREEN%✅ Migraciones completadas%NC%
exit /b 0

:run_tests
echo %BLUE%🧪 Ejecutando tests...%NC%
docker-compose exec backend python manage.py test
echo %GREEN%✅ Tests completados%NC%
exit /b 0
