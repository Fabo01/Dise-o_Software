# Sistema de Gestión de Restaurante - Frontend

Frontend moderno desarrollado en React para el sistema de gestión de restaurante. Proporciona una interfaz de usuario intuitiva y responsiva para la gestión completa de operaciones de restaurante.

## 🚀 Características

### Funcionalidades Principales
- **Dashboard Interactivo**: Vista general con estadísticas en tiempo real
- **Gestión de Pedidos**: Creación, edición y seguimiento completo de pedidos
- **Vista de Cocina**: Interface especializada para el área de cocina con tickets
- **Gestión de Mesas**: Control de disponibilidad y estados de mesas
- **Gestión de Menús**: Administración de platos y precios
- **Gestión de Clientes**: Base de datos de clientes y historial
- **Reportes**: Estadísticas y análisis de ventas
- **Sistema de Usuarios**: Autenticación y roles de usuario

### Características Técnicas
- **React 18**: Framework moderno con Hooks y Context API
- **TypeScript**: Tipado estático para mayor robustez
- **React Router**: Navegación SPA con rutas protegidas
- **React Query**: Gestión eficiente de estado del servidor
- **Tailwind CSS**: Diseño responsivo y componentes estilizados
- **Headless UI**: Componentes accesibles y personalizables
- **Axios**: Cliente HTTP para comunicación con API
- **Heroicons**: Iconografía moderna y consistente

## 🛠️ Tecnologías Utilizadas

```json
{
  "framework": "React 18.2.0",
  "language": "JavaScript/TypeScript",
  "routing": "React Router DOM 6.8.1",
  "state": "React Query 4.24.6",
  "styling": "Tailwind CSS 3.2.6",
  "ui": "Headless UI 1.7.11",
  "icons": "Heroicons 2.0.16",
  "http": "Axios 1.3.4",
  "build": "Create React App"
}
```

## 📋 Requisitos Previos

- Node.js 16.0 o superior
- npm 8.0 o superior
- Backend Django ejecutándose en puerto 8000

## 🔧 Instalación

1. **Navegar al directorio del frontend**:
   ```bash
   cd Frontend
   ```

2. **Instalar dependencias**:
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**:
   ```bash
   # Crear archivo .env en la raíz del proyecto
   REACT_APP_API_URL=http://localhost:8000/api
   REACT_APP_API_TIMEOUT=10000
   ```

4. **Iniciar el servidor de desarrollo**:
   ```bash
   npm start
   ```

5. **Acceder a la aplicación**:
   ```
   http://localhost:3000
   ```

## 🏗️ Estructura del Proyecto

```
Frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/          # Componentes React
│   │   ├── Layout/         # Componentes de layout
│   │   │   ├── Layout.js
│   │   │   ├── Header.js
│   │   │   └── Sidebar.js
│   │   ├── Dashboard.js    # Dashboard principal
│   │   ├── PedidosList.js  # Lista de pedidos
│   │   ├── PedidoModal.js  # Modal de pedidos
│   │   ├── Cocina.js       # Vista de cocina
│   │   ├── Login.js        # Autenticación
│   │   └── ProtectedRoute.js
│   ├── context/            # Contextos React
│   │   └── AuthContext.js  # Contexto de autenticación
│   ├── services/           # Servicios API
│   │   ├── apiClient.js    # Cliente HTTP base
│   │   └── pedidoService.js # Servicio de pedidos
│   ├── App.js              # Componente principal
│   ├── index.js           # Punto de entrada
│   └── index.css          # Estilos globales
├── package.json           # Dependencias y scripts
└── tailwind.config.js     # Configuración Tailwind
```

## 🎨 Componentes Principales

### Dashboard
- Estadísticas en tiempo real
- Gráficos de ventas y pedidos
- Estados de cocina y mesas
- Pedidos recientes

### Gestión de Pedidos
- Lista paginada con filtros
- Modal para crear/editar pedidos
- Cambio de estados en tiempo real
- Impresión de tickets

### Vista de Cocina
- Tickets organizados por estado
- Tiempos de preparación
- Cambio de estados rápido
- Actualización automática

### Sistema de Autenticación
- Login seguro con JWT
- Rutas protegidas por rol
- Contexto global de usuario
- Logout automático

## 🔄 Estados de Pedidos

1. **Pendiente**: Pedido creado, esperando confirmación
2. **Confirmado**: Pedido confirmado, listo para cocina
3. **Preparando**: En proceso de preparación
4. **Listo**: Preparado, esperando entrega
5. **Entregado**: Entregado al cliente
6. **Cancelado**: Pedido cancelado

