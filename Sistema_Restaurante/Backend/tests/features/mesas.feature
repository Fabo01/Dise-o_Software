# language: es

Característica: Gestión de mesas
  Como administrador o mesero
  Quiero poder crear, consultar, actualizar y eliminar mesas
  Para gestionar la asignación y disponibilidad en el restaurante

  Escenario: Crear una mesa
    Dado que no existe una mesa con número 1
    Cuando creo una mesa con número 1 y capacidad 4
    Entonces la mesa 1 debe existir en el sistema con capacidad 4

  Escenario: Editar una mesa
    Dado que existe una mesa con número 2
    Cuando actualizo la mesa 2 a capacidad 6
    Entonces la mesa 2 debe tener capacidad 6

  Escenario: Eliminar una mesa
    Dado que existe una mesa con número 3
    Cuando elimino la mesa 3
    Entonces la mesa 3 no debe existir en el sistema

  Escenario: Listar mesas
    Dado que existen mesas registradas
    Cuando solicito la lista de mesas
    Entonces debo obtener una lista con las mesas existentes
