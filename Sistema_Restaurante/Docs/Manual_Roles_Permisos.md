# Documentación de Roles y Permisos - Sistema de Gestión de Restaurante
# S3-39: Documentación específica por rol

## 📋 Índice

1. [Introducción](#introducción)
2. [Matriz de Roles y Permisos](#matriz-de-roles-y-permisos)
3. [Administrador General](#administrador-general)
4. [Gerente de Operaciones](#gerente-de-operaciones)
5. [Supervisor de Turno](#supervisor-de-turno)
6. [Cajero/Mesero](#cajero-mesero)
7. [Chef/Cocina](#chef-cocina)
8. [Repartidor](#repartidor)
9. [Personal de Inventario](#personal-de-inventario)
10. [Auditor/Contador](#auditor-contador)

---

## 🎯 Introducción

Este documento define los roles específicos dentro del Sistema de Gestión de Restaurante, sus responsabilidades, permisos y las funcionalidades a las que cada rol tiene acceso. El sistema implementa un control de acceso basado en roles (RBAC) para garantizar la seguridad y la separación adecuada de funciones.

### Principios de Seguridad

- **Mínimo Privilegio**: Cada usuario tiene solo los permisos necesarios para su función
- **Separación de Funciones**: Funciones críticas requieren múltiples autorizaciones
- **Auditoría**: Todas las acciones son registradas con el usuario responsable
- **Revisión Periódica**: Los permisos se revisan y actualizan regularmente

---

## 📊 Matriz de Roles y Permisos

| Funcionalidad | Admin | Gerente | Supervisor | Cajero | Chef | Repartidor | Inventario | Auditor |
|---------------|-------|---------|------------|--------|------|------------|------------|---------|
| **Gestión de Usuarios** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 👁️ |
| **Configuración Sistema** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 👁️ |
| **Gestión Clientes** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | 👁️ |
| **Gestión Menús** | ✅ | ✅ | ✅ | 👁️ | ✅ | ❌ | ❌ | 👁️ |
| **Gestión Pedidos** | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ | ❌ | 👁️ |
| **Gestión Inventario** | ✅ | ✅ | ✅ | ❌ | 👁️ | ❌ | ✅ | 👁️ |
| **Gestión Pagos** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | 👁️ |
| **Gestión Delivery** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | 👁️ |
| **Reportes Financieros** | ✅ | ✅ | 👁️ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Analytics Avanzados** | ✅ | ✅ | 👁️ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Backup/Restauración** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Leyenda:**
- ✅ **Acceso Completo**: Crear, leer, actualizar, eliminar
- 👁️ **Solo Lectura**: Consultar información sin modificar
- ❌ **Sin Acceso**: No puede acceder a esta funcionalidad

---

## 👨‍💼 Administrador General

### Descripción del Rol
El Administrador General tiene acceso completo al sistema y es responsable de la configuración, mantenimiento y supervisión general de la plataforma.

### Responsabilidades Principales
- **Gestión del Sistema**: Configuración, mantenimiento y actualizaciones
- **Gestión de Usuarios**: Crear, modificar y desactivar cuentas de usuario
- **Supervisión General**: Monitoreo de todas las operaciones del restaurante
- **Seguridad**: Gestión de permisos y auditoría de accesos
- **Backup y Recuperación**: Administración de respaldos del sistema

### Permisos Específicos

#### ✅ Gestión de Usuarios
```
• Crear nuevos usuarios y asignar roles
• Modificar permisos de usuarios existentes
• Activar/desactivar cuentas de usuario
• Resetear contraseñas
• Ver logs de auditoría de usuarios
```

#### ✅ Configuración del Sistema
```
• Modificar configuraciones generales
• Gestionar integraciones con servicios externos
• Configurar métodos de pago
• Establecer parámetros operacionales
• Gestionar zonas de delivery
```

#### ✅ Backup y Seguridad
```
• Ejecutar backups manuales
• Restaurar desde backups
• Revisar logs de seguridad
• Configurar alertas del sistema
• Gestionar certificados SSL
```

#### ✅ Acceso Total a Datos
```
• Ver todos los reportes financieros
• Acceder a analytics avanzados
• Exportar datos del sistema
• Modificar cualquier registro (con auditoría)
```

### Flujo de Trabajo Típico

1. **Inicio de Jornada**
   - Revisar alertas del sistema
   - Verificar respaldos automáticos
   - Revisar métricas generales de performance

2. **Durante el Día**
   - Monitorear operaciones en tiempo real
   - Gestionar solicitudes de soporte
   - Revisar reportes de errores

3. **Fin de Jornada**
   - Revisar resumen de ventas
   - Verificar integridad de datos
   - Programar tareas de mantenimiento

### Limitaciones y Controles
- Cambios críticos requieren confirmación adicional
- Eliminaciones importantes requieren justificación
- Todas las acciones son auditadas automáticamente

---

## 👨‍💼 Gerente de Operaciones

### Descripción del Rol
El Gerente de Operaciones supervisa las operaciones diarias del restaurante y tiene acceso a la mayoría de funcionalidades operacionales y reportes de gestión.

### Responsabilidades Principales
- **Supervisión Operacional**: Monitoreo de ventas, pedidos y performance
- **Gestión de Personal**: Coordinación de equipos de trabajo
- **Análisis de Negocio**: Revisión de métricas y KPIs
- **Optimización**: Mejora continua de procesos

### Permisos Específicos

#### ✅ Gestión Operacional Completa
```
• Gestionar todos los pedidos
• Supervisar inventario y stock
• Gestionar menús y precios
• Configurar promociones
• Gestionar clientes VIP
```

#### ✅ Reportes y Analytics
```
• Acceder a reportes de ventas
• Ver analytics de performance
• Generar reportes personalizados
• Exportar datos operacionales
• Ver tendencias y proyecciones
```

#### ✅ Gestión de Personal Operativo
```
• Crear cuentas para personal operativo
• Asignar turnos y responsabilidades
• Revisar performance del personal
• Gestionar permisos temporales
```

### Flujo de Trabajo Típico

1. **Inicio de Turno**
   - Revisar dashboard operacional
   - Verificar estado del inventario
   - Revisar programación de personal

2. **Durante Operaciones**
   - Monitorear flujo de pedidos
   - Supervisar tiempos de entrega
   - Gestionar situaciones especiales

3. **Cierre de Turno**
   - Revisar métricas del día
   - Generar reportes de cierre
   - Planificar el siguiente turno

### Limitaciones
- No puede modificar configuraciones críticas del sistema
- No puede crear usuarios administradores
- Cambios de precios requieren justificación

---

## 👨‍💼 Supervisor de Turno

### Descripción del Rol
El Supervisor de Turno coordina las operaciones durante su horario específico y actúa como punto de contacto principal para resolución de problemas operativos.

### Responsabilidades Principales
- **Coordinación de Turno**: Supervisión directa del personal del turno
- **Resolución de Problemas**: Gestión de incidencias operacionales
- **Control de Calidad**: Supervisión de estándares de servicio
- **Reporte de Supervisión**: Comunicación con gerencia

### Permisos Específicos

#### ✅ Gestión de Pedidos
```
• Ver y modificar todos los pedidos del turno
• Autorizar cancelaciones
• Gestionar pedidos especiales
• Resolver problemas con entregas
• Aplicar descuentos autorizados
```

#### ✅ Supervisión de Personal
```
• Ver performance del personal del turno
• Autorizar permisos temporales
• Gestionar asignaciones de tareas
• Reportar incidencias
```

#### ✅ Control de Inventario
```
• Actualizar stock durante el turno
• Reportar faltantes o sobrantes
• Autorizar uso de ingredientes alternativos
• Gestionar alertas de stock bajo
```

### Flujo de Trabajo Típico

1. **Inicio de Turno**
   - Revisar estado de pedidos pendientes
   - Verificar disponibilidad de personal
   - Revisar alertas de inventario

2. **Durante el Turno**
   - Monitorear flujo de pedidos
   - Resolver problemas operativos
   - Coordinar con cocina y delivery

3. **Cierre de Turno**
   - Generar reporte de turno
   - Documentar incidencias
   - Preparar información para siguiente turno

### Limitaciones
- No puede modificar precios permanentemente
- No puede crear nuevos usuarios
- Reportes limitados a su turno específico

---

## 💰 Cajero/Mesero

### Descripción del Rol
El Cajero/Mesero gestiona la atención directa al cliente, procesamiento de pedidos y cobros, siendo el punto de contacto principal con los clientes.

### Responsabilidades Principales
- **Atención al Cliente**: Interacción directa con clientes
- **Procesamiento de Pedidos**: Toma y gestión de pedidos
- **Gestión de Pagos**: Procesamiento de transacciones
- **Servicio al Cliente**: Resolución de consultas básicas

### Permisos Específicos

#### ✅ Gestión de Clientes
```
• Crear nuevos clientes
• Actualizar información básica de clientes
• Ver historial de pedidos de clientes
• Gestionar direcciones de entrega
```

#### ✅ Gestión de Pedidos
```
• Crear nuevos pedidos
• Modificar pedidos en estado pendiente
• Ver estado de pedidos
• Cancelar pedidos (con autorización)
• Generar tickets y facturas
```

#### ✅ Procesamiento de Pagos
```
• Procesar pagos en efectivo
• Procesar pagos con tarjeta
• Generar vuelto
• Imprimir comprobantes
• Procesar reembolsos menores
```

#### 👁️ Consultas (Solo Lectura)
```
• Ver menús disponibles
• Consultar precios actuales
• Ver promociones activas
• Verificar stock disponible
```

### Flujo de Trabajo Típico

1. **Atención al Cliente**
   - Recibir al cliente o atender llamada
   - Consultar menús disponibles
   - Asesorar sobre opciones

2. **Procesamiento del Pedido**
   - Registrar items del pedido
   - Confirmar datos del cliente
   - Calcular total y aplicar promociones

3. **Gestión del Pago**
   - Procesar el pago según método elegido
   - Generar comprobante
   - Coordinar con cocina para preparación

### Limitaciones
- No puede modificar precios
- No puede acceder a reportes financieros
- No puede gestionar inventario
- Cancelaciones requieren autorización de supervisor

---

## 👨‍🍳 Chef/Cocina

### Descripción del Rol
El personal de cocina gestiona la preparación de alimentos, actualización de estados de pedidos y comunicación sobre disponibilidad de menús.

### Responsabilidades Principales
- **Preparación de Alimentos**: Cocina según especificaciones del menú
- **Gestión de Tiempos**: Coordinación de tiempos de preparación
- **Control de Calidad**: Supervisión de estándares culinarios
- **Comunicación**: Reporte de disponibilidad y problemas

### Permisos Específicos

#### ✅ Gestión de Pedidos (Estados)
```
• Ver pedidos asignados a cocina
• Actualizar estado de pedidos (en preparación, listo)
• Reportar demoras o problemas
• Priorizar pedidos urgentes
```

#### ✅ Gestión de Menús
```
• Marcar menús como no disponibles temporalmente
• Reportar falta de ingredientes
• Sugerir sustituciones de ingredientes
• Actualizar tiempo estimado de preparación
```

#### 👁️ Consulta de Inventario
```
• Ver stock actual de ingredientes
• Consultar ingredientes próximos a vencer
• Ver alertas de stock bajo
• Verificar disponibilidad para menús
```

### Flujo de Trabajo Típico

1. **Inicio de Turno**
   - Revisar pedidos pendientes
   - Verificar stock de ingredientes críticos
   - Preparar estación de trabajo

2. **Durante la Preparación**
   - Actualizar estados de pedidos
   - Comunicar demoras si es necesario
   - Reportar problemas de stock

3. **Fin de Turno**
   - Reportar consumo de ingredientes
   - Documentar problemas encontrados
   - Limpiar y organizar área de trabajo

### Limitaciones
- No puede modificar precios o crear menús
- No puede acceder a información de clientes
- No puede procesar pagos
- Solo puede ver pedidos asignados a cocina

---

## 🚚 Repartidor

### Descripción del Rol
El Repartidor gestiona las entregas a domicilio, actualiza estados de delivery y mantiene comunicación con clientes durante el proceso de entrega.

### Responsabilidades Principales
- **Entregas a Domicilio**: Transporte de pedidos a clientes
- **Comunicación**: Contacto con clientes sobre entregas
- **Actualización de Estados**: Reporte de progreso de entregas
- **Gestión de Efectivo**: Manejo de pagos contra entrega

### Permisos Específicos

#### ✅ Gestión de Entregas
```
• Ver entregas asignadas
• Actualizar estado de entregas (en camino, entregado)
• Reportar problemas de entrega
• Confirmar entrega exitosa
• Gestionar devoluciones
```

#### ✅ Gestión de Pagos (Contra Entrega)
```
• Procesar pagos en efectivo
• Registrar pagos recibidos
• Calcular vuelto
• Reportar problemas de pago
```

#### 👁️ Información de Pedidos
```
• Ver detalles de pedidos a entregar
• Consultar información de contacto del cliente
• Ver dirección de entrega
• Consultar instrucciones especiales
```

### Flujo de Trabajo Típico

1. **Recepción de Entrega**
   - Revisar pedidos asignados
   - Verificar dirección y contacto
   - Recoger pedido de cocina

2. **Durante la Entrega**
   - Actualizar estado a "en camino"
   - Contactar cliente si es necesario
   - Navegar a dirección de entrega

3. **Entrega Completada**
   - Entregar pedido al cliente
   - Procesar pago si es contra entrega
   - Actualizar estado a "entregado"
   - Confirmar entrega en sistema

### Limitaciones
- Solo puede ver pedidos asignados específicamente
- No puede modificar información de pedidos
- No puede acceder a información financiera general
- No puede gestionar otros aspectos del sistema

---

## 📦 Personal de Inventario

### Descripción del Rol
El Personal de Inventario gestiona el stock de ingredientes, proveedores y el control de calidad de los insumos del restaurante.

### Responsabilidades Principales
- **Control de Stock**: Gestión de inventario de ingredientes
- **Recepción de Mercadería**: Validación y registro de compras
- **Control de Calidad**: Verificación de ingredientes
- **Reportes de Inventario**: Documentación de movimientos

### Permisos Específicos

#### ✅ Gestión Completa de Inventario
```
• Agregar nuevos ingredientes
• Actualizar stock y precios
• Registrar entradas de mercadería
• Gestionar proveedores
• Configurar alertas de stock
```

#### ✅ Control de Calidad
```
• Marcar ingredientes vencidos
• Reportar productos defectuosos
• Gestionar devoluciones a proveedores
• Registrar desperdicios
```

#### ✅ Reportes de Inventario
```
• Generar reportes de stock
• Ver consumo de ingredientes
• Calcular costos de inventario
• Exportar datos de inventario
```

#### 👁️ Consulta de Menús
```
• Ver qué menús usan cada ingrediente
• Consultar recetas y cantidades
• Ver impacto de faltantes en menús
```

### Flujo de Trabajo Típico

1. **Inicio de Jornada**
   - Revisar alertas de stock bajo
   - Verificar entregas programadas
   - Planificar actividades del día

2. **Gestión de Inventario**
   - Actualizar stock según entradas
   - Verificar calidad de productos
   - Registrar movimientos de inventario

3. **Reportes y Análisis**
   - Generar reportes de consumo
   - Identificar productos de rotación lenta
   - Planificar próximas compras

### Limitaciones
- No puede acceder a información financiera detallada
- No puede gestionar pedidos o clientes
- No puede modificar precios de menús
- Solo reportes relacionados con inventario

---

## 📊 Auditor/Contador

### Descripción del Rol
El Auditor/Contador tiene acceso de solo lectura a la mayoría del sistema para propósitos de auditoría, control financiero y cumplimiento normativo.

### Responsabilidades Principales
- **Auditoría Financiera**: Revisión de transacciones y reportes
- **Control de Cumplimiento**: Verificación de procesos y políticas
- **Análisis Financiero**: Evaluación de performance financiera
- **Reporte Ejecutivo**: Preparación de informes para dirección

### Permisos Específicos

#### 👁️ Acceso Total de Lectura
```
• Ver todos los reportes financieros
• Acceder a analytics completos
• Consultar registros de auditoría
• Ver todas las transacciones
• Revisar logs del sistema
```

#### ✅ Reportes Especializados
```
• Generar reportes de auditoría
• Exportar datos para análisis externo
• Crear reportes personalizados
• Programar reportes automáticos
```

#### ✅ Análisis Financiero
```
• Calcular márgenes de ganancia
• Analizar tendencias de ventas
• Evaluar performance por período
• Identificar anomalías financieras
```

### Flujo de Trabajo Típico

1. **Revisión Diaria**
   - Revisar transacciones del día
   - Verificar cuadre de caja
   - Identificar transacciones anómalas

2. **Análisis Semanal**
   - Generar reportes de performance
   - Analizar tendencias de ventas
   - Revisar costos operacionales

3. **Reportes Mensuales**
   - Preparar reportes ejecutivos
   - Realizar análisis de rentabilidad
   - Generar informes de cumplimiento

### Limitaciones
- **Solo Lectura**: No puede modificar ningún dato
- No puede procesar transacciones
- No puede gestionar operaciones diarias
- Acceso limitado a funciones administrativas

---

## 🔐 Gestión de Permisos en el Sistema

### Implementación Técnica

**Definición de Roles:**
```python
# Backend/Config/roles.py
ROLES = {
    'ADMIN': {
        'permissions': ['*'],  # Todos los permisos
        'description': 'Administrador General'
    },
    'GERENTE': {
        'permissions': [
            'view_all_reports',
            'manage_users_operational',
            'manage_menus',
            'manage_inventory',
            'manage_orders',
            'view_analytics'
        ],
        'description': 'Gerente de Operaciones'
    },
    'SUPERVISOR': {
        'permissions': [
            'manage_shift_orders',
            'update_inventory',
            'authorize_discounts',
            'view_shift_reports'
        ],
        'description': 'Supervisor de Turno'
    },
    # ... otros roles
}
```

### Asignación de Permisos

1. **Por Defecto**: Cada rol tiene permisos predeterminados
2. **Personalizada**: Se pueden agregar permisos específicos por usuario
3. **Temporal**: Permisos temporales para situaciones especiales
4. **Delegación**: Supervisores pueden delegar permisos limitados

### Auditoría de Accesos

Todas las acciones son registradas incluyendo:
- Usuario que realizó la acción
- Fecha y hora exacta
- Acción específica realizada
- Datos modificados (antes y después)
- IP de origen
- Justificación (cuando se requiere)

---

## 📞 Soporte por Rol

### Contactos Especializados

**Administradores y Gerentes:**
- 📧 **Email**: admin-support@restaurant-system.com
- ☎️ **Teléfono**: +56 2 1234 5678 (Ext. 1)

**Personal Operativo:**
- 📧 **Email**: operations-support@restaurant-system.com
- ☎️ **Teléfono**: +56 2 1234 5678 (Ext. 2)

**Soporte Técnico Urgente:**
- 📱 **WhatsApp**: +56 9 8765 4321
- 💬 **Chat**: Disponible 24/7 en la aplicación

### Escalación de Problemas

1. **Nivel 1**: Supervisor inmediato
2. **Nivel 2**: Gerente de operaciones
3. **Nivel 3**: Administrador del sistema
4. **Nivel 4**: Soporte técnico especializado

---

**Documento actualizado: [Fecha actual]**
**Versión: 1.0**
**Aprobado por: Gerencia General**
