# Manual de Usuario - Sistema de Gestión de Restaurante
# S3-36: Documentación para usuarios finales

## 📖 Índice

1. [Introducción](#introducción)
2. [Primeros Pasos](#primeros-pasos)
3. [Gestión de Clientes](#gestión-de-clientes)
4. [Gestión de Inventario](#gestión-de-inventario)
5. [Gestión de Menús](#gestión-de-menús)
6. [Gestión de Pedidos](#gestión-de-pedidos)
7. [Sistema de Delivery](#sistema-de-delivery)
8. [Sistema de Pagos](#sistema-de-pagos)
9. [Dashboard y Analytics](#dashboard-y-analytics)
10. [Preguntas Frecuentes](#preguntas-frecuentes)
11. [Soporte Técnico](#soporte-técnico)

---

## 🚀 Introducción

Bienvenido al Sistema de Gestión de Restaurante, una solución integral diseñada para optimizar todas las operaciones de su establecimiento gastronómico. Este sistema le permitirá gestionar clientes, inventario, menús, pedidos, entregas y pagos de manera eficiente y centralizada.

### Características Principales

- ✅ **Gestión de Clientes**: Base de datos completa de clientes con historial
- ✅ **Control de Inventario**: Seguimiento en tiempo real de ingredientes y stock
- ✅ **Menús Dinámicos**: Creación y gestión de menús con ingredientes
- ✅ **Pedidos Integrados**: Procesamiento completo de pedidos
- ✅ **Sistema de Delivery**: Gestión de entregas a domicilio
- ✅ **Pagos Seguros**: Múltiples métodos de pago
- ✅ **Analytics**: Reportes y métricas de negocio
- ✅ **Interfaz Intuitiva**: Diseño responsive y fácil de usar

---

## 🏁 Primeros Pasos

### Acceso al Sistema

1. **Ingrese a la aplicación** a través de su navegador web
2. **Inicie sesión** con sus credenciales proporcionadas por el administrador
3. **Familiarícese** con la interfaz principal

### Navegación Principal

La interfaz está organizada en las siguientes secciones:

```
┌─────────────────────────────────────────────────────────┐
│                    BARRA DE NAVEGACIÓN                  │
├─────────────┬─────────────┬─────────────┬─────────────┤
│  Clientes   │ Inventario  │   Menús     │   Pedidos   │
├─────────────┼─────────────┼─────────────┼─────────────┤
│  Delivery   │   Pagos     │ Analytics   │   Perfil    │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Dashboard Principal

Al ingresar, verá el dashboard con:
- **Resumen de ventas del día**
- **Pedidos pendientes**
- **Alertas de inventario**
- **Métricas clave**

---

## 👥 Gestión de Clientes

### Agregar Nuevo Cliente

1. **Navegue** a la sección "Clientes"
2. **Haga clic** en "Nuevo Cliente"
3. **Complete** los campos requeridos:
   - RUT (formato: 12345678-9)
   - Nombre completo
   - Email
   - Teléfono
   - Dirección (opcional)
4. **Guarde** los cambios

### Buscar Clientes

**Búsqueda Rápida:**
- Use la barra de búsqueda en la parte superior
- Puede buscar por nombre, RUT, email o teléfono

**Filtros Avanzados:**
- Estado del cliente (activo/inactivo)
- Fecha de registro
- Número de pedidos realizados

### Historial de Cliente

Para ver el historial de un cliente:

1. **Seleccione** al cliente de la lista
2. **Haga clic** en "Ver Historial"
3. **Revise** la información disponible:
   - Pedidos anteriores
   - Preferencias culinarias
   - Direcciones de entrega
   - Métodos de pago utilizados

### Actualizar Información

1. **Abra** la ficha del cliente
2. **Haga clic** en "Editar"
3. **Modifique** los campos necesarios
4. **Confirme** los cambios

---

## 📦 Gestión de Inventario

### Visualizar Inventario

El módulo de inventario muestra:
- **Stock actual** de cada ingrediente
- **Stock mínimo** configurado
- **Alertas** de productos con stock bajo
- **Precio unitario** de cada ingrediente

### Agregar Nuevo Ingrediente

1. **Vaya** a "Inventario" → "Agregar Ingrediente"
2. **Ingrese** la información:
   - Nombre del ingrediente
   - Stock inicial
   - Stock mínimo (para alertas)
   - Precio unitario
   - Unidad de medida
3. **Guarde** el ingrediente

### Actualizar Stock

**Entrada de Mercadería:**
1. **Seleccione** el ingrediente
2. **Haga clic** en "Actualizar Stock"
3. **Ingrese** la cantidad recibida
4. **Confirme** la actualización

**Ajustes de Inventario:**
1. **Acceda** a "Ajustes de Inventario"
2. **Seleccione** el motivo del ajuste
3. **Ingrese** la nueva cantidad
4. **Agregue** comentarios explicativos

### Alertas de Stock Bajo

El sistema automáticamente:
- ✅ **Identifica** productos con stock bajo
- ✅ **Envía notificaciones** al personal autorizado
- ✅ **Genera reportes** de reposición necesaria

**Para gestionar alertas:**
1. **Revise** la sección "Alertas" en el dashboard
2. **Priorice** según impacto en menús
3. **Genere** órdenes de compra
4. **Actualice** el stock al recibir mercadería

---

## 🍽️ Gestión de Menús

### Crear Nuevo Menú

1. **Navegue** a "Menús" → "Nuevo Menú"
2. **Complete** la información básica:
   - Nombre del plato
   - Descripción detallada
   - Categoría (Entrada, Plato Principal, Postre, etc.)
   - Precio de venta
3. **Agregue ingredientes:**
   - Seleccione ingredientes del inventario
   - Especifique cantidades necesarias
4. **Defina disponibilidad**
5. **Guarde** el menú

### Categorías de Menús

Las categorías disponibles son:
- 🥗 **Entradas**
- 🍖 **Platos Principales**
- 🍰 **Postres**
- 🥤 **Bebidas**
- 🍕 **Especialidades**
- 🥙 **Menús Ejecutivos**

### Gestionar Disponibilidad

**Activar/Desactivar Menús:**
1. **Seleccione** el menú deseado
2. **Use** el interruptor de disponibilidad
3. **Confirme** el cambio

Los menús no disponibles:
- No aparecen en el sistema de pedidos
- Se marcan claramente para el personal
- Mantienen su configuración para reactivación futura

### Calcular Costos

El sistema automáticamente:
- ✅ **Calcula** el costo de ingredientes
- ✅ **Muestra** el margen de ganancia
- ✅ **Alerta** sobre menús no rentables

---

## 🛒 Gestión de Pedidos

### Crear Nuevo Pedido

1. **Inicie** un nuevo pedido desde "Pedidos" → "Nuevo Pedido"
2. **Seleccione** o agregue cliente
3. **Agregue items al pedido:**
   - Busque menús disponibles
   - Especifique cantidades
   - Agregue observaciones especiales
4. **Seleccione** tipo de entrega:
   - Para llevar
   - Delivery
   - Consumo en local
5. **Confirme** el pedido

### Estados de Pedidos

Los pedidos pasan por estos estados:

```
Pendiente → En Preparación → Listo → En Camino → Entregado
```

**Descripción de Estados:**
- 🟡 **Pendiente**: Pedido recibido, esperando confirmación
- 🔵 **En Preparación**: Cocina trabajando en el pedido
- 🟢 **Listo**: Pedido completado, listo para entrega
- 🟠 **En Camino**: Repartidor en ruta (solo delivery)
- ✅ **Entregado**: Pedido completado exitosamente
- ❌ **Cancelado**: Pedido cancelado

### Modificar Pedidos

**Antes de la preparación:**
- Se pueden agregar o quitar items
- Se puede cambiar el tipo de entrega
- Se puede modificar información del cliente

**Durante la preparación:**
- Solo se pueden agregar items con autorización
- Las modificaciones requieren confirmación de cocina

### Generar Tickets

1. **Seleccione** el pedido
2. **Haga clic** en "Generar Ticket"
3. **Elija** el tipo:
   - Ticket de cocina
   - Ticket de cliente
   - Factura completa

---

## 🚚 Sistema de Delivery

### Configurar Zona de Delivery

1. **Vaya** a "Delivery" → "Configuración"
2. **Defina** zonas de entrega:
   - Nombre de la zona
   - Radio de cobertura
   - Costo de envío
   - Tiempo estimado

### Asignar Repartidores

**Registro de Repartidor:**
1. **Agregue** información del repartidor:
   - Nombre completo
   - Teléfono de contacto
   - Medio de transporte
   - Zonas asignadas

### Seguimiento de Entregas

**En Tiempo Real:**
- 📍 **Ubicación** del repartidor (si disponible)
- ⏱️ **Tiempo estimado** de llegada
- 📞 **Contacto directo** con repartidor

**Gestión de Entregas:**
1. **Visualice** entregas pendientes
2. **Asigne** repartidores disponibles
3. **Monitoree** el progreso
4. **Confirme** entregas completadas

### Optimización de Rutas

El sistema sugiere:
- ✅ **Rutas optimizadas** para múltiples entregas
- ✅ **Agrupación** de pedidos por zona
- ✅ **Priorización** por tiempo de espera

---

## 💳 Sistema de Pagos

### Métodos de Pago Disponibles

- 💳 **Tarjetas de Crédito/Débito**
- 💰 **Efectivo**
- 📱 **Transferencias Electrónicas**
- 🏪 **Pago contra entrega**

### Procesar Pagos

**Pago con Tarjeta:**
1. **Seleccione** "Pago con Tarjeta"
2. **Ingrese** o deslice la tarjeta
3. **Confirme** el monto
4. **Obtenga** autorización
5. **Genere** comprobante

**Pago en Efectivo:**
1. **Seleccione** "Pago en Efectivo"
2. **Ingrese** monto recibido
3. **Calcule** vuelto automáticamente
4. **Confirme** la transacción

### Devoluciones y Reembolsos

**Proceso de Reembolso:**
1. **Localice** la transacción original
2. **Verifique** motivo del reembolso
3. **Procese** según política de la empresa
4. **Genere** comprobante de reembolso

### Reportes de Caja

**Cierre Diario:**
1. **Acceda** a "Reportes de Caja"
2. **Genere** resumen del día
3. **Verifique** contra efectivo físico
4. **Registre** cualquier diferencia

---

## 📊 Dashboard y Analytics

### Panel Principal

El dashboard muestra métricas clave:

**Métricas del Día:**
- 💰 Total de ventas
- 📋 Número de pedidos
- 👥 Clientes atendidos
- ⏱️ Tiempo promedio de preparación

**Gráficos y Tendencias:**
- Ventas por hora
- Productos más vendidos
- Satisfacción del cliente
- Performance de repartidores

### Reportes Disponibles

**Reportes de Ventas:**
- Ventas diarias, semanales, mensuales
- Comparación con períodos anteriores
- Análisis por categoría de productos
- Rentabilidad por menú

**Reportes de Inventario:**
- Consumo de ingredientes
- Rotación de stock
- Predicción de reposición
- Análisis de desperdicios

**Reportes de Delivery:**
- Tiempos de entrega
- Zonas más demandadas
- Performance de repartidores
- Costos de delivery

### Exportar Datos

1. **Seleccione** el reporte deseado
2. **Configure** filtros y fechas
3. **Elija** formato de exportación:
   - PDF para impresión
   - Excel para análisis
   - CSV para integración
4. **Descargue** el archivo

---

## ❓ Preguntas Frecuentes

### Sobre Pedidos

**P: ¿Puedo cancelar un pedido que ya está en preparación?**
R: Sí, pero requiere autorización del supervisor y puede aplicar una penalización según la política del restaurante.

**P: ¿Cómo modifico un pedido después de confirmarlo?**
R: Use la opción "Modificar Pedido" antes de que pase a estado "En Preparación". Después de ese punto, contacte al supervisor.

### Sobre Inventory

**P: ¿Qué hago cuando un ingrediente está agotado?**
R: 
1. Marque el ingrediente como "Agotado"
2. El sistema automáticamente deshabilitará menús relacionados
3. Genere orden de compra urgente
4. Notifique al equipo de cocina

**P: ¿Cómo configuro alertas de stock?**
R: En la configuración de cada ingrediente, establezca el "Stock Mínimo". El sistema alertará automáticamente cuando se alcance ese nivel.

### Sobre Delivery

**P: ¿Qué hago si un repartidor no está disponible?**
R: 
1. Verifique otros repartidores disponibles
2. Reasigne la entrega
3. Si no hay disponibilidad, contacte al cliente para reprogramar

**P: ¿Cómo calculo el tiempo de entrega?**
R: El sistema calcula automáticamente basado en:
- Tiempo de preparación del pedido
- Distancia a destino
- Tráfico actual (si integrado)
- Disponibilidad de repartidores

### Problemas Técnicos

**P: ¿Qué hago si el sistema está lento?**
R:
1. Verifique su conexión a internet
2. Cierre otras aplicaciones del navegador
3. Reinicie el navegador
4. Contacte soporte técnico si persiste

**P: ¿Cómo recupero un pedido que se perdió?**
R:
1. Use la función "Buscar Pedidos"
2. Filtre por fecha y cliente
3. Verifique en "Pedidos Archivados"
4. Contacte al administrador si no lo encuentra

---

## 🆘 Soporte Técnico

### Contacto de Soporte

**Soporte Técnico 24/7:**
- ☎️ **Teléfono**: +56 2 1234 5678
- ✉️ **Email**: soporte@restaurante-sistema.com
- 💬 **Chat en vivo**: Disponible en la aplicación
- 🎫 **Tickets**: Portal de soporte interno

### Horarios de Atención

- **Lunes a Viernes**: 8:00 AM - 8:00 PM
- **Sábados**: 9:00 AM - 6:00 PM
- **Domingos**: 10:00 AM - 4:00 PM
- **Emergencias**: 24/7 vía WhatsApp

### Información Útil para Soporte

Cuando contacte soporte, tenga lista esta información:
- Nombre del restaurante
- Usuario que experimenta el problema
- Descripción detallada del problema
- Pasos que llevaron al error
- Mensajes de error (si aplica)
- Hora aproximada del incidente

### Videos Tutoriales

Acceda a nuestra biblioteca de videos:
- 🎥 **Introducción al Sistema** (15 min)
- 🎥 **Gestión de Pedidos** (20 min)
- 🎥 **Control de Inventario** (18 min)
- 🎥 **Sistema de Delivery** (12 min)
- 🎥 **Reportes y Analytics** (25 min)

### Actualizaciones del Sistema

- **Actualizaciones automáticas** cada domingo a las 2:00 AM
- **Notificaciones** 48 horas antes de actualizaciones mayores
- **Notas de la versión** disponibles en la aplicación
- **Capacitación** para nuevas funciones según sea necesario

---

## 📄 Información Adicional

### Política de Privacidad

Sus datos están protegidos bajo nuestras estrictas políticas de privacidad. Para más información, consulte el documento completo en la sección "Legal" de la aplicación.

### Términos de Uso

El uso de este sistema está sujeto a nuestros términos y condiciones. Por favor, revíselos periódicamente ya que pueden ser actualizados.

### Copias de Seguridad

El sistema realiza copias de seguridad automáticas cada 6 horas. Sus datos están seguros y pueden ser recuperados en caso de cualquier eventualidad.

---

**📧 ¿Necesita ayuda adicional?**

No dude en contactar a nuestro equipo de soporte. Estamos aquí para asegurar que aproveche al máximo el Sistema de Gestión de Restaurante.

*Documento actualizado: [Fecha actual]*
*Versión: 1.0*
