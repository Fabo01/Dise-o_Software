# Diagramas de Secuencia - Sistema de Gestión de Restaurante

Este documento presenta los diagramas de secuencia para cada caso de uso, tanto del sistema actual como del sistema refactorizado. Estos diagramas muestran la interacción entre actores, componentes y objetos a través del tiempo, ilustrando el flujo de mensajes y operaciones.

## SISTEMA ACTUAL

El sistema actual opera como una aplicación de escritorio monolítica con una arquitectura simple de tres capas:
- **Interfaz de Usuario**: Implementada con Python y customtkinter
- **Lógica de Negocio**: Módulos funcionales en Python
- **Acceso a Datos**: Conexión directa a SQLite

### Gestión de Clientes

#### CU-A01: Registrar Cliente

![Diagrama Registrar cliente](secuencia/gestion%20de%20clientes/registrar_client.webp)

#### CU-A02: Editar Cliente

![Diagrama Editar Cliente](secuencia/gestion%20de%20clientes/editar_cliente.webp)

#### CU-A03: Eliminar Cliente

![Diagrama Eliminar Cliente](secuencia/gestion%20de%20clientes/eliminar_cliente.webp)

#### CU-A04: Buscar Cliente

![Diagrama Buscar Cliente](secuencia/gestion%20de%20clientes/Buscar_cliente.webp)

#### CU-A05: Ver Historial de Pedidos

![Diagrama Ver historial Cliente](secuencia/gestion%20de%20clientes/verhistorial_pedido.webp)

### Gestión de Ingredientes

#### CU-A06: Agregar Ingrediente

![Diagrama Agregar Ingrediente](secuencia/gestion%20de%20ingredientes/agregar_ingrediente.webp)

#### CU-A07: Editar Ingrediente

![Diagrama Editar Ingrediente](secuencia/gestion%20de%20ingredientes/editar_ingrediente.webp)

#### CU-A08: Eliminar Ingrediente

![Diagrama Eliminar Ingrediente](secuencia/gestion%20de%20ingredientes/eliminar_ingrediente.webp)

#### CU-A09: Actualizar Stock

![Diagrama Editar Ingrediente](secuencia/gestion%20de%20ingredientes/editar_ingrediente.webp)

#### CU-A10: Verificar Disponibilidad de Ingredientes

![Diagrama Verificar Disponibilidad Ingrediente](secuencia/gestion%20de%20ingredientes/verificar_disp_ingredientes.webp)

### Gestión de Menús

#### CU-A11: Crear Menú

![Diagrama Crear Menú](secuencia/gestion%20de%20menus/crear_menu.webp)

#### CU-A12: Editar Menú

![Diagrama Editar Menú](secuencia/gestion%20de%20menus/Editar_menu.webp)

#### CU-A13: Eliminar Menú

![Diagrama Eliminar Menú](secuencia/gestion%20de%20menus/Eliminar_menu.webp)

#### CU-A14: Asignar Ingredientes a Menú

![Diagrama Asignar Ingredientes Menú](secuencia/gestion%20de%20menus/asignar_ingrediente_menu.webp)

#### CU-A15: Verificar Disponibilidad de Menú

![Diagrama Verificar Disponibilidad Menú](secuencia/gestion%20de%20menus/verificar_disp_menu.webp)

### Gestión de Pedidos

#### CU-A16: Crear Pedido

![Diagrama Crear Pedido](secuencia/gestion%20de%20pedidos/crear_pedido.webp)

#### CU:A17: Editar Pedido

![Diagrama Editar Pedido](secuencia/gestion%20de%20pedidos/Editar_pedido.webp)

#### CU-A18: Cancelar Pedido

![Diagrama Cancelar Pedido](secuencia/gestion%20de%20pedidos/Cancelar_pedido.webp)

#### CU-A19: Asignar Cliente a Pedido

![Diagrama  Asignar Cliente Pedido](secuencia/gestion%20de%20pedidos/Asignar_Cliente_pedido.webp)

