# Cómo Commitear y Hacer Pull Requests

Este documento describe el flujo de trabajo para trabajar con las ramas del proyecto, cómo realizar correctamente commits y pull requests, y cómo entender la arquitectura de GitHub para programadores principiantes.

---

## Introducción a GitHub y Flujo de Trabajo

GitHub es una plataforma de control de versiones basada en Git que permite a los desarrolladores colaborar en proyectos de software. En este proyecto, seguimos un flujo de trabajo estructurado para garantizar que el código sea mantenible y fácil de integrar.

### Conceptos Básicos

1. **Repositorio:** Es el lugar donde se almacena el código del proyecto.
2. **Rama (Branch):** Una línea de desarrollo independiente.
3. **Commit:** Un cambio registrado en el historial del proyecto.
4. **Pull Request (PR):** Una solicitud para fusionar cambios de una rama a otra.

---

## Flujo de Ramas

El proyecto sigue una estructura de ramas basada en niveles de abstracción y responsabilidades. A continuación, se detalla cómo se organizan las ramas y qué tipo de código debe incluir cada una.

### Estructura de Ramas

1. **`main`**
   - **Propósito:** Contiene el código en producción.
   - **Contenido:** Código estable y probado.

2. **`develop`**
   - **Propósito:** Rama principal para desarrollo.
   - **Contenido:** Código en desarrollo que integra cambios de las subramas.

3. **Subramas de `develop`**
   - **`frontend`**
     - **Propósito:** Desarrollo relacionado con la interfaz de usuario.
     - **Subramas:**
       - **`paginas`**: Desarrollo de páginas específicas.
       - **`componentes`**: Desarrollo de componentes reutilizables.
   - **`backend`**
     - **Propósito:** Desarrollo relacionado con la lógica del servidor.
     - **Subramas:**
       - **`aplicacion`**: Casos de uso y lógica de aplicación.
       - **`dominio`**: Entidades y reglas de negocio.
       - **`infraestructura`**: Repositorios, ORM y servicios externos.
       - **`presentacion`**: Controladores y serializadores.

---

## Detalle de las Capas de la Arquitectura

### Backend

#### **Capa de Dominio (`Dominio/`):**
- **Responsabilidad:** Define las reglas de negocio, entidades y objetos de valor.
- **Código que pertenece a esta capa:**
  - Entidades que representan objetos con identidad única.
  - Objetos de valor que encapsulan conceptos inmutables.
  - Excepciones específicas del dominio.
- **Ejemplo:**
  - Una entidad `Cliente` con validaciones de negocio (`cliente.py`):
    ```python
    class Cliente:
        def __init__(self, nombre, correo, rut, telefono=""):
            if not nombre:
                raise ValueError("El nombre es obligatorio")
            if not self._validar_rut(rut):
                raise ValueError("RUT inválido")
                
            self.id = None
            self.nombre = nombre
            self.correo = correo
            self.rut = rut
            self.telefono = telefono
            self.activo = True

        def _validar_rut(self, rut):
            # Implementación de validación de RUT chileno
            if not rut or len(rut) < 8:
                return False
            return True
            
        def desactivar(self):
            self.activo = False
            
        def actualizar_datos(self, nombre, correo, telefono):
            if not nombre:
                raise ValueError("El nombre es obligatorio")
            
            self.nombre = nombre
            self.correo = correo
            self.telefono = telefono
    ```
  
  - Un objeto de valor para encapsular correos (`correo.py`):
    ```python
    import re

    class correo:
        def __init__(self, direccion):
            if not self._es_valido(direccion):
                raise ValueError("Dirección de correo inválida")
            self._direccion = direccion.lower()
            
        def _es_valido(self, direccion):
            # Validación básica de formato de correo
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(patron, direccion) is not None
            
        def __str__(self):
            return self._direccion
            
        def __eq__(self, other):
            if not isinstance(other, correo):
                return False
            return self._direccion == other._direccion
    ```

#### **Capa de Infraestructura (`Infraestructura/`):**
- **Responsabilidad:** Maneja la persistencia y comunicación con servicios externos.
- **Código que pertenece a esta capa:**
  - Modelos ORM que mapean las entidades a tablas de base de datos.
  - Repositorios que abstraen el acceso a la base de datos.
  - Servicios externos como APIs de terceros o sistemas de mensajería.
