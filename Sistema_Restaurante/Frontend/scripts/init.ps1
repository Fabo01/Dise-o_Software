# Script de inicialización del Frontend para Windows PowerShell
# Este script configura e inicia el frontend del Sistema de Restaurante

Write-Host "🚀 Inicializando Frontend del Sistema de Restaurante..." -ForegroundColor Green

# Verificar que Node.js esté instalado
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js $nodeVersion detectado" -ForegroundColor Green
    
    # Verificar versión mínima
    $versionNumber = $nodeVersion.Replace('v', '').Split('.')[0]
    if ([int]$versionNumber -lt 16) {
        Write-Host "❌ Error: Se requiere Node.js 16.0 o superior" -ForegroundColor Red
        Write-Host "   Versión actual: $nodeVersion" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Error: Node.js no está instalado" -ForegroundColor Red
    Write-Host "   Por favor, instala Node.js 16.0 o superior desde https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Verificar que npm esté instalado
try {
    $npmVersion = npm --version
    Write-Host "✅ npm $npmVersion detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: npm no está instalado" -ForegroundColor Red
    exit 1
}

# Crear archivo .env si no existe
if (-not (Test-Path ".env")) {
    Write-Host "📄 Creando archivo .env desde .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Archivo .env creado" -ForegroundColor Green
    Write-Host "   📝 Revisa y modifica las variables de entorno según tu configuración" -ForegroundColor Yellow
} else {
    Write-Host "✅ Archivo .env encontrado" -ForegroundColor Green
}

# Instalar dependencias
Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias instaladas exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

# Verificar que el backend esté ejecutándose
Write-Host "🔍 Verificando conexión con el backend..." -ForegroundColor Yellow

# Leer la URL del backend desde .env
$backendUrl = "http://localhost:8000/api"
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    $backendLine = $envContent | Where-Object { $_ -like "REACT_APP_API_URL=*" }
    if ($backendLine) {
        $backendUrl = $backendLine.Split('=')[1]
    }
}

Write-Host "   Verificando: $backendUrl" -ForegroundColor Gray

# Verificar el backend con timeout
try {
    $response = Invoke-WebRequest -Uri $backendUrl -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Backend detectado en $backendUrl" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Advertencia: No se pudo conectar al backend en $backendUrl" -ForegroundColor Yellow
    Write-Host "   Asegúrate de que el backend Django esté ejecutándose" -ForegroundColor Yellow
    Write-Host "   Puedes continuar, pero algunas funcionalidades no estarán disponibles" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 ¡Frontend configurado exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Comandos disponibles:" -ForegroundColor Cyan
Write-Host "   npm start              - Inicia el servidor de desarrollo" -ForegroundColor White
Write-Host "   npm run build          - Construye para producción" -ForegroundColor White
Write-Host "   npm test               - Ejecuta las pruebas" -ForegroundColor White
Write-Host "   npm run lint           - Ejecuta el linter" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Para iniciar el frontend, ejecuta:" -ForegroundColor Cyan
Write-Host "   npm start" -ForegroundColor White
Write-Host ""
Write-Host "📚 El frontend estará disponible en: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📖 Documentación completa en: README.md" -ForegroundColor Cyan
Write-Host ""

# Preguntar si quiere iniciar automáticamente
$response = Read-Host "¿Quieres iniciar el servidor de desarrollo ahora? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host "🚀 Iniciando servidor de desarrollo..." -ForegroundColor Green
    npm start
}
