# Convenciones de Código y Estructura del Proyecto

Este documento define las convenciones a seguir en el desarrollo del proyecto Sistema de Gestión de Restaurante.

## Estructura de Directorios

### Convención de Nombres de Carpetas y Archivos

**REGLA PRINCIPAL:** Los inicios de todas las rutas (carpetas y nombres de archivos) comienzan con mayúscula.

Por ejemplo:
- `Sistema_Restaurante/Backend/Dominio/Entidades/Cliente_Entidad.py`
- `Sistema_Restaurante/Backend/Infraestructura/Repositorios/Repositorio_Cliente.py`

### Estructura de Carpetas del Backend

El backend sigue la arquitectura Clean Architecture con las siguientes capas:

1. **Dominio/**
   - `Entidades/`: Contiene las clases de entidades del dominio con reglas de negocio
   - `Objetos_Valor/`: Contiene objetos inmutables que representan conceptos del dominio
   - `Excepciones/`: Excepciones específicas del dominio

2. **Aplicacion/**
   - `Interfaces/`: Define interfaces que establecen contratos para repositorios y servicios
   - `Servicios/`: Implementa los casos de uso de la aplicación
   - `DTOs/`: Objetos para transferir datos entre capas
   - `Excepciones/`: Excepciones específicas de la capa de aplicación

3. **Infraestructura/**
   - `Modelos/`: Modelos ORM de Django
   - `Repositorios/`: Implementaciones concretas de los repositorios
   - `servicios_externos/`: Integraciones con servicios externos

4. **Presentacion/**
   - `controladores/`: Vistas de API que reciben las peticiones HTTP
   - `serializadores/`: Convertidores entre JSON y objetos del dominio
   - `urls/`: Definición de rutas de la API

## Convenciones de Nomenclatura

### Archivos

- Los nombres de archivo siguen el patrón `Nombre_Tipo.py`
  - Ejemplos: `Cliente_Entidad.py`, `correo_VO.py`, `Repositorio_Cliente.py`

### Clases

- Las clases del dominio tienen nombres en singular que reflejan conceptos del negocio
  - Ejemplos: `ClienteEntidad`, `CorreoVO`
- Las interfaces comienzan con "I"
  - Ejemplo: `IClienteRepositorio`

### Métodos y Variables

- Los nombres de métodos y variables siguen la convención snake_case
  - Ejemplos: `registrar_cliente()`, `buscar_por_rut()`
- Los métodos privados comienzan con guion bajo
  - Ejemplo: `_convertir_a_entidad()`

## Patrones de Diseño

El sistema implementa los siguientes patrones:

1. **Repository Pattern**: Para abstraer el acceso a datos
2. **Dependency Injection**: Para inyectar dependencias y facilitar pruebas
3. **Value Object**: Para encapsular conceptos inmutables del dominio
4. **Factory Method**: Para crear instancias complejas
5. **Service Layer**: Para implementar casos de uso de la aplicación

---

*Este documento debe actualizarse conforme evoluciona el proyecto y se establecen nuevas convenciones.*