# Diagramas del Sistema de Gestión de Restaurante

Este documento contiene diagramas comparativos entre el sistema actual (Python con customtkinter) y el sistema refactorizado propuesto (aplicación web con React/Django). Los diagramas se presentan en pares para mostrar claramente el antes y después de la refactorización.

## 1. Arquitectura del Sistema

### Arquitectura Actual (Aplicación de Escritorio)

```mermaid
graph TD
    A[Usuario] --> B[Aplicación Desktop<br/>Python + customtkinter]
    B --> C[(Base de Datos SQLite)]
    
    subgraph "Aplicación Desktop"
        B1[Interfaz de Usuario<br/>customtkinter] --> B2[Controladores<br/>Panels]
        B2 --> B3[Lógica de Negocio<br/>CRUD]
        B3 --> B4[Acceso a Datos<br/>SQLAlchemy ORM]
    end
    
    B4 --> C
```

### Arquitectura Refactorizada (Aplicación Web)

```mermaid
graph TD
    A[Cliente/Usuario] --> B[Navegador Web]
    B <--> C[Frontend<br/>React]
    C <--> D[Backend<br/>Django REST API]
    D --> E[(Base de Datos)]
    
    subgraph "Frontend (React)"
        C1[Componentes UI] --> C2[Gestión de Estado<br/>Context/Redux]
        C2 --> C3[Servicios API]
    end
    
    subgraph "Backend (Clean Architecture)"
        subgraph "Capa de Presentación"
            D1[API Controllers/Views]
            D1a[Serializers]
        end
        
        subgraph "Capa de Casos de Uso"
            D2[Services]
            D2a[Casos de Uso]
            D2b[Interfaces de Repositorios]
        end
        
        subgraph "Capa de Dominio"
            D3[Entidades]
            D3a[Value Objects]
            D3b[Reglas de Negocio]
        end
        
        subgraph "Capa de Infraestructura"
            D4[Repositorios Concretos]
            D4a[ORM Django]
            D4b[Servicios Externos]
        end
        
        D1 --> D1a
        D1a --> D2
        D2 --> D2a
        D2 --> D2b
        D2a --> D3
        D2b --> D4
        D3 --> D3a
        D3 --> D3b
        D4 --> D4a
        D4 --> D4b
        D4a --> E
    end
    
    C3 <--> D1
```

## 2. MER

### MER Actual

```mermaid
classDiagram
    Cliente "1" -- "*" Pedido
    Pedido "*" -- "*" Menu
    Menu "*" -- "*" Ingrediente
    MenuIngrediente -- Menu
    MenuIngrediente -- Ingrediente
    
    class Cliente {
        +rut: String PK
        +email: String
        +nombre: String
    }
    
    class Ingrediente {
        +id: Integer PK
        +nombre: String
        +tipo: String
        +cantidad: Float
        +unidad: String
    }
    
    class Menu {
        +id: Integer PK
        +nombre: String
        +descripcion: Text
        +precio: Float
        +ing_necesarios: JSON
    }
    
    class MenuIngrediente {
        +id: Integer PK
        +menu_id: Integer FK
        +ingrediente_id: Integer FK
        +cantidad: Float
    }
    
    class Pedido {
        +id: Integer PK
        +descripcion: String
        +total: Float
        +fecha: DateTime
        +cliente_rut: String FK
        +menus: JSON
    }
```

### MER Refactorizado

