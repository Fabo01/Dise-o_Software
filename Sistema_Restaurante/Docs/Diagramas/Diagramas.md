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
| **DCOA** | Diagrama de Componentes Actual |
| **DCOR** | Diagrama de Componentes Refactorizado |

## Índice
1. [Diagramas de Arquitectura](#diagramas-de-arquitectura)
2. [Diagramas de Patrones de Diseño](#diagramas-de-patrones-de-diseño)
3. [Diagramas de Clases](#diagramas-de-clases)
4. [Diagramas MER (Modelo Entidad-Relación)](#diagramas-mer)
5. [Diagramas de Objetos](#diagramas-de-objetos)
6. [Diagramas de Componentes](#diagramas-de-componentes)

## Diagramas de Arquitectura

### Sistema Actual: Arquitectura Monolítica de Escritorio (DAA)

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

### Sistema Refactorizado: Arquitectura de Aplicación Web Distribuida (DAR)

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

### Sistema Actual: Patrones Limitados (DPA)

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

### Sistema Refactorizado: Implementación de Múltiples Patrones (DPR)

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

### Sistema Actual: Modelo Simplificado (DCA)

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

### Sistema Refactorizado: Modelo Expandido (DCR)

```mermaid
classDiagram
    %% Aplicación de principio de inversión de dependencia (D)
    %% Interfaces base para repositorios
    class IRepository~T~ {
        <<interface>>
        +findById(id: string): T
        +findAll(): List~T~
        +save(entity: T): T
        +update(entity: T): T
        +delete(id: string): void
    }

    %% Interfaces específicas para cada dominio (Principio I - Segregación de interfaces)
    class IClienteRepository {
        <<interface>>
        +findByRut(rut: string): Cliente
        +findByNombre(nombre: string): List~Cliente~
        +obtenerHistorialPedidos(clienteId: string): List~Pedido~
    }

    class IIngredienteRepository {
        <<interface>>
        +findByCategoria(categoria: string): List~Ingrediente~
        +actualizarStock(id: string, cantidad: number): void
        +obtenerIngredientesBajoCritico(): List~Ingrediente~
    }

    class IMenuRepository {
        <<interface>>
        +findByCategoria(categoria: string): List~Menu~
        +verificarDisponibilidad(id: string): boolean
        +obtenerConIngredientes(id: string): Menu
        +buscarPorIngrediente(ingredienteId: string): List~Menu~
    }

    class IPedidoRepository {
        <<interface>>
        +findByCliente(clienteId: string): List~Pedido~
        +findByEstado(estado: string): List~Pedido~
        +findByFecha(inicio: Date, fin: Date): List~Pedido~
        +actualizarEstado(id: string, estado: string): void
    }

    class IMesaRepository {
        <<interface>>
        +findByEstado(estado: string): List~Mesa~
        +asignarCliente(mesaId: string, clienteId: string): void
        +actualizarEstado(id: string, estado: string): void
    }

    %% Implementaciones concretas
    class ClienteRepositoryImpl {
        -clienteDAO: ClienteDAO
        +findById(id: string): Cliente
        +findAll(): List~Cliente~
        +save(cliente: Cliente): Cliente
        +update(cliente: Cliente): Cliente
        +delete(id: string): void
        +findByRut(rut: string): Cliente
        +findByNombre(nombre: string): List~Cliente~
        +obtenerHistorialPedidos(clienteId: string): List~Pedido~
    }

    class IngredienteRepositoryImpl {
        -ingredienteDAO: IngredienteDAO
        +findById(id: string): Ingrediente
        +findAll(): List~Ingrediente~
        +save(ingrediente: Ingrediente): Ingrediente
        +update(ingrediente: Ingrediente): Ingrediente
        +delete(id: string): void
        +findByCategoria(categoria: string): List~Ingrediente~
        +actualizarStock(id: string, cantidad: number): void
        +obtenerIngredientesBajoCritico(): List~Ingrediente~
    }

    %% Clases de servicio (Principio S - Responsabilidad única)
    class ClienteService {
        -clienteRepository: IClienteRepository
        -pedidoRepository: IPedidoRepository
        -notificationService: INotificationService
        +registrarCliente(cliente: ClienteDTO): Cliente
        +actualizarCliente(cliente: ClienteDTO): Cliente
        +eliminarCliente(id: string): void
        +buscarCliente(criterio: string): List~Cliente~
        +obtenerHistorialCliente(id: string): HistorialClienteDTO
    }

    class InventarioService {
        -ingredienteRepository: IIngredienteRepository
        -menuRepository: IMenuRepository
        -notificationService: INotificationService
        +registrarIngrediente(ingrediente: IngredienteDTO): Ingrediente
        +actualizarStock(id: string, cantidad: number, motivo: string): void
        +verificarDisponibilidadIngredientes(): List~EstadoIngredienteDTO~
        +obtenerIngredientesBajoCritico(): List~Ingrediente~
    }

    class MenuService {
        -menuRepository: IMenuRepository
        -ingredienteRepository: IIngredienteRepository
        +crearMenu(menu: MenuDTO): Menu
        +actualizarMenu(id: string, menu: MenuDTO): Menu
        +eliminarMenu(id: string): void
        +verificarDisponibilidadMenu(id: string): DisponibilidadMenuDTO
        +asignarIngredientesAMenu(menuId: string, ingredientes: List~MenuIngredienteDTO~): void
    }

    %% Patrón State para estados de pedido
    class PedidoState {
        <<interface>>
        +procesarSiguienteEstado(pedido: Pedido): void
        +getNombre(): string
        +puedeTransicionarA(estadoObjetivo: string): boolean
    }

    class RecibidoState {
        +procesarSiguienteEstado(pedido: Pedido): void
        +getNombre(): string
        +puedeTransicionarA(estadoObjetivo: string): boolean
    }

    class PreparacionState {
        +procesarSiguienteEstado(pedido: Pedido): void
        +getNombre(): string
        +puedeTransicionarA(estadoObjetivo: string): boolean
    }

    class ListoState {
        +procesarSiguienteEstado(pedido: Pedido): void
        +getNombre(): string
        +puedeTransicionarA(estadoObjetivo: string): boolean
    }

    class EntregadoState {
        +procesarSiguienteEstado(pedido: Pedido): void
        +getNombre(): string
        +puedeTransicionarA(estadoObjetivo: string): boolean
    }

    class CanceladoState {
        +procesarSiguienteEstado(pedido: Pedido): void
        +getNombre(): string
        +puedeTransicionarA(estadoObjetivo: string): boolean
    }

    %% Patrón Factory para creación de pedidos
    class PedidoFactory {
        +crearPedidoLocal(datos: PedidoDTO): Pedido
        +crearPedidoDelivery(datos: DeliveryPedidoDTO): DeliveryPedido
    }
    
    %% Patrón Observer para notificaciones
    class INotificationObserver {
        <<interface>>
        +update(subject: any, data: any): void
    }
    
    class CocinaNotificationObserver {
        +update(subject: any, data: any): void
    }
    
    class MeseroNotificationObserver {
        +update(subject: any, data: any): void
    }
    
    class ClienteNotificationObserver {
        +update(subject: any, data: any): void
    }

    %% Patrón Strategy para diferentes lógicas de procesamiento
    class IPagoProcesador {
        <<interface>>
        +procesarPago(transaccion: TransaccionDTO): ResultadoPagoDTO
    }
    
    class EfectivoProcesador {
        +procesarPago(transaccion: TransaccionDTO): ResultadoPagoDTO
    }
    
    class TarjetaProcesador {
        +procesarPago(transaccion: TransaccionDTO): ResultadoPagoDTO
    }
    
    class TransferenciaProcesador {
        +procesarPago(transaccion: TransaccionDTO): ResultadoPagoDTO
    }

    %% Patrón Facade para simplificar subsistemas complejos
    class DashboardFacade {
        -ventasAnalyzer: VentasAnalyzer
        -inventarioAnalyzer: InventarioAnalyzer
        -clienteAnalyzer: ClienteAnalyzer
        +obtenerResumenVentas(periodo: string): ResumenVentasDTO
        +obtenerMenusPopulares(): List~MenuPopularDTO~
        +obtenerEstadoInventario(): EstadoInventarioDTO
        +obtenerEstadisticasClientes(): EstadisticasClientesDTO
    }

    %% Entidad base aplicando herencia (Principio L - Sustitución de Liskov)
    class EntidadBase {
        #id: string
        #fechaCreacion: Date
        #fechaActualizacion: Date
        #estado: string
    }

    %% Entidades del dominio
    class Cliente {
        -rut: string
        -nombre: string
        -telefono: string
        -direccion: string
        -correo: string
        -preferencias: Map
        -fechaRegistro: Date
        -ultimaVisita: Date
    }

    class Ingrediente {
        -nombre: string
        -categoria: string
        -cantidad: number
        -unidad: string
        -nivelCritico: number
        -codigoBarras: string
        -imagen: string
        -proveedorId: string
    }

    class Menu {
        -nombre: string
        -descripcion: string
        -precio: number
        -costo: number
        -tiempoPreparacion: number
        -categoria: string
        -imagen: string
        -disponible: boolean
        -disponibleDelivery: boolean
        -ingredientes: List~MenuIngrediente~
    }

    class MenuIngrediente {
        -menuId: string
        -ingredienteId: string
        -cantidad: number
    }

    class Pedido {
        -clienteId: string
        -mesaId: string
        -fecha: Date
        -total: number
        -estado: PedidoState
        -notas: string
        -creadoPor: string
        -tipo: string
        -items: List~ItemPedido~
        +cambiarEstado(nuevoEstado: PedidoState): void
        +calcularTotal(): number
        +agregarItem(item: ItemPedido): void
        +eliminarItem(itemId: string): void
        +notificarObservadores(): void
    }
    
    class DeliveryPedido {
        -pedidoId: string
        -direccionEntrega: string
        -tiempoEstimado: number
        -repartidorId: string
        -estadoDelivery: string
        -appId: string
        -codigoExterno: string
        -costoEnvio: number
    }

    class ItemPedido {
        -pedidoId: string
        -menuId: string
        -cantidad: number
        -precioUnitario: number
        -subtotal: number
        -personalizaciones: Map
        -estado: string
    }

    class Mesa {
        -numero: number
        -capacidad: number
        -estado: string
        -ubicacion: string
        -caracteristicas: string
        -horaInicio: Date
    }

    %% Relaciones de herencia
    EntidadBase <|-- Cliente
    EntidadBase <|-- Ingrediente
    EntidadBase <|-- Menu
    EntidadBase <|-- Pedido
    EntidadBase <|-- Mesa

    %% Implementación de interfaces
    IClienteRepository <|.. ClienteRepositoryImpl
    IIngredienteRepository <|.. IngredienteRepositoryImpl
    IRepository <|-- IClienteRepository
    IRepository <|-- IIngredienteRepository
    IRepository <|-- IMenuRepository
    IRepository <|-- IPedidoRepository
    IRepository <|-- IMesaRepository
    PedidoState <|.. RecibidoState
    PedidoState <|.. PreparacionState
    PedidoState <|.. ListoState
    PedidoState <|.. EntregadoState
    PedidoState <|.. CanceladoState
    INotificationObserver <|.. CocinaNotificationObserver
    INotificationObserver <|.. MeseroNotificationObserver
    INotificationObserver <|.. ClienteNotificationObserver
    IPagoProcesador <|.. EfectivoProcesador
    IPagoProcesador <|.. TarjetaProcesador
    IPagoProcesador <|.. TransferenciaProcesador

    %% Composición y asociaciones
    ClienteService o-- IClienteRepository : usa
    ClienteService o-- IPedidoRepository : usa
    InventarioService o-- IIngredienteRepository : usa
    InventarioService o-- IMenuRepository : usa
    MenuService o-- IMenuRepository : usa
    MenuService o-- IIngredienteRepository : usa
    Pedido o-- PedidoState : tiene
    Pedido *-- ItemPedido : contiene
    Menu *-- MenuIngrediente : contiene
    DeliveryPedido -- Pedido : extiende

    %% Notas para patrones de diseño
    class IRepository~T~ {
        <<Interface>>
        Repository Pattern - Abstracción para acceso a datos
    }

    class PedidoFactory {
        <<Factory Method Pattern>>
        Crea diferentes tipos de pedidos
    }

    class DashboardFacade {
        <<Facade Pattern>>
        Simplifica interacción con subsistemas analíticos
    }

    class PedidoState {
        <<State Pattern>>
        Cambia comportamiento según estado
    }

    class IPagoProcesador {
        <<Strategy Pattern>>
        Algoritmos intercambiables para procesar pagos
    }

    class INotificationObserver {
        <<Observer Pattern>>
        Notificación de eventos a múltiples observadores
    }
```

## Diagramas MER

### Sistema Actual: Modelo Entidad-Relación Básico (MERA)

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

### Sistema Refactorizado: Modelo Entidad-Relación Completo (MERR)

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

### Sistema Actual: Instancias Básicas (DOA)

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

### Sistema Refactorizado: Instancias Avanzadas (DOR)

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

### Sistema Actual: Componentes Básicos (DCOA)

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

### Sistema Refactorizado: Componentes Distribuidos (DCOR)

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

1. **Arquitectura (DAA → DAR)**: Migración de una aplicación monolítica de escritorio a una arquitectura web cliente-servidor con separación de responsabilidades.

2. **Patrones de Diseño (DPA → DPR)**: Implementación de múltiples patrones como Repository, Factory, Observer, State y Facade para mejorar la mantenibilidad y escalabilidad.

3. **Modelo de Datos (DCA → DCR, MERA → MERR)**: Expansión del modelo con nuevas entidades como Mesa, DeliveryPedido, Transaccion y Usuario, habilitando nuevas funcionalidades de negocio.

4. **Componentes (DCOA → DCOR)**: Distribución en componentes independientes y especializados que pueden evolucionar de manera separada.

5. **Acceso**: Transformación de un sistema de acceso único a uno multiusuario con diferentes roles y permisos.

6. **Tecnología**: Actualización tecnológica de Python con customtkinter a una stack moderna con React para frontend y Django para backend.

Estos cambios no solo modernizan la infraestructura tecnológica sino que transforman fundamentalmente la manera en que opera el restaurante, proporcionando nuevas capacidades y mejorando la experiencia de todos los involucrados.
