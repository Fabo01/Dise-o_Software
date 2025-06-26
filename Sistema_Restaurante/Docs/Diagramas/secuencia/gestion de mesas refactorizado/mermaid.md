
#### CU-R21: Registrar Mesa

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as TableService
    participant RP as TableRepository
    participant ORM as ORM Django
    participant BD as Base de Datos

    Usuario->>UI: Selecciona "Gestionar mesas"
    activate UI
    Usuario->>UI: Selecciona "Agregar nueva mesa"

    UI->>UI: Muestra formulario de creación de mesa

    Usuario->>UI: Completa datos (número, capacidad, ubicación)
    Usuario->>UI: Posiciona la mesa en el mapa visual
    Usuario->>UI: Confirma creación de mesa
    
    UI->>GE: dispatch(createTable(tableData))
    activate GE
    GE->>SA: postTable(tableData)
    activate SA
    SA->>AC: POST /api/tables
    activate AC
    
    AC->>SZ: TableCreateSerializer(data)
    activate SZ
    SZ->>SZ: Validar datos
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: crearMesa(tableData)
    activate SV
    SV->>SV: verificarNumeroUnico(tableData.numero)
    SV->>SV: validarPosicion(tableData.posicion)
    
    SV->>RP: save(tableEntity)
    activate RP
    RP->>ORM: Mesa.objects.create()
    activate ORM
    ORM->>BD: INSERT INTO mesa...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    ORM-->>RP: Mesa creada
    deactivate ORM
    RP-->>SV: MesaDTO
    deactivate RP
    
    SV-->>AC: MesaDTO
    deactivate SV
    
    AC->>SZ: TableSerializer(mesa)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 201 Created
    deactivate AC
    SA-->>GE: Mesa creada
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Actualiza mapa visual con nueva mesa
    UI->>Usuario: Muestra confirmación de creación
    
    alt Crear múltiples mesas secuenciales
        Usuario->>UI: Selecciona "Crear mesas secuenciales"
        UI->>UI: Muestra formulario con rango
        Usuario->>UI: Define rango y características comunes
        
        UI->>GE: dispatch(createSequentialTables(data))
        activate GE
        GE->>SA: postSequentialTables(data)
        activate SA
        SA->>AC: POST /api/tables/sequential
        activate AC
        AC->>SV: crearMesasSecuenciales(data)
        activate SV
        
        loop Para cada mesa en el rango
            SV->>RP: save(mesaEntity)
            activate RP
            RP->>ORM: Mesa.objects.create()
            activate ORM
            ORM->>BD: INSERT INTO mesa...
            activate BD
            BD-->>ORM: Confirmación
            deactivate BD
            ORM-->>RP: Mesa creada
            deactivate ORM
            RP-->>SV: MesaDTO
            deactivate RP
        end
        
        SV-->>AC: Lista MesaDTO
        deactivate SV
        AC->>SZ: TableListSerializer(mesas)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 201 Created
        deactivate AC
        SA-->>GE: Mesas creadas
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>UI: Actualiza mapa visual con nuevas mesas
        UI->>Usuario: Muestra confirmación
    end
    deactivate UI
