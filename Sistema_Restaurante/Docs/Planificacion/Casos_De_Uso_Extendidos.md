# CASOS DE USO EXTENDIDOS - SISTEMA DE GESTIÓN DE RESTAURANTE

Este documento presenta la descripción detallada de los casos de uso para ambas versiones del sistema de gestión de restaurante: el sistema actual y el sistema refactorizado, de acuerdo con las especificaciones técnicas y los requerimientos de sistematización documentados.

## ÍNDICE DE CONTENIDO

1. [SISTEMA ACTUAL](#sistema-actual)
   - [Gestión de Clientes](#gestión-de-clientes)
   - [Gestión de Ingredientes](#gestión-de-ingredientes) 
   - [Gestión de Menús](#gestión-de-menús)
   - [Gestión de Pedidos](#gestión-de-pedidos)
   - [Generación de Reportes](#generación-de-reportes)
2. [SISTEMA REFACTORIZADO](#sistema-refactorizado)
   - [Gestión de Clientes](#gestión-de-clientes-refactorizado)
   - [Gestión de Ingredientes](#gestión-de-ingredientes-refactorizado)
   - [Gestión de Menús](#gestión-de-menús-refactorizado)
   - [Gestión de Pedidos](#gestión-de-pedidos-refactorizado)
   - [Gestión de Mesas](#gestión-de-mesas)
   - [Sistema de Delivery](#sistema-de-delivery)
   - [Sistema de Pagos](#sistema-de-pagos)
   - [Dashboard Analítico](#dashboard-analítico)
3. [COMPARATIVA DE CASOS DE USO](#comparativa-de-casos-de-uso)
4. [CONCLUSIONES](#conclusiones)

---

# SISTEMA ACTUAL

En esta sección se detallan los casos de uso del sistema actual, que opera como una aplicación de escritorio con funcionalidades centralizadas principalmente en el rol del Jefe de Local.

## Gestión de Clientes

### CU-A01: Registrar Cliente

**Nombre:** Registrar Cliente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local crear un nuevo registro de cliente en el sistema.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El cliente a registrar no existe previamente en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Registrar nuevo cliente" en el menú principal.
2. El sistema muestra un formulario con los campos necesarios (RUT, nombre, teléfono, dirección, correo electrónico).
3. El Jefe de Local ingresa los datos del cliente.
4. El sistema valida los datos ingresados.
5. El Jefe de Local confirma la operación seleccionando "Guardar".
6. El sistema registra el cliente y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- En el paso 4, si los datos son inválidos, el sistema muestra un mensaje de error y permite corregirlos.
- En cualquier momento, el Jefe de Local puede cancelar la operación seleccionando "Cancelar", volviendo al menú principal sin guardar cambios.

**Postcondiciones:**
- El nuevo cliente queda registrado en el sistema.
- El sistema puede buscar al cliente por su RUT o nombre.

**Excepciones:**
- Si el cliente ya existe en el sistema (mismo RUT), se muestra un mensaje de error.
- Si hay problemas de conexión con la base de datos, se muestra un mensaje de error explicativo.

**Frecuencia de uso:** Varias veces al día.

---

### CU-A02: Editar Cliente

**Nombre:** Editar Cliente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local modificar la información de un cliente existente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El cliente a modificar existe en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca el cliente mediante RUT o nombre.
2. El sistema muestra la información actual del cliente.
3. El Jefe de Local selecciona la opción "Editar".
4. El sistema habilita la edición de los campos.
5. El Jefe de Local modifica los datos necesarios.
6. El sistema valida los datos ingresados.
7. El Jefe de Local confirma la operación seleccionando "Guardar".
8. El sistema actualiza la información y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- En el paso 1, si el cliente no existe, se muestra un mensaje indicando que no se encontró el cliente.
- En cualquier momento, el Jefe de Local puede cancelar la edición seleccionando "Cancelar".

**Postcondiciones:**
- La información del cliente queda actualizada en el sistema.

**Excepciones:**
- Si hay problemas de conexión con la base de datos, se muestra un mensaje de error explicativo.

**Frecuencia de uso:** Ocasional, cuando cambian datos del cliente.

---

### CU-A03: Eliminar Cliente

**Nombre:** Eliminar Cliente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local eliminar un cliente del sistema.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El cliente a eliminar existe en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca el cliente mediante RUT o nombre.
2. El sistema muestra la información del cliente.
3. El Jefe de Local selecciona la opción "Eliminar".
4. El sistema solicita confirmación de la eliminación.
5. El Jefe de Local confirma la eliminación.
6. El sistema elimina el registro y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- En el paso 5, si el Jefe de Local no confirma la eliminación, el sistema cancela la operación.

**Postcondiciones:**
- El cliente ya no existe en el sistema.
- Los pedidos históricos asociados al cliente quedan marcados como "cliente eliminado".

**Excepciones:**
- Si el cliente tiene pedidos en proceso, el sistema impide su eliminación y muestra un mensaje explicativo.

**Frecuencia de uso:** Rara, solo cuando se requiere borrar datos obsoletos.

---

### CU-A04: Buscar Cliente

**Nombre:** Buscar Cliente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local buscar un cliente registrado en el sistema.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen clientes registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Buscar cliente" en el menú principal.
2. El sistema muestra un formulario de búsqueda con diferentes criterios (RUT, nombre, teléfono).
3. El Jefe de Local ingresa el criterio de búsqueda.
4. El sistema busca en la base de datos.
5. El sistema muestra los resultados que coinciden con el criterio ingresado.
6. El Jefe de Local puede seleccionar un cliente específico para ver sus detalles.

**Flujos Alternativos:**
- Si no hay resultados que coincidan, el sistema muestra un mensaje indicando que no se encontraron clientes.
- Si el Jefe de Local desea refinar la búsqueda, puede modificar los criterios y volver a buscar.

**Postcondiciones:**
- Se muestra la información del cliente buscado si existe.

**Excepciones:**
- Si hay problemas de conexión con la base de datos, se muestra un mensaje de error.

**Frecuencia de uso:** Varias veces al día, cuando se necesita acceder a la información de un cliente.

---

### CU-A05: Ver Historial de Pedidos

**Nombre:** Ver Historial de Pedidos  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local consultar el historial de pedidos de un cliente específico.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El cliente existe en el sistema y tiene pedidos registrados.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona un cliente específico.
2. El sistema muestra la información básica del cliente.
3. El Jefe de Local selecciona la opción "Ver historial de pedidos".
4. El sistema recupera y muestra todos los pedidos realizados por el cliente, ordenados cronológicamente.
5. Para cada pedido, se muestra la fecha, los ítems ordenados y el monto total.

**Flujos Alternativos:**
- Si el cliente no tiene pedidos registrados, el sistema muestra un mensaje indicando que no hay historial de pedidos.
- El Jefe de Local puede filtrar el historial por fechas o montos.

**Postcondiciones:**
- Se muestra el historial de pedidos del cliente seleccionado.

**Excepciones:**
- Si hay problemas al recuperar el historial, se muestra un mensaje de error.

**Frecuencia de uso:** Ocasional, cuando se necesita revisar los pedidos anteriores de un cliente.

---

## Gestión de Ingredientes

### CU-A06: Agregar Ingrediente

**Nombre:** Agregar Ingrediente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local añadir un nuevo ingrediente al inventario.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El ingrediente a registrar no existe previamente en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Agregar ingrediente" en el menú de inventario.
2. El sistema muestra un formulario con los campos necesarios (nombre, tipo, cantidad, unidad de medida, nivel crítico).
3. El Jefe de Local ingresa los datos del ingrediente.
4. El sistema valida los datos ingresados.
5. El Jefe de Local confirma la operación seleccionando "Guardar".
6. El sistema registra el ingrediente y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el Jefe de Local selecciona "Cancelar", el sistema vuelve al menú de inventario sin guardar cambios.

**Postcondiciones:**
- El nuevo ingrediente queda registrado en el sistema y disponible para su uso en menús.

**Excepciones:**
- Si ya existe un ingrediente con el mismo nombre, el sistema muestra un mensaje de error.

**Frecuencia de uso:** Ocasional, cuando se introduce un nuevo ingrediente al restaurante.

---

### CU-A07: Editar Ingrediente

**Nombre:** Editar Ingrediente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local modificar la información de un ingrediente existente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El ingrediente a modificar existe en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el ingrediente que desea modificar.
2. El sistema muestra la información actual del ingrediente.
3. El Jefe de Local selecciona la opción "Editar".
4. El sistema habilita la edición de los campos (nombre, tipo, unidad de medida, nivel crítico).
5. El Jefe de Local realiza los cambios necesarios.
6. El sistema valida los datos modificados.
7. El Jefe de Local confirma los cambios seleccionando "Guardar".
8. El sistema actualiza la información del ingrediente y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el Jefe de Local cancela la edición, el sistema vuelve a la visualización del ingrediente sin guardar cambios.

**Postcondiciones:**
- La información del ingrediente queda actualizada en el sistema.

**Excepciones:**
- Si se intenta cambiar a un nombre que ya existe, el sistema muestra un mensaje de error.
- Si hay problemas al guardar los cambios, se muestra un mensaje de error.

**Frecuencia de uso:** Ocasional, cuando es necesario corregir información o actualizar propiedades del ingrediente.

---

### CU-A08: Eliminar Ingrediente

**Nombre:** Eliminar Ingrediente  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local eliminar un ingrediente del sistema.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El ingrediente a eliminar existe en el sistema.
- El ingrediente no está siendo utilizado en ningún menú activo.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el ingrediente que desea eliminar.
2. El sistema muestra la información del ingrediente.
3. El Jefe de Local selecciona la opción "Eliminar".
4. El sistema verifica si el ingrediente está siendo utilizado en algún menú activo.
5. El sistema solicita confirmación para la eliminación.
6. El Jefe de Local confirma la eliminación.
7. El sistema elimina el registro y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el ingrediente está siendo utilizado en algún menú activo, el sistema muestra un mensaje de advertencia y no permite la eliminación.
- Si el Jefe de Local no confirma la eliminación, la operación se cancela.

**Postcondiciones:**
- El ingrediente es eliminado del sistema y ya no está disponible para su uso.

**Excepciones:**
- Si hay problemas durante la eliminación, se muestra un mensaje de error.

**Frecuencia de uso:** Rara, solo cuando un ingrediente ya no se utilizará más en el restaurante.

---

### CU-A09: Actualizar Stock

**Nombre:** Actualizar Stock  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local modificar la cantidad disponible de un ingrediente en el inventario.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El ingrediente existe en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el ingrediente a actualizar.
2. El sistema muestra la información actual del ingrediente, incluido su stock.
3. El Jefe de Local selecciona la opción "Actualizar stock".
4. El sistema muestra un campo para ingresar la nueva cantidad.
5. El Jefe de Local ingresa la nueva cantidad o el ajuste (+/-).
6. El sistema valida que la cantidad sea mayor o igual a cero.
7. El Jefe de Local confirma la operación.
8. El sistema actualiza el stock y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el Jefe de Local cancela la operación, el sistema mantiene el stock original.

**Postcondiciones:**
- El stock del ingrediente queda actualizado en el sistema.

**Excepciones:**
- Si se intenta actualizar a un valor negativo, el sistema muestra un mensaje de error.
- Si hay problemas al guardar la actualización, se muestra un mensaje de error.

**Frecuencia de uso:** Frecuente, cada vez que se reciben nuevos ingredientes o se realiza un inventario.

---

### CU-A10: Verificar Disponibilidad de Ingredientes

**Nombre:** Verificar Disponibilidad de Ingredientes  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local comprobar qué ingredientes están disponibles, escasos o agotados.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen ingredientes registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Verificar disponibilidad" en el menú de ingredientes.
2. El sistema muestra una lista de todos los ingredientes con su stock actual.
3. El sistema resalta aquellos ingredientes que están por debajo de su nivel crítico.
4. El Jefe de Local puede filtrar la lista para ver solo los ingredientes con bajo stock.
5. El Jefe de Local puede seleccionar un ingrediente para actualizar su stock.

**Flujos Alternativos:**
- El Jefe de Local puede generar un informe imprimible de los ingredientes escasos.

**Postcondiciones:**
- El Jefe de Local obtiene una visión clara del estado del inventario.

**Excepciones:**
- Si hay problemas al cargar los datos de inventario, se muestra un mensaje de error.

**Frecuencia de uso:** Diaria, para mantener control del inventario.

---

## Gestión de Menús

### CU-A11: Crear Menú

**Nombre:** Crear Menú  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local crear un nuevo plato o menú disponible para venta.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen ingredientes registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Crear menú" en la sección de gestión de menús.
2. El sistema muestra un formulario con los campos necesarios (nombre, descripción, precio, categoría).
3. El Jefe de Local ingresa la información básica del menú.
4. El Jefe de Local selecciona la opción "Agregar ingredientes".
5. El sistema muestra la lista de ingredientes disponibles.
6. El Jefe de Local selecciona los ingredientes necesarios y especifica las cantidades.
7. El sistema valida que las cantidades sean válidas.
8. El Jefe de Local confirma la creación del menú seleccionando "Guardar".
9. El sistema registra el menú y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el Jefe de Local selecciona "Cancelar" en cualquier momento, el sistema vuelve al menú principal sin guardar cambios.

**Postcondiciones:**
- El nuevo menú queda registrado en el sistema y disponible para ser incluido en pedidos.

**Excepciones:**
- Si no hay ingredientes suficientes para definir el menú, el sistema muestra un mensaje sugerido crear primero los ingredientes.

**Frecuencia de uso:** Ocasional, cuando se añaden nuevos platos a la carta.

---

### CU-A12: Editar Menú

**Nombre:** Editar Menú  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local modificar la información de un menú existente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El menú a modificar existe en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el menú que desea modificar.
2. El sistema muestra la información actual del menú.
3. El Jefe de Local selecciona la opción "Editar".
4. El sistema habilita la edición de los campos (nombre, descripción, precio, categoría).
5. El Jefe de Local realiza los cambios necesarios.
6. El Jefe de Local puede modificar los ingredientes asociados al menú.
7. El sistema valida los datos modificados.
8. El Jefe de Local confirma los cambios seleccionando "Guardar".
9. El sistema actualiza la información del menú y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el Jefe de Local cancela la edición, el sistema vuelve a la visualización del menú sin guardar cambios.

**Postcondiciones:**
- La información del menú queda actualizada en el sistema.

**Excepciones:**
- Si se intenta cambiar a un nombre que ya existe, el sistema muestra un mensaje de error.
- Si se eliminan ingredientes necesarios, el sistema muestra una advertencia.

**Frecuencia de uso:** Ocasional, cuando cambian precios o se modifican recetas.

---

### CU-A13: Eliminar Menú

**Nombre:** Eliminar Menú  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local eliminar un menú del sistema.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El menú a eliminar existe en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el menú que desea eliminar.
2. El sistema muestra la información del menú.
3. El Jefe de Local selecciona la opción "Eliminar".
4. El sistema verifica si el menú está incluido en pedidos activos.
5. El sistema solicita confirmación para la eliminación.
6. El Jefe de Local confirma la eliminación.
7. El sistema elimina el registro y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el menú está incluido en pedidos activos, el sistema muestra una advertencia.
- Si el Jefe de Local no confirma la eliminación, la operación se cancela.

**Postcondiciones:**
- El menú es eliminado del sistema y ya no está disponible para pedidos.
- Las relaciones con ingredientes asociados a este menú también se eliminan.

**Excepciones:**
- Si hay problemas durante la eliminación, se muestra un mensaje de error.

**Frecuencia de uso:** Rara, normalmente cuando un plato se descontinúa permanentemente.

---

### CU-A14: Asignar Ingredientes a Menú

**Nombre:** Asignar Ingredientes a Menú  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local asociar ingredientes y sus cantidades a un menú específico.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El menú existe en el sistema.
- Existen ingredientes registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el menú al que desea asignar ingredientes.
2. El sistema muestra la información actual del menú y los ingredientes ya asociados.
3. El Jefe de Local selecciona la opción "Asignar ingredientes".
4. El sistema muestra la lista de ingredientes disponibles.
5. El Jefe de Local selecciona un ingrediente y especifica la cantidad necesaria.
6. El Jefe de Local puede repetir el paso 5 para agregar múltiples ingredientes.
7. El sistema valida que las cantidades sean válidas.
8. El Jefe de Local confirma los cambios seleccionando "Guardar".
9. El sistema actualiza las relaciones menú-ingrediente y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- El Jefe de Local puede eliminar ingredientes previamente asignados al menú.
- El Jefe de Local puede modificar las cantidades de ingredientes ya asignados.

**Postcondiciones:**
- El menú queda asociado con los ingredientes seleccionados y sus respectivas cantidades.

**Excepciones:**
- Si se especifica una cantidad inválida (0 o negativa), el sistema muestra un mensaje de error.

**Frecuencia de uso:** Ocasional, cuando se crean nuevos menús o se ajustan recetas.

---

### CU-A15: Verificar Disponibilidad de Menú

**Nombre:** Verificar Disponibilidad de Menú  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local comprobar si un menú específico puede prepararse con los ingredientes disponibles.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El menú existe en el sistema con ingredientes asignados.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el menú que desea verificar.
2. El sistema muestra la información del menú.
3. El Jefe de Local selecciona la opción "Verificar disponibilidad".
4. El sistema comprueba el stock actual de cada ingrediente necesario para el menú.
5. El sistema compara las cantidades disponibles con las necesarias para preparar el menú.
6. El sistema muestra el resultado, indicando si el menú puede prepararse y cuántas porciones son posibles.

**Flujos Alternativos:**
- El Jefe de Local puede verificar la disponibilidad de todos los menús a la vez.

**Postcondiciones:**
- El Jefe de Local conoce la disponibilidad actual del menú seleccionado.

**Excepciones:**
- Si hay problemas al comprobar el inventario, se muestra un mensaje de error.

**Frecuencia de uso:** Frecuente, especialmente antes y durante el servicio.

---

## Gestión de Pedidos

### CU-A16: Crear Pedido

**Nombre:** Crear Pedido  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local registrar un nuevo pedido para un cliente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen menús disponibles en el sistema.
- El cliente está registrado en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Crear pedido" en el menú principal.
2. El sistema solicita identificar al cliente.
3. El Jefe de Local busca y selecciona al cliente.
4. El sistema muestra la lista de menús disponibles.
5. El Jefe de Local selecciona los ítems que el cliente desea ordenar y especifica la cantidad.
6. El sistema calcula el total del pedido.
7. El Jefe de Local confirma el pedido seleccionando "Guardar".
8. El sistema registra el pedido y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el cliente no está registrado, el Jefe de Local puede crear un nuevo cliente antes de continuar.
- Si el Jefe de Local selecciona "Cancelar", el sistema vuelve al menú principal sin guardar el pedido.

**Postcondiciones:**
- El pedido queda registrado en el sistema.
- Se actualiza el historial de pedidos del cliente.

**Excepciones:**
- Si alguno de los menús seleccionados no está disponible por falta de ingredientes, el sistema muestra una advertencia.

**Frecuencia de uso:** Varias veces al día, cada vez que un cliente realiza un pedido.

---

### CU-A17: Editar Pedido

**Nombre:** Editar Pedido  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local modificar un pedido existente que aún no ha sido procesado.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El pedido existe en el sistema y no ha sido completado.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el pedido que desea modificar.
2. El sistema muestra los detalles actuales del pedido.
3. El Jefe de Local selecciona la opción "Editar".
4. El sistema habilita la modificación de los ítems del pedido.
5. El Jefe de Local puede agregar, eliminar o modificar la cantidad de menús en el pedido.
6. El sistema recalcula el total del pedido.
7. El Jefe de Local confirma los cambios seleccionando "Guardar".
8. El sistema actualiza el pedido y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el pedido ya ha sido entregado o pagado, el sistema no permite su edición.
- El Jefe de Local puede cambiar el cliente asociado al pedido.

**Postcondiciones:**
- El pedido queda actualizado con los cambios realizados.
- El total del pedido se recalcula automáticamente.

**Excepciones:**
- Si alguno de los menús añadidos no está disponible, el sistema muestra una advertencia.

**Frecuencia de uso:** Ocasional, cuando es necesario modificar un pedido por solicitud del cliente.

---

### CU-A18: Cancelar Pedido

**Nombre:** Cancelar Pedido  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local cancelar un pedido existente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El pedido existe en el sistema y no ha sido completado o pagado.

**Flujo Principal:**
1. El Jefe de Local busca y selecciona el pedido que desea cancelar.
2. El sistema muestra los detalles del pedido.
3. El Jefe de Local selecciona la opción "Cancelar pedido".
4. El sistema solicita un motivo para la cancelación.
5. El Jefe de Local ingresa el motivo.
6. El sistema solicita confirmación de la cancelación.
7. El Jefe de Local confirma la cancelación.
8. El sistema marca el pedido como cancelado y registra el motivo.

**Flujos Alternativos:**
- Si el pedido ya ha sido pagado, el sistema sugiere realizar un reembolso en lugar de cancelación.
- Si el Jefe de Local no confirma la cancelación, la operación se cancela.

**Postcondiciones:**
- El pedido queda marcado como cancelado en el sistema.
- Los ingredientes reservados para ese pedido vuelven a estar disponibles.

**Excepciones:**
- Si el pedido ya está en preparación avanzada, el sistema muestra una advertencia antes de permitir la cancelación.

**Frecuencia de uso:** Rara, solo en situaciones específicas como error en el pedido o solicitud del cliente.

---

### CU-A19: Asignar Cliente a Pedido

**Nombre:** Asignar Cliente a Pedido  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local asociar un cliente registrado a un pedido.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El pedido existe en el sistema.
- Existen clientes registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local crea un nuevo pedido o selecciona uno existente.
2. El Jefe de Local selecciona la opción "Asignar cliente".
3. El sistema muestra un buscador de clientes.
4. El Jefe de Local busca al cliente por nombre o RUT.
5. El sistema muestra los resultados que coinciden.
6. El Jefe de Local selecciona el cliente correcto.
7. El sistema asocia el cliente al pedido.

**Flujos Alternativos:**
- Si el cliente no existe, el Jefe de Local puede crear un nuevo registro de cliente.
- El Jefe de Local puede modificar el cliente asignado a un pedido existente.

**Postcondiciones:**
- El pedido queda asociado al cliente seleccionado.
- El pedido aparecerá en el historial del cliente.

**Excepciones:**
- Si no se encuentran coincidencias en la búsqueda, el sistema muestra opciones para refinar la búsqueda o crear un nuevo cliente.

**Frecuencia de uso:** Frecuente, casi en cada pedido.

---

### CU-A20: Agregar Menús a Pedido

**Nombre:** Agregar Menús a Pedido  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local seleccionar los menús que el cliente desea incluir en su pedido.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El pedido ha sido creado en el sistema.
- Existen menús disponibles en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona un pedido existente.
2. El Jefe de Local selecciona la opción "Agregar menús".
3. El sistema muestra la lista de menús disponibles.
4. El Jefe de Local selecciona un menú y especifica la cantidad.
5. El sistema verifica la disponibilidad de ingredientes para la cantidad solicitada.
6. El Jefe de Local puede repetir los pasos 4-5 para agregar múltiples menús.
7. El sistema calcula el subtotal por cada menú y el total del pedido.
8. El Jefe de Local confirma los menús seleccionados.
9. El sistema actualiza el pedido con los menús agregados.

**Flujos Alternativos:**
- Si un menú seleccionado no está disponible por falta de ingredientes, el sistema muestra una advertencia.
- El Jefe de Local puede aplicar descuentos o promociones específicas a ciertos ítems.

**Postcondiciones:**
- El pedido se actualiza con los menús seleccionados y sus cantidades.
- El total del pedido se recalcula con los nuevos ítems.

**Excepciones:**
- Si no hay ingredientes suficientes para todos los menús seleccionados, el sistema muestra qué menús no pueden prepararse.

**Frecuencia de uso:** Muy frecuente, en cada pedido.

---

### CU-A21: Generar Boleta

**Nombre:** Generar Boleta  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local crear una boleta o factura para un pedido completado.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- El pedido existe y contiene ítems.
- El pedido está listo para ser pagado.

**Flujo Principal:**
1. El Jefe de Local selecciona un pedido completado.
2. El Jefe de Local selecciona la opción "Generar boleta".
3. El sistema muestra una vista previa de la boleta incluyendo todos los ítems, cantidades, precios y el total.
4. El sistema aplica automáticamente los impuestos correspondientes.
5. El Jefe de Local confirma los detalles de la boleta.
6. El sistema genera el documento y lo muestra para impresión.

**Flujos Alternativos:**
- Si el cliente requiere factura en lugar de boleta, el Jefe de Local puede seleccionar "Generar factura" e ingresar los datos fiscales necesarios.
- El Jefe de Local puede aplicar descuentos o propinas antes de generar el documento.

**Postcondiciones:**
- Se genera la boleta o factura asociada al pedido.
- El pedido queda marcado como "boleta generada".

**Excepciones:**
- Si hay problemas con la impresora, el sistema guarda la boleta digitalmente para imprimirla más tarde.

**Frecuencia de uso:** Muy frecuente, para cada pedido completado.

---

## Generación de Reportes

### CU-A22: Generar Reporte de Ventas

**Nombre:** Generar Reporte de Ventas  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local obtener un informe sobre las ventas realizadas.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen pedidos registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Reportes" en el menú principal.
2. El sistema muestra los tipos de reportes disponibles.
3. El Jefe de Local selecciona "Reporte de ventas".
4. El sistema solicita el rango de fechas para el reporte.
5. El Jefe de Local ingresa las fechas de inicio y fin.
6. El sistema genera y muestra el reporte con los pedidos y montos correspondientes.
7. El Jefe de Local puede imprimir el reporte o guardarlo como archivo.

**Flujos Alternativos:**
- Si no hay pedidos en el rango de fechas seleccionado, el sistema muestra un mensaje indicando que no hay datos disponibles.

**Postcondiciones:**
- El reporte queda disponible para consulta o impresión.

**Excepciones:**
- Si el rango de fechas es inválido, el sistema muestra un mensaje de error.

**Frecuencia de uso:** Semanal o mensual, para análisis de desempeño.

---

### CU-A23: Ver Estadísticas Básicas

**Nombre:** Ver Estadísticas Básicas  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local visualizar estadísticas generales sobre las operaciones del restaurante.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen datos de pedidos registrados en el sistema.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Estadísticas" en el menú principal.
2. El sistema muestra las estadísticas básicas predeterminadas:
   - Número de pedidos del día actual
   - Total de ventas del día
   - Promedio de ventas por pedido
   - Número de clientes atendidos
3. El Jefe de Local puede seleccionar un rango de fechas diferente.
4. El sistema actualiza las estadísticas según el rango seleccionado.

**Flujos Alternativos:**
- El Jefe de Local puede ver estadísticas por categorías de menú.
- El Jefe de Local puede comparar estadísticas entre diferentes períodos.

**Postcondiciones:**
- Se muestran las estadísticas solicitadas.

**Excepciones:**
- Si no hay datos para el período seleccionado, el sistema muestra un mensaje indicando que no hay información disponible.

**Frecuencia de uso:** Diaria o semanal, para monitoreo básico del negocio.

---

### CU-A24: Ver Uso de Ingredientes

**Nombre:** Ver Uso de Ingredientes  
**Actores:** Jefe de Local  
**Descripción:** Permite al Jefe de Local analizar el consumo de ingredientes en un período determinado.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema como Jefe de Local.
- Existen pedidos registrados en el sistema que utilizaron ingredientes.

**Flujo Principal:**
1. El Jefe de Local selecciona la opción "Uso de ingredientes" en el menú de reportes.
2. El sistema solicita el rango de fechas a analizar.
3. El Jefe de Local ingresa las fechas de inicio y fin.
4. El sistema calcula y muestra:
   - Cantidad total utilizada de cada ingrediente
   - Costo asociado a cada ingrediente
   - Ingredientes más utilizados
   - Ingredientes con mayor variación de uso respecto al período anterior

**Flujos Alternativos:**
- El Jefe de Local puede filtrar por categoría de ingredientes.
- El Jefe de Local puede ordenar los resultados por diferentes criterios (cantidad, costo).

**Postcondiciones:**
- Se muestra el informe de uso de ingredientes para el período seleccionado.

**Excepciones:**
- Si hay inconsistencias en los datos de inventario, el sistema muestra advertencias junto con los resultados.

**Frecuencia de uso:** Semanal o mensual, para análisis de costos y planificación de compras.

# SISTEMA REFACTORIZADO (PARTE 1)

Esta sección detalla la primera parte de los casos de uso del sistema refactorizado, que opera como una aplicación web moderna con responsabilidades distribuidas entre diferentes roles. Esta primera parte cubre las funcionalidades refactorizadas que existían en el sistema anterior.

## Gestión de Clientes (Refactorizado)

### CU-R01: Registrar Cliente

**Nombre:** Registrar Cliente  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite registrar un nuevo cliente en el sistema.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- La conexión a internet está activa para sincronización en tiempo real.

**Flujo Principal:**
1. El usuario selecciona la opción "Registrar cliente" en el sistema.
2. El sistema muestra un formulario web con los campos necesarios (RUT, nombre, teléfono, dirección, correo electrónico).
3. El usuario ingresa los datos del cliente.
4. El sistema valida los datos en tiempo real, mostrando errores o sugerencias mientras se completa el formulario.
5. El usuario confirma la operación seleccionando "Guardar".
6. El sistema registra el cliente, sincroniza la información en todos los dispositivos y muestra un mensaje de confirmación.

**Flujos Alternativos:**
- Si el usuario es un Mesero, puede registrar clientes directamente desde su dispositivo móvil mientras atiende la mesa.
- El sistema ofrece auto-completado para direcciones usando API de mapas.
- Si el cliente proporciona un correo electrónico, se puede enviar una confirmación automática de registro.

**Postcondiciones:**
- El nuevo cliente queda registrado en el sistema y disponible para todos los usuarios autorizados.
- Se crea automáticamente un perfil para seguimiento de preferencias y pedidos frecuentes.

**Excepciones:**
- Si el cliente ya existe, el sistema permite actualizar sus datos o crear un duplicado justificado.
- Si hay problemas de sincronización, los datos se almacenan localmente y se sincronizan cuando la conexión se restablece.

**Frecuencia de uso:** Varias veces al día por diferentes usuarios del sistema.

**Notas:** A diferencia del sistema anterior, los Meseros ahora pueden registrar clientes durante el servicio, lo que agiliza el proceso y mejora la experiencia del cliente.

---

### CU-R02: Editar Cliente

**Nombre:** Editar Cliente  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite modificar la información de un cliente existente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- El cliente a modificar existe en el sistema.

**Flujo Principal:**
1. El usuario busca el cliente mediante el buscador (por RUT, nombre o teléfono).
2. El sistema muestra la información actual del cliente.
3. El usuario selecciona la opción "Editar".
4. El sistema habilita los campos editables y muestra validaciones en tiempo real.
5. El usuario modifica los datos necesarios.
6. El sistema valida los datos mientras se modifican, mostrando feedback inmediato.
7. El usuario confirma los cambios seleccionando "Guardar".
8. El sistema actualiza la información, sincroniza en todos los dispositivos y muestra confirmación.

**Flujos Alternativos:**
- Los meseros pueden editar datos básicos durante la atención en mesa.
- El sistema ofrece completado automático para direcciones y detecta duplicados potenciales.

**Postcondiciones:**
- La información del cliente queda actualizada en tiempo real en todo el sistema.
- Se registra qué usuario realizó la modificación y cuándo.

**Excepciones:**
- Si se detecta un conflicto porque otro usuario está editando simultáneamente, el sistema notifica y gestiona el conflicto.
- Si hay errores de validación, se muestran inmediatamente sin esperar al envío del formulario.

**Frecuencia de uso:** Frecuente, cuando los clientes actualizan sus datos de contacto o preferencias.

---

### CU-R03: Eliminar Cliente

**Nombre:** Eliminar Cliente  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite eliminar un cliente del sistema cuando ya no es necesario mantenerlo en la base de datos.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- El cliente a eliminar existe en el sistema.
- El cliente no tiene pedidos activos en proceso.

**Flujo Principal:**
1. El usuario busca el cliente mediante el buscador (por RUT, nombre o teléfono).
2. El sistema muestra la información del cliente.
3. El usuario selecciona la opción "Eliminar cliente".
4. El sistema verifica si el cliente tiene pedidos activos o en proceso.
5. El sistema solicita confirmación para la eliminación, advirtiendo sobre las consecuencias.
6. El usuario confirma la eliminación e ingresa su contraseña como medida de seguridad.
7. El sistema marca el cliente como eliminado y anonimiza sus datos personales por cumplimiento de privacidad.

**Flujos Alternativos:**
- Si el cliente tiene pedidos activos, el sistema no permite la eliminación y muestra los pedidos pendientes.
- El usuario puede optar por desactivar el cliente en lugar de eliminarlo, manteniendo el historial pero impidiendo nuevos pedidos.

**Postcondiciones:**
- Los datos personales identificables del cliente son anonimizados.
- Se mantiene el historial de pedidos para fines estadísticos pero sin asociación directa a datos personales.
- Se registra qué usuario realizó la eliminación y cuándo.

**Excepciones:**
- Si hay problemas durante el proceso de eliminación, el sistema revierte los cambios y muestra un mensaje de error.

**Frecuencia de uso:** Rara, principalmente para cumplir con solicitudes de eliminación de datos personales o limpiar registros obsoletos.

---

### CU-R04: Buscar Cliente

**Nombre:** Buscar Cliente  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite buscar clientes registrados utilizando diferentes criterios.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen clientes registrados en el sistema.

**Flujo Principal:**
1. El usuario accede a la sección de clientes o utiliza la barra de búsqueda global.
2. El usuario ingresa texto en el campo de búsqueda (que busca coincidencias en RUT, nombre, teléfono o dirección).
3. El sistema muestra resultados en tiempo real mientras el usuario escribe.
4. El usuario puede refinar la búsqueda utilizando filtros adicionales.
5. El usuario selecciona el cliente deseado de los resultados.
6. El sistema muestra la información detallada del cliente seleccionado.

**Flujos Alternativos:**
- El usuario puede escanear un código QR de cliente fidelizado para acceder directamente a su perfil.
- El sistema permite búsqueda avanzada con múltiples criterios combinados.
- Los resultados pueden guardarse como listas personalizadas para acceso rápido futuro.

**Postcondiciones:**
- Se muestra la información del cliente seleccionado y sus opciones de gestión.

**Excepciones:**
- Si la búsqueda no produce resultados, se ofrecen sugerencias alternativas o la opción de crear un nuevo cliente.
- Si hay demasiados resultados, el sistema sugiere refinar la búsqueda.

**Frecuencia de uso:** Muy frecuente, cada vez que se atiende a un cliente existente.

---

### CU-R05: Ver Historial de Pedidos

**Nombre:** Ver Historial de Pedidos  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite consultar el historial completo de pedidos de un cliente específico.

**Precondiciones:**
- El usuario ha iniciado sesión con los permisos adecuados.
- El cliente existe en el sistema y tiene al menos un pedido registrado.

**Flujo Principal:**
1. El usuario accede a la información del cliente deseado.
2. El usuario selecciona la pestaña o sección "Historial de pedidos".
3. El sistema muestra una lista cronológica de todos los pedidos del cliente, mostrando:
   - Fecha y hora del pedido
   - Total gastado
   - Ítems principales ordenados
   - Método de pago utilizado
   - Estado final del pedido
4. El usuario puede seleccionar un período específico para filtrar los pedidos.
5. El usuario puede seleccionar cualquier pedido para ver sus detalles completos.

**Flujos Alternativos:**
- El usuario puede generar un reporte en PDF con el historial de pedidos del cliente.
- El sistema puede mostrar gráficos de tendencias de consumo del cliente.
- El usuario puede ordenar los pedidos por diferentes criterios (monto, fecha, tipo de menú).

**Postcondiciones:**
- Se visualiza el historial completo o filtrado de pedidos del cliente.
- Se puede acceder a los detalles específicos de cualquier pedido histórico.

**Excepciones:**
- Si el cliente no tiene pedidos registrados, el sistema muestra un mensaje indicándolo.
- Si hay problemas al recuperar el historial, el sistema muestra un error explicativo.

**Frecuencia de uso:** Frecuente, para entender los hábitos de consumo de los clientes y ofrecer mejor servicio.

---

## Gestión de Ingredientes (Refactorizado)

### CU-R06: Agregar Ingrediente

**Nombre:** Agregar Ingrediente  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite añadir un nuevo ingrediente al inventario del restaurante.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- El ingrediente a registrar no existe previamente en el sistema.

**Flujo Principal:**
1. El usuario selecciona la opción "Agregar ingrediente" en la sección de inventario.
2. El sistema muestra un formulario con campos para:
   - Nombre del ingrediente
   - Categoría (lácteos, carnes, verduras, etc.)
   - Unidad de medida (kg, litros, unidades)
   - Stock inicial
   - Nivel crítico de stock
   - Proveedor preferido (opcional)
   - Código de barras (opcional)
   - Imagen (opcional)
3. El usuario completa los campos requeridos y opcionales.
4. El sistema valida los datos en tiempo real, mostrando sugerencias y posibles duplicados.
5. El usuario confirma la creación del ingrediente.
6. El sistema registra el nuevo ingrediente y actualiza el inventario en tiempo real.

**Flujos Alternativos:**
- El usuario puede escanear un código de barras para completar automáticamente los datos del ingrediente.
- El usuario puede cargar múltiples ingredientes a la vez mediante un archivo CSV.
- El sistema puede sugerir niveles críticos basados en el uso histórico de ingredientes similares.

**Postcondiciones:**
- El nuevo ingrediente queda registrado en el sistema.
- El ingrediente está disponible para ser asignado a menús.
- Se crea un registro en el historial de movimientos de inventario.

**Excepciones:**
- Si se detecta un ingrediente con nombre similar, el sistema advierte al usuario antes de permitir la creación.
- Si hay campos obligatorios incompletos, el botón de confirmación permanece deshabilitado.

**Frecuencia de uso:** Moderada, cuando se incorporan nuevos productos al menú o cambian los proveedores.

---

### CU-R07: Editar Ingrediente

**Nombre:** Editar Ingrediente  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite modificar la información y propiedades de un ingrediente existente.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- El ingrediente a editar existe en el sistema.

**Flujo Principal:**
1. El usuario busca y selecciona el ingrediente que desea modificar.
2. El usuario selecciona la opción "Editar".
3. El sistema muestra un formulario con los datos actuales del ingrediente.
4. El usuario modifica los campos necesarios (nombre, categoría, unidad de medida, nivel crítico, etc.).
5. El sistema valida los cambios en tiempo real.
6. El usuario confirma las modificaciones.
7. El sistema actualiza la información del ingrediente y todos los menús relacionados.

**Flujos Alternativos:**
- El usuario puede adjuntar una nueva imagen del ingrediente.
- El sistema permite la modificación masiva de ingredientes de la misma categoría.

**Postcondiciones:**
- La información del ingrediente queda actualizada en el sistema.
- Se registra el historial de cambios, incluyendo qué usuario realizó la modificación.
- Si se realizaron cambios críticos, se actualiza el estado de disponibilidad de los menús afectados.

**Excepciones:**
- Si el ingrediente está siendo utilizado en pedidos activos, ciertos campos críticos no pueden modificarse.
- Si los cambios afectan negativamente a la disponibilidad de menús populares, el sistema muestra una advertencia.

**Frecuencia de uso:** Ocasional, principalmente cuando cambian especificaciones de productos o proveedores.

---

### CU-R08: Actualizar Stock

**Nombre:** Actualizar Stock  
**Actores:** Jefe de Local, Jefe de Turno, Cocina  
**Descripción:** Permite actualizar la cantidad disponible de un ingrediente en el inventario.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- El ingrediente a actualizar existe en el sistema.

**Flujo Principal:**
1. El usuario busca el ingrediente mediante el buscador o filtros de categoría.
2. El sistema muestra la información actual del ingrediente incluyendo el stock actual.
3. El usuario selecciona la opción "Actualizar stock".
4. El sistema muestra un formulario para ingresar la nueva cantidad o el ajuste (+/-).
5. El usuario ingresa la cantidad nueva o el ajuste y opcionalmente un motivo.
6. El sistema valida los datos ingresados.
7. El usuario confirma la operación.
8. El sistema actualiza el stock y registra la transacción en el historial de movimientos.

**Flujos Alternativos:**
- Si el usuario es de Cocina, puede utilizar un escáner de códigos QR para identificar rápidamente el ingrediente.
- El sistema permite actualizar múltiples ingredientes a la vez mediante una importación de archivo CSV.
- Si la actualización lleva el stock por debajo del nivel crítico, el sistema muestra una alerta visual.

**Postcondiciones:**
- El stock del ingrediente queda actualizado.
- Se actualiza el historial de movimientos de inventario, registrando quién realizó el cambio.
- Si el nivel es crítico, se generan alertas automáticas para el Jefe de Local y Jefe de Turno.

**Excepciones:**
- Si se intenta actualizar a un valor negativo, el sistema solicita confirmación adicional o bloquea la operación según la configuración.

**Frecuencia de uso:** Varias veces al día, especialmente al recibir nuevos suministros o durante inventarios.

**Notas:** La participación del personal de Cocina en esta función reduce significativamente la carga administrativa del Jefe de Local y mejora la precisión del inventario en tiempo real.

---

### CU-R09: Eliminar Ingrediente

**Nombre:** Eliminar Ingrediente  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite eliminar un ingrediente del catálogo del sistema.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- El ingrediente existe en el sistema.
- El ingrediente no está siendo utilizado en ningún menú activo.

**Flujo Principal:**
1. El usuario busca y selecciona el ingrediente que desea eliminar.
2. El usuario selecciona la opción "Eliminar ingrediente".
3. El sistema verifica si el ingrediente está siendo utilizado en algún menú o pedido activo.
4. Si el ingrediente no está en uso, el sistema solicita confirmación para la eliminación.
5. El usuario confirma la operación ingresando su contraseña.
6. El sistema elimina el ingrediente y registra la acción en el log de operaciones.

**Flujos Alternativos:**
- Si el ingrediente está asociado a menús, el sistema ofrece la opción de marcar el ingrediente como "Descontinuado" en lugar de eliminarlo completamente.
- El usuario puede optar por desactivar el ingrediente temporalmente, manteniendo su registro histórico.

**Postcondiciones:**
- El ingrediente ya no está disponible para nuevos menús.
- Se mantiene un registro histórico del ingrediente para fines de reportes de períodos anteriores.

**Excepciones:**
- Si el ingrediente está siendo utilizado en menús activos, el sistema impide la eliminación y muestra la lista de menús afectados.
- Si el ingrediente tiene movimientos de inventario recientes, el sistema solicita confirmación adicional.

**Frecuencia de uso:** Rara, principalmente cuando se discontinúan productos o se corrigen errores de entrada.

---

### CU-R10: Verificar Disponibilidad de Ingredientes

**Nombre:** Verificar Disponibilidad de Ingredientes  
**Actores:** Jefe de Local, Jefe de Turno, Cocina  
**Descripción:** Permite comprobar el estado actual del inventario de ingredientes con alertas visuales.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen ingredientes registrados en el sistema con niveles críticos definidos.

**Flujo Principal:**
1. El usuario accede a la sección "Inventario" en el sistema.
2. El sistema muestra el tablero de ingredientes con indicadores visuales de estado:
   - Verde: Stock adecuado
   - Amarillo: Stock bajo (próximo al nivel crítico)
   - Rojo: Stock crítico o agotado
3. El usuario puede filtrar la vista por categoría, estado o proveedor.
4. El usuario puede seleccionar un ingrediente específico para ver detalles y tendencias de uso.
5. El sistema muestra predicciones de cuándo se agotará cada ingrediente según el ritmo actual de consumo.

**Flujos Alternativos:**
- El sistema genera notificaciones automáticas cuando un ingrediente alcanza nivel crítico.
- El usuario puede iniciar el proceso de pedido a proveedores directamente desde la vista de disponibilidad.
- El personal de cocina puede reportar discrepancias entre el stock digital y físico.

**Postcondiciones:**
- Se visualiza claramente el estado actual del inventario.
- Las alertas se distribuyen a los roles pertinentes.

**Excepciones:**
- Si hay inconsistencias significativas entre registros y conteo físico, el sistema marca esos ingredientes para inventario físico urgente.

**Frecuencia de uso:** Constante, el sistema actualiza automáticamente la disponibilidad y los usuarios la consultan varias veces al día.

---

## Gestión de Menús (Refactorizado)

### CU-R11: Crear Menú

**Nombre:** Crear Menú  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite crear un nuevo plato o menú para ofertar a los clientes.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- Existen ingredientes registrados en el sistema.

**Flujo Principal:**
1. El usuario selecciona la opción "Crear nuevo menú".
2. El sistema muestra un formulario con campos para:
   - Nombre del menú
   - Descripción
   - Categoría (entrada, plato principal, postre, etc.)
   - Precio de venta
   - Tiempo estimado de preparación
   - Imagen del plato (opcional)
   - Disponible para delivery (sí/no)
3. El usuario completa la información básica y avanza a la siguiente sección.
4. El sistema muestra la interfaz para asignar ingredientes al menú.
5. El usuario busca y selecciona los ingredientes necesarios, especificando la cantidad para cada uno.
6. El sistema calcula automáticamente el costo de producción y el margen de beneficio.
7. El usuario puede ajustar el precio de venta según el margen deseado.
8. El usuario finaliza la creación del menú.

**Flujos Alternativos:**
- El usuario puede duplicar un menú existente y modificarlo para crear variantes.
- El sistema permite añadir notas especiales de preparación para la cocina.
- El usuario puede definir opciones de personalización disponibles para este menú (sin cebolla, nivel de picante, etc.).

**Postcondiciones:**
- El nuevo menú queda registrado en el sistema.
- El sistema verifica automáticamente su disponibilidad según el stock de ingredientes.
- El menú aparece en la carta digital para ser ofrecido a los clientes.

**Excepciones:**
- Si faltan ingredientes esenciales en el stock, el sistema marca automáticamente el menú como "No disponible".
- Si el costo calculado supera el precio de venta, el sistema muestra una advertencia de margen negativo.

**Frecuencia de uso:** Periódica, cuando se actualizan ofertas o se crean promociones especiales.

---

### CU-R12: Editar Menú

**Nombre:** Editar Menú  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite modificar un menú existente en el sistema.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- El menú a modificar existe en el sistema.

**Flujo Principal:**
1. El usuario busca y selecciona el menú que desea modificar.
2. El usuario selecciona la opción "Editar menú".
3. El sistema muestra un formulario con los datos actuales del menú.
4. El usuario modifica los campos necesarios (nombre, descripción, precio, categoría).
5. El usuario puede modificar la lista de ingredientes y sus cantidades.
6. El sistema recalcula automáticamente el costo y margen de beneficio.
7. El usuario confirma los cambios realizados.
8. El sistema actualiza el menú y verifica automáticamente su disponibilidad.

**Flujos Alternativos:**
- El sistema permite definir un nuevo precio sin modificar ingredientes.
- El usuario puede cambiar la imagen del plato o añadir imágenes adicionales.
- El sistema permite programar cambios para activarse en una fecha futura.

**Postcondiciones:**
- La información del menú queda actualizada en el sistema.
- Se actualiza el estado de disponibilidad según el stock de ingredientes.
- Los cambios se reflejan inmediatamente en la carta digital.

**Excepciones:**
- Si los cambios en ingredientes afectan a pedidos en curso, el sistema muestra una advertencia.
- Si se modifica un elemento incluido en promociones activas, el sistema muestra una alerta.

**Frecuencia de uso:** Ocasional, principalmente para actualizar precios o ajustar recetas.

---

### CU-R13: Eliminar Menú

**Nombre:** Eliminar Menú  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite eliminar un menú del catálogo del sistema.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.
- El menú a eliminar existe en el sistema.
- El menú no está incluido en pedidos activos.

**Flujo Principal:**
1. El usuario busca y selecciona el menú que desea eliminar.
2. El usuario selecciona la opción "Eliminar menú".
3. El sistema verifica si el menú está incluido en pedidos activos o promociones vigentes.
4. El sistema solicita confirmación para la eliminación.
5. El usuario confirma la operación ingresando su contraseña.
6. El sistema elimina el menú y registra la acción en el log de operaciones.

**Flujos Alternativos:**
- El sistema ofrece la opción de desactivar temporalmente el menú en lugar de eliminarlo.
- El usuario puede programar la eliminación para una fecha futura.

**Postcondiciones:**
- El menú ya no está disponible para nuevos pedidos.
- Se mantiene un registro histórico del menú para reportes de períodos anteriores.

**Excepciones:**
- Si el menú está incluido en pedidos activos, el sistema impide la eliminación y muestra los pedidos afectados.
- Si el menú forma parte de promociones vigentes, el sistema solicita confirmar la acción.

**Frecuencia de uso:** Rara, principalmente cuando se discontinúan platos o se renueva completamente la carta.

---

### CU-R14: Verificar Disponibilidad de Menú

**Nombre:** Verificar Disponibilidad de Menú  
**Actores:** Jefe de Local, Jefe de Turno, Cocina  
**Descripción:** Permite comprobar si hay suficientes ingredientes para preparar un menú específico o todos los menús.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen menús e ingredientes registrados en el sistema.

**Flujo Principal:**
1. El usuario selecciona la opción "Verificar disponibilidad" en la sección de menús.
2. El sistema muestra la lista de menús con un indicador visual de disponibilidad (verde: disponible, amarillo: próximo a agotarse, rojo: no disponible).
3. El usuario puede seleccionar un menú específico para ver detalles.
4. El sistema muestra qué ingredientes están disponibles y cuáles están escasos o agotados para ese menú.
5. El usuario puede marcar menús como "no disponibles temporalmente" en la carta.

**Flujos Alternativos:**
- El sistema realiza verificaciones automáticas periódicas y actualiza los estados de disponibilidad.
- Si un nuevo pedido reduce el stock por debajo del necesario para un menú, su estado se actualiza automáticamente.

**Postcondiciones:**
- La disponibilidad de menús queda actualizada en tiempo real para todos los usuarios.
- Los meseros ven automáticamente qué platos pueden ofrecer a los clientes.

**Excepciones:**
- Si hay inconsistencias en el inventario, el sistema marca el menú como "estado indeterminado" hasta que se resuelva.

**Frecuencia de uso:** Constante (verificación automática) y varias veces al día (verificación manual).

**Notas:** Esta funcionalidad evita situaciones incómodas donde se ofrece a los clientes platos que luego no pueden prepararse por falta de ingredientes.

---

### CU-R15: Ver Menús Disponibles

**Nombre:** Ver Menús Disponibles  
**Actores:** Jefe de Local, Jefe de Turno, Cocina, Mesero  
**Descripción:** Permite visualizar en tiempo real qué menús pueden prepararse actualmente según el inventario.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen menús registrados en el sistema con sus ingredientes asociados.

**Flujo Principal:**
1. El usuario accede a la sección "Menús disponibles".
2. El sistema calcula automáticamente qué menús pueden prepararse con el inventario actual.
3. El sistema muestra un tablero visual con todos los menús categorizados por:
   - Disponibles (verde)
   - Cantidad limitada (amarillo, indicando cuántas porciones pueden prepararse)
   - No disponibles (rojo)
4. El usuario puede filtrar por categoría, popularidad o disponibilidad.
5. El usuario puede seleccionar un menú para ver detalles sobre qué ingredientes están limitando su disponibilidad.

**Flujos Alternativos:**
- Los meseros ven esta información optimizada para dispositivos móviles mientras atienden mesas.
- La cocina puede marcar temporalmente un menú como "no disponible" independientemente del inventario (ej. equipamiento dañado).
- El sistema sugiere menús alternativos similares cuando uno no está disponible.

**Postcondiciones:**
- Todos los usuarios tienen información actualizada sobre qué ofrecer a los clientes.

**Excepciones:**
- Si la sincronización de datos falla, se muestra la última información conocida con marca de tiempo.

**Frecuencia de uso:** Muy frecuente, especialmente durante horas de servicio.

---

## Gestión de Pedidos (Refactorizado)

### CU-R16: Crear Pedido

**Nombre:** Crear Pedido  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite crear un nuevo pedido para un cliente.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen menús disponibles en el sistema.
- El cliente está registrado en el sistema o se registra durante el proceso.

**Flujo Principal:**
1. El usuario selecciona la opción "Nuevo pedido" o selecciona directamente una mesa para iniciar un pedido.
2. El sistema solicita asociar el pedido a un cliente existente o crear uno nuevo.
3. El usuario selecciona o crea el cliente asociado al pedido.
4. El sistema muestra la lista de menús disponibles, resaltando visualmente su disponibilidad.
5. El usuario selecciona los ítems y especifica cantidades y personalizaciones.
6. El sistema calcula en tiempo real el total del pedido.
7. El usuario puede asociar el pedido a una mesa específica.
8. El usuario confirma el pedido.
9. El sistema registra el pedido y notifica automáticamente a la cocina.

**Flujos Alternativos:**
- Si el usuario es un Mesero, puede crear pedidos directamente desde su dispositivo móvil junto a la mesa.
- El sistema permite agregar notas especiales para cada ítem (ej. "sin cebolla", "término medio").
- El usuario puede guardar un pedido como borrador para completarlo más tarde.

**Postcondiciones:**
- El pedido queda registrado en el sistema.
- Se actualiza el inventario de ingredientes reservando las cantidades necesarias.
- La cocina recibe una notificación del nuevo pedido.
- El pedido aparece asociado al historial del cliente.

**Excepciones:**
- Si durante la creación del pedido un menú deja de estar disponible, el sistema notifica inmediatamente al usuario.
- Si hay problemas de conexión, el pedido se guarda localmente y se sincroniza cuando la conexión se restablece.

**Frecuencia de uso:** Muy frecuente, varias veces por hora durante el servicio.

---

### CU-R17: Editar Pedido

**Nombre:** Editar Pedido  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite modificar un pedido existente que aún no ha sido completado.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- El pedido existe y no está en estado "completado" o "pagado".

**Flujo Principal:**
1. El usuario busca y selecciona el pedido que desea modificar.
2. El usuario selecciona la opción "Editar pedido".
3. El sistema muestra la información actual del pedido con opción de editar ítems.
4. El usuario puede agregar nuevos ítems, eliminar existentes o modificar cantidades.
5. El sistema recalcula el total del pedido en tiempo real.
6. El usuario confirma las modificaciones.
7. El sistema actualiza el pedido y notifica a los roles pertinentes sobre los cambios.

**Flujos Alternativos:**
- Si el pedido ya está en preparación, el sistema muestra una advertencia antes de permitir cambios.
- Si se añaden nuevos ítems a un pedido en preparación, estos se marcan como "agregados posteriormente".
- El usuario puede cambiar el cliente asociado al pedido si es necesario.

**Postcondiciones:**
- El pedido queda actualizado con los cambios realizados.
- El inventario se ajusta según los cambios en los ítems.
- Se notifica a la cocina sobre los cambios si el pedido ya está en preparación.

**Excepciones:**
- Si se intentan agregar menús que ya no están disponibles, el sistema muestra una advertencia.
- Si el pedido ha avanzado demasiado en su preparación, algunos cambios podrían estar restringidos.

**Frecuencia de uso:** Ocasional, cuando un cliente solicita modificaciones después de realizar el pedido.

---

### CU-R18: Actualizar Estado de Pedido

**Nombre:** Actualizar Estado de Pedido  
**Actores:** Jefe de Local, Jefe de Turno, Mesero, Cocina  
**Descripción:** Permite actualizar el estado de un pedido a través de su ciclo de vida (recibido, en preparación, listo, entregado, pagado).

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existe al menos un pedido activo en el sistema.

**Flujo Principal:**
1. El usuario accede a la lista de pedidos activos filtrados según su rol.
2. El sistema muestra los pedidos con sus estados actuales y un código de colores.
3. El usuario selecciona el pedido que desea actualizar.
4. El sistema muestra las opciones de estado disponibles según el estado actual y el rol del usuario.
5. El usuario selecciona el nuevo estado.
6. El sistema solicita confirmación del cambio.
7. El usuario confirma el cambio de estado.
8. El sistema actualiza el estado y notifica a los roles relevantes.

**Flujos Alternativos:**
- Cocina puede marcar pedidos individuales o múltiples como "en preparación" o "listos para servir".
- Meseros pueden marcar pedidos como "entregados" directamente desde dispositivos móviles.
- El sistema permite añadir notas al cambiar el estado (por ejemplo, razones de retraso).

**Postcondiciones:**
- El estado del pedido se actualiza en tiempo real para todos los usuarios.
- Se registra el historial de cambios de estado con marca de tiempo y usuario.
- Se envían notificaciones a los usuarios relevantes (por ejemplo, notificar a meseros cuando un pedido está listo).

**Excepciones:**
- Si se intenta cambiar a un estado inválido según el flujo de trabajo, el sistema muestra un mensaje de error.

**Frecuencia de uso:** Muy frecuente, cada pedido cambia de estado varias veces durante su ciclo de vida.

**Notas:** Este caso de uso representa una mejora significativa sobre el sistema anterior, permitiendo una comunicación fluida entre cocina y personal de servicio.

---

### CU-R19: Cancelar Pedido

**Nombre:** Cancelar Pedido  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite cancelar un pedido existente que aún no ha sido completamente procesado.

**Precondiciones:**
- El usuario ha iniciado sesión con los permisos adecuados.
- El pedido existe y no está en estado "completado" o "pagado".

**Flujo Principal:**
1. El usuario busca y selecciona el pedido que desea cancelar.
2. El usuario selecciona la opción "Cancelar pedido".
3. El sistema solicita un motivo para la cancelación y muestra opciones comunes.
4. El usuario selecciona o ingresa el motivo de la cancelación.
5. El sistema solicita confirmación de la acción.
6. El usuario confirma la cancelación.
7. El sistema actualiza el estado del pedido a "cancelado" y libera los ingredientes reservados.

**Flujos Alternativos:**
- Si el pedido ya está en preparación, se requiere autorización de un Jefe de Turno o Jefe de Local.
- Si ya se emitió una boleta, el sistema sugiere realizar un procedimiento de devolución.
- El sistema permite cancelar ítems individuales en lugar del pedido completo.

**Postcondiciones:**
- El pedido queda marcado como "cancelado" en el sistema.
- Se liberan los ingredientes reservados de vuelta al inventario.
- Se registra el motivo de la cancelación y quién la autorizó.
- Se generan alertas para análisis posterior si hay muchas cancelaciones similares.

**Excepciones:**
- Si el pedido ya fue pagado, el sistema muestra el proceso para realizar un reembolso en lugar de una simple cancelación.

**Frecuencia de uso:** Ocasional, principalmente por cambios de decisión del cliente o errores en el pedido.

---

### CU-R20: Ver Pedidos Pendientes

**Nombre:** Ver Pedidos Pendientes  
**Actores:** Jefe de Local, Jefe de Turno, Cocina  
**Descripción:** Permite al personal de cocina visualizar los pedidos que necesitan prepararse.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen pedidos en estado "recibido" o "en preparación".

**Flujo Principal:**
1. El usuario de cocina accede a la pantalla de "Pedidos pendientes".
2. El sistema muestra una lista organizada de todos los pedidos pendientes con:
   - Hora de recepción
   - Tiempo de espera actual
   - Mesa o cliente asociado
   - Ítems a preparar con sus especificaciones
3. Los pedidos se ordenan automáticamente por prioridad y tiempo de espera.
4. El usuario puede filtrar o reorganizar la vista según diferentes criterios.
5. El usuario puede seleccionar un pedido para ver los detalles completos.
6. El usuario puede marcar ítems individuales o pedidos completos como "en preparación" o "listos".

**Flujos Alternativos:**
- La pantalla se actualiza en tiempo real cuando llegan nuevos pedidos con alertas visuales y sonoras.
- El usuario puede enviar mensajes al personal de servicio sobre problemas específicos con un pedido.

**Postcondiciones:**
- La cocina tiene una visión clara de su carga de trabajo actual.
- Los meseros pueden ver el estado de preparación de sus pedidos.

**Excepciones:**
- Si hay sobrecarga de pedidos, el sistema sugiere tiempos de espera estimados para informar a los clientes.

**Frecuencia de uso:** Constante durante las horas de servicio.

# SISTEMA REFACTORIZADO (PARTE 2)

Esta sección detalla la segunda parte de los casos de uso del sistema refactorizado, enfocándose en las funcionalidades completamente nuevas que no existían en el sistema anterior.

## Gestión de Mesas

### CU-R21: Registrar Mesa

**Nombre:** Registrar Mesa  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite añadir una nueva mesa al sistema.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.

**Flujo Principal:**
1. El usuario selecciona la opción "Gestionar mesas" en el menú.
2. El usuario selecciona "Agregar nueva mesa".
3. El sistema muestra un formulario con campos para:
   - Número de mesa
   - Capacidad (número de personas)
   - Ubicación/zona del restaurante
   - Características especiales (ej. exterior, privada)
4. El usuario completa la información requerida.
5. El usuario posiciona la mesa en el mapa visual del restaurante usando arrastrar y soltar.
6. El usuario confirma la creación de la mesa.

**Flujos Alternativos:**
- El sistema permite la creación masiva de mesas secuenciales.
- El usuario puede duplicar una mesa existente para crear una similar.

**Postcondiciones:**
- La nueva mesa queda registrada en el sistema.
- La mesa aparece en el mapa visual con estado "libre".

**Excepciones:**
- Si ya existe una mesa con el mismo número, el sistema muestra un error.
- Si se intenta posicionar la mesa en un lugar ocupado del mapa, el sistema sugiere una posición alternativa.

**Frecuencia de uso:** Rara, principalmente cuando se modifica la distribución física del restaurante.

### CU-R22: Asignar Cliente a Mesa

**Nombre:** Asignar Cliente a Mesa  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite asignar un cliente a una mesa específica y marcarla como ocupada.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Hay al menos una mesa disponible.
- El cliente está registrado en el sistema o se registrará durante el proceso.

**Flujo Principal:**
1. El usuario accede al mapa visual de mesas del restaurante.
2. El sistema muestra el estado de todas las mesas (libre, ocupada, reservada, en limpieza).
3. El usuario selecciona una mesa disponible.
4. El sistema muestra las opciones de asignación.
5. El usuario busca y selecciona un cliente existente o crea uno nuevo.
6. El usuario especifica el número de personas y opcionalmente información adicional.
7. El sistema registra la asignación y cambia el estado de la mesa a "ocupada".
8. El sistema inicia automáticamente el contador de tiempo de ocupación.

**Flujos Alternativos:**
- El usuario puede utilizar la función de arrastrar y soltar para mover clientes de una mesa a otra.
- Si una mesa está reservada, el usuario puede confirmar la llegada del cliente con la reserva.

**Postcondiciones:**
- La mesa queda marcada como ocupada en el sistema.
- Se inicia el registro de tiempo de ocupación para análisis de rotación.
- El mesero asignado a la mesa recibe una notificación en su dispositivo.

**Excepciones:**
- Si todas las mesas están ocupadas, el sistema puede gestionar una lista de espera.

**Frecuencia de uso:** Muy frecuente durante las horas de servicio.

**Notas:** Esta nueva funcionalidad proporciona una visualización clara del estado del restaurante y optimiza la asignación de mesas según el tamaño de los grupos.

---

### CU-R23: Cambiar Estado de Mesa

**Nombre:** Cambiar Estado de Mesa  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite actualizar el estado actual de una mesa (libre, ocupada, reservada, en limpieza).

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- La mesa existe en el sistema.

**Flujo Principal:**
1. El usuario accede al mapa de mesas del restaurante.
2. El usuario selecciona la mesa cuyo estado desea cambiar.
3. El sistema muestra las opciones de estado disponibles según el estado actual:
   - Libre → Ocupada, Reservada
   - Ocupada → En limpieza, Libre (cerrando cuenta)
   - Reservada → Ocupada, Libre (cancelación)
   - En limpieza → Libre
4. El usuario selecciona el nuevo estado.
5. Si es necesario, el sistema solicita información adicional (como hora de reserva).
6. El usuario confirma el cambio.
7. El sistema actualiza el estado de la mesa y notifica a los roles relevantes.

**Flujos Alternativos:**
- El usuario puede añadir notas al cambio de estado (ej. "Cliente esperando en bar").
- El sistema puede cambiar automáticamente estados según eventos (ej. pago completado → en limpieza).
- Un mesero puede agrupar mesas para grupos grandes.

**Postcondiciones:**
- El estado de la mesa se actualiza en tiempo real para todos los usuarios.
- Se inician o detienen contadores de tiempo según el estado (tiempo de ocupación, tiempo de limpieza).

**Excepciones:**
- Si se intenta un cambio de estado no permitido, el sistema muestra un error explicativo.

**Frecuencia de uso:** Muy frecuente durante las horas de servicio.

---

### CU-R24: Calcular Tiempo de Ocupación

**Nombre:** Calcular Tiempo de Ocupación  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite monitorear y analizar el tiempo que cada mesa permanece ocupada.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen mesas registradas en el sistema con estados activos.

**Flujo Principal:**
1. El sistema inicia automáticamente un contador cuando una mesa cambia a estado "ocupada".
2. El usuario puede ver el tiempo transcurrido para cada mesa ocupada en el mapa de mesas.
3. El sistema utiliza códigos de color para indicar tiempos de ocupación:
   - Verde: Dentro del tiempo promedio
   - Amarillo: Superando el tiempo promedio
   - Rojo: Tiempo excesivamente largo
4. El usuario puede seleccionar la opción "Análisis de tiempos" para ver estadísticas detalladas.
5. El sistema muestra tiempo promedio por mesa, por hora del día y por tamaño de grupo.

**Flujos Alternativos:**
- El sistema puede generar alertas cuando una mesa supera significativamente el tiempo promedio.
- Los gerentes pueden ver análisis comparativos entre diferentes días o temporadas.
- El sistema puede sugerir reasignaciones de mesas para optimizar el flujo de clientes.

**Postcondiciones:**
- Se registran los tiempos de ocupación para análisis posteriores.
- Se generan recomendaciones para optimizar la rotación de mesas.

**Excepciones:**
- Si se detecta un tiempo de ocupación anómalo, el sistema solicita verificación.

**Frecuencia de uso:** Automático durante toda la operación del restaurante, consulta frecuente por gerentes.

---

## Sistema de Delivery

### CU-R25: Registrar Pedido Delivery

**Nombre:** Registrar Pedido Delivery  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite crear un nuevo pedido para entrega a domicilio, ya sea recibido por teléfono o a través de aplicaciones de delivery.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Hay menús disponibles para delivery.

**Flujo Principal:**
1. El usuario selecciona la opción "Nuevo pedido delivery".
2. El sistema muestra un formulario específico para pedidos a domicilio.
3. El usuario selecciona si el pedido es directo o a través de una aplicación de delivery.
4. El usuario busca o registra al cliente y la dirección de entrega.
5. El usuario selecciona los ítems del pedido.
6. El sistema calcula el total incluyendo costos de envío.
7. El usuario confirma el pedido.
8. El sistema registra el pedido y lo marca como "pendiente de preparación".

**Flujos Alternativos:**
- Si el pedido es a través de una app de delivery, el usuario especifica cuál y registra información adicional como código de pedido externo.
- El sistema puede estimar automáticamente el tiempo de entrega basado en la distancia y el tráfico actual.

**Postcondiciones:**
- El pedido delivery queda registrado en el sistema.
- La cocina recibe una notificación del nuevo pedido.
- El pedido aparece en el panel de control de delivery con su estado.

**Excepciones:**
- Si la dirección está fuera del área de cobertura, el sistema muestra una advertencia.
- Si algún menú no está disponible para delivery, el sistema lo indica.

**Frecuencia de uso:** Frecuente, especialmente durante horas pico y fines de semana.

**Notas:** Esta es una funcionalidad completamente nueva que permite al restaurante expandir sus canales de venta.

---

### CU-R26: Asignar Repartidor

**Nombre:** Asignar Repartidor  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite asignar un repartidor a un pedido de delivery listo para ser entregado.

**Precondiciones:**
- El usuario ha iniciado sesión con los permisos adecuados.
- Existe un pedido delivery en estado "listo para envío".
- Existen repartidores disponibles registrados en el sistema.

**Flujo Principal:**
1. El usuario accede al panel de control de delivery.
2. El sistema muestra los pedidos listos para envío sin repartidor asignado.
3. El usuario selecciona un pedido específico.
4. El sistema muestra la lista de repartidores disponibles con su estado actual.
5. El usuario asigna un repartidor al pedido.
6. El sistema actualiza el estado del pedido a "en ruta" y registra la hora de salida.
7. El sistema envía una notificación al repartidor con los detalles del pedido.

**Flujos Alternativos:**
- Si el pedido es a través de una app externa, el sistema registra el repartidor asignado por la plataforma.
- El sistema puede sugerir automáticamente el mejor repartidor según proximidad, carga de trabajo y ruta.

**Postcondiciones:**
- El pedido queda asociado a un repartidor específico.
- Se inicia el seguimiento del tiempo de entrega.
- El cliente puede recibir una notificación con la información estimada de entrega.

**Excepciones:**
- Si no hay repartidores disponibles, el sistema muestra una alerta y sugiere opciones para gestionar el retraso.

**Frecuencia de uso:** Frecuente durante el servicio de delivery.

---

### CU-R27: Seguir Estado de Entrega

**Nombre:** Seguir Estado de Entrega  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite monitorear el estado actual de los pedidos de delivery desde su preparación hasta su entrega.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen pedidos de delivery activos en el sistema.

**Flujo Principal:**
1. El usuario accede a la sección "Seguimiento de Delivery".
2. El sistema muestra todos los pedidos de delivery activos con su estado actual:
   - En preparación
   - Listo para envío
   - En camino
   - Entregado
   - Problemas de entrega
3. El usuario puede filtrar por estado, repartidor o zona de entrega.
4. El usuario puede seleccionar un pedido para ver detalles completos.
5. El sistema muestra en un mapa la ubicación aproximada del repartidor (si está integrado).
6. El sistema muestra tiempos estimados de entrega y alertas si hay retrasos.

**Flujos Alternativos:**
- El usuario puede comunicarse con el repartidor a través del sistema.
- El sistema permite registrar incidencias en la entrega.
- En caso de pedidos a través de plataformas externas, el sistema muestra el estado según la información disponible de la API.

**Postcondiciones:**
- Se mantiene un registro actualizado del estado de cada entrega.
- Se generan estadísticas de tiempos de entrega y eficiencia.

**Excepciones:**
- Si se pierde la comunicación con un repartidor, el sistema marca el pedido para seguimiento especial.

**Frecuencia de uso:** Constante durante las operaciones de delivery.

---

## Sistema de Pagos

### CU-R28: Registrar Medio de Pago

**Nombre:** Registrar Medio de Pago  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite configurar y activar diferentes métodos de pago aceptados por el restaurante.

**Precondiciones:**
- El usuario ha iniciado sesión como Jefe de Local o Jefe de Turno.

**Flujo Principal:**
1. El usuario accede a la sección "Configuración de pagos".
2. El usuario selecciona "Agregar medio de pago".
3. El sistema muestra un formulario con opciones como:
   - Nombre del medio de pago
   - Tipo (efectivo, tarjeta, transferencia, apps)
   - Comisión asociada
   - Información adicional (terminales, cuentas bancarias)
   - Estado (activo/inactivo)
4. El usuario completa la información requerida.
5. El usuario confirma la creación del nuevo medio de pago.

**Flujos Alternativos:**
- El usuario puede modificar o desactivar temporalmente un medio de pago existente.
- El sistema permite configurar reglas específicas para cada medio de pago (montos mínimos, máximos).

**Postcondiciones:**
- El nuevo medio de pago queda disponible para ser utilizado en transacciones.
- Los usuarios con permisos verán la nueva opción al procesar pagos.

**Excepciones:**
- Si se intenta configurar una integración con un servicio externo, el sistema valida las credenciales antes de activarlo.

**Frecuencia de uso:** Ocasional, principalmente cuando se incorporan nuevos métodos de pago.

---

### CU-R29: Procesar Pago

**Nombre:** Procesar Pago  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite registrar y procesar el pago de un pedido utilizando diferentes medios de pago.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existe un pedido en estado "entregado" o "listo para pago".

**Flujo Principal:**
1. El usuario accede al pedido que se va a pagar.
2. El sistema muestra el detalle del pedido con el monto total.
3. El usuario selecciona la opción "Procesar pago".
4. El sistema muestra los medios de pago disponibles (efectivo, tarjeta, transferencia, aplicaciones).
5. El usuario selecciona el medio de pago deseado.
6. El sistema solicita la información específica para ese medio de pago.
7. El usuario ingresa los datos necesarios.
8. El sistema registra el pago y actualiza el estado del pedido a "pagado".
9. El sistema genera el comprobante correspondiente.

**Flujos Alternativos:**
- El sistema permite dividir el pago entre múltiples medios de pago.
- Si el cliente desea una factura en lugar de boleta, el usuario puede solicitar los datos adicionales necesarios.
- El usuario puede aplicar descuentos o propinas antes de finalizar el pago, con la autorización correspondiente.

**Postcondiciones:**
- El pedido queda marcado como pagado.
- Se genera un comprobante digital que puede ser impreso o enviado por email.
- Se registra la transacción para propósitos contables.

**Excepciones:**
- Si la transacción electrónica es rechazada, el sistema muestra el error específico y permite intentar con otro medio de pago.

**Frecuencia de uso:** Muy frecuente, cada pedido termina con un proceso de pago.

**Notas:** Esta nueva funcionalidad elimina la necesidad de sistemas de pago separados, centralizando todas las transacciones.

---

### CU-R30: Emitir Comprobante

**Nombre:** Emitir Comprobante  
**Actores:** Jefe de Local, Jefe de Turno, Mesero  
**Descripción:** Permite generar y entregar el comprobante fiscal correspondiente a un pago.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existe un pedido con pago procesado.

**Flujo Principal:**
1. Tras procesar un pago exitosamente, el sistema ofrece automáticamente las opciones de comprobante.
2. El usuario selecciona el tipo de comprobante requerido (boleta, factura, comprobante simplificado).
3. Si es factura, el sistema solicita los datos fiscales necesarios (que pueden autocompletarse si el cliente está registrado).
4. El usuario confirma los detalles del comprobante.
5. El sistema genera el documento fiscal con número único y cumpliendo requisitos legales.
6. El usuario selecciona el método de entrega (impresión, email, mensajería).
7. El sistema envía o imprime el comprobante según la selección.

**Flujos Alternativos:**
- El usuario puede generar un comprobante para un pago anterior desde el historial de transacciones.
- Para clientes frecuentes, el sistema recuerda su preferencia de tipo de comprobante y método de entrega.
- El sistema permite generar comprobantes consolidados para múltiples pedidos del mismo cliente.

**Postcondiciones:**
- Se genera y entrega el comprobante fiscal.
- El comprobante queda registrado en el sistema para propósitos contables.
- Se cumple con los requisitos fiscales correspondientes.

**Excepciones:**
- Si hay problemas con la impresora, el sistema ofrece alternativas digitales.
- Si faltan datos fiscales obligatorios, el sistema no permite continuar hasta completarlos.

**Frecuencia de uso:** Para cada transacción que requiera comprobante fiscal.

---

## Dashboard Analítico

### CU-R31: Visualizar KPIs

**Nombre:** Visualizar KPIs  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite visualizar indicadores clave de desempeño del restaurante a través de un panel interactivo.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- Existen datos suficientes para generar métricas significativas.

**Flujo Principal:**
1. El usuario accede a la sección "Dashboard" del sistema.
2. El sistema muestra por defecto los KPIs del día actual comparados con el día anterior.
3. El usuario puede ajustar el período de tiempo a analizar (día, semana, mes, trimestre, año).
4. El sistema actualiza los gráficos y métricas según el período seleccionado.
5. El usuario puede explorar diferentes categorías de KPIs (ventas, inventario, eficiencia, satisfacción).
6. El usuario puede interactuar con los gráficos para obtener información más detallada.

**Flujos Alternativos:**
- El usuario puede guardar configuraciones personalizadas del dashboard.
- El sistema permite programar informes periódicos automáticos por email.
- El usuario puede exportar cualquier gráfico o tabla en formato PDF, Excel o CSV.

**Postcondiciones:**
- El usuario obtiene insights sobre el rendimiento del negocio para toma de decisiones.

**Excepciones:**
- Si no hay datos suficientes para alguna métrica, el sistema muestra un mensaje informativo.

**Frecuencia de uso:** Diaria para análisis operativo, semanal/mensual para análisis estratégico.

**Notas:** Este módulo representa una mejora significativa sobre los reportes estáticos del sistema anterior, permitiendo análisis dinámicos y profundos del negocio.

---

### CU-R32: Filtrar por Periodo

**Nombre:** Filtrar por Periodo  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite ajustar el rango de tiempo para el análisis de datos en el dashboard analítico.

**Precondiciones:**
- El usuario ha iniciado sesión en el sistema con los permisos adecuados.
- El usuario está visualizando el dashboard analítico.
- Existen datos para analizar en el sistema.

**Flujo Principal:**
1. El usuario selecciona la opción de filtro de tiempo en el dashboard.
2. El sistema muestra las opciones predefinidas (hoy, semana actual, mes actual, año actual) y la opción de periodo personalizado.
3. Si el usuario selecciona un periodo predefinido, el sistema actualiza inmediatamente todos los gráficos y KPIs.
4. Si el usuario selecciona "personalizado", el sistema muestra un selector de fechas.
5. El usuario selecciona las fechas de inicio y fin para el análisis.
6. El sistema valida que el rango sea coherente.
7. El usuario confirma la selección.
8. El sistema recalcula y actualiza todos los datos visualizados según el periodo seleccionado.

**Flujos Alternativos:**
- El usuario puede comparar el periodo seleccionado con un periodo anterior (mismo rango).
- El usuario puede guardar filtros personalizados frecuentemente utilizados.
- El sistema permite excluir días específicos del análisis (ej. días cerrados por feriado).

**Postcondiciones:**
- Todos los gráficos y métricas se actualizan para reflejar los datos del periodo seleccionado.
- La selección de periodo se mantiene mientras el usuario navega entre diferentes secciones del dashboard.

**Excepciones:**
- Si se selecciona un periodo sin datos, el sistema muestra una advertencia.
- Si se selecciona un periodo muy extenso, el sistema puede mostrar advertencias sobre el rendimiento.

**Frecuencia de uso:** Muy frecuente durante el análisis de datos.

---

### CU-R33: Exportar Reportes PDF

**Nombre:** Exportar Reportes PDF  
**Actores:** Jefe de Local, Jefe de Turno  
**Descripción:** Permite generar y exportar reportes detallados en formato PDF u otros formatos.

**Precondiciones:**
- El usuario ha iniciado sesión con los permisos adecuados.
- El usuario ha configurado los filtros y visualizaciones deseadas en el dashboard.

**Flujo Principal:**
1. El usuario configura el dashboard con las métricas y periodo deseados.
2. El usuario selecciona la opción "Exportar reporte".
3. El sistema muestra opciones de configuración:
   - Formato (PDF, Excel, CSV)
   - Secciones a incluir
   - Información de encabezado/pie de página
   - Orientación y tamaño de página
4. El usuario configura las opciones y confirma la exportación.
5. El sistema genera el documento según las especificaciones.
6. El sistema ofrece opciones para descargar o enviar por email el reporte.

**Flujos Alternativos:**
- El usuario puede programar la generación automática de reportes con una frecuencia específica.
- El usuario puede guardar configuraciones de reportes para uso frecuente.

**Postcondiciones:**
- Se genera el documento en el formato solicitado.
- Opcionalmente, el reporte se envía a los destinatarios especificados.
- Se registra la exportación en el historial de reportes.

**Excepciones:**
- Si la generación falla debido a la complejidad o cantidad de datos, el sistema sugiere simplificar los filtros.
- Si hay problemas con el formato de salida, el sistema ofrece alternativas.

**Frecuencia de uso:** Semanal o mensual para reportes gerenciales o contables.

---

# COMPARATIVA DE CASOS DE USO

La siguiente tabla presenta un resumen de los principales cambios y mejoras entre el sistema actual y el sistema refactorizado:

| Módulo | Sistema Actual | Sistema Refactorizado | Principales Beneficios |
|--------|--------------|---------------------|----------------------|
| **Gestión de Clientes** | 5 casos de uso limitados al Jefe de Local | 5 casos de uso con acceso distribuido entre 3 roles | Mayor agilidad en registro y atención, validación en tiempo real, acceso descentralizado |
| **Gestión de Ingredientes** | 5 casos de uso centralizados | 5 casos de uso con participación del personal de cocina | Actualización en tiempo real del inventario, alertas automáticas, mejor control de stock |
| **Gestión de Menús** | 5 casos de uso manuales | 5 casos de uso con verificación automática | Prevención de ofertas de menús no disponibles, cálculo automático de costos y márgenes |
| **Gestión de Pedidos** | 6 casos de uso centralizados | 5 casos de uso distribuidos entre múltiples roles | Reducción de tiempos de espera, comunicación en tiempo real, mejor coordinación entre áreas |
| **Reportes y Análisis** | 3 casos de uso básicos | 3 casos de uso con análisis avanzado | Toma de decisiones basada en datos, visualizaciones interactivas, filtros dinámicos |
| **Gestión de Mesas** | No existía | 3 nuevos casos de uso | Optimización del espacio, mejor rotación de mesas, control visual del restaurante |
| **Sistema de Delivery** | No existía | 3 nuevos casos de uso | Nuevos canales de venta, integración con plataformas externas, seguimiento de entregas |
| **Sistema de Pagos** | No existía | 3 nuevos casos de uso | Múltiples métodos de pago, generación automática de comprobantes, control financiero |
| **Dashboard Analítico** | No existía | 3 nuevos casos de uso | Métricas en tiempo real, análisis profundo de datos, exportación de reportes personalizados |

## Evolución de Roles y Responsabilidades

| Rol | Sistema Actual | Sistema Refactorizado | Beneficio |
|-----|---------------|------------------------|-----------|
| **Jefe de Local** | 24 casos de uso (100% del sistema) | 33 casos de uso (100% del sistema refactorizado) | Acceso a nuevas funcionalidades analíticas y estratégicas |
| **Jefe de Turno** | No existía como rol | 17 casos de uso (52%) | Distribución eficiente de responsabilidades administrativas |
| **Mesero** | No tenía acceso al sistema | 16 casos de uso (48%) | Atención más ágil y personalizada al cliente |
| **Cocina** | No tenía acceso al sistema | 6 casos de uso (18%) | Mejor control de ingredientes y comunicación en tiempo real |

# CONCLUSIONES

El análisis detallado de los casos de uso extendidos para ambas versiones del sistema revela transformaciones fundamentales en el modo de operar del restaurante:

1. **Distribución de responsabilidades:** El sistema refactorizado redistribuye las tareas que originalmente estaban concentradas en el Jefe de Local, asignándolas a los roles más apropiados dentro de la organización. Esta descentralización no solo alivia la carga de trabajo del administrador, sino que también empodera a otros miembros del equipo para ejecutar las tareas que naturalmente corresponden a sus funciones.

2. **Automatización inteligente:** Muchos procesos que requerían intervención manual constante ahora cuentan con automatizaciones que reducen errores y tiempo invertido. La verificación automática de disponibilidad de menús según el inventario de ingredientes es un ejemplo claro de cómo la tecnología puede prevenir problemas antes de que afecten al cliente.

3. **Comunicación integrada:** El nuevo sistema facilita el flujo de información entre diferentes áreas del restaurante. La actualización del estado de pedidos, visible para todos los roles relevantes, elimina la necesidad de comunicación verbal constante entre cocina y servicio, reduciendo malentendidos y retrasos.

4. **Expansión de capacidades:** La inclusión de módulos completamente nuevos como la gestión de mesas, sistema de delivery y procesamiento de pagos diversificados permite al restaurante ampliar su oferta de servicios y adaptarse a las expectativas actuales del mercado.

5. **Toma de decisiones basada en datos:** El dashboard analítico transforma datos operativos en insights accionables, permitiendo a los jefes identificar tendencias, problemas y oportunidades que serían difíciles de detectar mediante observación directa o reportes básicos.

6. **Mejora en la experiencia del cliente:** Aunque no participan directamente en el sistema, los clientes son los beneficiarios finales de estas mejoras. Desde la reducción en tiempos de espera hasta la prevención de situaciones donde un plato no está disponible, cada optimización del sistema se traduce en una experiencia más satisfactoria.

7. **Adaptabilidad y escalabilidad:** La arquitectura refactorizada no solo resuelve problemas actuales, sino que establece una base sólida para futuras expansiones. La clara separación de responsabilidades en el sistema facilita la incorporación de nuevas funcionalidades sin afectar los componentes existentes.

En resumen, el paso del sistema actual al refactorizado representa mucho más que una actualización tecnológica; constituye una reconfiguración del modelo operativo del restaurante que impacta positivamente en su eficiencia, capacidad de servicio y potencial de crecimiento. La inversión en esta transformación digital promete retornos significativos tanto en términos de satisfacción del cliente como en resultados financieros a mediano y largo plazo.