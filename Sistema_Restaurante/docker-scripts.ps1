# Scripts de PowerShell para Sistema de Restaurante con Docker
# Uso: .\docker-scripts.ps1 [comando]

param(
    [Parameter(Position=0)]
    [ValidateSet("help", "build", "up", "up-dev", "down", "logs", "logs-backend", "logs-frontend", "shell-backend", "shell-frontend", "shell-db", "test", "migrate", "makemigrations", "collectstatic", "superuser", "clean", "restart", "status", "health")]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Comandos disponibles para el Sistema de Restaurante:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  build          - Construir todas las imágenes Docker" -ForegroundColor Yellow
    Write-Host "  up             - Levantar todos los servicios" -ForegroundColor Yellow
    Write-Host "  up-dev         - Levantar servicios en modo desarrollo" -ForegroundColor Yellow
    Write-Host "  down           - Detener todos los servicios" -ForegroundColor Yellow
    Write-Host "  logs           - Mostrar logs de todos los servicios" -ForegroundColor Yellow
    Write-Host "  logs-backend   - Mostrar logs solo del backend" -ForegroundColor Yellow
    Write-Host "  logs-frontend  - Mostrar logs solo del frontend" -ForegroundColor Yellow
    Write-Host "  shell-backend  - Abrir shell en el contenedor backend" -ForegroundColor Yellow
    Write-Host "  shell-frontend - Abrir shell en el contenedor frontend" -ForegroundColor Yellow
    Write-Host "  shell-db       - Abrir shell en la base de datos" -ForegroundColor Yellow
    Write-Host "  test           - Ejecutar todas las pruebas" -ForegroundColor Yellow
    Write-Host "  migrate        - Ejecutar migraciones de Django" -ForegroundColor Yellow
    Write-Host "  makemigrations - Crear nuevas migraciones" -ForegroundColor Yellow
    Write-Host "  collectstatic  - Recopilar archivos estáticos" -ForegroundColor Yellow
    Write-Host "  superuser      - Crear superusuario de Django" -ForegroundColor Yellow
    Write-Host "  clean          - Limpiar contenedores y volúmenes" -ForegroundColor Yellow
    Write-Host "  restart        - Reiniciar todos los servicios" -ForegroundColor Yellow
    Write-Host "  status         - Mostrar estado de los servicios" -ForegroundColor Yellow
    Write-Host "  health         - Verificar salud de los servicios" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Ejemplo de uso:" -ForegroundColor Cyan
    Write-Host "  .\docker-scripts.ps1 up" -ForegroundColor White
}

function Build-Images {
    Write-Host "Construyendo imágenes Docker..." -ForegroundColor Green
    docker-compose build --no-cache
}

function Start-Services {
    Write-Host "Levantando servicios..." -ForegroundColor Green
    docker-compose up -d
    Write-Host ""
    Write-Host "Servicios levantados. Accede a:" -ForegroundColor Green
    Write-Host "  - Frontend: http://localhost:80" -ForegroundColor Cyan
    Write-Host "  - Backend API: http://localhost:80/api/" -ForegroundColor Cyan
    Write-Host "  - Django Admin: http://localhost:80/admin/" -ForegroundColor Cyan
    Write-Host "  - Swagger: http://localhost:80/swagger/" -ForegroundColor Cyan
    Write-Host "  - Adminer: http://localhost:8080" -ForegroundColor Cyan
}

function Start-Dev-Services {
    Write-Host "Levantando servicios de desarrollo..." -ForegroundColor Green
    docker-compose -f docker-compose.dev.yml up -d
    Write-Host ""
    Write-Host "Servicios de desarrollo levantados. Accede a:" -ForegroundColor Green
    Write-Host "  - Frontend: http://localhost:3001" -ForegroundColor Cyan
    Write-Host "  - Backend API: http://localhost:8001/api/" -ForegroundColor Cyan
    Write-Host "  - Django Admin: http://localhost:8001/admin/" -ForegroundColor Cyan
    Write-Host "  - Swagger: http://localhost:8001/swagger/" -ForegroundColor Cyan
}

function Stop-Services {
    Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
    docker-compose down
}

function Show-Logs {
    Write-Host "Mostrando logs de todos los servicios..." -ForegroundColor Green
    docker-compose logs -f
}

