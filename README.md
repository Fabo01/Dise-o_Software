# Sistema de Gestión de Clientes y Pedidos en un Restaurante

Este proyecto consiste en la refactorización de un sistema de gestión de restaurante, migrando de una aplicación de escritorio (Python + customtkinter) a una plataforma web moderna con React en el frontend y Django en el backend, siguiendo principios de Clean Architecture.

## Principios SOLID implementados en la refactorización

Los principios SOLID son fundamentales para crear software mantenible, escalable y fácil de modificar. A continuación, se describe cómo cada principio se aplica en nuestro sistema refactorizado:

### 1. Principio de Responsabilidad Única (SRP)

**¿Qué es?** Una clase debe tener una única razón para cambiar, es decir, debe tener una sola responsabilidad.

**¿Dónde se implementa en nuestra refactorización?**

- **Sistema Actual:** Tenemos clases como `OrderManager` que manejan múltiples responsabilidades (crear pedidos, editarlos, cancelarlos y generar recibos).
  
- **Sistema Refactorizado:** Separamos en clases específicas:
  ```python
  # Ejemplo de implementación
  class OrderRepository:
      # Solo responsable de persistencia de datos
      def get(self, id): pass
      def save(self, order): pass
      def update(self, order): pass
      
  class OrderService:
      # Responsable de la lógica de negocio
      def __init__(self, repository):
          self.repository = repository
      
      def create_order(self, data): pass
      def calculate_total(self, order): pass
      
  class ReceiptGenerator:
      # Responsable únicamente de generar recibos
      def generate(self, order): pass
  ```

La arquitectura Clean Architecture implementada refuerza este principio al separar claramente las capas (presentación, casos de uso, dominio e infraestructura), asignando responsabilidades específicas a cada componente.

### 2. Principio Abierto/Cerrado (OCP)

**¿Qué es?** Las entidades de software deben estar abiertas para extensión pero cerradas para modificación.

**¿Dónde se implementa en nuestra refactorización?**

- **Sistema Actual:** Cada nueva funcionalidad requería modificar las clases existentes.

- **Sistema Refactorizado:** Utilizamos interfaces y herencia para extender funcionalidades:
  ```python
  # Ejemplo de implementación
  class OrderState:
      # Interfaz que define comportamiento de estados
      def next_state(self): pass
      def get_status_info(self): pass
      
  class ReceivedState(OrderState):
      # Implementación específica sin modificar la interfaz
      def next_state(self): 
          return PreparingState()
      def get_status_info(self): 
          return "Pedido recibido"
  
  class PreparingState(OrderState):
      # Nueva implementación sin modificar código existente
      def next_state(self): 
          return ReadyState()
      def get_status_info(self): 
          return "En preparación"
  ```

El módulo de pedidos implementa este principio, permitiendo añadir nuevos estados (como "Cancelado" o "En ruta") sin modificar la lógica existente.

### 3. Principio de Sustitución de Liskov (LSP)

**¿Qué es?** Los objetos de un programa deberían ser reemplazables por instancias de sus subtipos sin alterar el correcto funcionamiento del programa.

**¿Dónde se implementa en nuestra refactorización?**

- **Sistema Refactorizado:** La jerarquía de pedidos cumple con este principio:
  ```python
  # Ejemplo de implementación
  class Order:
      def calculate_total(self): pass
      def assign_to_table(self, table): pass
      
  class DeliveryOrder(Order):
      def calculate_total(self):
          # Incluye costo de envío pero respeta la interfaz
          base_total = super().calculate_total()
          return base_total + self.delivery_fee
      
      def assign_to_table(self, table):
          # No aplica para delivery, pero no rompe el comportamiento
          pass
  ```

Los repositorios también siguen este principio, permitiendo intercambiar implementaciones sin afectar a los servicios que los utilizan.

### 4. Principio de Segregación de Interfaces (ISP)

**¿Qué es?** Ningún cliente debería verse obligado a depender de métodos que no usa.

**¿Dónde se implementa en nuestra refactorización?**

- **Sistema Actual:** Interfaces monolíticas con múltiples métodos.

- **Sistema Refactorizado:** Interfaces específicas para cada contexto:
  ```python
  # Ejemplo de implementación
  class ReadOnlyRepository:
      def get(self, id): pass
      def get_all(self): pass
      
  class WriteRepository:
      def save(self, entity): pass
      def update(self, entity): pass
      def delete(self, id): pass
      
  class FullRepository(ReadOnlyRepository, WriteRepository):
      # Implementación completa para clases que necesitan todas las operaciones
      pass
      
  class MenuService:
      # Solo necesita lectura
      def __init__(self, read_repository: ReadOnlyRepository):
          self.repository = read_repository
  ```

En la capa de casos de uso, se crean interfaces específicas para cada servicio, evitando dependencias innecesarias.

### 5. Principio de Inversión de Dependencias (DIP)

**¿Qué es?** Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.

**¿Dónde se implementa en nuestra refactorización?**

- **Sistema Actual:** Dependencias directas entre componentes.

- **Sistema Refactorizado:** Uso de inyección de dependencias y abstracciones:
  ```python
  # Ejemplo de implementación
  class IRepository:
      # Abstracción
      def get(self, id): pass
      def save(self, entity): pass
      
  class ClientService:
      # Depende de la abstracción, no de la implementación
      def __init__(self, repository: IRepository):
          self.repository = repository
          
  class DjangoClientRepository(IRepository):
      # Implementación concreta
      def get(self, id): 
          return Client.objects.get(pk=id)
      def save(self, entity):
          entity.save()
  ```

La Clean Architecture implementada enfatiza este principio al hacer que todas las dependencias apunten hacia el dominio (centro), y no al revés.