```mermaid
classDiagram
    Cliente "1" -- "*" Pedido
    Pedido "*" -- "*" Menu
    Menu "*" -- "*" Ingrediente
    MenuIngrediente -- Menu
    MenuIngrediente -- Ingrediente
    Mesa "0..1" -- "0..1" Pedido
    Pedido "1" -- "*" Transaccion
    DeliveryPedido --|> Pedido
    DeliveryPedido -- DeliveryApp
    DeliveryPedido -- DeliveryRepartidor
    MedioPago "1" -- "*" Transaccion
    
    class Cliente {
        +rut: String PK
        +email: String
        +nombre: String
        +telefono: String
        +direccion: String
        +historial_pedidos()
    }
    
    class Ingrediente {
        +id: Integer PK
        +nombre: String
        +tipo: String
        +cantidad: Float
        +unidad: String
        +nivel_critico: Float
        +verificarDisponibilidad()
        +actualizarStock()
    }
    
    class Menu {
        +id: Integer PK
        +nombre: String
        +descripcion: Text
        +precio: Float
        +ing_necesarios: JSON
        +imagen: String
        +categoria: String
        +disponible: Boolean
        +calcularCosto()
        +verificarDisponibilidad()
    }
    
    class MenuIngrediente {
        +id: Integer PK
        +menu_id: Integer FK
        +ingrediente_id: Integer FK
        +cantidad: Float
    }
    
    class Pedido {
        +id: Integer PK
        +descripcion: String
        +total: Float
        +fecha: DateTime
        +cliente_rut: String FK
        +estado: String
        +menus: JSON
        +mesa_id: Integer FK
        +generarBoleta()
        +calcularTotal()
    }
    
    class Mesa {
        +id: Integer PK
        +numero: Integer
        +capacidad: Integer
        +estado: String
        +hora_inicio: DateTime
        +calcularTiempoOcupacion()
    }
    
    class Transaccion {
        +id: Integer PK
        +pedido_id: Integer FK
        +monto: Float
        +fecha: DateTime
        +medio_pago_id: Integer FK
        +estado: String
    }
    
    class MedioPago {
        +id: Integer PK
        +nombre: String
        +activo: Boolean
    }
    
    class DeliveryPedido {
        +pedido_id: Integer PK, FK
        +direccion_entrega: String
        +tiempo_estimado: Integer
        +delivery_app_id: Integer FK
        +repartidor_id: Integer FK
        +estado_delivery: String
    }
    
    class DeliveryApp {
        +id: Integer PK
        +nombre: String
        +comision: Float
    }
    
    class DeliveryRepartidor {
        +id: Integer PK
        +nombre: String
        +telefono: String
    }
```

## 3. Patrones de Diseño

### Patrones de Diseño Actuales

```mermaid
graph TD
    A[MainApp] --> B[PanelFactory]
    B -->|Factory Method| C1[ClientePanel]
    B -->|Factory Method| C2[IngredientePanel]
    B -->|Factory Method| C3[MenuPanel]
    B -->|Factory Method| C4[PanelCompra]
    B -->|Factory Method| C5[PanelPedido]
    B -->|Factory Method| C6[GraficosPanel]
    
    subgraph "CRUD Operations"
        D1[ClienteCRUD]
        D2[IngredienteCRUD]
        D3[MenuCRUD]
        D4[PedidoCRUD]
    end
    
    C1 --> D1
    C2 --> D2
    C3 --> D3
    C4 --> D3 & D4
    C5 --> D4
```

### Patrones de Diseño Refactorizados

```mermaid
graph TD
    subgraph "Frontend"
        A[App] --> B[Router]
        B --> C[Pages/Components]
        C --> D[Custom Hooks/Context]
        D --> E[API Services]
    end
    
    subgraph "Backend (Clean Architecture)"
        F[Controllers] --> G[Use Cases]
        G --> H[Domain Model]
        G --> I[Repository Interfaces]
        I --> J[Repository Implementations]
    end
    
    subgraph "Patrones Implementados"
        P1[Repository] -.-> J
        P2[Factory Method] -.-> C & F
        P3[Strategy] -.-> G
        P4[Observer] -.-> D
        P5[Singleton] -.-> D
        P6[Decorator] -.-> G
        P7[Adapter] -.-> E & J
    end
```

## 4. Flujo de Trabajo de Pedidos

