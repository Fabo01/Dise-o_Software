
#### CU-R06: Agregar Ingrediente

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as IngredientService
    participant RP as IngredientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    
    Usuario->>UI: Selecciona "Agregar ingrediente"
    activate UI
    UI->>UI: Muestra formulario
    
    Usuario->>UI: Ingresa datos del ingrediente
    UI->>UI: Validación en tiempo real
    
    alt Datos válidos
        UI->>GE: dispatch(createIngredient(datos))
        activate GE
        GE->>SA: postIngredient(datos)
        activate SA
        SA->>AC: POST /api/ingredients
        activate AC
        AC->>SZ: IngredientSerializer(data)
        activate SZ
        SZ->>SZ: Validar datos
        SZ-->>AC: Datos validados
        deactivate SZ
        
        AC->>SV: crearIngrediente(datos)
        activate SV
        SV->>SV: validarDatos(datos)
        SV->>RP: add(ingredienteEntity)
        activate RP
        RP->>ORM: Ingrediente.objects.create()
        activate ORM
        ORM->>BD: INSERT INTO ingrediente...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
        ORM-->>RP: Ingrediente creado
        deactivate ORM
        RP-->>SV: Ingrediente creado
        deactivate RP
        
        SV->>SV: registrarMovimientoStock('entrada_inicial', datos.cantidad)
        SV-->>AC: IngredienteDTO
        deactivate SV
        
        AC->>SZ: IngredientSerializer(ingrediente)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 201 Created
        deactivate AC
        SA-->>GE: Ingrediente creado
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Notificación de éxito
    else Datos inválidos
        UI->>Usuario: Muestra errores en tiempo real
    end
    deactivate UI
```

#### CU-R07: Editar Ingrediente

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/Cocina)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as IngredientService
    participant RP as IngredientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    
    Usuario->>UI: Busca y selecciona ingrediente
    activate UI
    UI->>GE: dispatch(getIngredientDetails(id))
    activate GE
    GE->>SA: getIngredient(id)
    activate SA
    SA->>AC: GET /api/ingredients/{id}
    activate AC
    AC->>SV: obtenerIngrediente(id)
    activate SV
    SV->>RP: findById(id)
    activate RP
    RP->>ORM: Ingrediente.objects.get(id=id)
    activate ORM
    ORM->>BD: SELECT FROM ingrediente WHERE id=...
    activate BD
    BD-->>ORM: Datos del ingrediente
    deactivate BD
    ORM-->>RP: Ingrediente
    deactivate ORM
    RP-->>SV: IngredienteDTO
    deactivate RP
    SV-->>AC: IngredienteDTO
    deactivate SV
    
    AC->>SZ: IngredientSerializer(ingrediente)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Detalles del ingrediente
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Muestra formulario con datos existentes
    Usuario->>UI: Modifica información
    UI->>UI: Validación en tiempo real
    
    alt Datos válidos
        UI->>GE: dispatch(updateIngredient(id, datos))
        activate GE
        GE->>SA: putIngredient(id, datos)
        activate SA
        SA->>AC: PUT /api/ingredients/{id}
        activate AC
        AC->>SZ: IngredientSerializer(ingrediente, data)
        activate SZ
        SZ->>SZ: Validar datos
        SZ-->>AC: Datos validados
        deactivate SZ
        
        AC->>SV: actualizarIngrediente(id, datos)
        activate SV
        SV->>SV: validarDatos(datos)
        SV->>RP: update(id, ingredienteEntity)
        activate RP
        RP->>ORM: Ingrediente.objects.filter(id=id).update()
        activate ORM
        ORM->>BD: UPDATE ingrediente SET...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
        ORM-->>RP: Confirmación
        deactivate ORM
        RP-->>SV: Éxito
        deactivate RP
        
        SV->>SV: registrarHistorialCambio(id, 'actualización', datos)
        SV-->>AC: IngredienteDTO actualizado
        deactivate SV
        
        AC->>SZ: IngredientSerializer(ingrediente)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Ingrediente actualizado
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Notificación de éxito
    else Datos inválidos
        UI->>Usuario: Muestra errores en tiempo real
    end
    deactivate UI
```

