# Diagramas del Sistema de Gestión de Restaurante

Este documento presenta diversos diagramas que ilustran la arquitectura, diseño y componentes tanto del sistema actual como del sistema refactorizado, permitiendo una comparación visual de los cambios y mejoras implementadas.

## Índice
1. [Diagramas de Arquitectura](#diagramas-de-arquitectura)
2. [Diagramas de Patrones de Diseño](#diagramas-de-patrones-de-diseño)
3. [Diagramas de Clases](#diagramas-de-clases)
4. [Diagramas MER (Modelo Entidad-Relación)](#diagramas-mer)
5. [Diagramas de Objetos](#diagramas-de-objetos)
6. [Diagramas de Componentes](#diagramas-de-componentes)

## Diagramas de Arquitectura

### Sistema Actual: Arquitectura Monolítica de Escritorio

```mermaid
flowchart TD
    subgraph "Aplicación de Escritorio (Python + customtkinter)"
        UI[Interfaz de Usuario]
        LN[Lógica de Negocio]
        DA[Acceso a Datos]
    end
    
    UI <--> LN
    LN <--> DA
    DA <--> BD[(Base de Datos SQLite)]
    
    JL([Jefe Local]) --> UI
    
    classDef current fill:#f9f9f9,stroke:#999,stroke-width:1px
    class UI,LN,DA,BD current
```

**Características principales:**
- Aplicación monolítica de escritorio desarrollada en Python con customtkinter
- Acceso limitado desde un único punto (computadora con la aplicación instalada)
- Toda la lógica y presentación centralizada en un único componente
- Base de datos local SQLite sin capacidad de acceso simultáneo
- Único actor con acceso al sistema (Jefe de Local)

### Sistema Refactorizado: Arquitectura de Aplicación Web Distribuida

```mermaid
flowchart TD
    subgraph "Frontend (React)"
        UI[Componentes UI]
        GE[Gestión de Estado]
        SA[Servicios API]
    end
    
    subgraph "Backend (Django REST API)"
        subgraph "Capa de Presentación"
            AP[API Controllers/Views]
            SZ[Serializers]
        end
        
        subgraph "Capa de Aplicacion"
            SV[Services]
            CU[Casos de Uso]
            IR[Interfaces de Repositories]
        end
        
        subgraph "Capa de Dominio"
            ENT[Entidades]
            VO[Value Objects]
            RN[Reglas de Negocio]
        end
        
        subgraph "Capa de Infraestructura"
            RP[Repositories]
            ORM[ORM Django]
            SE[Servicios Externos]
        end
    end
    
    BD[(Base de Datos)]
    
    UI <--> GE
    GE <--> SA
    SA <---> AP
    AP <--> SZ
    SZ <--> SV
    SV <--> CU
    SV <--> IR
    CU <--> ENT
    IR <--> RP
    ENT <--> VO
    ENT <--> RN
    RP <--> ORM
    RP <--> SE
    ORM <--> BD
    
    JL([Jefe Local]) -.-> UI
    JT([Jefe Turno]) -.-> UI
    M([Mesero]) -.-> UI
    C([Cocina]) -.-> UI
    
    classDef frontend fill:#d0e0ff,stroke:#3c78d8,stroke-width:1px
    classDef presentation fill:#ffe6cc,stroke:#d79b00,stroke-width:1px
    classDef usecase fill:#d5e8d4,stroke:#82b366,stroke-width:1px
    classDef domain fill:#fff2cc,stroke:#d6b656,stroke-width:1px
    classDef infra fill:#f8cecc,stroke:#b85450,stroke-width:1px
    
    class UI,GE,SA frontend
    class AP,SZ presentation
    class SV,CU,IR usecase
    class ENT,VO,RN domain
    class RP,ORM,SE infra
```

**Características principales:**
- Arquitectura cliente-servidor con separación clara de responsabilidades
- Frontend en React con componentes reutilizables
- Backend en Django siguiendo principios de Clean Architecture
- API RESTful para la comunicación entre frontend y backend
- Acceso desde múltiples dispositivos y ubicaciones
- Base de datos centralizada con acceso concurrente
- Múltiples actores con diferentes niveles de acceso (Jefe de Local, Jefe de Turno, Mesero, Cocina)

## Diagramas de Patrones de Diseño

### Sistema Actual: Patrones Limitados

```mermaid
classDiagram
    class MainApplication {
        -initialize_ui()
        -connect_database()
        -show_main_menu()
    }
    
    class DBConnection {
        -connection: SQLite
        +execute_query()
        +fetch_data()
    }
    
    class ClientManager {
        +register_client()
        +edit_client()
        +delete_client()
        +search_client()
    }
    
    class MenuManager {
        +create_menu()
        +edit_menu()
        +delete_menu()
        +assign_ingredients()
    }
    
    class OrderManager {
        +create_order()
        +edit_order()
        +cancel_order()
        +generate_receipt()
    }
    
    class ReportGenerator {
        +generate_sales_report()
        +show_basic_stats()
        +show_ingredient_usage()
    }
    
    MainApplication --> DBConnection
    MainApplication --> ClientManager
    MainApplication --> MenuManager
    MainApplication --> OrderManager
    MainApplication --> ReportGenerator
    
    note for MainApplication "Singleton Pattern\nÚnica instancia de aplicación"
    note for DBConnection "Singleton Pattern\nÚnica conexión a BD"
```

### Sistema Refactorizado: Implementación de Múltiples Patrones

```mermaid
classDiagram
    class IRepository~T~ {
        <<interface>>
        +get(id) T
        +getAll() List~T~
        +add(entity) void
        +update(entity) void
        +delete(id) void
    }
    
    class ClientRepository {
        +get(id) Cliente
        +getAll() List~Cliente~
        +add(cliente) void
        +update(cliente) void
        +delete(id) void
        +findByName(name) List~Cliente~
        +findByRut(rut) Cliente
    }
    
    class MenuRepository {
        +get(id) Menu
        +getAll() List~Menu~
        +add(menu) void
        +update(menu) void
        +delete(id) void
        +findByCategory(category) List~Menu~
        +checkAvailability(id) boolean
    }
    
    class ClientService {
        -clientRepository: IRepository~Cliente~
        +registerClient(clientData)
        +updateClient(clientData)
        +deleteClient(id)
        +getClientHistory(id)
    }
    
    class MenuService {
        -menuRepository: IRepository~Menu~
        -ingredientRepository: IRepository~Ingrediente~
        +createMenu(menuData)
        +updateMenu(menuData)
        +deleteMenu(id)
        +checkIngredientAvailability()
    }
    
    class OrderFactory {
        +createLocalOrder() Order
        +createDeliveryOrder() DeliveryOrder
    }
    
    class NotificationObserver {
        +update(subject)
    }
    
    class Order {
        -state: OrderState
        +changeState(newState)
        +notifyObservers()
    }
    
    class OrderState {
        <<interface>>
        +nextState()
        +getStatusInfo()
    }
    
    class ReceivedState {
        +nextState()
        +getStatusInfo()
    }
    
    class PreparingState {
        +nextState()
        +getStatusInfo()
    }
    
    class ReadyState {
        +nextState()
        +getStatusInfo()
    }
    
    class DeliveredState {
        +nextState()
        +getStatusInfo()
    }
    
    class DashboardFacade {
        -salesAnalyzer
        -inventoryAnalyzer
        -customerAnalyzer
        +getSalesSummary()
        +getPopularMenus()
        +getInventoryStatus()
        +getCustomerStatistics()
    }
    
    IRepository <|-- ClientRepository
    IRepository <|-- MenuRepository
    ClientService o-- IRepository
    MenuService o-- IRepository
    OrderState <|-- ReceivedState
    OrderState <|-- PreparingState
    OrderState <|-- ReadyState
    OrderState <|-- DeliveredState
    Order o-- OrderState
    Order --> NotificationObserver
    
    note for IRepository "Repository Pattern\nAbstracción de acceso a datos"
    note for OrderFactory "Factory Pattern\nCreación de diferentes tipos de pedidos"
    note for Order "Observer Pattern\nNotificación de cambios de estado"
    note for OrderState "State Pattern\nDistintos comportamientos según estado"
    note for DashboardFacade "Facade Pattern\nInterface simplificada para análisis"
```

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

### Sistema Actual: Modelo Simplificado

```mermaid
classDiagram
    class Cliente {
        -rut: String
        -nombre: String
        -telefono: String
        -direccion: String
        -correo: String
    }
    
    class Ingrediente {
        -id: Integer
        -nombre: String
        -cantidad: Float
        -unidad: String
        -nivel_critico: Float
    }
    
    class Menu {
        -id: Integer
        -nombre: String
        -descripcion: String
        -precio: Float
    }
    
    class Pedido {
        -id: Integer
        -cliente_rut: String
        -fecha: Date
        -total: Float
        -estado: String
    }
    
    class ItemPedido {
        -id: Integer
        -pedido_id: Integer
        -menu_id: Integer
        -cantidad: Integer
        -subtotal: Float
    }
    
    class MenuIngrediente {
        -menu_id: Integer
        -ingrediente_id: Integer
        -cantidad: Float
    }
    
    Pedido "1" -- "*" ItemPedido
    ItemPedido "*" -- "1" Menu
    Menu "*" -- "*" Ingrediente
    MenuIngrediente -- Menu
    MenuIngrediente -- Ingrediente
    Pedido "*" -- "1" Cliente
```

### Sistema Refactorizado: Modelo Expandido

```mermaid
classDiagram
    class Cliente {
        -rut: String
        -nombre: String
        -telefono: String
        -direccion: String
        -correo: String
        -preferencias: JSON
        -fecha_registro: DateTime
        -ultima_visita: DateTime
        -estado: String
    }
    
    class Ingrediente {
        -id: Integer
        -nombre: String
        -categoria: String
        -cantidad: Float
        -unidad: String
        -nivel_critico: Float
        -codigo_barras: String
        -imagen: String
        -proveedor_id: Integer
        -estado: String
    }
    
    class Menu {
        -id: Integer
        -nombre: String
        -descripcion: String
        -precio: Float
        -costo: Float
        -tiempo_preparacion: Integer
        -categoria: String
        -imagen: String
        -disponible: Boolean
        -disponible_delivery: Boolean
    }
    
    class Pedido {
        -id: Integer
        -cliente_id: Integer
        -mesa_id: Integer
        -fecha: DateTime
        -total: Float
        -estado: String
        -notas: String
        -creado_por: Integer
        -tipo: String
    }
    
    class ItemPedido {
        -id: Integer
        -pedido_id: Integer
        -menu_id: Integer
        -cantidad: Integer
        -precio_unitario: Float
        -subtotal: Float
        -personalizaciones: JSON
        -estado: String
    }
    
    class MenuIngrediente {
        -menu_id: Integer
        -ingrediente_id: Integer
        -cantidad: Float
    }
    
    class Mesa {
        -id: Integer
        -numero: Integer
        -capacidad: Integer
        -estado: String
        -ubicacion: String
        -caracteristicas: String
        -hora_inicio: DateTime
    }
    
    class DeliveryPedido {
        -pedido_id: Integer
        -direccion_entrega: String
        -tiempo_estimado: Integer
        -repartidor_id: Integer
        -estado_delivery: String
        -app_id: Integer
        -codigo_externo: String
        -costo_envio: Float
    }
    
    class DeliveryRepartidor {
        -id: Integer
        -nombre: String
        -telefono: String
        -estado: String
        -ubicacion_actual: String
    }
    
    class DeliveryApp {
        -id: Integer
        -nombre: String
        -comision: Float
        -activa: Boolean
        -configuracion: JSON
    }
    
    class MedioPago {
        -id: Integer
        -nombre: String
        -tipo: String
        -comision: Float
        -activo: Boolean
        -configuracion: JSON
    }
    
    class Transaccion {
        -id: Integer
        -pedido_id: Integer
        -medio_pago_id: Integer
        -monto: Float
        -fecha: DateTime
        -estado: String
        -referencia_externa: String
    }
    
    class Comprobante {
        -id: Integer
        -transaccion_id: Integer
        -tipo: String
        -numero: String
        -fecha: DateTime
        -total: Float
        -impuestos: Float
        -datos_fiscales: JSON
    }
    
    class Usuario {
        -id: Integer
        -username: String
        -password: String
        -nombre: String
        -rol: String
        -activo: Boolean
        -ultimo_acceso: DateTime
    }
    
    Pedido "1" -- "*" ItemPedido
    ItemPedido "*" -- "1" Menu
    Menu "*" -- "*" Ingrediente
    MenuIngrediente -- Menu
    MenuIngrediente -- Ingrediente
    Pedido "*" -- "1" Cliente
    Pedido "0..1" -- "0..1" Mesa
    DeliveryPedido --|> Pedido
    DeliveryPedido -- DeliveryRepartidor
    DeliveryPedido -- DeliveryApp
    Pedido "1" -- "*" Transaccion
    Transaccion "1" -- "0..1" Comprobante
    Transaccion "*" -- "1" MedioPago
    Pedido "*" -- "1" Usuario
```

## Diagramas MER

### Sistema Actual: Modelo Entidad-Relación Básico

```mermaid
erDiagram
    CLIENTE {
        string rut PK
        string nombre
        string telefono
        string direccion
        string correo
    }
    
    PEDIDO {
        int id PK
        string cliente_rut FK
        date fecha
        float total
        string estado
    }
    
    MENU {
        int id PK
        string nombre
        string descripcion
        float precio
    }
    
    ITEM_PEDIDO {
        int id PK
        int pedido_id FK
        int menu_id FK
        int cantidad
        float subtotal
    }
    
    INGREDIENTE {
        int id PK
        string nombre
        float cantidad
        string unidad
        float nivel_critico
    }
    
    MENU_INGREDIENTE {
        int menu_id FK
        int ingrediente_id FK
        float cantidad
    }
    
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--o{ ITEM_PEDIDO : contiene
    ITEM_PEDIDO }o--|| MENU : referencia
    MENU }o--o{ INGREDIENTE : requiere
    MENU_INGREDIENTE }|--|| MENU : pertenece
    MENU_INGREDIENTE }|--|| INGREDIENTE : usa
```

### Sistema Refactorizado: Modelo Entidad-Relación Completo

```mermaid
erDiagram
    CLIENTE {
        string rut PK
        string nombre
        string telefono
        string direccion
        string correo
        json preferencias
        datetime fecha_registro
        datetime ultima_visita
        string estado
    }
    
    PEDIDO {
        int id PK
        string cliente_id FK
        int mesa_id FK
        datetime fecha
        float total
        string estado
        string notas
        int creado_por FK
        string tipo
    }
    
    MESA {
        int id PK
        int numero
        int capacidad
        string estado
        string ubicacion
        string caracteristicas
        datetime hora_inicio
    }
    
    MENU {
        int id PK
        string nombre
        string descripcion
        float precio
        float costo
        int tiempo_preparacion
        string categoria
        string imagen
        boolean disponible
        boolean disponible_delivery
    }
    
    ITEM_PEDIDO {
        int id PK
        int pedido_id FK
        int menu_id FK
        int cantidad
        float precio_unitario
        float subtotal
        json personalizaciones
        string estado
    }
    
    INGREDIENTE {
        int id PK
        string nombre
        string categoria
        float cantidad
        string unidad
        float nivel_critico
        string codigo_barras
        string imagen
        int proveedor_id FK
        string estado
    }
    
    MENU_INGREDIENTE {
        int menu_id FK
        int ingrediente_id FK
        float cantidad
    }
    
    DELIVERY_PEDIDO {
        int pedido_id PK,FK
        string direccion_entrega
        int tiempo_estimado
        int repartidor_id FK
        string estado_delivery
        int app_id FK
        string codigo_externo
        float costo_envio
    }
    
    DELIVERY_REPARTIDOR {
        int id PK
        string nombre
        string telefono
        string estado
        string ubicacion_actual
    }
    
    DELIVERY_APP {
        int id PK
        string nombre
        float comision
        boolean activa
        json configuracion
    }
    
    MEDIO_PAGO {
        int id PK
        string nombre
        string tipo
        float comision
        boolean activo
        json configuracion
    }
    
    TRANSACCION {
        int id PK
        int pedido_id FK
        int medio_pago_id FK
        float monto
        datetime fecha
        string estado
        string referencia_externa
    }
    
    COMPROBANTE {
        int id PK
        int transaccion_id FK
        string tipo
        string numero
        datetime fecha
        float total
        float impuestos
        json datos_fiscales
    }
    
    USUARIO {
        int id PK
        string username
        string password
        string nombre
        string rol
        boolean activo
        datetime ultimo_acceso
    }
    
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO |o--o| MESA : asignado_a
    PEDIDO ||--o{ ITEM_PEDIDO : contiene
    ITEM_PEDIDO }o--|| MENU : referencia
    MENU }o--o{ INGREDIENTE : requiere
    MENU_INGREDIENTE }|--|| MENU : pertenece
    MENU_INGREDIENTE }|--|| INGREDIENTE : usa
    PEDIDO |o--o| DELIVERY_PEDIDO : extiende
    DELIVERY_PEDIDO }o--|| DELIVERY_REPARTIDOR : asignado_a
    DELIVERY_PEDIDO }o--|| DELIVERY_APP : gestionado_por
    PEDIDO ||--o{ TRANSACCION : genera
    TRANSACCION }o--|| MEDIO_PAGO : utiliza
    TRANSACCION ||--o| COMPROBANTE : emite
    PEDIDO }o--|| USUARIO : creado_por
```

## Diagramas de Objetos

### Sistema Actual: Instancias Básicas

```mermaid
classDiagram
    class Cliente_Maria {
        rut: "12345678-9"
        nombre: "María Pérez"
        telefono: "912345678"
        direccion: "Av. Principal 123"
        correo: "maria@gmail.com"
    }
    
    class Ingrediente_Tomate {
        id: 1
        nombre: "Tomate"
        cantidad: 5.0
        unidad: "kg"
        nivel_critico: 1.0
    }
    
    class Ingrediente_Queso {
        id: 2
        nombre: "Queso"
        cantidad: 2.0
        unidad: "kg"
        nivel_critico: 0.5
    }
    
    class Menu_PizzaMargarita {
        id: 1
        nombre: "Pizza Margarita"
        descripcion: "Pizza con salsa de tomate y queso"
        precio: 8900
    }
    
    class MenuIngrediente_PizzaTomate {
        menu_id: 1
        ingrediente_id: 1
        cantidad: 0.2
    }
    
    class MenuIngrediente_PizzaQueso {
        menu_id: 1
        ingrediente_id: 2
        cantidad: 0.15
    }
    
    class Pedido_1234 {
        id: 1234
        cliente_rut: "12345678-9"
        fecha: "2023-10-20"
        total: 8900
        estado: "completado"
    }
    
    class ItemPedido_Pizza {
        id: 1
        pedido_id: 1234
        menu_id: 1
        cantidad: 1
        subtotal: 8900
    }
    
    Pedido_1234 --> Cliente_Maria
    Pedido_1234 --> ItemPedido_Pizza
    ItemPedido_Pizza --> Menu_PizzaMargarita
    Menu_PizzaMargarita --> MenuIngrediente_PizzaTomate
    Menu_PizzaMargarita --> MenuIngrediente_PizzaQueso
    MenuIngrediente_PizzaTomate --> Ingrediente_Tomate
    MenuIngrediente_PizzaQueso --> Ingrediente_Queso
```

### Sistema Refactorizado: Instancias Avanzadas

```mermaid
classDiagram
    class Cliente_Maria {
        rut: "12345678-9"
        nombre: "María Pérez"
        telefono: "912345678"
        direccion: "Av. Principal 123"
        correo: "maria@email .com"
        preferencias: "JSON-bebida preferida Limonada"
        fecha_registro: "2023-01-15T10:30:00"
        ultima_visita: "2023-10-20T19:45:00"
        estado: "activo"
    }
    
    class Ingrediente_Tomate {
        id: 1
        nombre: "Tomate"
        categoria: "Verduras"
        cantidad: 5.0
        unidad: "kg"
        nivel_critico: 1.0
        codigo_barras: "7891234567890"
        imagen: "tomate.jpg"
        proveedor_id: 12
        estado: "disponible"
    }
    
    class Ingrediente_Queso {
        id: 2
        nombre: "Queso Mozzarella"
        categoria: "Lácteos"
        cantidad: 2.0
        unidad: "kg"
        nivel_critico: 0.5
        codigo_barras: "7892345678901"
        imagen: "queso.jpg"
        proveedor_id: 8
        estado: "disponible"
    }
    
    class Menu_PizzaMargarita {
        id: 1
        nombre: "Pizza Margarita"
        descripcion: "Pizza con salsa de tomate y queso"
        precio: 8900
        costo: 3200
        tiempo_preparacion: 15
        categoria: "Pizzas"
        imagen: "pizza_margarita.jpg"
        disponible: true
        disponible_delivery: true
    }
    
    class Mesa_5 {
        id: 5
        numero: 5
        capacidad: 4
        estado: "ocupada"
        ubicacion: "terraza"
        caracteristicas: "vista jardín"
        hora_inicio: "2023-10-20T19:30:00"
    }
    
    class Pedido_1234 {
        id: 1234
        cliente_id: "12345678-9"
        mesa_id: 5
        fecha: "2023-10-20T19:45:00"
        total: 8900
        estado: "entregado"
        notas: "sin aceitunas"
        creado_por: 3
        tipo: "local"
    }
    
    class ItemPedido_Pizza {
        id: 1
        pedido_id: 1234
        menu_id: 1
        cantidad: 1
        precio_unitario: 8900
        subtotal: 8900
        personalizaciones: "JSON-sin aceitunas"
        estado: "entregado"
    }
    
    class Transaccion_T567 {
        id: 567
        pedido_id: 1234
        medio_pago_id: 2
        monto: 8900
        fecha: "2023-10-20T20:30:00"
        estado: "completada"
        referencia_externa: "REF89012"
    }
    
    class MedioPago_Tarjeta {
        id: 2
        nombre: "Tarjeta de Crédito"
        tipo: "tarjeta"
        comision: 0.03
        activo: true
        configuracion: "JSON-procesador PaymentProcessor"
    }
    
    class Comprobante_B2345 {
        id: 2345
        transaccion_id: 567
        tipo: "boleta"
        numero: "B-2345"
        fecha: "2023-10-20T20:35:00"
        total: 8900
        impuestos: 1691
        datos_fiscales: "JSON-vacío"
    }
    
    class Usuario_Carlos {
        id: 3
        username: "carlos"
        password: "[encrypted]"
        nombre: "Carlos Rodríguez"
        rol: "mesero"
        activo: true
        ultimo_acceso: "2023-10-20T19:00:00"
    }
    
    Pedido_1234 --> Cliente_Maria
    Pedido_1234 --> Mesa_5
    Pedido_1234 --> ItemPedido_Pizza
    ItemPedido_Pizza --> Menu_PizzaMargarita
    Menu_PizzaMargarita --> Ingrediente_Tomate
    Menu_PizzaMargarita --> Ingrediente_Queso
    Pedido_1234 --> Transaccion_T567
    Transaccion_T567 --> MedioPago_Tarjeta
    Transaccion_T567 --> Comprobante_B2345
    Pedido_1234 --> Usuario_Carlos
```

## Diagramas de Componentes

### Sistema Actual: Componentes Básicos

```mermaid
flowchart TD
    App["Aplicación de Escritorio"]
    Clientes["Módulo de Clientes"]
    Ingredientes["Módulo de Ingredientes"]
    Menus["Módulo de Menús"]
    Pedidos["Módulo de Pedidos"]
    Reportes["Módulo de Reportes"]
    DB[(Base de Datos SQLite)]
    
    App --- Clientes
    App --- Ingredientes
    App --- Menus
    App --- Pedidos
    App --- Reportes
    
    Clientes --- DB
    Ingredientes --- DB
    Menus --- DB
    Pedidos --- DB
    Reportes --- DB
```

### Sistema Refactorizado: Componentes Distribuidos

```mermaid
flowchart TD
    subgraph "Frontend (Cliente)"
        ReactApp["React App"]
        UI["Componentes UI"]
        Estado["Gestión de Estado"]
        ApiClient["Servicios API"]
        Router["Router"]
    end
    
    subgraph "Backend (Servidor)"
        DjangoAPI["Django API"]
        Auth["Autenticación JWT"]
        ApiControllers["Controladores API"]
        Services["Servicios"]
        Repos["Repositories"]
    end
    
    subgraph "Capa de Base de Datos"
        ORM["ORM Django"]
        DB[(Base de Datos PostgreSQL)]
    end
    
    subgraph "Servicios Externos"
        DeliveryAPI["APIs de Delivery"]
        PaymentProcessors["Procesadores de Pago"]
    end
    
    ReactApp --- UI
    ReactApp --- Estado
    ReactApp --- Router
    Estado --- ApiClient
    
    ApiClient ---|"HTTP/JSON"| DjangoAPI
    
    DjangoAPI --- Auth
    DjangoAPI --- ApiControllers
    ApiControllers --- Services
    Services --- Repos
    
    Repos --- ORM
    ORM --- DB
    
    Services ---|"HTTP/JSON"| DeliveryAPI
    Services ---|"HTTP/JSON"| PaymentProcessors
    
    ReactApp -.- ReactNote[("SPA accesible desde<br>múltiples dispositivos")]
    Auth -.- AuthNote[("Autenticación basada<br>en tokens JWT con<br>diferentes roles")]
    DeliveryAPI -.- DeliveryNote[("Integración con<br>plataformas externas<br>como Rappi, Uber Eats")]
    
    classDef note fill:#f9f9f9,stroke:#ccc,stroke-width:1px,color:#666
    class ReactNote,AuthNote,DeliveryNote note
```

## Resumen de Mejoras

La refactorización del sistema incluye las siguientes mejoras significativas:

1. **Arquitectura**: Migración de una aplicación monolítica de escritorio a una arquitectura web cliente-servidor con separación de responsabilidades.

2. **Patrones de Diseño**: Implementación de múltiples patrones como Repository, Factory, Observer, State y Facade para mejorar la mantenibilidad y escalabilidad.

3. **Modelo de Datos**: Expansión del modelo con nuevas entidades como Mesa, DeliveryPedido, Transaccion y Usuario, habilitando nuevas funcionalidades de negocio.

4. **Componentes**: Distribución en componentes independientes y especializados que pueden evolucionar de manera separada.

5. **Acceso**: Transformación de un sistema de acceso único a uno multiusuario con diferentes roles y permisos.

6. **Tecnología**: Actualización tecnológica de Python con customtkinter a una stack moderna con React para frontend y Django para backend.

Estos cambios no solo modernizan la infraestructura tecnológica sino que transforman fundamentalmente la manera en que opera el restaurante, proporcionando nuevas capacidades y mejorando la experiencia de todos los involucrados.