function Show-Backend-Logs {
    Write-Host "Mostrando logs del backend..." -ForegroundColor Green
    docker-compose logs -f backend
}

function Show-Frontend-Logs {
    Write-Host "Mostrando logs del frontend..." -ForegroundColor Green
    docker-compose logs -f frontend
}

function Open-Backend-Shell {
    Write-Host "Abriendo shell del backend..." -ForegroundColor Green
    docker-compose exec backend bash
}

function Open-Frontend-Shell {
    Write-Host "Abriendo shell del frontend..." -ForegroundColor Green
    docker-compose exec frontend sh
}

function Open-DB-Shell {
    Write-Host "Abriendo shell de la base de datos..." -ForegroundColor Green
    docker-compose exec postgres psql -U restaurant_user -d restaurant_db
}

function Run-Tests {
    Write-Host "Ejecutando pruebas..." -ForegroundColor Green
    docker-compose exec backend pytest
}

function Run-Migrations {
    Write-Host "Ejecutando migraciones..." -ForegroundColor Green
    docker-compose exec backend python manage.py migrate
}

function Make-Migrations {
    Write-Host "Creando migraciones..." -ForegroundColor Green
    docker-compose exec backend python manage.py makemigrations
}

function Collect-Static {
    Write-Host "Recopilando archivos estáticos..." -ForegroundColor Green
    docker-compose exec backend python manage.py collectstatic --noinput
}

function Create-Superuser {
    Write-Host "Creando superusuario..." -ForegroundColor Green
    docker-compose exec backend python manage.py createsuperuser
}

function Clean-Docker {
    Write-Host "Limpiando contenedores y volúmenes..." -ForegroundColor Yellow
    docker-compose down -v --remove-orphans
    docker system prune -f
    docker volume prune -f
}

function Restart-Services {
    Write-Host "Reiniciando servicios..." -ForegroundColor Yellow
    docker-compose restart
}

function Show-Status {
    Write-Host "Estado de los servicios:" -ForegroundColor Green
    docker-compose ps
}

function Check-Health {
    Write-Host "Verificando salud de los servicios..." -ForegroundColor Green
    
    # Verificar backend
    try {
        $backendHealth = docker-compose exec backend curl -f http://localhost:8000/admin/ 2>$null
        Write-Host "Backend: OK" -ForegroundColor Green
    }
    catch {
        Write-Host "Backend: ERROR" -ForegroundColor Red
    }
    
    # Verificar frontend
    try {
        $frontendHealth = docker-compose exec frontend curl -f http://localhost:3000 2>$null
        Write-Host "Frontend: OK" -ForegroundColor Green
    }
    catch {
        Write-Host "Frontend: ERROR" -ForegroundColor Red
    }
    
    # Verificar PostgreSQL
    try {
        $dbHealth = docker-compose exec postgres pg_isready -U restaurant_user 2>$null
        Write-Host "PostgreSQL: OK" -ForegroundColor Green
    }
    catch {
        Write-Host "PostgreSQL: ERROR" -ForegroundColor Red
    }
    
    # Verificar Redis
    try {
        $redisHealth = docker-compose exec redis redis-cli ping 2>$null
        Write-Host "Redis: OK" -ForegroundColor Green
    }
    catch {
        Write-Host "Redis: ERROR" -ForegroundColor Red
    }
}

# Ejecutar comando
switch ($Command) {
    "help" { Show-Help }
    "build" { Build-Images }
    "up" { Start-Services }
    "up-dev" { Start-Dev-Services }
    "down" { Stop-Services }
    "logs" { Show-Logs }
    "logs-backend" { Show-Backend-Logs }
    "logs-frontend" { Show-Frontend-Logs }
    "shell-backend" { Open-Backend-Shell }
    "shell-frontend" { Open-Frontend-Shell }
    "shell-db" { Open-DB-Shell }
    "test" { Run-Tests }
    "migrate" { Run-Migrations }
    "makemigrations" { Make-Migrations }
    "collectstatic" { Collect-Static }
    "superuser" { Create-Superuser }
    "clean" { Clean-Docker }
    "restart" { Restart-Services }
    "status" { Show-Status }
    "health" { Check-Health }
}
