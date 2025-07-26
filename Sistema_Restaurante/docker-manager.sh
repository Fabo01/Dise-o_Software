#!/bin/bash
# Script para gestión de Docker del Sistema de Restaurante

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}🐳 Sistema de Gestión de Restaurante - Docker Manager${NC}"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponibles:"
    echo "  build     - Construir todas las imágenes"
    echo "  up        - Levantar todos los servicios"
    echo "  down      - Detener todos los servicios"
    echo "  restart   - Reiniciar todos los servicios"
    echo "  logs      - Mostrar logs de todos los servicios"
    echo "  status    - Mostrar estado de los servicios"
    echo "  clean     - Limpiar contenedores, imágenes y volúmenes"
    echo "  reset     - Reiniciar completamente (down + clean + build + up)"
    echo "  backend   - Conectar al contenedor del backend"
    echo "  frontend  - Conectar al contenedor del frontend"
    echo "  db        - Conectar a la base de datos PostgreSQL"
    echo "  migrate   - Ejecutar migraciones de Django"
    echo "  test      - Ejecutar tests"
    echo "  help      - Mostrar esta ayuda"
}

# Función para verificar si Docker está ejecutándose
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Error: Docker no está ejecutándose${NC}"
        echo "Por favor, inicia Docker Desktop y vuelve a intentar."
        exit 1
    fi
}

# Función para construir imágenes
build_images() {
    echo -e "${BLUE}🔨 Construyendo imágenes Docker...${NC}"
    docker-compose build --no-cache
    echo -e "${GREEN}✅ Imágenes construidas exitosamente${NC}"
}

# Función para levantar servicios
start_services() {
    echo -e "${BLUE}🚀 Iniciando servicios...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ Servicios iniciados${NC}"
    echo ""
    echo -e "${YELLOW}📋 URLs disponibles:${NC}"
    echo "  🌐 Frontend: http://localhost:3000"
    echo "  🔧 Backend API: http://localhost:8000"
    echo "  📖 Swagger/API Docs: http://localhost:8000/swagger/"
    echo "  👑 Django Admin: http://localhost:8000/admin/"
    echo "  🗄️  PostgreSQL: localhost:5432"
    echo "  🗃️  Redis: localhost:6379"
}

# Función para detener servicios
stop_services() {
    echo -e "${BLUE}🛑 Deteniendo servicios...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Servicios detenidos${NC}"
}

# Función para mostrar logs
show_logs() {
    echo -e "${BLUE}📜 Mostrando logs...${NC}"
    docker-compose logs -f
}

# Función para mostrar estado
show_status() {
    echo -e "${BLUE}📊 Estado de los servicios:${NC}"
    docker-compose ps
    echo ""
    echo -e "${BLUE}💾 Uso de volúmenes:${NC}"
    docker system df
}

# Función para limpiar
clean_all() {
    echo -e "${YELLOW}⚠️  Esto eliminará todos los contenedores, imágenes y volúmenes${NC}"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🧹 Limpiando...${NC}"
        docker-compose down -v --rmi all --remove-orphans
        docker system prune -af --volumes
        echo -e "${GREEN}✅ Limpieza completada${NC}"
    else
        echo -e "${YELLOW}❌ Limpieza cancelada${NC}"
    fi
}

# Función para reset completo
reset_all() {
    echo -e "${YELLOW}⚠️  Esto reiniciará completamente el sistema${NC}"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        stop_services
        clean_all
        build_images
        start_services
        echo -e "${GREEN}✅ Reset completado${NC}"
    else
        echo -e "${YELLOW}❌ Reset cancelado${NC}"
    fi
}

# Función para conectar al backend
connect_backend() {
    echo -e "${BLUE}🔗 Conectando al contenedor del backend...${NC}"
    docker-compose exec backend bash
}

# Función para conectar al frontend
connect_frontend() {
    echo -e "${BLUE}🔗 Conectando al contenedor del frontend...${NC}"
    docker-compose exec frontend sh
}

# Función para conectar a la base de datos
connect_db() {
    echo -e "${BLUE}🔗 Conectando a PostgreSQL...${NC}"
    docker-compose exec postgres psql -U restaurant_user -d restaurant_db
}

# Función para ejecutar migraciones
run_migrations() {
    echo -e "${BLUE}🔄 Ejecutando migraciones...${NC}"
    docker-compose exec backend python manage.py migrate
    echo -e "${GREEN}✅ Migraciones completadas${NC}"
}

# Función para ejecutar tests
run_tests() {
    echo -e "${BLUE}🧪 Ejecutando tests...${NC}"
    docker-compose exec backend python manage.py test
    echo -e "${GREEN}✅ Tests completados${NC}"
}

# Verificar Docker
check_docker

# Procesar comando
case "$1" in
    build)
        build_images
        ;;
    up)
        start_services
        ;;
    down)
        stop_services
        ;;
    restart)
        stop_services
        start_services
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    reset)
        reset_all
        ;;
    backend)
        connect_backend
        ;;
    frontend)
        connect_frontend
        ;;
    db)
        connect_db
        ;;
    migrate)
        run_migrations
        ;;
    test)
        run_tests
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando desconocido: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
