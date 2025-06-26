# language: es

Característica: Gestión de clientes
  Como administrador o mesero
  Quiero poder crear, consultar, actualizar y eliminar clientes
  Para gestionar correctamente la información de los clientes

  Escenario: Crear un cliente
    Dado que no existe un cliente con nombre "Pedro"
    Cuando creo un cliente con nombre "Pedro", correo "pedro@email.com"
    Entonces el cliente "Pedro" debe existir en el sistema con correo "pedro@email.com"

  Escenario: Editar un cliente
    Dado que existe un cliente con nombre "Ana"
    Cuando actualizo el cliente "Ana" a correo "ana@nuevo.com"
    Entonces el cliente "Ana" debe tener correo "ana@nuevo.com"

  Escenario: Eliminar un cliente
    Dado que existe un cliente con nombre "Luis"
    Cuando elimino el cliente "Luis"
    Entonces el cliente "Luis" no debe existir en el sistema

  Escenario: Listar clientes
    Dado que existen clientes registrados
    Cuando solicito la lista de clientes
    Entonces debo obtener una lista con los clientes existentes
