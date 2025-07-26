# Makefile para Sistema de Restaurante con Docker
# Uso: make [comando]

.PHONY: help build up down logs shell-backend shell-frontend test clean restart migrate collectstatic

# Comando por defecto
help:
	@echo "Comandos disponibles para el Sistema de Restaurante:"
	@echo ""
	@echo "  build          - Construir todas las imágenes Docker"
	@echo "  up             - Levantar todos los servicios"
	@echo "  up-dev         - Levantar servicios en modo desarrollo"
	@echo "  down           - Detener todos los servicios"
	@echo "  logs           - Mostrar logs de todos los servicios"
	@echo "  logs-backend   - Mostrar logs solo del backend"
	@echo "  logs-frontend  - Mostrar logs solo del frontend"
	@echo "  shell-backend  - Abrir shell en el contenedor backend"
	@echo "  shell-frontend - Abrir shell en el contenedor frontend"
	@echo "  shell-db       - Abrir shell en la base de datos"
	@echo "  test           - Ejecutar todas las pruebas"
	@echo "  test-backend   - Ejecutar pruebas del backend"
	@echo "  migrate        - Ejecutar migraciones de Django"
	@echo "  makemigrations - Crear nuevas migraciones"
	@echo "  collectstatic  - Recopilar archivos estáticos"
	@echo "  superuser      - Crear superusuario de Django"
	@echo "  clean          - Limpiar contenedores y volúmenes"
	@echo "  restart        - Reiniciar todos los servicios"
	@echo "  status         - Mostrar estado de los servicios"

# Construcción
build:
	docker-compose build --no-cache

build-dev:
	docker-compose -f docker-compose.dev.yml build --no-cache

# Servicios
up:
	docker-compose up -d
	@echo "Servicios levantados. Accede a:"
	@echo "  - Frontend: http://localhost:80"
	@echo "  - Backend API: http://localhost:80/api/"
	@echo "  - Django Admin: http://localhost:80/admin/"
	@echo "  - Swagger: http://localhost:80/swagger/"
	@echo "  - Adminer: http://localhost:8080"

up-dev:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Servicios de desarrollo levantados. Accede a:"
	@echo "  - Frontend: http://localhost:3001"
	@echo "  - Backend API: http://localhost:8001/api/"
	@echo "  - Django Admin: http://localhost:8001/admin/"
	@echo "  - Swagger: http://localhost:8001/swagger/"

down:
	docker-compose down

down-dev:
	docker-compose -f docker-compose.dev.yml down

# Logs
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f postgres

# Shells
shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

shell-db:
	docker-compose exec postgres psql -U restaurant_user -d restaurant_db

# Base de datos
migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

superuser:
	docker-compose exec backend python manage.py createsuperuser

# Archivos estáticos
collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput

# Pruebas
test:
	docker-compose exec backend python manage.py test

test-backend:
	docker-compose exec backend pytest

test-bdd:
	docker-compose exec backend pytest --bdd-features=tests/features/

# Utilidades
status:
	docker-compose ps

restart:
	docker-compose restart

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
	docker volume prune -f

# Desarrollo
install-backend:
	docker-compose exec backend pip install -r requirements.txt

install-frontend:
	docker-compose exec frontend npm install

# Monitoreo
health:
	@echo "Verificando salud de los servicios..."
	@docker-compose exec backend curl -f http://localhost:8000/admin/ || echo "Backend: ERROR"
	@docker-compose exec frontend curl -f http://localhost:3000 || echo "Frontend: ERROR"
	@docker-compose exec postgres pg_isready -U restaurant_user || echo "PostgreSQL: ERROR"
	@docker-compose exec redis redis-cli ping || echo "Redis: ERROR"
