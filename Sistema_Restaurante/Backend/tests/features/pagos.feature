# language: es

Característica: Sistema de Pagos
  Como mesero o jefe de local
  Quiero procesar pagos de pedidos
  Para completar las transacciones de los clientes

  Escenario: Registrar nuevo medio de pago
    Dado que no existe un medio de pago "Tarjeta Visa"
    Cuando creo un medio de pago "Tarjeta Visa" tipo "tarjeta_credito"
    Entonces el medio de pago "Tarjeta Visa" debe existir en el sistema
    Y debe tener tipo "tarjeta_credito"

  Escenario: Procesar pago en efectivo
    Dado que existe un pedido con ID 100 en estado "entregado"
    Y que existe un medio de pago "Efectivo" activo
    Cuando proceso el pago del pedido 100 con "Efectivo" por $15000
    Entonces debe existir una transacción para el pedido 100
    Y la transacción debe tener estado "exitosa"
    Y el pedido debe cambiar a estado "pagado"

  Escenario: Procesar pago con tarjeta
    Dado que existe un pedido con ID 101 en estado "entregado"
    Y que existe un medio de pago "Tarjeta Débito" con comisión 2%
    Cuando proceso el pago del pedido 101 con "Tarjeta Débito" por $10000
    Entonces debe existir una transacción con monto $10000
    Y la comisión debe ser $200
    Y el monto neto debe ser $9800

  Escenario: Fallar procesamiento de pago
    Dado que existe un pedido con ID 102 en estado "entregado"
    Y que existe un medio de pago "Tarjeta Externa" con validación externa
    Cuando proceso un pago que falla en la validación externa
    Entonces la transacción debe tener estado "fallida"
    Y el pedido debe mantener estado "entregado"

  Escenario: Dividir pago entre múltiples medios
    Dado que existe un pedido con ID 103 por $20000 en estado "entregado"
    Cuando proceso pago parcial con "Efectivo" por $12000
    Y proceso pago parcial con "Tarjeta" por $8000
    Entonces deben existir 2 transacciones para el pedido 103
    Y ambas transacciones deben tener estado "exitosa"
    Y el pedido debe cambiar a estado "pagado"

  Escenario: Generar comprobante de pago
    Dado que existe una transacción exitosa con ID 500
    Cuando genero el comprobante de la transacción 500
    Entonces debe existir un comprobante en formato PDF
    Y debe contener los datos del pedido
    Y debe contener los datos del pago

  Escenario: Consultar historial de transacciones
    Dado que existen transacciones registradas en el sistema
    Cuando consulto el historial de transacciones del día actual
    Entonces debo obtener la lista de transacciones del día
    Y cada transacción debe incluir pedido, medio de pago y estado

  Escenario: Calcular total de ventas por medio de pago
    Dado que existen transacciones exitosas con diferentes medios de pago
    Cuando consulto el resumen de ventas por medio de pago
    Entonces debo obtener el total por cada medio de pago
    Y debo obtener el gran total de todas las ventas