- **Ejemplo:**
  - Un modelo ORM para `Cliente` (`Cliente_Modelo.py`):
    ```python
    from django.db import models
    
    class ClienteModel(models.Model):
        nombre = models.CharField(max_length=100)
        correo = models.correoField()
        rut = models.CharField(max_length=12, unique=True)
        telefono = models.CharField(max_length=15, blank=True)
        activo = models.BooleanField(default=True)
        fecha_registro = models.DateTimeField(auto_now_add=True)
        
        class Meta:
            db_table = 'clientes'
            ordering = ['nombre']
    ```
    
  - Un repositorio para gestionar clientes (`Cliente_Repositorio.py`):
    ```python
    from Dominio.Entidades.cliente import Cliente
    from Dominio.objetos_valor.correo import correo
    from Infraestructura.Modelos.cliente_model import ClienteModel

    class ClienteRepositorio:
        def guardar(self, cliente):
            # Crear o actualizar
            if cliente.id:
                # Actualizar cliente existente
                cliente_model = ClienteModel.objects.get(id=cliente.id)
                cliente_model.nombre = cliente.nombre
                cliente_model.correo = str(cliente.correo)
                cliente_model.telefono = cliente.telefono
                cliente_model.activo = cliente.activo
                cliente_model.save()
            else:
                # Crear nuevo cliente
                cliente_model = ClienteModel.objects.create(
                    nombre=cliente.nombre,
                    correo=str(cliente.correo),
                    rut=cliente.rut,
                    telefono=cliente.telefono,
                    activo=cliente.activo
                )
                cliente.id = cliente_model.id
            
            return self._convertir_a_entidad(cliente_model)
            
        def buscar_por_rut(self, rut):
            try:
                cliente_model = ClienteModel.objects.get(rut=rut)
                return self._convertir_a_entidad(cliente_model)
            except ClienteModel.DoesNotExist:
                return None
                
        def listar_activos(self):
            clientes_model = ClienteModel.objects.filter(activo=True)
            return [self._convertir_a_entidad(c) for c in clientes_model]
                
        def _convertir_a_entidad(self, cliente_model):
            cliente = Cliente(
                nombre=cliente_model.nombre,
                correo=correo(cliente_model.correo),
                rut=cliente_model.rut,
                telefono=cliente_model.telefono
            )
            cliente.id = cliente_model.id
            cliente.activo = cliente_model.activo
            return cliente
    ```

#### **Capa de Aplicación (`Aplicacion/`):**
- **Responsabilidad:** Contiene los casos de uso y servicios.
- **Código que pertenece a esta capa:**
  - Servicios que implementan la lógica de negocio específica de cada caso de uso.
  - DTOs (Data Transfer Objects) para transferir datos entre capas.
  - Interfaces que definen contratos para los servicios.
- **Ejemplo:**
  - Un servicio para registrar un cliente (`cliente_servicio.py`):
    ```python
    from Dominio.Entidades.cliente import Cliente
    from Dominio.objetos_valor.correo import correo
    from Infraestructura.Repositorios.Cliente_Repositorio import ClienteRepositorio

    class ClienteServicio:
        def __init__(self):
            self.repositorio = ClienteRepositorio()

        def crear_cliente(self, cliente_dto):
            # Crear entidad de dominio desde el DTO
            cliente = Cliente(
                nombre=cliente_dto['nombre'],
                correo=correo(cliente_dto['correo']),
                rut=cliente_dto['rut'],
                telefono=cliente_dto.get('telefono', '')
            )
            
            # Verificar si ya existe cliente con ese RUT
            cliente_existente = self.repositorio.buscar_por_rut(cliente.rut)
            if cliente_existente:
                raise ValueError("Ya existe un cliente con ese RUT")
                
            # Guardar cliente
            return self.repositorio.guardar(cliente)
    ```

---

### Frontend

#### **Capa de Componentes (`src/componentes/`):**
- **Responsabilidad:** Contiene componentes reutilizables para la interfaz de usuario.
- **Código que pertenece a esta capa:**
  - Componentes presentacionales que manejan la presentación visual.
  - Componentes contenedores que manejan la lógica y el estado.

#### **Capa de Páginas (`src/Paginas/`):**
- **Responsabilidad:** Define las vistas principales de la aplicación.
- **Código que pertenece a esta capa:**
  - Páginas que combinan múltiples componentes para formar una vista completa.

#### **Capa de Servicios (`src/Servicios/`):**
- **Responsabilidad:** Maneja la comunicación con el backend.
- **Código que pertenece a esta capa:**
  - Servicios que realizan solicitudes HTTP al backend.

#### **Capa de Gestión de Estado (`src/Store/`):**
- **Responsabilidad:** Centraliza el estado global de la aplicación.
- **Código que pertenece a esta capa:**
  - Acciones que describen eventos que modifican el estado.
  - Reductores que definen cómo cambia el estado en respuesta a las acciones.
  - Segmentos que agrupan el estado relacionado.

