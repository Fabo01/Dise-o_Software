# language: es

Característica: Gestión de reportes
  Como gerente o administrador
  Quiero poder generar y consultar reportes
  Para analizar el desempeño y la operación del restaurante

  Escenario: Generar reporte de ventas
    Dado que existen pedidos registrados
    Cuando genero un reporte de ventas
    Entonces debo obtener un reporte con el resumen de ventas

  Escenario: Generar reporte de inventario
    Dado que existen ingredientes registrados
    Cuando genero un reporte de inventario
    Entonces debo obtener un reporte con el estado del inventario
