
#### CU-R11: Crear Menú

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as MenuService
    participant RP as MenuRepository
    participant IRP as IngredientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos

    Usuario->>UI: Selecciona "Crear nuevo menú"
    activate UI
    UI->>UI: Muestra formulario de creación
    
    Usuario->>UI: Ingresa información básica del menú
    UI->>UI: Valida información en tiempo real
    
    Usuario->>UI: Avanza a selección de ingredientes
    UI->>GE: dispatch(loadIngredients())
    activate GE
    GE->>SA: getIngredients()
    activate SA
    SA->>AC: GET /api/ingredients
    activate AC
    AC->>SV: obtenerIngredientesDisponibles()
    activate SV
    SV->>IRP: findAvailable()
    activate IRP
    IRP->>ORM: Ingrediente.objects.filter(estado='disponible')
    activate ORM
    ORM->>BD: SELECT FROM ingrediente WHERE estado='disponible'
    activate BD
    BD-->>ORM: Lista de ingredientes
    deactivate BD
    ORM-->>IRP: Ingredientes disponibles
    deactivate ORM
    IRP-->>SV: Lista IngredienteDTO
    deactivate IRP
    SV-->>AC: Lista IngredienteDTO
    deactivate SV
    
    AC->>SZ: IngredientListSerializer(ingredientes)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Lista de ingredientes
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>Usuario: Muestra lista de ingredientes disponibles
    
    Usuario->>UI: Selecciona ingredientes y cantidades
    UI->>UI: Calcula costos y márgenes en tiempo real
    
    Usuario->>UI: Finaliza creación del menú
    UI->>GE: dispatch(createMenu(menuData))
    activate GE
    GE->>SA: postMenu(menuData)
    activate SA
    SA->>AC: POST /api/menus
    activate AC
    AC->>SZ: MenuCreateSerializer(data)
    activate SZ
    SZ->>SZ: Validar datos
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: crearMenu(menuData)
    activate SV
    SV->>SV: calcularCosto(ingredientes)
    SV->>SV: verificarMargen(precio, costo)
    SV->>RP: save(menuEntity)
    activate RP
    RP->>ORM: transaction.atomic()
    activate ORM
    ORM->>BD: INSERT INTO menu...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    
    loop Para cada ingrediente
        ORM->>BD: INSERT INTO menu_ingrediente...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
    end
    
    ORM-->>RP: Menú creado
    deactivate ORM
    RP-->>SV: MenuDTO
    deactivate RP
    SV-->>AC: MenuDTO
    deactivate SV
    
    AC->>SZ: MenuSerializer(menu)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 201 Created
    deactivate AC
    SA-->>GE: Menú creado
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    UI->>Usuario: Notificación de éxito
    deactivate UI