```

#### CU-R22: Asignar Cliente a Mesa

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/ME)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as TableService
    participant RP as TableRepository
    participant CR as ClientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant WS as WebSocket Service

    Usuario->>UI: Accede al mapa visual de mesas
    activate UI
    
    UI->>GE: dispatch(loadTables())
    activate GE
    GE->>SA: getTables()
    activate SA
    SA->>AC: GET /api/tables
    activate AC
    AC->>SV: obtenerMesas()
    activate SV
    SV->>RP: findAll()
    activate RP
    RP->>ORM: Mesa.objects.all()
    activate ORM
    ORM->>BD: SELECT FROM mesa
    activate BD
    BD-->>ORM: Datos de mesas
    deactivate BD
    ORM-->>RP: Lista de mesas
    deactivate ORM
    RP-->>SV: Lista MesaDTO
    deactivate RP
    SV-->>AC: Lista MesaDTO
    deactivate SV
    
    AC->>SZ: TableListSerializer(mesas)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Lista de mesas
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Muestra mapa con estados de mesas
    
    Usuario->>UI: Selecciona una mesa disponible
    UI->>UI: Muestra opciones de asignación
    
    alt Cliente existente
        Usuario->>UI: Busca cliente por nombre/RUT
        UI->>GE: dispatch(searchClients(searchTerm))
        activate GE
        GE->>SA: getClients({search: searchTerm})
        activate SA
        SA->>AC: GET /api/clients?search=...
        activate AC
        AC->>SV: buscarClientes(criterio)
        activate SV
        SV->>CR: findBySearchTerm(criterio)
        activate CR
        CR->>ORM: Cliente.objects.filter(...)
        activate ORM
        ORM->>BD: SELECT FROM cliente WHERE...
        activate BD
        BD-->>ORM: Clientes encontrados
        deactivate BD
        ORM-->>CR: Lista de clientes
        deactivate ORM
        CR-->>SV: Lista ClienteDTO
        deactivate CR
        SV-->>AC: Lista ClienteDTO
        deactivate SV
        
        AC->>SZ: ClientSerializer(clientes)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Clientes encontrados
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        
        UI->>Usuario: Muestra resultados de búsqueda
        Usuario->>UI: Selecciona el cliente deseado
    else Nuevo cliente
        Usuario->>UI: Elige crear nuevo cliente
        UI->>UI: Muestra formulario de cliente
        Usuario->>UI: Ingresa datos del cliente
        UI->>GE: dispatch(createClient(clientData))
        activate GE
        GE->>SA: postClient(clientData)
        activate SA
        SA->>AC: POST /api/clients
        activate AC
        
        // Proceso de creación de cliente similar a CU-R01
        
        AC-->>SA: Response 201 Created
        deactivate AC
        SA-->>GE: Cliente creado
        deactivate SA
        GE->>UI: Actualiza estado con nuevo cliente
        deactivate GE
    end
    
    Usuario->>UI: Especifica número de personas
    Usuario->>UI: Confirma asignación
    
    UI->>GE: dispatch(assignClientToTable(tableId, {clientId, persons, info}))
    activate GE
    GE->>SA: postTableAssignment(tableId, data)
    activate SA
    SA->>AC: POST /api/tables/{id}/assign
    activate AC
    AC->>SZ: TableAssignmentSerializer(data)
    activate SZ
    SZ->>SZ: Validar datos
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: asignarClienteAMesa(id, data)
    activate SV
    SV->>RP: findById(id)
    activate RP
    RP->>ORM: Mesa.objects.get(id=id)
    activate ORM
    ORM->>BD: SELECT FROM mesa WHERE id=...
    activate BD
    BD-->>ORM: Datos de la mesa
    deactivate BD
    ORM-->>RP: Mesa
    deactivate ORM
    RP-->>SV: MesaDTO
    deactivate RP
    
    SV->>SV: verificarDisponibilidad(mesa)
    SV->>RP: updateStatus(id, 'ocupada', data)
    activate RP
    RP->>ORM: Mesa.objects.filter(id=id).update(...)
    activate ORM
    ORM->>BD: UPDATE mesa SET estado='ocupada', cliente_id=..., ...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    ORM-->>RP: Confirmación
    deactivate ORM
    RP-->>SV: Éxito
    deactivate RP
    
    SV->>WS: broadcastTableUpdate(id, 'ocupada', data)
    activate WS
    WS-->>WS: Notifica a todos los clientes conectados
    deactivate WS
    
    SV-->>AC: MesaAsignadaDTO
    deactivate SV
    
    AC->>SZ: TableAssignmentResponseSerializer(data)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Asignación completada
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Actualiza mapa visual (mesa cambia a ocupada)
    UI->>UI: Inicia contador de tiempo de ocupación
    UI->>Usuario: Muestra confirmación
    deactivate UI
```