#### CU-A20: Agregar Menús a Pedido

![Diagrama   Agregar Menús Pedido](secuencia/gestion%20de%20pedidos/Agregar_Menus_pedido.webp)

#### CU-A21: Generar Boleta

![Diagrama Generar Boleta](secuencia/gestion%20de%20pedidos/Generar_Boleta.webp)

### Generación de Reportes

#### CU-A22: Generar Reporte de Ventas

![Diagrama Generar Reporte de Ventas](secuencia/generacion%20de%20reportes/generar_reporte_ventas.webp)

#### CU-A23: Ver Estadísticas Básicas

![Diagrama Estadísticas Básicas](secuencia/generacion%20de%20reportes/ver_estadisticas_basicas.webp)

#### CU-24: Ver Uso de Ingredientes

![Diagrama Uso de Ingredientes](secuencia/generacion%20de%20reportes/ver_uso_ingredientes.webp)

## SISTEMA REFACTORIZADO (PARTE 1)

El sistema refactorizado implementa una arquitectura web moderna siguiendo principios de Clean Architecture con las siguientes capas:

### Frontend
- **Componentes UI**: Interfaces de usuario en React
- **Gestión de Estado**: Manejo centralizado del estado con Redux/Context
- **Servicios API**: Comunicación con el backend

### Backend
- **Capa de Presentación**: API Controllers y Serializers
- **Capa de Servicios**: Services, Casos de Uso e Interfaces de Repositories
- **Capa de Dominio**: Entidades, Value Objects y Reglas de Negocio
- **Capa de Infraestructura**: Repositories, ORM y Servicios Externos

### Gestión de Clientes (Refactorizado)

#### CU-R01: Registrar Cliente

![Diagrama Registrar cliente](secuencia/gestion%20de%20clientes%20refactorizado/registrar_clienter.webp)

#### CU-R02: Editar Cliente

![Diagrama Editar cliente](secuencia/gestion%20de%20clientes%20refactorizado/Editar_clienter.webp)

#### CU-R03: Eliminar Cliente

![Diagrama Eliminar cliente](secuencia/gestion%20de%20clientes%20refactorizado/Eliminar_clienter.webp)

#### CU-R04: Buscar Cliente

![Diagrama Buscar cliente](secuencia/gestion%20de%20clientes%20refactorizado/Buscar_clienter.webp)

#### CU-R05: Ver Historial de Pedidos

![Diagrama Historial de Pedidos cliente](secuencia/gestion%20de%20clientes%20refactorizado/ver_historial_pedidos.webp)

### Gestión de Ingredientes (Refactorizado)

#### CU-R06: Agregar Ingrediente

![Diagrama Agregar Ingrediente](secuencia/gestion%20de%20ingredientes%20refactorizado/agregar_ingredientrer.webp)

#### CU-R07: Editar Ingrediente

![Diagrama Editar Ingrediente](secuencia/gestion%20de%20ingredientes%20refactorizado/editar_ingredientrer.webp)

#### CU-R08: Actualizar Stock

![Diagrama Actualizar Stock Ingrediente](secuencia/gestion%20de%20ingredientes%20refactorizado/actualizar_stockr.webp)

#### CU-R09: Eliminar Ingrediente

![Diagrama Eliminar Ingrediente](secuencia/gestion%20de%20ingredientes%20refactorizado/eliminar_ingredienter.webp)

#### CU-R10: Verificar Disponibilidad de Ingredientes

![Diagrama Eliminar Ingrediente](secuencia/gestion%20de%20ingredientes%20refactorizado/verificar_disp_ingredienter.webp)

### Gestión de Menús (Refactorizado)

#### CU-R11: Crear Menú

![Diagrama Crear Menú](secuencia/gestion%20de%20menus%20refactorizado/crear_menur.webp)

#### CU-R12: Editar Menú

![Diagrama Editar Menú](secuencia/gestion%20de%20menus%20refactorizado/Editar_menur.webp)

#### CU-R13: Eliminar Menú