#### **Capa de Utilidades (`src/Utilidades/`):**
- **Responsabilidad:** Contiene funciones y herramientas auxiliares.
- **Código que pertenece a esta capa:**
  - Funciones de ayuda para formatear datos, manejar errores, etc.

## Cómo Realizar Commits

1. **Escribe mensajes claros y descriptivos:**
   - Usa el formato: `Tipo: Descripción breve`.
   - Ejemplo: `feat: Agregar ORM Cliente`.

2. **Tipos de commits:**
   - `feat`: Para nuevas funcionalidades.
   - `fix`: Para correcciones de errores.
   - `refactor`: Para cambios en el código que no afectan la funcionalidad.
   - `docs`: Para cambios en la documentación.
   - `test`: Para agregar o modificar pruebas.

3. **Proceso para Crear un Nuevo Commit:**
   - **Identificar la Rama Correspondiente:** Determina en qué capa de la arquitectura se encuentra el commit que vas a implementar (En qué capa de la arquitectura estás trabajando). 
   
   Ejemplo: Si estás creando un modelo ORM para la entidad `Cliente`, debes trabajar en la rama `backend/infraestructura`.
   
   - **Implementar el Commit:** Realiza los cambios necesarios en el código, asegurándote de seguir las convenciones de la arquitectura y los patrones establecidos.
   - **Realizar Commits Atomizados:** Realiza commits pequeños y descriptivos para registrar tus cambios, estos deben de tener sus tareas específicas finalizadas. Ejemplo:
     ```bash
     git add .
     git commit -m "feat(backend/infraestructura): Crear modelo ORM para Cliente"
     ```

---

## Cómo Hacer Pull Requests

1. **Sincroniza tu rama con la rama base:**
   - Antes de abrir un pull request, asegúrate de que tu rama esté actualizada:
     ```bash
     git checkout backend/infraestructura
     git pull origin backend/infraestructura
     ```

2. **Realiza los cambios necesarios y commitea:**
   - Trabaja directamente en la rama correspondiente a la capa de arquitectura. Por ejemplo, si estás trabajando en la capa de Infraestructura para modificar o crear un ORM, realiza los cambios en la rama `backend/infraestructura`.
   - Realiza un commit con un mensaje claro y descriptivo. Ejemplo:
     ```bash
     git add .
     git commit -m "feat(backend/infraestructura): Crear modelo ORM para Cliente"
     ```

3. **Abre un Pull Request:**
   - Ve al repositorio en GitHub.
   - Selecciona la rama correspondiente a la capa de arquitectura como origen (`backend/infraestructura`) y la rama `backend` como destino.
   - Escribe un título y descripción claros para el pull request. Ejemplo:
     ```plaintext
     Título: feat(backend/infraestructura): Crear modelo ORM para Cliente

     Descripción:
     - Se implementa el modelo ORM `Cliente` en la capa de Infraestructura.
     - El modelo incluye los campos `rut`, `correo`, `nombre` y la relación con `Pedido`.
     - Este modelo sigue el patrón Repository para abstraer el acceso a la base de datos.
     ```
   - Asigna revisores y etiquetas si es necesario.

4. **Resuelve conflictos si los hay:**
   - Si GitHub detecta conflictos, resuélvelos localmente:
     ```bash
     git merge backend
     # Resuelve los conflictos en los archivos
     git add .
     git commit
     ```

5. **Espera la aprobación:**
   - No fusiones tu propio pull request sin aprobación.
   - Una vez aprobado, el pull request puede ser fusionado por el revisor o por ti mismo si tienes permisos.

---

## Ejemplo Real: Commit para la Creación del Modelo ORM del Cliente Refactorizado

### Código del Modelo ORM Refactorizado

```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(String(9), unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    pedidos = relationship("Pedido", back_populates="cliente")
```

### Mensaje del Commit

```plaintext
feat(backend/infraestructura): Crear modelo ORM para Cliente

- Se implementa el modelo ORM `Cliente` en la capa de Infraestructura.
- El modelo incluye los campos `id`, `rut`, `nombre`, `correo`, `telefono` y `direccion`.
- Se establece una relación uno a muchos con el modelo `Pedido`.
- Este modelo sigue el patrón Repository para abstraer el acceso a la base de datos.
- Se asegura la unicidad del campo `rut` y se permite la relación con pedidos.

```

### Flujo del Commit

1. Crear la rama `backend/infraestructura/modelo-cliente` desde `develop`.
2. Implementar el modelo en el archivo correspondiente.
3. Ejecutar pruebas unitarias para validar la funcionalidad.
4. Realizar el commit con el mensaje detallado.
5. Crear un pull request hacia la rama `backend`.

---

Este flujo asegura que el modelo se integre correctamente en la arquitectura y cumpla con los estándares del proyecto.