#### CU-R23: Cambiar Estado de Mesa

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/ME)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as TableService
    participant RP as TableRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant WS as WebSocket Service

    Usuario->>UI: Accede al mapa de mesas
    activate UI
    
    UI->>GE: dispatch(loadTables())
    activate GE
    GE->>SA: getTables()
    activate SA
    SA->>AC: GET /api/tables
    activate AC
    AC->>SV: obtenerMesas()
    activate SV
    SV->>RP: findAll()
    activate RP
    RP->>ORM: Mesa.objects.all()
    activate ORM
    ORM->>BD: SELECT FROM mesa
    activate BD
    BD-->>ORM: Datos de mesas
    deactivate BD
    ORM-->>RP: Lista de mesas
    deactivate ORM
    RP-->>SV: Lista MesaDTO
    deactivate RP
    SV-->>AC: Lista MesaDTO
    deactivate SV
    
    AC->>SZ: TableListSerializer(mesas)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Lista de mesas
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Muestra mapa visual de mesas
    
    Usuario->>UI: Selecciona una mesa
    UI->>UI: Muestra opciones de estados disponibles
    
    Usuario->>UI: Selecciona nuevo estado
    Usuario->>UI: Opcionalmente ingresa notas adicionales
    Usuario->>UI: Confirma el cambio
    
    UI->>GE: dispatch(updateTableStatus(tableId, {estado: nuevoEstado, notas: notas}))
    activate GE
    GE->>SA: patchTableStatus(tableId, data)
    activate SA
    SA->>AC: PATCH /api/tables/{id}/status
    activate AC
    AC->>SZ: TableStatusUpdateSerializer(data)
    activate SZ
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: actualizarEstadoMesa(id, nuevoEstado, notas)
    activate SV
    SV->>SV: validarTransicionEstado(estadoActual, nuevoEstado)
    
    SV->>RP: updateStatus(id, nuevoEstado, notas)
    activate RP
    RP->>ORM: Mesa.objects.filter(id=id).update(estado=nuevoEstado, ...)
    activate ORM
    ORM->>BD: UPDATE mesa SET estado=..., notas=... WHERE id=...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    
    alt Cambio a estado "ocupada"
        ORM->>BD: UPDATE mesa SET hora_inicio=NOW() WHERE id=...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
    else Cambio a estado "libre"
        ORM->>BD: INSERT INTO historial_ocupacion (mesa_id, inicio, fin, duracion)...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
    end
    
    ORM-->>RP: Confirmación
    deactivate ORM
    RP-->>SV: Éxito
    deactivate RP
    
    SV->>WS: broadcastTableUpdate(id, nuevoEstado)
    activate WS
    WS-->>WS: Notifica a todos los clientes conectados
    deactivate WS
    
    SV-->>AC: MesaActualizadaDTO
    deactivate SV
    
    AC->>SZ: TableStatusSerializer(mesa)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Estado actualizado
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Actualiza visualización de la mesa con nuevo estado
    UI->>Usuario: Muestra confirmación del cambio
    
    alt Nueva mesa ocupada
        UI->>UI: Inicia contador de tiempo de ocupación
    else Mesa liberada
        UI->>UI: Detiene y guarda tiempo de ocupación
    end
    
    deactivate UI