```

#### CU-R12: Editar Menú

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as MenuService
    participant RP as MenuRepository
    participant ORM as ORM Django
    participant BD as Base de Datos

    Usuario->>UI: Busca y selecciona menú
    activate UI
    UI->>GE: dispatch(getMenuDetails(id))
    activate GE
    GE->>SA: getMenu(id)
    activate SA
    SA->>AC: GET /api/menus/{id}
    activate AC
    AC->>SV: obtenerMenu(id)
    activate SV
    SV->>RP: findById(id, {withIngredients: true})
    activate RP
    RP->>ORM: Menu.objects.get(id=id)
    activate ORM
    ORM->>BD: SELECT FROM menu WHERE id=...
    activate BD
    BD-->>ORM: Datos del menú
    deactivate BD
    
    ORM->>BD: SELECT FROM menu_ingrediente WHERE menu_id=...
    activate BD
    BD-->>ORM: Ingredientes del menú
    deactivate BD
    ORM-->>RP: Menú completo con ingredientes
    deactivate ORM
    RP-->>SV: MenuDTO
    deactivate RP
    SV-->>AC: MenuDTO
    deactivate SV
    
    AC->>SZ: MenuDetailSerializer(menu)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Detalles del menú
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Muestra formulario con datos actuales
    UI->>Usuario: Presenta formulario editable
    
    Usuario->>UI: Modifica información del menú
    Usuario->>UI: Actualiza lista de ingredientes
    UI->>UI: Recalcula costos y márgenes
    
    Usuario->>UI: Confirma cambios
    UI->>GE: dispatch(updateMenu(id, menuData))
    activate GE
    GE->>SA: putMenu(id, menuData)
    activate SA
    SA->>AC: PUT /api/menus/{id}
    activate AC
    AC->>SZ: MenuUpdateSerializer(menu, data)
    activate SZ
    SZ->>SZ: Validar datos
    SZ-->>AC: Datos validados
    deactivate SZ
    
    AC->>SV: actualizarMenu(id, menuData)
    activate SV
    SV->>SV: recalcularCosto(ingredientes)
    SV->>RP: update(id, menuEntity)
    activate RP
    RP->>ORM: transaction.atomic()
    activate ORM
    ORM->>BD: UPDATE menu SET... WHERE id=...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    
    ORM->>BD: DELETE FROM menu_ingrediente WHERE menu_id=...
    activate BD
    BD-->>ORM: Confirmación
    deactivate BD
    
    loop Para cada ingrediente
        ORM->>BD: INSERT INTO menu_ingrediente...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
    end
    
    ORM-->>RP: Menú actualizado
    deactivate ORM
    RP-->>SV: MenuDTO
    deactivate RP
    
    SV->>SV: verificarDisponibilidadMenus()
    SV-->>AC: MenuDTO actualizado
    deactivate SV
    
    AC->>SZ: MenuSerializer(menu)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Menú actualizado
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    UI->>Usuario: Notificación de éxito
    deactivate UI
```

#### CU-R13: Eliminar Menú

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SV as MenuService
    participant RP as MenuRepository
    participant PRP as PedidoRepository
    participant ORM as ORM Django
    participant BD as Base de Datos

    Usuario->>UI: Selecciona menú y elige "Eliminar"
    activate UI
    UI->>UI: Solicita confirmación
    Usuario->>UI: Confirma eliminación
    
    UI->>GE: dispatch(deleteMenu(id))
    activate GE
    GE->>SA: deleteMenu(id)
    activate SA
    SA->>AC: DELETE /api/menus/{id}
    activate AC
    
    AC->>SV: eliminarMenu(id)
    activate SV
    
    SV->>PRP: findPendingOrdersWithMenu(id)
    activate PRP
    PRP->>ORM: Queries para buscar pedidos activos con el menú
    activate ORM
    ORM->>BD: SELECT FROM pedido JOIN item_pedido ON... WHERE menu_id=... AND estado IN...
    activate BD
    BD-->>ORM: Pedidos activos
    deactivate BD
    ORM-->>PRP: Lista de pedidos
    deactivate ORM
    PRP-->>SV: PedidosDTO activos
    deactivate PRP
    
    alt Sin pedidos activos
        SV->>RP: logicalDelete(id)
        activate RP
        RP->>ORM: Menu.objects.filter(id=id).update(estado='eliminado')
        activate ORM
        ORM->>BD: UPDATE menu SET estado='eliminado' WHERE id=...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
        ORM-->>RP: Confirmación
        deactivate ORM
        RP-->>SV: Éxito
        deactivate RP
        
        SV->>SV: registrarHistorialCambio(id, 'eliminación')
        SV-->>AC: Éxito
        deactivate SV
        
        AC-->>SA: Response 204 No Content
        deactivate AC
        SA-->>GE: Menú eliminado
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Notificación de éxito
    else Con pedidos activos
        SV-->>AC: Error: Menú en uso en pedidos activos
        deactivate SV
        
        AC-->>SA: Response 400 Bad Request
        deactivate AC
        SA-->>GE: Error con detalles
        deactivate SA
        GE->>UI: Actualiza estado con error
        deactivate GE
        UI->>Usuario: Muestra error y lista de pedidos afectados
    end
    deactivate UI
