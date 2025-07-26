#!/bin/bash
# Script de entrada para el backend Django

set -e

echo "🚀 Iniciando el backend del Sistema de Restaurante..."

# Esperar a que PostgreSQL esté disponible
echo "⏳ Esperando a PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL está disponible"

# Esperar a que Redis esté disponible
echo "⏳ Esperando a Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "✅ Redis está disponible"

# Cambiar al directorio del backend
cd /app/Backend

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "📂 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe (para desarrollo)
echo "👤 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@restaurant.com', 'admin123')
    print('✅ Superusuario creado: admin/admin123')
else:
    print('✅ Superusuario ya existe')
"

# Cargar datos de prueba si están disponibles
if [ -f "/app/Backend/fixtures/initial_data.json" ]; then
    echo "📊 Cargando datos de prueba..."
    python manage.py loaddata initial_data.json
fi

echo "🎯 Iniciando servidor Django en puerto 8000..."
exec python manage.py runserver 0.0.0.0:8000