#### CU-R08: Actualizar Stock

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/Cocina)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as InventoryService
    participant RP as IngredientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    participant NS as NotificationService
    
    Usuario->>UI: Busca y selecciona ingrediente
    activate UI
    Usuario->>UI: Selecciona "Actualizar stock"
    UI->>UI: Muestra formulario de actualización
    
    Usuario->>UI: Ingresa cantidad y motivo
    UI->>UI: Validación en tiempo real
    
    alt Datos válidos
        UI->>GE: dispatch(updateStock(id, {cantidad, motivo}))
        activate GE
        GE->>SA: patchIngredientStock(id, {cantidad, motivo})
        activate SA
        SA->>AC: PATCH /api/ingredients/{id}/stock
        activate AC
        AC->>SZ: StockUpdateSerializer(data)
        activate SZ
        SZ->>SZ: Validar datos
        SZ-->>AC: Datos validados
        deactivate SZ
        
        AC->>SV: actualizarStock(id, cantidad, motivo)
        activate SV
        
        SV->>RP: findById(id)
        activate RP
        RP->>ORM: Ingrediente.objects.get(id=id)
        activate ORM
        ORM->>BD: SELECT FROM ingrediente WHERE id=...
        activate BD
        BD-->>ORM: Datos del ingrediente
        deactivate BD
        ORM-->>RP: Ingrediente
        deactivate ORM
        RP-->>SV: IngredienteDTO
        deactivate RP
        
        SV->>SV: validarNuevaCantidad(stockActual, cantidad)
        SV->>RP: updateStock(id, nuevaCantidad)
        activate RP
        RP->>ORM: transaction.atomic()
        activate ORM
        ORM->>BD: UPDATE ingrediente SET cantidad=... WHERE id=...
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
        
        ORM->>BD: INSERT INTO movimiento_stock (ingrediente_id, cantidad, tipo, motivo...)
        activate BD
        BD-->>ORM: Confirmación
        deactivate BD
        ORM-->>RP: Éxito
        deactivate ORM
        RP-->>SV: Éxito
        deactivate RP
        
        alt Stock bajo nivel crítico
            SV->>NS: notificarStockCritico(ingredienteDTO)
            activate NS
            NS->>NS: enviarAlertaStockCritico(ingredienteDTO)
            NS-->>SV: Alerta enviada
            deactivate NS
        end
        
        SV-->>AC: StockUpdateResultDTO
        deactivate SV
        
        AC->>SZ: StockUpdateResultSerializer(resultado)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Stock actualizado
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        
        UI->>Usuario: Notificación de éxito
    else Datos inválidos
        UI->>Usuario: Muestra errores en tiempo real
    end
    deactivate UI
```

#### CU-R09: Eliminar Ingrediente

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SV as IngredientService
    participant RP as IngredientRepository
    participant MR as MenuRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    
    Usuario->>UI: Selecciona ingrediente y "Eliminar"
    activate UI
    UI->>UI: Solicita confirmación
    Usuario->>UI: Confirma eliminación
    
    UI->>GE: dispatch(deleteIngredient(id))
    activate GE
    GE->>SA: deleteIngredient(id)
    activate SA
    SA->>AC: DELETE /api/ingredients/{id}
    activate AC
    
    AC->>SV: eliminarIngrediente(id)
    activate SV
    
    SV->>MR: findMenusUsingIngredient(id)
    activate MR
    MR->>ORM: MenuIngrediente.objects.filter(ingrediente_id=id).select_related('menu')
    activate ORM
    ORM->>BD: SELECT FROM menu_ingrediente JOIN menu... WHERE ingrediente_id=...
    activate BD
    BD-->>ORM: Menús asociados
    deactivate BD
    ORM-->>MR: Lista de menús
    deactivate ORM
    MR-->>SV: Lista de menús que usan el ingrediente
    deactivate MR
    
    alt Sin menús asociados o solo en menús inactivos
        SV->>RP: logicalDelete(id)
        activate RP
        RP->>ORM: Ingrediente.objects.filter(id=id).update(estado='eliminado')
        activate ORM
        ORM->>BD: UPDATE ingrediente SET estado='eliminado' WHERE id=...
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
        SA-->>GE: Ingrediente eliminado
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Notificación de éxito
    else Con menús activos asociados
        SV-->>AC: Error: Ingrediente en uso en menús activos
        deactivate SV
        
        AC-->>SA: Response 400 Bad Request
        deactivate AC
        SA-->>GE: Error con detalles
        deactivate SA
        GE->>UI: Actualiza estado con error
        deactivate GE
        UI->>Usuario: Muestra error y lista de menús afectados
    end
    deactivate UI
```