## 🎯 Roles de Usuario

### Administrador
- Acceso completo a todas las funcionalidades
- Gestión de usuarios y configuración
- Reportes y estadísticas avanzadas

### Mesero
- Gestión de pedidos y mesas
- Atención al cliente
- Vista de estados de cocina

### Cocinero
- Vista exclusiva de cocina
- Gestión de estados de preparación
- Tiempos de cocina

## 🚀 Scripts Disponibles

```bash
# Desarrollo
npm start          # Inicia servidor de desarrollo

# Construcción
npm run build      # Construye para producción
npm run build:dev  # Construye para desarrollo

# Testing
npm test           # Ejecuta tests
npm run test:coverage  # Tests con cobertura

# Linting
npm run lint       # Ejecuta ESLint
npm run lint:fix   # Corrige errores automáticamente

# Formateo
npm run format     # Formatea código con Prettier
```

## 🔧 Configuración de Desarrollo

### Variables de Entorno

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_API_TIMEOUT=10000

# App Configuration
REACT_APP_NAME=Sistema Restaurante
REACT_APP_VERSION=1.0.0

# Development
REACT_APP_DEBUG=true
REACT_APP_MOCK_API=false
```

### ESLint y Prettier

El proyecto incluye configuración para:
- ESLint para análisis de código
- Prettier para formateo automático
- Husky para pre-commit hooks

## 🎨 Personalización de Estilos

### Tailwind CSS
- Configuración personalizada en `tailwind.config.js`
- Clases utilitarias personalizadas
- Tema y colores corporativos
- Componentes reutilizables

### Estilos Personalizados
```css
/* Clases utilitarias personalizadas */
.btn-primary { /* Botón principal */ }
.stat-card { /* Tarjetas de estadísticas */ }
.kitchen-ticket { /* Tickets de cocina */ }
.estado-* { /* Estados de pedidos */ }
```

## 📱 Responsividad

- **Mobile First**: Diseño optimizado para móviles
- **Breakpoints**: sm, md, lg, xl, 2xl
- **Sidebar Responsive**: Colapsable en dispositivos móviles
- **Grid Adaptativo**: Layouts que se ajustan automáticamente

## 🔒 Seguridad

- **JWT Tokens**: Autenticación basada en tokens
- **Rutas Protegidas**: Control de acceso por rol
- **Validación**: Validación de formularios y datos
- **HTTPS**: Configuración para producción segura

## 📊 Performance

- **Code Splitting**: Carga diferida de componentes
- **Lazy Loading**: Componentes cargados bajo demanda
- **Optimización**: Bundle optimizado para producción
- **Caching**: Estrategias de cache para API

## 🧪 Testing

```bash
# Tests unitarios
npm test

# Tests con cobertura
npm run test:coverage

# Tests E2E (cuando estén configurados)
npm run test:e2e
```

## 🚀 Despliegue

### Build de Producción
```bash
npm run build
```

### Variables de Entorno para Producción
```env
REACT_APP_API_URL=https://api.restaurante.com/api
REACT_APP_DEBUG=false
```

### Servidor Web
- Compatible con cualquier servidor web estático
- Nginx, Apache, o servicios cloud
- CDN recomendado para assets estáticos

## 📝 Convenciones de Código

### Estructura de Componentes
```jsx
// Imports
import React, { useState, useEffect } from 'react';

// Componente
const ComponentName = ({ prop1, prop2 }) => {
  // Hooks
  const [state, setState] = useState(initialValue);
  
  // Effects
  useEffect(() => {
    // Effect logic
  }, [dependencies]);
  
  // Handlers
  const handleEvent = () => {
    // Handler logic
  };
  
  // Render
  return (
    <div className="component-container">
      {/* JSX */}
    </div>
  );
};

export default ComponentName;
```

### Naming Conventions
- **Componentes**: PascalCase (e.g., `PedidosList`)
- **Archivos**: camelCase (e.g., `pedidoService.js`)
- **Variables**: camelCase (e.g., `currentUser`)
- **Constantes**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📞 Soporte

Para soporte técnico o consultas:
- **Documentación**: Ver archivos en `/docs`
- **Issues**: Crear issue en el repositorio
- **Email**: contacto@restaurante.com

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**Estado del Proyecto**: ✅ Funcional - En desarrollo activo

**Última Actualización**: Diciembre 2024
