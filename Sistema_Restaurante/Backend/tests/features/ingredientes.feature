Feature: Gestión de ingredientes
  Como administrador o jefe de local
  Quiero poder gestionar ingredientes
  Para mantener actualizado el inventario del restaurante

  Scenario: Crear un ingrediente
    Given que no existe un ingrediente llamado "Tomate"
    When creo un ingrediente con nombre "Tomate", cantidad 10, unidad "kg", categoría "Verdura", nivel crítico 2
    Then el ingrediente "Tomate" debe existir en el sistema con cantidad 10 y unidad "kg"

  Scenario: Editar un ingrediente
    Given que existe un ingrediente llamado "Tomate" con cantidad 10
    When actualizo el ingrediente "Tomate" a cantidad 20
    Then el ingrediente "Tomate" debe tener cantidad 20

  Scenario: Eliminar un ingrediente
    Given que existe un ingrediente llamado "Tomate"
    When elimino el ingrediente "Tomate"
    Then el ingrediente "Tomate" no debe existir en el sistema

  Scenario: Listar ingredientes
    Given que existen ingredientes registrados
    When solicito la lista de ingredientes
    Then debo obtener una lista con los ingredientes existentes
