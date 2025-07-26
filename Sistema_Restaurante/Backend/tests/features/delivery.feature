# language: es

Característica: Sistema de Delivery
  Como jefe de local
  Quiero gestionar pedidos de delivery
  Para ofrecer servicio de entrega a domicilio

  Escenario: Registrar pedido delivery directo
    Dado que no existe un pedido delivery con ID 100
    Y que existe un cliente con nombre "Pedro Gonzalez"
    Cuando creo un pedido delivery directo con ID 100, cliente "Pedro Gonzalez" y dirección "Av. Principal 123"
    Entonces el pedido delivery 100 debe existir en el sistema
    Y debe tener estado "pendiente"
    Y debe tener dirección "Av. Principal 123"

  Escenario: Registrar pedido desde app externa
    Dado que existe una app de delivery "Rappi" activa
    Y que no existe un pedido delivery con código externo "RPP-456"
    Cuando creo un pedido desde app externa "Rappi" con código "RPP-456"
    Entonces el pedido debe estar registrado como delivery externo
    Y debe tener la app "Rappi" asociada

  Escenario: Asignar repartidor a pedido
    Dado que existe un pedido delivery con ID 100 en estado "listo"
    Y que existe un repartidor "Juan Pérez" disponible
    Cuando asigno el repartidor "Juan Pérez" al pedido 100
    Entonces el pedido 100 debe tener repartidor "Juan Pérez" asignado
    Y el repartidor debe cambiar a estado "en_ruta"

  Escenario: Seguir estado de entrega
    Dado que existe un pedido delivery con ID 100 en estado "en_ruta"
    Y que tiene repartidor "Juan Pérez" asignado
    Cuando consulto el estado del pedido 100
    Entonces debo obtener la información del repartidor
    Y debo obtener el estado actual "en_ruta"
    Y debo obtener tiempo estimado de entrega

  Escenario: Completar entrega
    Dado que existe un pedido delivery con ID 100 en estado "en_ruta"
    Cuando el repartidor marca el pedido como "entregado"
    Entonces el pedido 100 debe cambiar a estado "entregado"
    Y el repartidor debe volver a estado "disponible"

  Escenario: Calcular comisión de app externa
    Dado que existe una app "Rappi" con comisión 15%
    Y que existe un pedido desde "Rappi" por $20000
    Cuando calculo la comisión del pedido
    Entonces la comisión debe ser $3000
    Y el monto neto debe ser $17000