```

#### CU-R14: Verificar Disponibilidad de Menú

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/Cocina)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as MenuService
    participant RP as MenuRepository
    participant IRP as IngredientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos

    Usuario->>UI: Accede a "Verificar disponibilidad"
    activate UI
    
    UI->>GE: dispatch(checkMenusAvailability())
    activate GE
    GE->>SA: getMenusAvailability()
    activate SA
    SA->>AC: GET /api/menus/availability
    activate AC
    AC->>SV: verificarDisponibilidadMenus()
    activate SV
    
    SV->>RP: findAllWithIngredients()
    activate RP
    RP->>ORM: Queries para obtener menús con ingredientes
    activate ORM
    ORM->>BD: SELECT... JOIN... (menús con ingredientes)
    activate BD
    BD-->>ORM: Menús con ingredientes
    deactivate BD
    ORM-->>RP: Lista de menús
    deactivate ORM
    RP-->>SV: Lista MenuDTO
    deactivate RP
    
    SV->>IRP: getIngredientsStock()
    activate IRP
    IRP->>ORM: Ingrediente.objects.all()
    activate ORM
    ORM->>BD: SELECT FROM ingrediente
    activate BD
    BD-->>ORM: Todos los ingredientes
    deactivate BD
    ORM-->>IRP: Lista de ingredientes
    deactivate ORM
    IRP-->>SV: Stock actual de ingredientes
    deactivate IRP
    
    loop Para cada menú
        SV->>SV: verificarIngredientesDisponibles(menu, stockActual)
        SV->>SV: calcularMaximasPorciones(menu, stockActual)
        SV->>SV: asignarEstadoDisponibilidad(menu, porciones)
    end
    
    SV-->>AC: MenusDisponibilidadDTO
    deactivate SV
    
    AC->>SZ: MenuAvailabilitySerializer(result)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Estado de disponibilidad
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Aplica códigos de color por disponibilidad
    UI->>Usuario: Muestra menús con indicadores visuales
    
    alt Ver detalles de un menú específico
        Usuario->>UI: Selecciona un menú
        UI->>GE: dispatch(getMenuAvailabilityDetails(id))
        activate GE
        GE->>SA: getMenuAvailabilityDetails(id)
        activate SA
        SA->>AC: GET /api/menus/{id}/availability
        activate AC
        AC->>SV: obtenerDetallesDisponibilidad(id)
        activate SV
        
        SV->>RP: findById(id)
        activate RP
        RP->>ORM: Menu.objects.get(id=id)...
        activate ORM
        ORM->>BD: Queries para menú y sus ingredientes
        activate BD
        BD-->>ORM: Datos detallados
        deactivate BD
        ORM-->>RP: Menú con ingredientes
        deactivate ORM
        RP-->>SV: MenuDTO
        deactivate RP
        
        SV->>IRP: getIngredientsForMenu(id)
        activate IRP
        IRP->>ORM: Queries para stock de ingredientes
        activate ORM
        ORM->>BD: SELECT... (stock de ingredientes del menú)
        activate BD
        BD-->>ORM: Stock de ingredientes
        deactivate BD
        ORM-->>IRP: Detalles de stock
        deactivate ORM
        IRP-->>SV: Stock actual
        deactivate IRP
        
        SV->>SV: analizarLimitacionesStock(menu, stock)
        SV-->>AC: MenuDisponibilidadDetalleDTO
        deactivate SV
        
        AC->>SZ: MenuAvailabilityDetailSerializer(data)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Detalles de disponibilidad
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Muestra detalles de limitaciones
    end
    
    alt Marcar como no disponible temporalmente
        Usuario->>UI: Marca menú como "no disponible temporalmente"
        UI->>GE: dispatch(setMenuTemporaryStatus(id, false))
        activate GE
        GE->>SA: patchMenuStatus(id, {disponible: false})
        activate SA
        SA->>AC: PATCH /api/menus/{id}/status
        activate AC
        AC->>SV: cambiarDisponibilidadTemporal(id, false)
        activate SV
        
        SV->>RP: updateStatus(id, false)
        activate RP
        RP->>ORM: Menu.objects.filter(id=id).update(disponible=False)
        activate ORM
        ORM->>BD: UPDATE menu SET disponible=FALSE WHERE id=...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
        ORM-->>RP: Confirmación
        deactivate ORM
        RP-->>SV: Éxito
        deactivate RP
        
        SV->>SV: registrarCambioEstado(id, 'no disponible manual')
        SV-->>AC: Éxito
        deactivate SV
        
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Estado actualizado
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Muestra confirmación
    end
    deactivate UI
```