#### CU-R10: Verificar Disponibilidad de Ingredientes

```mermaid
sequenceDiagram
    actor Usuario as Usuario (JL/JT/Cocina)
    participant UI as Frontend UI
    participant GE as Gestión Estado
    participant SA as Servicios API
    participant AC as API Controller
    participant SZ as Serializer
    participant SV as InventoryService
    participant RP as IngredientRepository
    participant ORM as ORM Django
    participant BD as Base de Datos
    
    Usuario->>UI: Accede a "Inventario"
    activate UI
    
    UI->>GE: dispatch(loadIngredientsStatus())
    activate GE
    GE->>SA: getIngredientsStatus()
    activate SA
    SA->>AC: GET /api/ingredients/status
    activate AC
    AC->>SV: verificarDisponibilidadIngredientes()
    activate SV
    SV->>RP: findAllWithStatus()
    activate RP
    RP->>ORM: Ingrediente.objects.all()
    activate ORM
    ORM->>BD: SELECT FROM ingrediente
    activate BD
    BD-->>ORM: Lista completa de ingredientes
    deactivate BD
    ORM-->>RP: Lista de ingredientes
    deactivate ORM
    RP-->>SV: Lista IngredienteDTO
    deactivate RP
    
    loop Por cada ingrediente
        SV->>SV: calcularEstadoDisponibilidad(ingrediente)
        SV->>SV: calcularTendenciaConsumo(ingrediente)
        SV->>SV: predecirFechaAgotamiento(ingrediente)
    end
    
    SV-->>AC: IngredientesStatusDTO
    deactivate SV
    
    AC->>SZ: IngredientStatusSerializer(data)
    activate SZ
    SZ-->>AC: JSON response
    deactivate SZ
    AC-->>SA: Response 200 OK
    deactivate AC
    SA-->>GE: Estado de ingredientes
    deactivate SA
    GE->>UI: Actualiza estado
    deactivate GE
    
    UI->>UI: Aplica códigos de color por estado
    UI->>Usuario: Muestra tablero con estado de ingredientes
    
    alt Filtrar vista
        Usuario->>UI: Selecciona filtros (categoría, estado)
        UI->>UI: Aplica filtros localmente
        UI->>Usuario: Muestra ingredientes filtrados
    end
    
    alt Ver detalles de ingrediente
        Usuario->>UI: Selecciona un ingrediente específico
        UI->>GE: dispatch(getIngredientDetails(id))
        activate GE
        GE->>SA: getIngredient(id)
        activate SA
        SA->>AC: GET /api/ingredients/{id}
        activate AC
        AC->>SV: obtenerDetallesIngrediente(id)
        activate SV
        SV->>RP: findByIdWithHistory(id)
        activate RP
        RP->>ORM: Queries para obtener detalles e historial
        activate ORM
        ORM->>BD: Múltiples consultas
        activate BD
        BD-->>ORM: Datos detallados
        deactivate BD
        ORM-->>RP: Datos completos
        deactivate ORM
        RP-->>SV: DetalleIngredienteDTO
        deactivate RP
        SV-->>AC: DetalleIngredienteDTO
        deactivate SV
        
        AC->>SZ: IngredientDetailSerializer(detalle)
        activate SZ
        SZ-->>AC: JSON response
        deactivate SZ
        AC-->>SA: Response 200 OK
        deactivate AC
        SA-->>GE: Detalles completos
        deactivate SA
        GE->>UI: Actualiza estado
        deactivate GE
        UI->>Usuario: Muestra detalles y tendencias de uso
    end
    deactivate UI
```