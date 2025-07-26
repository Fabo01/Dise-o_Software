# language: es

Característica: Dashboard Analytics
  Como jefe de local o jefe de turno
  Quiero visualizar KPIs y analytics del restaurante
  Para tomar decisiones informadas sobre el negocio

  Escenario: Visualizar KPIs del día actual
    Dado que existen pedidos y transacciones registradas hoy
    Cuando accedo al dashboard de analytics para el día actual
    Entonces debo ver el total de ventas del día
    Y debo ver el número de pedidos del día
    Y debo ver el ticket promedio
    Y debo ver el número de clientes activos

  Escenario: Filtrar datos por período personalizado
    Dado que existen datos históricos en el sistema
    Cuando filtro el dashboard por período del 1 al 31 de enero 2024
    Entonces debo ver datos solo de ese período
    Y los gráficos deben actualizarse con los datos filtrados
    Y debo ver la comparación con el período anterior

  Escenario: Visualizar gráfico de ventas por día
    Dado que existen ventas registradas en los últimos 7 días
    Cuando accedo al gráfico de ventas por día
    Entonces debo ver una línea de tiempo con las ventas diarias
    Y cada punto debe mostrar el monto de ventas del día
    Y debo poder interactuar con los puntos para ver detalles

  Escenario: Ver métodos de pago más utilizados
    Dado que existen transacciones con diferentes métodos de pago
    Cuando visualizo el gráfico de métodos de pago
    Entonces debo ver un gráfico circular con los métodos más usados
    Y cada segmento debe mostrar el porcentaje de uso
    Y debo ver el ranking de métodos por popularidad

  Escenario: Identificar menús más populares
    Dado que existen pedidos con diferentes menús
    Cuando consulto los menús más populares
    Entonces debo ver un ranking de menús por cantidad de pedidos
    Y cada menú debe mostrar su nombre y total de pedidos
    Y debo poder filtrar por categoría de menú

  Escenario: Monitorear inventario crítico
    Dado que existen ingredientes con stock bajo el nivel crítico
    Cuando accedo al dashboard
    Entonces debo ver una alerta de ingredientes críticos
    Y debo ver el número de ingredientes en estado crítico
    Y debo poder acceder a los detalles del inventario

  Escenario: Exportar reporte en PDF
    Dado que estoy visualizando el dashboard con datos del mes actual
    Cuando selecciono exportar reporte en formato PDF
    Entonces el sistema debe generar un archivo PDF
    Y debe incluir todos los gráficos y métricas visibles
    Y debe incluir el período de análisis en el reporte

  Escenario: Exportar datos en Excel
    Dado que estoy visualizando KPIs de ventas
    Cuando selecciono exportar en formato Excel
    Entonces el sistema debe generar un archivo Excel
    Y debe incluir tablas con datos de ventas, inventario y operaciones
    Y los datos deben estar organizados en hojas separadas

  Escenario: Ver tendencias de crecimiento
    Dado que existen datos del período actual y anterior
    Cuando visualizo las tendencias de crecimiento
    Entonces debo ver el porcentaje de crecimiento en ventas
    Y debo ver el porcentaje de crecimiento en número de pedidos
    Y debo ver indicadores visuales de mejora o deterioro

  Escenario: Analizar pedidos por hora del día
    Dado que existen pedidos registrados en diferentes horas
    Cuando visualizo el gráfico de pedidos por hora
    Entonces debo ver barras que representen la cantidad de pedidos por hora
    Y debo poder identificar las horas pico del restaurante
    Y debo ver el promedio de pedidos por hora
