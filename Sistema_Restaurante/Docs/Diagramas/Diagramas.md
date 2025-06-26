# Diagramas del Sistema de Gestión de Restaurante

Este documento presenta diversos diagramas que ilustran la arquitectura, diseño y componentes tanto del sistema actual como del sistema refactorizado, permitiendo una comparación visual de los cambios y mejoras implementadas.

## Glosario de Referencias

Para facilitar la referencia a diagramas específicos en la documentación y en futuras implementaciones, utilizamos el siguiente sistema de codificación:

| Código | Descripción |
|--------|-------------|
| **DAA** | Diagrama de Arquitectura Actual |
| **DAR** | Diagrama de Arquitectura Refactorizado |
| **DPA** | Diagrama de Patrones Actual |
| **DPR** | Diagrama de Patrones Refactorizado |
| **DCA** | Diagrama de Clases Actual |
| **DCR** | Diagrama de Clases Refactorizado |
| **MERA** | Modelo Entidad-Relación Actual |
| **MERR** | Modelo Entidad-Relación Refactorizado |
| **DOA** | Diagrama de Objetos Actual |
| **DOR** | Diagrama de Objetos Refactorizado |
| **DCOB** | Diagrama de Componentes Basicos |
| **DCOD** | Diagrama de Componentes Distribuidos |
| **DCU** | Diagrama de Caso de Uso |

## Índice
1. [Diagramas de Arquitectura](#diagramas-de-arquitectura)
2. [Diagramas de Patrones de Diseño](#diagramas-de-patrones-de-diseño)
3. [Diagramas de Clases](#diagramas-de-clases)
4. [Diagramas MER (Modelo Entidad-Relación)](#diagramas-mer)
5. [Diagramas de Objetos](#diagramas-de-objetos)
6. [Diagramas de Componentes](#diagramas-de-componentes)
7. [Diagramas de Caso de Uso](#diagramas-de-caso-de-uso)

## Diagramas de Arquitectura

### Sistema Actual: Arquitectura Monolítica de Escritorio (DAA)

![Diagrama arquitectura actual](arquitectura/arquitectura_actual.webp)

**Características principales:**
- Aplicación monolítica de escritorio desarrollada en Python con customtkinter
- Acceso limitado desde un único punto (computadora con la aplicación instalada)
- Toda la lógica y presentación centralizada en un único componente
- Base de datos local SQLite sin capacidad de acceso simultáneo
- Único actor con acceso al sistema (Jefe de Local)

### Sistema Refactorizado: Arquitectura de Aplicación Web Distribuida (DAR)

![Diagrama arquitectura refactorizado](arquitectura/arquitectura_refactorizada.webp)

**Características principales:**
- Arquitectura cliente-servidor con separación clara de responsabilidades
- Frontend en React con componentes reutilizables
- Backend en Django siguiendo principios de Clean Architecture
- API RESTful para la comunicación entre frontend y backend
- Acceso desde múltiples dispositivos y ubicaciones
- Base de datos centralizada con acceso concurrente
- Múltiples actores con diferentes niveles de acceso (Jefe de Local, Jefe de Turno, Mesero, Cocina)

## Diagramas de Patrones de Diseño

### Sistema Actual: Patrones Limitados (DPA)

![Diagrama patron de diseño actual](patrones/patrones_actual.webp)

### Sistema Refactorizado: Implementación de Múltiples Patrones (DPR)

![Diagrama patron de diseño refactorizado](patrones/patrones_refactorizado.webp)

**Patrones implementados en el sistema refactorizado:**
1. **Repository Pattern**: Abstracción del acceso a datos con interfaces genéricas
2. **Dependency Injection**: Inyección de repositorios en servicios
3. **Factory Method**: Creación de diferentes tipos de pedidos
4. **Observer**: Notificaciones de cambios de estado en pedidos
5. **State**: Manejo de diferentes estados de pedidos
6. **Facade**: Simplificación de subsistemas complejos para el dashboard
7. **Strategy**: Diferentes estrategias para cálculos de precios, impuestos, etc.
8. **Template Method**: Para procesos estándar con variaciones (como diferentes tipos de reportes)

## Diagramas de Clases

### Sistema Actual: Modelo Simplificado (DCA)

![Diagrama clases actual](clases/clases_actual.webp)

### Sistema Refactorizado: Modelo Expandido (DCR)

![Diagrama clases refactorizado](clases/clases_refactorizado.webp)

## Diagramas MER

### Sistema Actual: Modelo Entidad-Relación Básico (MERA)

![Diagrama MER actual](mer/mer_actual.webp)

### Sistema Refactorizado: Modelo Entidad-Relación Completo (MERR)

![Diagrama MER refactorizado](mer/mer_refactorizado.webp)

## Diagramas de Objetos

### Sistema Actual: Instancias Básicas (DOA)

![Diagrama objetos actual](objetos/objetos_actual.webp)

### Sistema Refactorizado: Instancias Avanzadas (DOR)

![Diagrama objetos refactorizado](objetos/objetos_refactorizado.webp)

## Diagramas de Componentes

### Sistema Actual: Componentes Básicos (DCOB)

![Diagrama componentes basicos](componentes/componentes_actual.webp)

### Sistema Refactorizado: Componentes Distribuidos (DCOD)

![Diagrama componentes distribuidos](componentes/componentes_actual.webp)

## Diagramas de Caso de Uso

![Diagrama Caso de Uso](casos_uso/Casos_de_uso.webp)

## Resumen de Mejoras

La refactorización del sistema incluye las siguientes mejoras significativas:

1. **Arquitectura (DAA → DAR)**: Migración de una aplicación monolítica de escritorio a una arquitectura web cliente-servidor con separación de responsabilidades.

2. **Patrones de Diseño (DPA → DPR)**: Implementación de múltiples patrones como Repository, Factory, Observer, State y Facade para mejorar la mantenibilidad y escalabilidad.

3. **Modelo de Datos (DCA → DCR, MERA → MERR)**: Expansión del modelo con nuevas entidades como Mesa, DeliveryPedido, Transaccion y Usuario, habilitando nuevas funcionalidades de negocio.

4. **Componentes (DCOA → DCOR)**: Distribución en componentes independientes y especializados que pueden evolucionar de manera separada.

5. **Acceso**: Transformación de un sistema de acceso único a uno multiusuario con diferentes roles y permisos.

6. **Tecnología**: Actualización tecnológica de Python con customtkinter a una stack moderna con React para frontend y Django para backend.

Estos cambios no solo modernizan la infraestructura tecnológica sino que transforman fundamentalmente la manera en que opera el restaurante, proporcionando nuevas capacidades y mejorando la experiencia de todos los involucrados.