#### CU-R15: Ver Menús Disponibles

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/ME/Cocina)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as MenuService
    participant RP as MenuRepository
    participant ORM as ORM Django
    participant BD as Base de Datos

    Usuario->>UI: Accede a "Menús disponibles"
    activate UI
    
    UI->>GE: dispatch(loadAvailableMenus())
    activate GE
    GE->>SA: getAvailableMenus()
    activate SA
    SA->>AC: GET /api/menus/available
    activate AC
    AC->>SV: obtenerMenusDisponibles()
    activate SV
    
    SV->>RP: findAvailableWithDetails()
    activate RP
    RP->>ORM: Queries para menús disponibles
    activate ORM
    ORM->>BD: SELECT FROM menus WHERE disponible=TRUE...
    activate BD
    BD-->>ORM: Menús disponibles
    deactivate BD
    ORM-->>RP: Lista filtrada
    deactivate ORM
    RP-->>SV: Lista MenuDTO
    deactivate RP
    
    SV->>SV: verificarDisponibilidadReal(menus)
    SV->>SV: clasificarPorDisponibilidad(menus)
    SV-->>AC: MenusDisponiblesDTO categorizado
    deactivate SV
    
    AC->>SZ: AvailableMenusSerializer(data)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Menús categorizados
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Organiza por categorías con códigos de colores
    UI->>Usuario: Muestra tablero de menús disponibles
    
    alt Filtrar vista
        Usuario->>UI: Selecciona filtros (categoría, popularidad)
        UI->>UI: Aplica filtros a la vista
        UI->>Usuario: Muestra resultados filtrados
    end
    
    alt Usuario es Mesero con dispositivo móvil
        Usuario->>UI: Accede desde vista móvil optimizada
        UI->>UI: Ajusta visualización para móvil
        UI->>Usuario: Muestra versión optimizada para atención en mesa
    end
    
    alt Ver alternativas para menú no disponible
        Usuario->>UI: Selecciona menú no disponible
        UI->>GE: dispatch(getMenuAlternatives(id))
        activate GE
        GE->>SA: getMenuAlternatives(id)
        activate SA
        SA->>AC: GET /api/menus/{id}/alternatives
        activate AC
        AC->>SV: buscarAlternativasSimilares(id)
        activate SV
        
        SV->>RP: findSimilarMenus(id)
        activate RP
        RP->>ORM: Queries para menús similares disponibles
        activate ORM
        ORM->>BD: Consultas complejas para similitud
        activate BD
        BD-->>ORM: Menús alternativos
        deactivate BD
        ORM-->>RP: Alternativas
        deactivate ORM
        RP-->>SV: Lista alternativas
        deactivate RP
        
        SV-->>AC: MenusAlternativosDTO
        deactivate SV
        AC->>SZ: MenuAlternativesSerializer(data)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Alternativas disponibles
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Muestra sugerencias alternativas
    end
    deactivate UI
```
