# Manual Técnico - Sistema de Gestión de Restaurante
# S3-38: Documentación técnica para desarrolladores

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Backend - Django](#backend---django)
4. [Frontend - React](#frontend---react)
5. [Base de Datos](#base-de-datos)
6. [APIs y Servicios](#apis-y-servicios)
7. [Testing](#testing)
8. [Performance y Optimización](#performance-y-optimización)
9. [Deployment](#deployment)
10. [Contribución](#contribución)

---

## 🏗️ Arquitectura del Sistema

### Arquitectura General

El sistema sigue una arquitectura en capas (Clean Architecture) con separación clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLEAN ARCHITECTURE                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  PRESENTACIÓN   │   APLICACIÓN    │         DOMINIO             │
│                 │                 │                             │
│ • Controllers   │ • Services      │ • Entities                  │
│ • Serializers   │ • DTOs          │ • Value Objects             │
│ • Views         │ • Interfaces    │ • Domain Services           │
│ • URLs          │ • Exceptions    │ • Factories                 │
├─────────────────┼─────────────────┼─────────────────────────────┤
│                        INFRAESTRUCTURA                         │
│ • Models        • Repositories    • External Services          │
│ • Database      • Cache           • Email, SMS, etc.           │
│ • ORM           • File System     • Payment Gateways           │
└─────────────────────────────────────────────────────────────────┘
```

### Patrones de Diseño Implementados

1. **Repository Pattern**: Abstracción de acceso a datos
2. **Service Layer**: Lógica de negocio centralizada
3. **Factory Pattern**: Creación de objetos complejos
4. **Observer Pattern**: Notificaciones y eventos
5. **Strategy Pattern**: Diferentes métodos de pago
6. **Command Pattern**: Operaciones del sistema

### Stack Tecnológico

**Backend:**
- Python 3.11+
- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL 14+
- Redis 6+ (Cache)
- Celery (Tareas asíncronas)

**Frontend:**
- React 18+
- TypeScript/JavaScript
- Tailwind CSS 3+
- Vite (Build tool)
- React Router 6+
- Axios (HTTP client)

**DevOps:**
- Docker & Docker Compose
- Nginx (Reverse proxy)
- Gunicorn (WSGI server)
- Pytest (Testing)
- GitHub Actions (CI/CD)

---

## 📁 Estructura del Proyecto

### Estructura Completa

```
Sistema_Restaurante/
├── Backend/
│   ├── Aplicacion/
│   │   ├── DTOs/
│   │   ├── Excepciones/
│   │   ├── Interfaces/
│   │   └── Servicios/
│   ├── Config/
│   │   ├── Settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Dominio/
│   │   ├── Entidades/
│   │   ├── Excepciones/
│   │   ├── Factories/
│   │   ├── Interfaces/
│   │   └── Objetos_Valor/
│   ├── Infraestructura/
│   │   ├── Modelos/
│   │   ├── Repositorios/
│   │   └── servicios_externos/
│   ├── Presentacion/
│   │   ├── Controladores/
│   │   ├── Serializadores/
│   │   ├── Views/
│   │   └── urls.py
│   └── tests/
├── Frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── utils/
│   │   └── pages/
│   └── tests/
├── Docs/
└── requirements.txt
```

### Convenciones de Nomenclatura

**Backend (Python):**
- Clases: `PascalCase` (ej: `ClienteService`)
- Funciones/métodos: `snake_case` (ej: `obtener_cliente`)
- Variables: `snake_case` (ej: `total_pedido`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `MAX_INTENTOS`)

**Frontend (JavaScript/React):**
- Componentes: `PascalCase` (ej: `ClienteCard`)
- Funciones: `camelCase` (ej: `handleSubmit`)
- Variables: `camelCase` (ej: `userData`)
- Archivos: `kebab-case` (ej: `user-service.js`)

---

## ⚙️ Backend - Django

### Estructura de Capas

#### 1. Capa de Dominio

**Entidades:**
```python
# Backend/Dominio/Entidades/Cliente.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Cliente:
    id: Optional[int]
    rut: str
    nombre: str
    email: str
    telefono: str
    direccion: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    activo: bool = True
    
    def validar_rut(self) -> bool:
        """Validar formato y dígito verificador del RUT"""
        # Implementación de validación
        pass
    
    def es_cliente_frecuente(self, umbral_pedidos: int = 10) -> bool:
        """Determinar si es cliente frecuente"""
        # Lógica de negocio
        pass
```

**Value Objects:**
```python
# Backend/Dominio/Objetos_Valor/Dinero.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Dinero:
    monto: Decimal
    moneda: str = 'CLP'
    
    def __post_init__(self):
        if self.monto < 0:
            raise ValueError("El monto no puede ser negativo")
    
    def sumar(self, otro: 'Dinero') -> 'Dinero':
        if self.moneda != otro.moneda:
            raise ValueError("No se pueden sumar monedas diferentes")
        return Dinero(self.monto + otro.monto, self.moneda)
```

#### 2. Capa de Aplicación

**Servicios:**
```python
# Backend/Aplicacion/Servicios/ClienteService.py
from typing import List, Optional
from Backend.Dominio.Entidades.Cliente import Cliente
from Backend.Dominio.Interfaces.IClienteRepository import IClienteRepository
from Backend.Aplicacion.DTOs.ClienteDTO import ClienteDTO, CrearClienteDTO

class ClienteService:
    def __init__(self, cliente_repository: IClienteRepository):
        self._cliente_repository = cliente_repository
    
    def crear_cliente(self, datos: CrearClienteDTO) -> ClienteDTO:
        """Crear nuevo cliente con validaciones de negocio"""
        # Validar RUT único
        if self._cliente_repository.existe_rut(datos.rut):
            raise ValueError("El RUT ya está registrado")
        
        # Crear entidad
        cliente = Cliente(
            id=None,
            rut=datos.rut,
            nombre=datos.nombre,
            email=datos.email,
            telefono=datos.telefono,
            direccion=datos.direccion
        )
        
        # Validar entidad
        if not cliente.validar_rut():
            raise ValueError("RUT inválido")
        
        # Persistir
        cliente_creado = self._cliente_repository.guardar(cliente)
        
        # Retornar DTO
        return ClienteDTO.from_entity(cliente_creado)
    
    def obtener_clientes_activos(self) -> List[ClienteDTO]:
        """Obtener lista de clientes activos"""
        clientes = self._cliente_repository.obtener_activos()
        return [ClienteDTO.from_entity(c) for c in clientes]
```

**DTOs:**
```python
# Backend/Aplicacion/DTOs/ClienteDTO.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ClienteDTO:
    id: int
    rut: str
    nombre: str
    email: str
    telefono: str
    direccion: Optional[str]
    fecha_creacion: datetime
    activo: bool
    
    @classmethod
    def from_entity(cls, cliente: Cliente) -> 'ClienteDTO':
        return cls(
            id=cliente.id,
            rut=cliente.rut,
            nombre=cliente.nombre,
            email=cliente.email,
            telefono=cliente.telefono,
            direccion=cliente.direccion,
            fecha_creacion=cliente.fecha_creacion,
            activo=cliente.activo
        )

@dataclass
class CrearClienteDTO:
    rut: str
    nombre: str
    email: str
    telefono: str
    direccion: Optional[str] = None
```

#### 3. Capa de Infraestructura

**Modelos:**
```python
# Backend/Infraestructura/Modelos/ClienteModel.py
from django.db import models
from django.core.validators import RegexValidator

class ClienteModel(models.Model):
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[0-9Kk]$',
                message='Formato de RUT inválido'
            )
        ]
    )
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'clientes'
        indexes = [
            models.Index(fields=['rut']),
            models.Index(fields=['email']),
            models.Index(fields=['-fecha_creacion']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.rut})"
```

**Repositorios:**
```python
# Backend/Infraestructura/Repositorios/ClienteRepository.py
from typing import List, Optional
from Backend.Dominio.Entidades.Cliente import Cliente
from Backend.Dominio.Interfaces.IClienteRepository import IClienteRepository
from Backend.Infraestructura.Modelos.ClienteModel import ClienteModel

class ClienteRepository(IClienteRepository):
    def guardar(self, cliente: Cliente) -> Cliente:
        """Guardar cliente en base de datos"""
        if cliente.id:
            # Actualizar
            model = ClienteModel.objects.get(id=cliente.id)
            model.nombre = cliente.nombre
            model.email = cliente.email
            model.telefono = cliente.telefono
            model.direccion = cliente.direccion
            model.activo = cliente.activo
        else:
            # Crear
            model = ClienteModel(
                rut=cliente.rut,
                nombre=cliente.nombre,
                email=cliente.email,
                telefono=cliente.telefono,
                direccion=cliente.direccion,
                activo=cliente.activo
            )
        
        model.save()
        return self._model_to_entity(model)
    
    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Obtener cliente por ID"""
        try:
            model = ClienteModel.objects.get(id=cliente_id)
            return self._model_to_entity(model)
        except ClienteModel.DoesNotExist:
            return None
    
    def obtener_activos(self) -> List[Cliente]:
        """Obtener clientes activos"""
        models = ClienteModel.objects.filter(activo=True)
        return [self._model_to_entity(m) for m in models]
    
    def existe_rut(self, rut: str) -> bool:
        """Verificar si RUT ya existe"""
        return ClienteModel.objects.filter(rut=rut).exists()
    
    def _model_to_entity(self, model: ClienteModel) -> Cliente:
        """Convertir model a entidad"""
        return Cliente(
            id=model.id,
            rut=model.rut,
            nombre=model.nombre,
            email=model.email,
            telefono=model.telefono,
            direccion=model.direccion,
            fecha_creacion=model.fecha_creacion,
            activo=model.activo
        )
```

#### 4. Capa de Presentación

**Controladores:**
```python
# Backend/Presentacion/Controladores/ClienteController.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Backend.Aplicacion.Servicios.ClienteService import ClienteService
from Backend.Aplicacion.DTOs.ClienteDTO import CrearClienteDTO
from Backend.Presentacion.Serializadores.ClienteSerializer import ClienteSerializer

@api_view(['GET', 'POST'])
def clientes_list(request):
    """Lista de clientes y creación"""
    cliente_service = ClienteService()
    
    if request.method == 'GET':
        clientes = cliente_service.obtener_clientes_activos()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                dto = CrearClienteDTO(**serializer.validated_data)
                cliente_creado = cliente_service.crear_cliente(dto)
                response_serializer = ClienteSerializer(cliente_creado)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Serializadores:**
```python
# Backend/Presentacion/Serializadores/ClienteSerializer.py
from rest_framework import serializers

class ClienteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rut = serializers.CharField(max_length=12)
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    telefono = serializers.CharField(max_length=15)
    direccion = serializers.CharField(required=False, allow_blank=True)
    fecha_creacion = serializers.DateTimeField(read_only=True)
    activo = serializers.BooleanField(default=True)
    
    def validate_rut(self, value):
        """Validar formato de RUT"""
        import re
        if not re.match(r'^\d{7,8}-[0-9Kk]$', value):
            raise serializers.ValidationError("Formato de RUT inválido")
        return value
```

### Dependencias y Configuración

**requirements.txt:**
```
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.7
redis==4.6.0
celery==5.3.4
django-cors-headers==4.3.1
django-environ==0.11.2
gunicorn==21.2.0
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
```

**Settings:**
```python
# Backend/Config/Settings/base.py
import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [
    'Backend.Infraestructura',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Backend.Config.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

---

## ⚛️ Frontend - React

### Estructura de Componentes

```
src/
├── components/
│   ├── common/           # Componentes reutilizables
│   ├── layout/           # Layout y navegación
│   ├── forms/            # Formularios
│   └── ui/               # Componentes UI básicos
├── pages/                # Páginas principales
├── hooks/                # Custom hooks
├── services/             # Servicios API
├── utils/                # Utilidades
├── context/              # Context providers
├── types/                # TypeScript types
└── __tests__/            # Tests
```

### Componentes Principales

**Componente de Cliente:**
```jsx
// Frontend/src/components/Cliente/ClienteCard.jsx
import React from 'react';
import { formatRut, formatDate } from '../../utils/formatters';

const ClienteCard = ({ cliente, onEdit, onDelete, onViewHistory }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {cliente.nombre}
          </h3>
          <p className="text-sm text-gray-600">
            RUT: {formatRut(cliente.rut)}
          </p>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          cliente.activo 
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}>
          {cliente.activo ? 'Activo' : 'Inactivo'}
        </span>
      </div>
      
      <div className="space-y-2 mb-4">
        <p className="text-sm">
          <span className="font-medium">Email:</span> {cliente.email}
        </p>
        <p className="text-sm">
          <span className="font-medium">Teléfono:</span> {cliente.telefono}
        </p>
        {cliente.direccion && (
          <p className="text-sm">
            <span className="font-medium">Dirección:</span> {cliente.direccion}
          </p>
        )}
        <p className="text-sm text-gray-500">
          Registrado: {formatDate(cliente.fecha_creacion)}
        </p>
      </div>
      
      <div className="flex justify-end space-x-2">
        <button
          onClick={() => onViewHistory(cliente.id)}
          className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
        >
          Historial
        </button>
        <button
          onClick={() => onEdit(cliente)}
          className="px-3 py-1 text-sm bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
        >
          Editar
        </button>
        <button
          onClick={() => onDelete(cliente.id)}
          className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
        >
          Eliminar
        </button>
      </div>
    </div>
  );
};

export default ClienteCard;
```

**Custom Hook para Cliente:**
```jsx
// Frontend/src/hooks/useClientes.js
import { useState, useEffect } from 'react';
import { clienteService } from '../services/clienteService';

export const useClientes = () => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const cargarClientes = async () => {
    try {
      setLoading(true);
      const data = await clienteService.obtenerTodos();
      setClientes(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const crearCliente = async (clienteData) => {
    try {
      const nuevoCliente = await clienteService.crear(clienteData);
      setClientes(prev => [nuevoCliente, ...prev]);
      return nuevoCliente;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const actualizarCliente = async (id, clienteData) => {
    try {
      const clienteActualizado = await clienteService.actualizar(id, clienteData);
      setClientes(prev => 
        prev.map(c => c.id === id ? clienteActualizado : c)
      );
      return clienteActualizado;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  const eliminarCliente = async (id) => {
    try {
      await clienteService.eliminar(id);
      setClientes(prev => prev.filter(c => c.id !== id));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  useEffect(() => {
    cargarClientes();
  }, []);

  return {
    clientes,
    loading,
    error,
    cargarClientes,
    crearCliente,
    actualizarCliente,
    eliminarCliente
  };
};
```

**Servicio de API:**
```jsx
// Frontend/src/services/clienteService.js
import api from './api';

export const clienteService = {
  async obtenerTodos() {
    const response = await api.get('/clientes/');
    return response.data;
  },

  async obtenerPorId(id) {
    const response = await api.get(`/clientes/${id}/`);
    return response.data;
  },

  async crear(clienteData) {
    const response = await api.post('/clientes/', clienteData);
    return response.data;
  },

  async actualizar(id, clienteData) {
    const response = await api.patch(`/clientes/${id}/`, clienteData);
    return response.data;
  },

  async eliminar(id) {
    await api.delete(`/clientes/${id}/`);
  },

  async buscar(termino) {
    const response = await api.get(`/clientes/?search=${termino}`);
    return response.data;
  }
};
```

**Configuración de API:**
```jsx
// Frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Estado Global con Context

```jsx
// Frontend/src/context/AppContext.jsx
import React, { createContext, useContext, useReducer } from 'react';

const AppContext = createContext();

const initialState = {
  user: null,
  pedidos: [],
  notificaciones: [],
  loading: false
};

const appReducer = (state, action) => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'ADD_NOTIFICACION':
      return { 
        ...state, 
        notificaciones: [...state.notificaciones, action.payload] 
      };
    default:
      return state;
  }
};

export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const setUser = (user) => {
    dispatch({ type: 'SET_USER', payload: user });
  };

  const setLoading = (loading) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const addNotificacion = (notificacion) => {
    dispatch({ type: 'ADD_NOTIFICACION', payload: notificacion });
  };

  return (
    <AppContext.Provider value={{
      ...state,
      setUser,
      setLoading,
      addNotificacion
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp debe usarse dentro de AppProvider');
  }
  return context;
};
```

---

## 🗄️ Base de Datos

### Modelo de Datos

**Diagrama ER Principal:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Cliente   │    │   Pedido    │    │    Menu     │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ id (PK)     │───▶│ id (PK)     │◄──┤ id (PK)     │
│ rut         │    │ cliente_id  │   │ nombre      │
│ nombre      │    │ fecha       │   │ precio      │
│ email       │    │ total       │   │ categoria   │
│ telefono    │    │ estado      │   │ disponible  │
└─────────────┘    └─────────────┘   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ PedidoItem  │
                   ├─────────────┤
                   │ id (PK)     │
                   │ pedido_id   │
                   │ menu_id     │
                   │ cantidad    │
                   │ precio_unit │
                   └─────────────┘
```

### Migraciones Importantes

**Migración inicial de Cliente:**
```python
# Backend/Infraestructura/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='ClienteModel',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'clientes',
            },
        ),
        migrations.AddIndex(
            model_name='clientemodel',
            index=models.Index(fields=['rut'], name='idx_cliente_rut'),
        ),
        migrations.AddIndex(
            model_name='clientemodel',
            index=models.Index(fields=['email'], name='idx_cliente_email'),
        ),
    ]
```

### Optimizaciones de BD

**Índices estratégicos:**
```sql
-- Índices para consultas frecuentes
CREATE INDEX idx_pedido_fecha_estado ON pedidos(fecha_creacion, estado);
CREATE INDEX idx_pedido_cliente_fecha ON pedidos(cliente_id, fecha_creacion DESC);
CREATE INDEX idx_menu_categoria_disponible ON menus(categoria, disponible);
CREATE INDEX idx_ingrediente_stock ON ingredientes(stock_actual, stock_minimo);

-- Índices compuestos para queries específicas
CREATE INDEX idx_pedido_delivery ON pedidos(tipo_entrega, estado) WHERE tipo_entrega = 'delivery';
```

**Consultas optimizadas:**
```python
# Ejemplo de consulta optimizada con select_related y prefetch_related
def obtener_pedidos_con_detalles():
    return Pedido.objects.select_related('cliente')\
                        .prefetch_related('items__menu__ingredientes')\
                        .filter(estado='pendiente')\
                        .order_by('-fecha_creacion')
```

---

## 🔌 APIs y Servicios

### Documentación OpenAPI

**Configuración Swagger:**
```python
# Backend/Config/Settings/base.py
INSTALLED_APPS += [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Restaurant Management API',
    'DESCRIPTION': 'API para el sistema de gestión de restaurante',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

**Decorador para documentar endpoints:**
```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    operation_id='cliente_create',
    description='Crear nuevo cliente',
    request=ClienteSerializer,
    responses={201: ClienteSerializer},
    examples=[
        {
            'rut': '12345678-9',
            'nombre': 'Juan Pérez',
            'email': 'juan@email.com',
            'telefono': '987654321'
        }
    ]
)
@api_view(['POST'])
def crear_cliente(request):
    # Implementación
    pass
```

### Versionado de API

```python
# Backend/Config/urls.py
urlpatterns = [
    path('api/v1/', include('Backend.Presentacion.Urls.v1')),
    path('api/v2/', include('Backend.Presentacion.Urls.v2')),
]

# Versionado por header
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

### Rate Limiting

```python
# Configuración de throttling
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'create_pedido': '20/hour'
    }
}

# Throttle personalizado
class CrearPedidoThrottle(UserRateThrottle):
    scope = 'create_pedido'
```

---

## 🧪 Testing

### Estructura de Tests

```
tests/
├── unit/                 # Tests unitarios
│   ├── test_models.py
│   ├── test_services.py
│   └── test_repositories.py
├── integration/          # Tests de integración
│   ├── test_api.py
│   └── test_database.py
├── e2e/                  # Tests end-to-end
│   └── test_workflows.py
├── performance/          # Tests de rendimiento
│   └── test_performance.py
└── fixtures/             # Datos de prueba
    └── sample_data.json
```

### Tests Unitarios

```python
# Backend/tests/unit/test_cliente_service.py
import pytest
from unittest.mock import Mock
from Backend.Aplicacion.Servicios.ClienteService import ClienteService
from Backend.Aplicacion.DTOs.ClienteDTO import CrearClienteDTO

class TestClienteService:
    def setup_method(self):
        self.mock_repository = Mock()
        self.service = ClienteService(self.mock_repository)
    
    def test_crear_cliente_exitoso(self):
        # Arrange
        dto = CrearClienteDTO(
            rut='12345678-9',
            nombre='Test Cliente',
            email='test@email.com',
            telefono='987654321'
        )
        self.mock_repository.existe_rut.return_value = False
        
        # Act
        resultado = self.service.crear_cliente(dto)
        
        # Assert
        assert resultado.nombre == 'Test Cliente'
        self.mock_repository.guardar.assert_called_once()
    
    def test_crear_cliente_rut_duplicado(self):
        # Arrange
        dto = CrearClienteDTO(rut='12345678-9', nombre='Test', email='test@email.com', telefono='123')
        self.mock_repository.existe_rut.return_value = True
        
        # Act & Assert
        with pytest.raises(ValueError, match="El RUT ya está registrado"):
            self.service.crear_cliente(dto)
```

### Tests de Integración

```python
# Backend/tests/integration/test_cliente_api.py
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class TestClienteAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_crear_cliente_valido(self):
        data = {
            'rut': '12345678-9',
            'nombre': 'Test Cliente',
            'email': 'test@email.com',
            'telefono': '987654321'
        }
        
        response = self.client.post('/api/clientes/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['nombre'] == 'Test Cliente'
    
    def test_listar_clientes(self):
        response = self.client.get('/api/clientes/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data or isinstance(response.data, list)
```

### Tests de Performance

```python
# Backend/tests/performance/test_cliente_performance.py
import pytest
import time
from django.test import TransactionTestCase
from Backend.Infraestructura.Modelos.ClienteModel import ClienteModel

class TestClientePerformance(TransactionTestCase):
    def test_consulta_masiva_clientes(self):
        # Crear 1000 clientes
        clientes = []
        for i in range(1000):
            clientes.append(ClienteModel(
                rut=f'1234567{i:02d}',
                nombre=f'Cliente {i}',
                email=f'cliente{i}@test.com',
                telefono=f'98765432{i:02d}'
            ))
        ClienteModel.objects.bulk_create(clientes)
        
        # Medir tiempo de consulta
        start_time = time.time()
        result = list(ClienteModel.objects.all())
        end_time = time.time()
        
        # Verificar que se ejecuta en menos de 1 segundo
        assert end_time - start_time < 1.0
        assert len(result) == 1000
```

### Frontend Testing

```jsx
// Frontend/src/__tests__/components/ClienteCard.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ClienteCard from '../components/Cliente/ClienteCard';

const mockCliente = {
  id: 1,
  rut: '12345678-9',
  nombre: 'Juan Pérez',
  email: 'juan@email.com',
  telefono: '987654321',
  activo: true,
  fecha_creacion: '2023-01-01T00:00:00Z'
};

describe('ClienteCard', () => {
  const mockOnEdit = jest.fn();
  const mockOnDelete = jest.fn();
  const mockOnViewHistory = jest.fn();

  test('renderiza información del cliente correctamente', () => {
    render(
      <ClienteCard 
        cliente={mockCliente}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onViewHistory={mockOnViewHistory}
      />
    );

    expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    expect(screen.getByText('RUT: 12.345.678-9')).toBeInTheDocument();
    expect(screen.getByText('juan@email.com')).toBeInTheDocument();
  });

  test('llama onEdit cuando se hace clic en editar', () => {
    render(
      <ClienteCard 
        cliente={mockCliente}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onViewHistory={mockOnViewHistory}
      />
    );

    fireEvent.click(screen.getByText('Editar'));
    expect(mockOnEdit).toHaveBeenCalledWith(mockCliente);
  });
});
```

---

## 🚀 Performance y Optimización

### Optimizaciones Backend

**Cache strategies:**
```python
# Backend/Infraestructura/Servicios/CacheService.py
from django.core.cache import cache
from django.conf import settings
import hashlib

class CacheService:
    @staticmethod
    def get_cache_key(prefix: str, *args) -> str:
        """Generar clave de cache única"""
        key_data = f"{prefix}:{''.join(str(arg) for arg in args)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    @staticmethod
    def cache_result(prefix: str, timeout: int = 300):
        """Decorador para cachear resultados"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                cache_key = CacheService.get_cache_key(prefix, *args, **kwargs)
                result = cache.get(cache_key)
                
                if result is None:
                    result = func(*args, **kwargs)
                    cache.set(cache_key, result, timeout)
                
                return result
            return wrapper
        return decorator

# Uso del decorador
@CacheService.cache_result('menu_disponibles', timeout=600)
def obtener_menus_disponibles():
    return Menu.objects.filter(disponible=True)
```

**Database optimization:**
```python
# Consultas optimizadas con select_related y prefetch_related
class PedidoService:
    def obtener_pedidos_dashboard(self):
        return Pedido.objects.select_related('cliente')\
                           .prefetch_related(
                               'items__menu',
                               'delivery'
                           )\
                           .filter(fecha_creacion__date=timezone.now().date())\
                           .order_by('-fecha_creacion')
    
    def obtener_estadisticas_ventas(self, fecha_inicio, fecha_fin):
        # Usar agregaciones a nivel de BD
        return Pedido.objects.filter(
            fecha_creacion__range=[fecha_inicio, fecha_fin],
            estado='completado'
        ).aggregate(
            total_ventas=Sum('total'),
            total_pedidos=Count('id'),
            ticket_promedio=Avg('total')
        )
```

### Optimizaciones Frontend

**Code splitting:**
```jsx
// Frontend/src/utils/lazyComponents.js
import { lazy } from 'react';

export const LazyClientes = lazy(() => import('../pages/Clientes'));
export const LazyPedidos = lazy(() => import('../pages/Pedidos'));
export const LazyInventario = lazy(() => import('../pages/Inventario'));
export const LazyAnalytics = lazy(() => import('../pages/Analytics'));

// App.jsx con Suspense
import { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { LazyClientes, LazyPedidos } from './utils/lazyComponents';
import LoadingSpinner from './components/common/LoadingSpinner';

function App() {
  return (
    <Routes>
      <Route path="/clientes" element={
        <Suspense fallback={<LoadingSpinner />}>
          <LazyClientes />
        </Suspense>
      } />
      <Route path="/pedidos" element={
        <Suspense fallback={<LoadingSpinner />}>
          <LazyPedidos />
        </Suspense>
      } />
    </Routes>
  );
}
```

**Optimización de renders:**
```jsx
// Uso de memo para evitar re-renders innecesarios
import React, { memo } from 'react';

const ClienteCard = memo(({ cliente, onEdit, onDelete }) => {
  return (
    <div className="cliente-card">
      {/* Contenido del componente */}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function
  return prevProps.cliente.id === nextProps.cliente.id &&
         prevProps.cliente.nombre === nextProps.cliente.nombre;
});

// Custom hook optimizado
import { useMemo, useCallback } from 'react';

export const useClientesOptimizado = () => {
  const [clientes, setClientes] = useState([]);
  
  const clientesActivos = useMemo(() => 
    clientes.filter(c => c.activo), 
    [clientes]
  );
  
  const buscarCliente = useCallback((termino) => {
    return clientes.filter(c => 
      c.nombre.toLowerCase().includes(termino.toLowerCase()) ||
      c.rut.includes(termino)
    );
  }, [clientes]);
  
  return { clientesActivos, buscarCliente };
};
```

---

## 🚀 Deployment

### Docker Configuration

**Dockerfile Backend:**
```dockerfile
# Backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Backend.Config.wsgi:application"]
```

**Dockerfile Frontend:**
```dockerfile
# Frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Build app
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy build files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: restaurant_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./Backend
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/restaurant_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"

  frontend:
    build: ./Frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### CI/CD Configuration

**GitHub Actions:**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r Backend/requirements.txt
    
    - name: Run tests
      run: |
        cd Backend
        python manage.py test
        pytest --cov=Backend --cov-report=xml
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install frontend dependencies
      run: |
        cd Frontend
        npm ci
    
    - name: Run frontend tests
      run: |
        cd Frontend
        npm run test:ci
    
    - name: Build frontend
      run: |
        cd Frontend
        npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add deployment scripts here
```

---

## 🤝 Contribución

### Estándares de Código

**Python (Backend):**
- Seguir PEP 8
- Usar type hints
- Documentar funciones con docstrings
- Máximo 88 caracteres por línea (Black)

**JavaScript/React (Frontend):**
- Seguir ESLint configuration
- Usar JSDoc para documentación
- Componentes funcionales con hooks
- PropTypes o TypeScript para tipado

### Git Workflow

**Branch Strategy:**
```
main
├── develop
│   ├── feature/nueva-funcionalidad
│   ├── bugfix/corregir-error
│   └── hotfix/parche-urgente
└── release/v1.0.0
```

**Commit Messages:**
```
type(scope): description

feat(cliente): agregar validación de RUT
fix(pedido): corregir cálculo de total
docs(api): actualizar documentación de endpoints
test(service): agregar tests unitarios para ClienteService
```

### Pull Request Template

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## Testing
- [ ] Tests unitarios agregados/actualizados
- [ ] Tests de integración verificados
- [ ] Tests manuales realizados

## Checklist
- [ ] El código sigue los estándares del proyecto
- [ ] Se realizó self-review del código
- [ ] Se agregaron comentarios en código complejo
- [ ] Se actualizó la documentación
- [ ] Los tests pasan exitosamente
```

---

**Documento mantenido por: Equipo de Desarrollo**
**Última actualización: [Fecha actual]**
**Versión: 1.0**
