#!/bin/bash

# Script de inicialización del Frontend
# Este script configura e inicia el frontend del Sistema de Restaurante

echo "🚀 Inicializando Frontend del Sistema de Restaurante..."

# Verificar que Node.js esté instalado
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    echo "   Por favor, instala Node.js 16.0 o superior desde https://nodejs.org/"
    exit 1
fi

# Verificar versión de Node.js
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt "16" ]; then
    echo "❌ Error: Se requiere Node.js 16.0 o superior"
    echo "   Versión actual: $(node --version)"
    exit 1
fi

echo "✅ Node.js $(node --version) detectado"

# Verificar que npm esté instalado
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm no está instalado"
    exit 1
fi

echo "✅ npm $(npm --version) detectado"

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📄 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo "   📝 Revisa y modifica las variables de entorno según tu configuración"
else
    echo "✅ Archivo .env encontrado"
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas exitosamente"
else
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Verificar que el backend esté ejecutándose
echo "🔍 Verificando conexión con el backend..."
BACKEND_URL=$(grep REACT_APP_API_URL .env | cut -d'=' -f2)
if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL="http://localhost:8000/api"
fi

echo "   Verificando: $BACKEND_URL"

# Usar curl para verificar el backend (timeout de 5 segundos)
if curl -s --max-time 5 "$BACKEND_URL" > /dev/null 2>&1; then
    echo "✅ Backend detectado en $BACKEND_URL"
else
    echo "⚠️  Advertencia: No se pudo conectar al backend en $BACKEND_URL"
    echo "   Asegúrate de que el backend Django esté ejecutándose"
    echo "   Puedes continuar, pero algunas funcionalidades no estarán disponibles"
fi

echo ""
echo "🎉 ¡Frontend configurado exitosamente!"
echo ""
echo "📋 Comandos disponibles:"
echo "   npm start              - Inicia el servidor de desarrollo"
echo "   npm run build          - Construye para producción"
echo "   npm test               - Ejecuta las pruebas"
echo "   npm run lint           - Ejecuta el linter"
echo ""
echo "🌐 Para iniciar el frontend, ejecuta:"
echo "   npm start"
echo ""
echo "📚 El frontend estará disponible en: http://localhost:3000"
echo "📖 Documentación completa en: README.md"
echo ""

# Preguntar si quiere iniciar automáticamente
read -p "¿Quieres iniciar el servidor de desarrollo ahora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Iniciando servidor de desarrollo..."
    npm start
fi