```

#### CU-R24: Calcular Tiempo de Ocupación

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/ME)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as TableService
    participant RP as TableRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant TMR as Timer Service

    Usuario->>UI: Accede al mapa de mesas o informes de ocupación
    activate UI
    
    UI->>GE: dispatch(loadTablesWithOccupationTimes())
    activate GE
    GE->>SA: getTablesWithTimes()
    activate SA
    SA->>AC: GET /api/tables/occupation
    activate AC
    AC->>SV: obtenerMesasConTiemposOcupacion()
    activate SV
    SV->>RP: findAllWithOccupationTimes()
    activate RP
    RP->>ORM: Mesa.objects.all()
    activate ORM
    ORM->>BD: SELECT FROM mesa
    activate BD
    BD-->>ORM: Datos de mesas
    deactivate BD
    
    loop Para cada mesa ocupada
        ORM->>BD: SELECT TIMESTAMPDIFF(MINUTE, hora_inicio, NOW()) FROM mesa WHERE id=...
        activate BD
        BD-->>ORM: Tiempo transcurrido
        deactivate BD
    end
    
    ORM-->>RP: Mesas con tiempos
    deactivate ORM
    RP-->>SV: Lista MesaConTiempoDTO
    deactivate RP
    
    SV->>SV: calcularEstadisticasOcupacion()
    SV->>SV: categorizarPorTiempo(mesas)
    SV-->>AC: MesasConTiemposDTO
    deactivate SV
    
    AC->>SZ: TableOccupationSerializer(data)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Mesas con tiempos
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Configura temporizadores para mesas ocupadas
    UI->>TMR: startTimers(mesasOcupadas)
    activate TMR
    TMR-->>UI: Temporizadores iniciados
    deactivate TMR
    
    UI->>UI: Aplica códigos de color según duración
    UI->>Usuario: Muestra mapa de mesas con indicadores de tiempo
    
    alt Usuario solicita análisis detallado
        Usuario->>UI: Selecciona "Análisis de tiempos"
        UI->>GE: dispatch(getOccupationAnalytics())
        activate GE
        GE->>SA: getTableAnalytics()
        activate SA
        SA->>AC: GET /api/analytics/tables/occupation
        activate AC
        AC->>SV: obtenerAnalisisOcupacion()
        activate SV
        SV->>RP: getOccupationStatistics()
        activate RP
        RP->>ORM: Queries para estadísticas
        activate ORM
        ORM->>BD: SELECT AVG(duracion)... GROUP BY mesa_id, hora...
        activate BD
        BD-->>ORM: Datos estadísticos
        deactivate BD
        ORM-->>RP: Estadísticas
        deactivate ORM
        RP-->>SV: EstadisticasDTO
        deactivate RP
        
        SV->>SV: calcularTendenciasOcupacion()
        SV->>SV: identificarPatrones()
        SV-->>AC: AnalisisOcupacionDTO
        deactivate SV
        
        AC->>SZ: OccupationAnalyticsSerializer(datos)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Datos de análisis
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        
        UI->>UI: Genera gráficos y visualizaciones
        UI->>Usuario: Muestra panel de análisis con métricas
    end
    
    loop Cada minuto para mesas ocupadas
        TMR->>UI: updateOccupationTimes()
        activate TMR
        UI->>UI: Actualiza contadores y cambia colores si necesario
        TMR-->>UI: Actualización completa
        deactivate TMR
    end
    
    alt Mesa supera tiempo promedio
        TMR->>UI: triggerAlert(mesaId)
        activate TMR
        UI->>UI: Muestra alerta visual
        UI->>Usuario: Notifica sobre mesa con tiempo excesivo
        TMR-->>UI: Alerta enviada
        deactivate TMR
    end
    
    deactivate UI
```