### Flujo Actual

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Interfaz Usuario
    participant PanelCompra
    participant PedidoCRUD
    participant MenuCRUD
    participant IngredienteCRUD
    participant DB as Base de Datos
    
    Usuario->>UI: Selecciona Panel de Compra
    UI->>PanelCompra: Carga panel
    PanelCompra->>MenuCRUD: Solicita menús disponibles
    MenuCRUD->>DB: Consulta menús
    DB-->>MenuCRUD: Devuelve menús
    MenuCRUD-->>PanelCompra: Lista de menús
    PanelCompra->>ClienteCRUD: Solicita clientes
    ClienteCRUD->>DB: Consulta clientes
    DB-->>ClienteCRUD: Devuelve clientes
    ClienteCRUD-->>PanelCompra: Lista de clientes
    
    Usuario->>PanelCompra: Selecciona menú y cantidad
    PanelCompra->>PanelCompra: Verifica disponibilidad de ingredientes
    PanelCompra->>PanelCompra: Agrega al carrito
    
    Usuario->>PanelCompra: Selecciona cliente
    Usuario->>PanelCompra: Confirma pedido
    PanelCompra->>PedidoCRUD: Crear pedido
    PedidoCRUD->>DB: Guarda pedido
    DB-->>PedidoCRUD: Confirma guardado
    PedidoCRUD->>IngredienteCRUD: Actualiza stock de ingredientes
    IngredienteCRUD->>DB: Guarda cambios en inventario
    DB-->>IngredienteCRUD: Confirma actualización
    PedidoCRUD-->>PanelCompra: Confirma creación de pedido
    PanelCompra->>Usuario: Muestra confirmación y genera boleta
```

### Flujo Refactorizado

```mermaid
sequenceDiagram
    actor Usuario
    participant Frontend
    participant API
    participant PedidoService
    participant MenuService
    participant IngredienteService
    participant MesaService
    participant DB as Base de Datos
    
    Usuario->>Frontend: Navega a página de pedidos
    Frontend->>API: GET /api/menus/
    API->>MenuService: Solicita menús disponibles
    MenuService->>DB: Consulta menús
    DB-->>MenuService: Devuelve menús
    MenuService-->>API: Devuelve menús disponibles
    API-->>Frontend: Lista de menús
    
    Frontend->>API: GET /api/mesas/disponibles/
    API->>MesaService: Solicita mesas disponibles
    MesaService->>DB: Consulta estado de mesas
    DB-->>MesaService: Devuelve mesas disponibles
    MesaService-->>API: Lista de mesas disponibles
    API-->>Frontend: Lista de mesas
    
    Usuario->>Frontend: Selecciona mesa
    Usuario->>Frontend: Selecciona menús y cantidades
    Frontend->>API: POST /api/pedidos/verificar/
    API->>PedidoService: Verifica disponibilidad
    PedidoService->>IngredienteService: Consulta stock de ingredientes
    IngredienteService->>DB: Verifica stock
    DB-->>IngredienteService: Confirma disponibilidad
    IngredienteService-->>PedidoService: Confirma disponibilidad
    PedidoService-->>API: Confirma viabilidad del pedido
    API-->>Frontend: Confirmación de disponibilidad
    
    Usuario->>Frontend: Confirma pedido
    Frontend->>API: POST /api/pedidos/
    API->>PedidoService: Crear pedido
    PedidoService->>DB: Guarda pedido
    PedidoService->>MesaService: Actualiza estado de mesa
    MesaService->>DB: Actualiza mesa a "ocupada"
    PedidoService->>IngredienteService: Actualiza stock
    IngredienteService->>DB: Actualiza inventario
    DB-->>PedidoService: Confirma cambios
    PedidoService-->>API: Devuelve pedido creado
    API-->>Frontend: Confirmación y detalles del pedido
    Frontend->>Usuario: Muestra confirmación y opción de pago
```

## 5. Diagrama de Componentes

### Componentes Actuales

```mermaid
graph TD
    A[MainApp] --> B[CustomTkinter UI]
    A --> C[PanelFactory]
    
    C --> D1[ClientePanel]
    C --> D2[IngredientePanel]
    C --> D3[MenuPanel]
    C --> D4[PanelCompra]
    C --> D5[PanelPedido]
    C --> D6[GraficosPanel]
    
    D1 --> E1[ClienteCRUD]
    D2 --> E2[IngredienteCRUD]
    D3 --> E3[MenuCRUD]
    D4 --> E3 & E4[PedidoCRUD]
    D5 --> E4
    
    E1 --> F[SQLAlchemy ORM]
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G[SQLite Database]
    
    D6 --> H[Matplotlib]
    
    D4 --> I[FPDF Generator]
