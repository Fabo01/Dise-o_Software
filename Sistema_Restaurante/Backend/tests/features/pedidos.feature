# language: es

Característica: Gestión de pedidos
  Como mesero o administrador
  Quiero poder crear, consultar, actualizar y eliminar pedidos
  Para gestionar correctamente los pedidos de los clientes

  Escenario: Crear un pedido
    Dado que no existe un pedido con número 100
    Cuando creo un pedido con número 100 y cliente "Pedro"
    Entonces el pedido 100 debe existir en el sistema con cliente "Pedro"

  Escenario: Editar un pedido
    Dado que existe un pedido con número 101
    Cuando actualizo el pedido 101 a cliente "Ana"
    Entonces el pedido 101 debe tener cliente "Ana"

  Escenario: Eliminar un pedido
    Dado que existe un pedido con número 102
    Cuando elimino el pedido 102
    Entonces el pedido 102 no debe existir en el sistema

  Escenario: Listar pedidos
    Dado que existen pedidos registrados
    Cuando solicito la lista de pedidos
    Entonces debo obtener una lista con los pedidos existentes
