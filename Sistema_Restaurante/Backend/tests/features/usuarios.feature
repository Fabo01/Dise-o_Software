# language: es

Característica: Gestión de usuarios
  Como administrador
  Quiero poder crear, consultar, actualizar y eliminar usuarios
  Para gestionar el acceso y roles en el sistema

  Escenario: Crear un usuario
    Dado que no existe un usuario con username "admin"
    Cuando creo un usuario con username "admin", nombre "Administrador", rol "administrador"
    Entonces el usuario "admin" debe existir en el sistema con rol "administrador"

  Escenario: Editar un usuario
    Dado que existe un usuario con username "mesero1"
    Cuando actualizo el usuario "mesero1" a nombre "Juan Pérez"
    Entonces el usuario "mesero1" debe tener nombre "Juan Pérez"

  Escenario: Eliminar un usuario
    Dado que existe un usuario con username "cocinero1"
    Cuando elimino el usuario "cocinero1"
    Entonces el usuario "cocinero1" no debe existir en el sistema

  Escenario: Listar usuarios
    Dado que existen usuarios registrados
    Cuando solicito la lista de usuarios
    Entonces debo obtener una lista con los usuarios existentes