```

### Componentes Refactorizados

```mermaid
graph TD
    subgraph "Frontend"
        A1[App] --> A2[Router]
        A2 --> B1[Páginas]
        B1 --> B2[Componentes]
        B2 --> C1[Custom Hooks]
        C1 --> C2[API Client]
    end
    
    subgraph "Backend"
        D1[URLs/Routes] --> D2[Views/Controllers]
        D2 --> E1[Serializers]
        D2 --> E2[Services]
        E2 --> F1[Repositories]
        F1 --> F2[Models]
        F2 --> G[Database]
    end
    
    subgraph "Frontend Components"
        B1 --> H1[Dashboard]
        B1 --> H2[Cliente]
        B1 --> H3[Ingrediente]
        B1 --> H4[Menu]
        B1 --> H5[Pedido]
        B1 --> H6[Mesa]
        B1 --> H7[Delivery]
        B1 --> H8[Pagos]
    end
    
    subgraph "Backend Services"
        E2 --> I1[ClienteService]
        E2 --> I2[IngredienteService]
        E2 --> I3[MenuService]
        E2 --> I4[PedidoService]
        E2 --> I5[MesaService]
        E2 --> I6[DeliveryService]
        E2 --> I7[PagoService]
        E2 --> I8[ReporteService]
    end
    
    C2 <--> D1
```

## 6. Diagrama de Despliegue

### Despliegue Actual

```mermaid
graph TD
    A[PC con Aplicación Desktop] --> B[(Base de Datos SQLite Local)]
```

### Despliegue Refactorizado

```mermaid
graph TD
    A[Usuario] --> B[Navegador Web]
    B <--> C[Servidor Web/Proxy - Nginx]
    C --> D[Servidor Frontend - React]
    C --> E[Servidor Backend - Django]
    E --> F[(Base de Datos PostgreSQL)]
    
    subgraph "Infraestructura Cloud"
        C
        D
        E
        F
    end
```

## 7. Comparación de Arquitecturas

```mermaid
graph TB
    subgraph "Arquitectura Actual"
        A1[Monolítica]
        A2[UI: customtkinter]
        A3[Lógica: PanelFactory + CRUD]
        A4[Datos: SQLAlchemy ORM]
        A5[DB: SQLite Local]
        
        A1 --- A2
        A1 --- A3
        A1 --- A4
        A1 --- A5
    end
    
    subgraph "Arquitectura Refactorizada"
        B1[Distribuida Cliente-Servidor]
        B2[UI: React Components]
        B3[Frontend: Estado + API Client]
        B4[Backend: API Controllers]
        B5[Services: Casos de Uso]
        B6[Repositories: Acceso a Datos]
        B7[DB: PostgreSQL]
        
        B1 --- B2
        B1 --- B3
        B1 --- B4
        B1 --- B5
        B1 --- B6
        B1 --- B7
    end
    
    A1 --->|Evolución| B1
    A2 --->|Reemplazado por| B2
    A3 --->|Separado en| B3 & B4 & B5
    A4 --->|Abstraído mediante| B6
    A5 --->|Migrado a| B7
