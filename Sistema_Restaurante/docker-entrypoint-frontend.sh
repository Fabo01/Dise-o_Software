#!/bin/bash
# Script de entrada para el frontend React

set -e

echo "🚀 Iniciando el frontend del Sistema de Restaurante..."

# Verificar que las dependencias estén instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias de Node.js..."
    npm install
fi

echo "🎯 Iniciando servidor de desarrollo React en puerto 3000..."
exec npm start
