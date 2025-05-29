# language: es

Característica: Gestión de menús
  Como administrador o jefe de cocina
  Quiero poder crear, consultar, actualizar y eliminar menús
  Para gestionar la oferta gastronómica del restaurante

  Escenario: Crear un menú
    Dado que no existe un menú llamado "Desayuno"
    Cuando creo un menú con nombre "Desayuno", categoría "Mañana"
    Entonces el menú "Desayuno" debe existir en el sistema con categoría "Mañana"

  Escenario: Editar un menú
    Dado que existe un menú llamado "Almuerzo"
    Cuando actualizo el menú "Almuerzo" a categoría "Tarde"
    Entonces el menú "Almuerzo" debe tener categoría "Tarde"

  Escenario: Eliminar un menú
    Dado que existe un menú llamado "Cena"
    Cuando elimino el menú "Cena"
    Entonces el menú "Cena" no debe existir en el sistema

  Escenario: Listar menús
    Dado que existen menús registrados
    Cuando solicito la lista de menús
    Entonces debo obtener una lista con los menús existentes