![Diagrama Eliminar Menú](secuencia/gestion%20de%20menus%20refactorizado/eliminar_menur.webp)

#### CU-R14: Verificar Disponibilidad de Menú

![Diagrama Verificar Disponibilidad de Menú](secuencia/gestion%20de%20menus%20refactorizado/ver_menus_dispor.webp)

#### CU-R15: Ver Menús Disponibles

![Diagrama Menús Disponibles](secuencia/gestion%20de%20menus%20refactorizado/ver_menus_dispor.webp)

### Gestión de Pedidos (Refactorizado)

#### CU-R16: Crear Pedido

![Diagrama Crear Pedido](secuencia/gestion%20de%20pedidos%20refactorizados/crear_pedidor.webp)

#### CU-R17: Editar Pedido

![Diagrama Editar Pedido](secuencia/gestion%20de%20pedidos%20refactorizados/Editar_pedidor.webp)

#### CU-R18: Actualizar Estado de Pedido

![Diagrama Actualizar Pedido](secuencia/gestion%20de%20pedidos%20refactorizados/actualizar_estado_pedidor.webp)

#### CU-R19: Cancelar Pedido

![Diagrama Cancelar Pedido](secuencia/gestion%20de%20pedidos%20refactorizados/cancelar_pedidor.webp)

#### CU-R20: Ver Pedidos Pendientes

![Diagrama Pedidos Pendientes](secuencia/gestion%20de%20pedidos%20refactorizados/ver_pedidos_pendientesr.webp)

### Gestión de Mesas (Refactorizado)

#### CU-R21: Registrar Mesa

![Diagrama Registrar Mesa](secuencia/gestion%20de%20mesas%20refactorizado/registrar_mesasr.webp)

#### CU-R22: Asignar Cliente a Mesa

![Diagrama Asignar Cliente a Mesa](secuencia/gestion%20de%20mesas%20refactorizado/asignar_cliente_mesar.webp)

#### CU-R23: Cambiar Estado de Mesa

![Diagrama Cambiar Estado de Mesa](secuencia/gestion%20de%20mesas%20refactorizado/cambio_estado_mesar.webp)

#### CU-R24: Calcular Tiempo de Ocupación

![Diagrama Calcular Tiempo de Ocupación](secuencia/gestion%20de%20mesas%20refactorizado/calcular_tiempo_ocupacionr.webp)

#### CU-R25: Registrar Pedido Delivery

![Diagrama Registrar Pedido Delivery](secuencia/gestion%20de%20mesas%20refactorizado/registrar_pedido_deliveryr.webp)

#### CU-R26: Asignar Repartidor

![Diagrama Asignar Repartidor](secuencia/gestion%20de%20mesas%20refactorizado/asignar_repartidorr.webp)

#### CU-R27: Seguir Estado de Entrega

![Diagrama Seguir Estado de Entrega](secuencia/gestion%20de%20mesas%20refactorizado/seguir_estado_entregar.webp)

### Sistema de Pagos

#### CU-R28: Registrar Medio de Pago

![Diagrama Registrar Medio de Pago](secuencia/sistema%20de%20pagos/registar_medio_pagor.webp)

#### CU-R29: Procesar Pago

![Diagrama Procesar Pago](secuencia/sistema%20de%20pagos/procesar_pagor.webp)

#### CU-R30: Emitir Comprobante

![Diagrama Procesar Pago](secuencia/sistema%20de%20pagos/emitir_comprobanter.webp)

### Dashboard Analítico

#### CU-R31: Visualizar KPIs

![Diagrama Visualizar KPIs](secuencia/dashboard%20analitico/visualizar_kpis.webp)

#### CU-R32: Filtrar por Periodo

![Diagrama Visualizar KPIs](secuencia/dashboard%20analitico/filtrar_periodo.webp)

#### CU-R33: Exportar Reportes PDF

![Diagrama Visualizar KPIs](secuencia/dashboard%20analitico/exportar_reportes_pdf.webp)