#### CU-R25: Registrar Pedido Delivery

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/ME)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as DeliveryService
    participant OS as OrderService
    participant RP as DeliveryRepository
    participant OR as OrderRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant NS as NotificationService

    Usuario->>UI: Selecciona "Nuevo pedido delivery"
    activate UI
    
    UI->>GE: dispatch(loadDeliveryData())
    activate GE
    GE->>SA: getDeliveryData()
    activate SA
    SA->>AC: GET /api/delivery/setup
    activate AC
    AC->>SV: obtenerConfiguracionDelivery()
    activate SV
    SV->>RP: getDeliveryApps()
    activate RP
    RP->>ORM: DeliveryApp.objects.filter(activa=True)
    activate ORM
    ORM->>BD: SELECT FROM delivery_app WHERE activa=TRUE
    activate BD
    BD-->>ORM: Apps disponibles
    deactivate BD
    ORM-->>RP: Lista de apps
    deactivate ORM
    RP-->>SV: Lista DeliveryAppDTO
    deactivate RP
    SV-->>AC: ConfiguracionDeliveryDTO
    deactivate SV
    
    AC->>SZ: DeliveryConfigurationSerializer(config)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Datos de configuración
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>GE: dispatch(loadAvailableMenus())
    activate GE
    // ... (similar a CU-R16 para cargar menús) ...
    GE->>UI: Actualiza estado con menús disponibles
    deactivate GE
    
    UI->>UI: Muestra formulario específico para delivery
    UI->>Usuario: Solicita selección de tipo de delivery
    
    Usuario->>UI: Selecciona directo o app externa
    
    alt Pedido por app externa
        Usuario->>UI: Selecciona plataforma (Rappi, Uber Eats, etc.)
        Usuario->>UI: Ingresa código pedido externo
    else Pedido directo
        Usuario->>UI: Busca o crea cliente
        Usuario->>UI: Ingresa dirección de entrega
        UI->>UI: Calcula costo de envío basado en distancia
    end
    
    Usuario->>UI: Selecciona menús para el pedido
    Usuario->>UI: Ajusta cantidades y opciones
    UI->>UI: Calcula subtotales y total
    
    Usuario->>UI: Confirma creación del pedido
    UI->>GE: dispatch(createDeliveryOrder(deliveryData))
    activate GE
    GE->>SA: postDeliveryOrder(deliveryData)
    activate SA
    SA->>AC: POST /api/delivery/orders
    activate AC
    AC->>SZ: DeliveryOrderCreateSerializer(data)
    activate SZ
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: crearPedidoDelivery(deliveryData)
    activate SV
    SV->>OS: crearPedidoBase(datos)
    activate OS
    OS->>OR: save(pedidoEntity)
    activate OR
    OR->>ORM: transaction.atomic()
    activate ORM
    ORM->>BD: INSERT INTO pedido...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    
    loop Para cada ítem
        ORM->>BD: INSERT INTO item_pedido...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
    end
    
    ORM-->>OR: Pedido base creado
    deactivate ORM
    OR-->>OS: PedidoDTO
    deactivate OR
    OS-->>SV: PedidoDTO
    deactivate OS
    
    SV->>RP: saveDeliveryInfo(pedidoId, deliveryData)
    activate RP
    RP->>ORM: DeliveryPedido.objects.create(...)
    activate ORM
    ORM->>BD: INSERT INTO delivery_pedido...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    ORM-->>RP: Confirmación
    deactivate ORM
    RP-->>SV: DeliveryPedidoDTO
    deactivate RP
    
    SV->>NS: notificarNuevoPedidoDelivery(pedidoDTO)
    activate NS
    NS->>NS: enviarNotificacionGestorDelivery()
    NS-->>SV: Notificación enviada
    deactivate NS
    
    SV-->>AC: PedidoDeliveryDTO
    deactivate SV
    
    AC->>SZ: DeliveryOrderSerializer(pedido)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 201 Created
    deactivate AC
    SA-->>GE: Pedido delivery creado
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>Usuario: Muestra confirmación y detalles del pedido
    deactivate UI