```

### Tabla Comparativa de Arquitecturas

| **Aspecto** | **Arquitectura Actual** | **Arquitectura Refactorizada** | **Beneficios del Cambio** |
|-------------|-------------------------|-------------------------------|---------------------------|
| **Tipo** | Monolítica de escritorio | Distribuida cliente-servidor | Acceso simultáneo desde múltiples dispositivos |
| **Interfaz de Usuario** | CustomTkinter (Python) | React Components (JavaScript) | UI responsive, moderna e interactiva |
| **Estructura de Capas** | 3 capas básicas integradas:<br>- UI<br>- Lógica de negocio<br>- Acceso a datos | 6 capas claramente separadas:<br>- Componentes UI<br>- Gestión de estado<br>- API Client<br>- API Controllers<br>- Services (casos de uso)<br>- Repositories | Mejor separación de responsabilidades, código más mantenible |
| **Integración** | Directa entre capas | A través de interfaces y contratos | Menor acoplamiento, mayor facilidad para pruebas |
| **Base de Datos** | SQLite local | PostgreSQL | Mayor escalabilidad, concurrencia y herramientas avanzadas |
| **Despliegue** | Instalación en cada PC | Servidores centralizados | Actualizaciones inmediatas para todos los usuarios |
| **Concurrencia** | Un usuario a la vez | Múltiples usuarios simultáneos | Elimina cuellos de botella operativos |
| **Escalabilidad** | Limitada por hardware local | Alta, con posibilidad de escalar servicios individualmente | Puede crecer con las necesidades del negocio |

## 8. Comparación de Patrones de Diseño

```mermaid
graph TD
    subgraph "Patrones Actuales"
        A1[Factory Method]
        A2[Basic CRUD Operations]
        A3[Simple Template Method]
    end
    
    subgraph "Patrones Refactorizados"
        B1[Factory Method]
        B2[Repository]
        B3[Strategy]
        B4[Observer]
        B5[Singleton]
        B6[Decorator]
        B7[Adapter]
    end
    
    A1 ---|Evoluciona| B1
    A2 ---|Se transforma en| B2
    A3 ---|Se expande a| B3
    
    style A1 fill:#f9d5e5,stroke:#333
    style A2 fill:#f9d5e5,stroke:#333
    style A3 fill:#f9d5e5,stroke:#333
    
    style B1 fill:#d5e5f9,stroke:#333
    style B2 fill:#d5e5f9,stroke:#333
    style B3 fill:#d5e5f9,stroke:#333
    style B4 fill:#e5f9d5,stroke:#333
    style B5 fill:#e5f9d5,stroke:#333
    style B6 fill:#e5f9d5,stroke:#333
    style B7 fill:#e5f9d5,stroke:#333
```

### Tabla Comparativa de Patrones de Diseño

| **Patrón** | **Implementación Actual** | **Implementación Refactorizada** | **Mejora** |
|------------|---------------------------|----------------------------------|------------|
| **Factory Method** | `PanelFactory` crea interfaces de usuario | Implementado tanto en frontend para crear componentes como en backend para crear servicios | Uso más sofisticado en ambas capas, permitiendo extensibilidad |
| **Repository** | No implementado claramente, operaciones CRUD básicas | Interfaces de repositorio para cada entidad con implementaciones concretas | Abstracción del acceso a datos, facilitando cambios en la fuente de datos y pruebas unitarias |
| **Strategy** | No implementado | Estrategias para diferentes lógicas de negocio (descuentos, pagos, etc.) | Flexibilidad para cambiar algoritmos en tiempo de ejecución |
| **Observer** | No implementado | En frontend para reaccionar a cambios de estado y en backend para eventos del sistema | Comunicación desacoplada entre componentes |
| **Singleton** | No implementado | Gestión de estado global en frontend y servicios compartidos en backend | Garantiza una única instancia para recursos compartidos |
| **Decorator** | No implementado | Añade funcionalidades como logging, caché o validación a los casos de uso | Extensión de comportamiento sin modificar clases existentes |
| **Adapter** | No implementado | Adaptar servicios externos (como API de delivery) a la interfaz del sistema | Integración con sistemas externos sin modificar código existente |

### Evolución de Implementaciones

1. **De Simple CRUD a Repository Pattern**:
   * **Antes**: Operaciones CRUD directamente en clases como `ClienteCRUD`
   * **Después**: Interfaces de repositorio (`IClienteRepository`) con implementaciones concretas

2. **De Panels a Components con Hooks**:
   * **Antes**: Paneles grandes con múltiples responsabilidades
   * **Después**: Componentes pequeños y reutilizables con hooks para lógica compartida

3. **De Acceso Directo a Datos a Services**:
   * **Antes**: Los paneles acceden directamente a las operaciones CRUD
   * **Después**: Capa de servicio intermedia que encapsula la lógica de negocio

4. **De Custom Widget a Componentes React**:
   * **Antes**: Widgets customizados de Tkinter
   * **Después**: Componentes React reutilizables y con estado propio