## Patrones de Diseño implementados

La refactorización implementa varios patrones de diseño para resolver problemas específicos de manera elegante y reutilizable:

### 1. Patrón Repository

**¿Qué es?** Abstrae el acceso a datos, desacoplando la lógica de negocio de la persistencia.

**Implementación:**
```python
# Ejemplo de implementación
class IClientRepository:
    def get(self, id): pass
    def get_all(self): pass
    def add(self, client): pass
    def update(self, client): pass
    def delete(self, id): pass
    
class DjangoClientRepository(IClientRepository):
    def get(self, id):
        return Cliente.objects.get(pk=id)
    def get_all(self):
        return Cliente.objects.all()
    # Implementación de otros métodos...
```

El diagrama de clases muestra este patrón en la relación entre `IRepository<T>` y sus implementaciones concretas como `ClientRepository` y `MenuRepository`.

### 2. Patrón Factory

**¿Qué es?** Proporciona una interfaz para crear objetos en una superclase, pero permite que las subclases alteren el tipo de objetos que se crean.

**Implementación:**
```python
# Ejemplo de implementación
class OrderFactory:
    def create_local_order(self, data):
        order = Order()
        order.tipo = "local"
        # Configuración específica
        return order
        
    def create_delivery_order(self, data):
        order = DeliveryOrder()
        order.tipo = "delivery"
        # Configuración específica
        return order
```

Este patrón facilita la creación de diferentes tipos de pedidos (locales o delivery) con sus configuraciones específicas.

### 3. Patrón Observer

**¿Qué es?** Define una dependencia uno-a-muchos entre objetos, de modo que cuando un objeto cambia su estado, todos sus dependientes son notificados y actualizados automáticamente.

**Implementación:**
```python
# Ejemplo de implementación
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
        
    def detach(self, observer):
        self._observers.remove(observer)
        
    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)
            
class Order(Subject):
    def change_state(self, new_state):
        self.state = new_state
        self.notify()
        
class KitchenDisplay:
    def update(self, subject, *args, **kwargs):
        # Actualizar la visualización en la cocina
        pass
        
class CustomerNotifier:
    def update(self, subject, *args, **kwargs):
        # Enviar notificación al cliente
        pass
```

Este patrón se utiliza para notificar cambios de estado en los pedidos a diferentes componentes del sistema.

### 4. Patrón State

**¿Qué es?** Permite que un objeto altere su comportamiento cuando su estado interno cambia.

**Implementación:**
```python
# Ejemplo de implementación
class OrderState:
    def next_state(self): pass
    def get_status_info(self): pass
    
class ReceivedState(OrderState):
    def next_state(self):
        return PreparingState()
    def get_status_info(self):
        return "Pedido recibido"
        
class PreparingState(OrderState):
    def next_state(self):
        return ReadyState()
    def get_status_info(self):
        return "En preparación"
        
class ReadyState(OrderState):
    def next_state(self):
        return DeliveredState()
    def get_status_info(self):
        return "Listo para entregar"
        
class DeliveredState(OrderState):
    def next_state(self):
        return self  # Estado final
    def get_status_info(self):
        return "Entregado"
        
class Order:
    def __init__(self):
        self.state = ReceivedState()
        
    def next_state(self):
        self.state = self.state.next_state()
        
    def get_status_info(self):
        return self.state.get_status_info()
```

Este patrón se utiliza para gestionar los diferentes estados de un pedido (recibido, en preparación, listo, entregado).

### 5. Patrón Facade

**¿Qué es?** Proporciona una interfaz unificada para un conjunto de interfaces en un subsistema.

**Implementación:**
```python
# Ejemplo de implementación
class DashboardFacade:
    def __init__(self):
        self.sales_analyzer = SalesAnalyzer()
        self.inventory_analyzer = InventoryAnalyzer()
        self.customer_analyzer = CustomerAnalyzer()
    
    def get_sales_summary(self, date_range):
        return self.sales_analyzer.get_summary(date_range)
        
    def get_popular_menus(self):
        return self.sales_analyzer.get_popular_items()
        
    def get_inventory_status(self):
        return self.inventory_analyzer.get_status()
        
    def get_customer_statistics(self):
        return self.customer_analyzer.get_statistics()
```

Este patrón simplifica la interacción con el subsistema de análisis de datos, proporcionando una interfaz unificada para el dashboard.

### 6. Patrón Dependency Injection

**¿Qué es?** Técnica que permite la inversión de control entre clases y sus dependencias.

**Implementación:**
```python
# Ejemplo de implementación
class MenuService:
    def __init__(self, menu_repository, ingredient_repository):
        self.menu_repository = menu_repository
        self.ingredient_repository = ingredient_repository
        
    def create_menu(self, menu_data):
        # Lógica utilizando los repositorios inyectados
        pass
```

Este patrón se utiliza en toda la aplicación para inyectar dependencias, lo que facilita el testing y la flexibilidad del sistema.

## Beneficios de la aplicación de SOLID y Patrones de Diseño

1. **Mayor mantenibilidad:** El código está estructurado de forma que los cambios afectan a áreas mínimas.
2. **Facilidad para testing:** Las dependencias están claramente definidas y pueden ser simuladas.
3. **Escalabilidad:** El sistema puede crecer con nuevas funcionalidades sin modificar código existente.
4. **Flexibilidad:** Los componentes pueden evolucionar independientemente.
5. **Robustez:** La aplicación es más resistente a cambios y menos propensa a errores.

## Metodología del Proyecto

El proyecto sigue la metodología Scrum con 5 integrantes dedicando 5 horas semanales cada uno. Se han definido 4 sprints (un Sprint 0 de 2 semanas y 3 sprints de 4 semanas cada uno) para completar la refactorización.