```

#### CU-R26: Asignar Repartidor

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as DeliveryService
    participant RP as DeliveryRepository
    participant CR as CourierRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant NS as NotificationService
    participant ES as External Services

    Usuario->>UI: Accede al panel de control de delivery
    activate UI
    
    UI->>GE: dispatch(loadPendingDeliveryOrders())
    activate GE
    GE->>SA: getPendingDeliveries()
    activate SA
    SA->>AC: GET /api/delivery/orders/pending
    activate AC
    AC->>SV: obtenerPedidosPendientesAsignacion()
    activate SV
    SV->>RP: findPendingAssignment()
    activate RP
    RP->>ORM: DeliveryPedido.objects.filter(repartidor_id=None, estado='listo')
    activate ORM
    ORM->>BD: SELECT FROM delivery_pedido WHERE repartidor_id IS NULL AND estado='listo'
    activate BD
    BD-->>ORM: Pedidos pendientes
    deactivate BD
    ORM-->>RP: Lista pedidos
    deactivate ORM
    RP-->>SV: Lista DeliveryPedidoDTO
    deactivate RP
    SV-->>AC: PedidosPendientesDTO
    deactivate SV
    
    AC->>SZ: PendingDeliveryOrdersSerializer(pedidos)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Pedidos pendientes
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Muestra lista de pedidos listos para asignación
    
    Usuario->>UI: Selecciona un pedido específico
    UI->>GE: dispatch(getAvailableCouriers())
    activate GE
    GE->>SA: getAvailableCouriers()
    activate SA
    SA->>AC: GET /api/delivery/couriers/available
    activate AC
    AC->>SV: obtenerRepartidoresDisponibles()
    activate SV
    SV->>CR: findAvailableCouriers()
    activate CR
    CR->>ORM: DeliveryRepartidor.objects.filter(estado='disponible')
    activate ORM
    ORM->>BD: SELECT FROM delivery_repartidor WHERE estado='disponible'
    activate BD
    BD-->>ORM: Repartidores disponibles
    deactivate BD
    ORM-->>CR: Lista de repartidores
    deactivate ORM
    CR-->>SV: Lista RepartidorDTO
    deactivate CR
    
    alt Integración con app externa
        SV->>ES: getExternalCouriers()
        activate ES
        ES-->>SV: Repartidores externos
        deactivate ES
    end
    
    SV-->>AC: RepartidoresDisponiblesDTO
    deactivate SV
    
    AC->>SZ: AvailableCouriersSerializer(repartidores)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Repartidores disponibles
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Muestra lista de repartidores disponibles
    
    alt Asignación sugerida
        UI->>UI: Sugiere repartidor óptimo basado en proximidad
    end
    
    Usuario->>UI: Selecciona un repartidor
    Usuario->>UI: Confirma asignación
    
    UI->>GE: dispatch(assignCourier(orderId, courierId))
    activate GE
    GE->>SA: postCourierAssignment(orderId, courierId)
    activate SA
    SA->>AC: POST /api/delivery/orders/{id}/assign
    activate AC
    AC->>SZ: CourierAssignmentSerializer(data)
    activate SZ
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: asignarRepartidor(pedidoId, repartidorId)
    activate SV
    SV->>RP: assignCourier(pedidoId, repartidorId)
    activate RP
    RP->>ORM: transaction.atomic()
    activate ORM
    ORM->>BD: UPDATE delivery_pedido SET repartidor_id=..., estado='en_ruta', hora_salida=NOW() WHERE id=...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    
    ORM->>BD: UPDATE delivery_repartidor SET estado='en_ruta', pedido_actual=... WHERE id=...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    ORM-->>RP: Confirmación
    deactivate ORM
    RP-->>SV: Asignación exitosa
    deactivate RP
    
    alt Repartidor externo
        SV->>ES: notifyExternalAssignment(pedidoId, externalCourierId)
        activate ES
        ES-->>SV: Confirmación
        deactivate ES
    end
    
    SV->>NS: notificarAsignacionRepartidor(pedidoId, repartidorId)
    activate NS
    NS->>NS: enviarNotificacionRepartidor()
    NS->>NS: actualizarPanelGestion()
    NS-->>SV: Notificaciones enviadas
    deactivate NS
    
    SV-->>AC: AsignacionRepartidorDTO
    deactivate SV
    
    AC->>SZ: CourierAssignmentResponseSerializer(data)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Asignación completada
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Actualiza panel con nuevo estado del pedido
    UI->>Usuario: Muestra confirmación de asignación
    
    alt Sistema con seguimiento GPS
        UI->>UI: Habilita opción de seguimiento en mapa
    end
    
    deactivate UI
```

#### CU-R27: Seguir Estado de Entrega

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/ME)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as DeliveryService
    participant RP as DeliveryRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant WS as WebSocket Service
    participant ES as External Services
    participant MS as Map Service

    Usuario->>UI: Accede a "Seguimiento de Delivery"
    activate UI
    
    UI->>GE: dispatch(loadActiveDeliveries())
    activate GE
    GE->>SA: getActiveDeliveries()
    activate SA
    SA->>AC: GET /api/delivery/orders/active
    activate AC
    AC->>SV: obtenerPedidosDeliveryActivos()
    activate SV
    SV->>RP: findActiveDeliveries()
    activate RP
    RP->>ORM: DeliveryPedido.objects.filter(estado__in=['preparacion', 'listo', 'en_ruta'])
    activate ORM
    ORM->>BD: SELECT FROM delivery_pedido WHERE estado IN...
    activate BD
    BD-->>ORM: Pedidos activos
    deactivate BD
    ORM-->>RP: Lista de pedidos
    deactivate ORM
    RP-->>SV: Lista DeliveryPedidoDTO
    deactivate RP
    
    alt Integración con apps externas
        SV->>ES: getExternalOrdersStatus()
        activate ES
        ES-->>SV: Estados actualizados
        deactivate ES
    end
    
    SV-->>AC: PedidosActivosDTO
    deactivate SV
    
    AC->>SZ: ActiveDeliveryOrdersSerializer(pedidos)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Pedidos activos
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Conecta a WebSocket para actualizaciones en tiempo real
    UI->>WS: connect()
    activate WS
    WS-->>UI: Conexión establecida
    deactivate WS
    
    UI->>UI: Inicializa mapa para seguimiento
    UI->>MS: initMap()
    activate MS
    MS-->>UI: Mapa inicializado
    deactivate MS
    
    UI->>UI: Organiza pedidos por estados y tiempos
    UI->>Usuario: Muestra panel de seguimiento con pedidos activos
    
    alt Usuario selecciona pedido específico
        Usuario->>UI: Selecciona un pedido para detalles
        UI->>GE: dispatch(getDeliveryDetails(id))
        activate GE
        GE->>SA: getDeliveryDetails(id)
        activate SA
        SA->>AC: GET /api/delivery/orders/{id}
        activate AC
        AC->>SV: obtenerDetallesPedidoDelivery(id)
        activate SV
        SV->>RP: findDetailedById(id)
        activate RP
        RP->>ORM: Queries para obtener detalles completos
        activate ORM
        ORM->>BD: Múltiples consultas JOIN
        activate BD
        BD-->>ORM: Datos detallados
        deactivate BD
        ORM-->>RP: Pedido con detalles
        deactivate ORM
        RP-->>SV: DeliveryPedidoDetalladoDTO
        deactivate RP
        SV-->>AC: DetallesPedidoDTO
        deactivate SV
        
        AC->>SZ: DeliveryOrderDetailSerializer(pedido)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Detalles del pedido
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        
        UI->>MS: centerMapOn(coordinates)
        activate MS
        MS-->>UI: Mapa centrado
        deactivate MS
        
        UI->>Usuario: Muestra detalles completos y ruta en mapa
    end
    
    alt Usuario contacta al repartidor
        Usuario->>UI: Selecciona "Contactar repartidor"
        UI->>NS: sendCourierMessage(courierId, message)
        activate NS
        NS-->>UI: Mensaje enviado
        deactivate NS
    end
    
    alt Actualización automática (WebSocket)
        WS->>UI: event('delivery_status_update', data)
        activate WS
        UI->>UI: Actualiza estado del pedido
        UI->>MS: updateCourierPosition(coordinates)
        activate MS
        MS-->>UI: Posición actualizada en mapa
        deactivate MS
        UI->>UI: Actualiza tiempo estimado y distancia
        UI->>Usuario: Muestra actualización visual
        deactivate WS
    end
    
    alt Pedido entregado (WebSocket)
        WS->>UI: event('delivery_completed', data)
        activate WS
        UI->>UI: Marca pedido como entregado
        UI->>UI: Muestra tiempo total de entrega
        UI->>Usuario: Muestra confirmación de entrega
        deactivate WS
    end
    
    alt Problema de entrega
        WS->>UI: event('delivery_issue', data)
        activate WS
        UI->>UI: Muestra alerta de problema
        UI->>Usuario: Notifica sobre incidencia con detalles
        deactivate WS
        
        Usuario->>UI: Toma acción (contactar cliente, reasignar, etc.)
        UI->>GE: dispatch(resolveDeliveryIssue(id, resolution))
        activate GE
        // ... (lógica de resolución de problemas) ...
        GE->>UI: Actualiza estado
        deactivate GE
    end
    
    deactivate UI
```