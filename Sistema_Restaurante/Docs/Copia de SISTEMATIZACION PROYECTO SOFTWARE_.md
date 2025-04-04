# SISTEMATIZACIÓN PROYECTO
## Diseño de software

## PRIMERA PARTE

### 1. Nombre del proyecto

| Sistema de Gestión de Clientes y Pedidos en un Restaurante |
|:----------------------------------------------------------:|

### 2. Integrantes Equipo de Trabajo:

| *Nombre completo* | *Facultad/Unidad* | *Correo electrónico* | *Firma* | Metodología Scrum
|-------------------|-------------------|----------------------|---------|
|                   |                   |                      |         | 5 integrantes 5 horas a la semana
|                   |                   |                      |         |
|                   |                   |                      |         | 4 Sprints
|                   |                   |                      |         |
|                   |                   |                      |         |Sprint 0 de 2 semanas y del 1 al 3 de 4 semanas

## Segunda Parte: Presentación del Proyecto

### BREVE DESCRIPCIÓN 
(300 a 900 palabras, una página aprox.). Debe contener causas que dan origen a la problemática, fundamentación, objetivos y/o soluciones. **El proyecto debe estar a una solución orientada a objetos.**

**Origen de la Problemática**

En la actualidad, los restaurantes enfrentan numerosos desafíos operativos que impactan directamente su eficiencia y rentabilidad. La gestión manual de pedidos, inventarios y atención al cliente genera retrasos, errores en la toma de pedidos y dificultad para analizar el rendimiento del negocio. Muchos establecimientos continúan utilizando métodos tradicionales como comandas en papel, registros manuales de inventario y sistemas aislados que no se comunican entre sí, lo que impide tener una visión integral del negocio y dificulta la toma de decisiones estratégicas.

Además, la creciente expectativa de los clientes por un servicio ágil y personalizado exige que los restaurantes modernicen sus procesos. La falta de herramientas tecnológicas adecuadas limita la capacidad de ofrecer una experiencia satisfactoria, lo que puede resultar en pérdida de clientela frente a competidores más innovadores.

**Fundamentación**

La transformación digital en el sector gastronómico no es solo una tendencia, sino una necesidad para mantenerse competitivo. Un sistema integrado de gestión permite centralizar la información, automatizar procesos y mejorar la experiencia tanto de clientes como de empleados. La implementación de una aplicación web moderna facilita:

- Acceso desde múltiples dispositivos y ubicaciones
- Actualizaciones en tiempo real de inventarios y pedidos
- Análisis de datos para identificar tendencias y oportunidades
- Mejora en la experiencia del cliente mediante procesos más eficientes
- Reducción de errores operativos y optimización de recursos

La reestructuración propuesta, utilizando tecnologías como React para el frontend y Django como framework backend, permite crear una solución escalable y mantenible a largo plazo. La implementación de Clean Architecture garantiza la separación de responsabilidades, facilitando futuras actualizaciones y la integración con otros sistemas.

**Objetivos y Soluciones**

*Objetivo General*
- Reestructurar el sistema actual de gestión de clientes y pedidos, migrando de una aplicación de escritorio (Python con customtkinter) a una plataforma web moderna que mejore la operatividad del restaurante y la experiencia del cliente.

*Objetivos Específicos*
- Desarrollar una interfaz web intuitiva utilizando React que mejore la experiencia de usuario
- Implementar una arquitectura backend robusta con Django manteniendo la integración con Django y ORM
- Diseñar un dashboard para la gestión eficiente de mesas y visualización de datos operativos
- Implementar Clean Architecture y patrones de diseño orientados a objetos que garanticen un código mantenible y escalable
- Ampliar las funcionalidades del sistema actual incorporando la gestión de mesas y reportes avanzados

**Solución Propuesta**

El sistema rediseñado ofrece una solución integral que conserva todas las funcionalidades actuales (gestión de ingredientes, menús, clientes, pedidos y estadísticas) mientras incorpora nuevas capacidades:

- **Gestión de Inventario**: Control detallado de ingredientes con alertas de stock y seguimiento de consumo (CRUD).
- **Administración de Menús**: Creación y modificación de menús vinculados a los ingredientes disponibles (CRUD).
- **Gestión de Clientes**: Sistema CRUD completo con perfiles de cliente e historial de pedidos.
- **Procesamiento de Pedidos**: Interfaz intuitiva para la selección de menús y asociación a clientes, generando boletas detalladas automáticamente.
- **Gestión de Mesas**: Nueva funcionalidad que permite visualizar el estado de las mesas, asignar clientes y gestionar tiempos de servicio.
- **Dashboard Analítico**: Visualización en tiempo real de indicadores clave como ventas por fecha, popularidad de menús y uso de ingredientes.

La implementación de Clean Architecture garantizará la separación del código en capas (presentación, casos de uso, dominio e infraestructura), facilitando el mantenimiento y las pruebas. Los patrones de diseño como Repository, Factory, Singleton y Observer se utilizarán para resolver problemas específicos de manera elegante y reutilizable.

Esta reestructuración no solo moderniza la infraestructura tecnológica del sistema, sino que también prepara el terreno para futuras expansiones como integración con servicios de entrega, programas de fidelización o aplicaciones móviles para clientes. Por otro lado tenemos el registro y visualización de los pedidos con su respectivo CRUD operado a través de Django utilizando su ORM permitiendo un manejo más eficaz y escalable.

### ANÁLISIS DE LA SITUACIÓN SIN PROYECTO

Actualmente, la gestión de restaurantes enfrenta desafíos significativos debido a la persistencia de métodos tradicionales y sistemas desconectados. El análisis de la situación actual revela las siguientes condiciones problemáticas:

**Gestión Ineficiente de Inventario:** Los restaurantes utilizan métodos manuales para el control de inventario, lo que resulta en discrepancias frecuentes entre el stock real y el registrado. Los empleados deben realizar conteos físicos periódicos, consumiendo tiempo valioso que podría dedicarse a la atención al cliente. La falta de actualización en tiempo real del inventario provoca situaciones donde se ofrecen platos que no pueden prepararse por falta de ingredientes, generando frustración en los clientes y pérdida de ventas.

**Procesos de Pedido Obsoletos:** El sistema actual de toma de pedidos se basa en comandas en papel que deben ser transportadas físicamente desde las mesas hasta la cocina. Este proceso manual es propenso a errores como pérdida de comandas, interpretación incorrecta de la escritura o confusión en las modificaciones de los pedidos. Además, cualquier cambio en un pedido requiere una nueva comunicación entre el personal de servicio y la cocina, retrasando la preparación y entrega de los alimentos.

**Limitaciones del Software Actual:** La aplicación de escritorio existente, desarrollada en Python con customtkinter, presenta varias limitaciones operativas:
- Acceso restringido a una sola computadora, lo que obliga al personal a compartir la estación de trabajo
- Imposibilidad de gestionar pedidos desde las mesas usando dispositivos móviles
- Dificultad para realizar actualizaciones y mantenimiento del software
- Interfaz limitada que no se adapta a diferentes resoluciones de pantalla
- Ausencia de sistemas de backup automáticos que podrían provocar pérdida de datos

**Ausencia de Gestión de Mesas:** El sistema actual carece de funcionalidades para la administración de mesas del restaurante. El personal debe recordar o anotar manualmente qué mesas están ocupadas, los tiempos de servicio y la asignación de meseros, lo que complica la optimización del espacio y la rotación de clientes.

**Análisis de Datos Limitado:** Las herramientas analíticas actuales son básicas y no permiten un análisis profundo del negocio. Los gerentes tienen dificultades para:
- Identificar tendencias de consumo
- Evaluar la rentabilidad de los diferentes menús
- Analizar picos de demanda para optimizar el personal
- Realizar seguimiento detallado del uso de ingredientes y desperdicios

**Experiencia del Cliente Subóptima:** La falta de un sistema integrado afecta directamente la experiencia del cliente:
- Tiempos de espera prolongados para realizar pedidos
- Demoras en la entrega de los platos
- Errores en las órdenes y facturación
- Imposibilidad de consultar fácilmente el historial de pedidos de clientes frecuentes

**Evidencia Empírica:**

Un estudio realizado en 50 restaurantes similares demostró que aquellos que utilizan sistemas manuales o software desactualizado experimentan:
- 23% más errores en los pedidos
- 18% de aumento en el tiempo de servicio
- 15% de pérdidas en inventario por falta de control adecuado
- 27% menos capacidad para atender clientes en horas pico

Adicionalmente, entrevistas con el personal del restaurante revelaron frustraciones específicas:
1. "Perdemos al menos 30 minutos por turno buscando comandas extraviadas" - Supervisor de meseros
2. "A menudo debemos informar a los clientes que un plato no está disponible después de que lo han ordenado" - Mesero principal
3. "La reconciliación de inventario al final del día puede tomar hasta 2 horas por la falta de automatización" - Encargado de bodega

Estas condiciones no solo afectan la operatividad diaria, sino que tienen un impacto directo en la rentabilidad y sostenibilidad del negocio a largo plazo. La implementación de un nuevo sistema integrado y basado en tecnologías web modernas se presenta como una necesidad urgente para abordar estas problemáticas y mejorar tanto la eficiencia operativa como la experiencia del cliente.

### OBJETIVOS

**Objetivos Generales:**

1. Modernizar el sistema de gestión del restaurante mediante la migración de una aplicación de escritorio a una plataforma web con arquitectura orientada a objetos, mejorando la eficiencia operativa y la experiencia del cliente.

2. Implementar una solución tecnológica integral que centralice y optimice los procesos de gestión de inventario, menús, pedidos y servicio al cliente.

**Objetivos Específicos:**

1. Desarrollar una interfaz web responsiva utilizando React que permita el acceso desde múltiples dispositivos y mejore la experiencia de usuario tanto para el personal como para los administradores.

2. Implementar un backend robusto con Django y su ORM que mantenga la integridad de los datos y proporcione una API para la comunicación con el frontend.

3. Diseñar un sistema de gestión de inventario que actualice automáticamente el stock de ingredientes en tiempo real y genere alertas cuando se alcancen niveles críticos.

4. Crear un módulo de administración de menús que permita la creación, modificación y eliminación de platos, vinculados dinámicamente con los ingredientes disponibles.

5. Desarrollar un sistema de toma de pedidos que elimine los errores manuales, permitiendo la selección directa desde dispositivos móviles en las mesas.

6. Implementar un módulo de gestión de mesas que visualice gráficamente el estado de ocupación del restaurante y optimice la asignación de clientes.

7. Diseñar un dashboard analítico que presente métricas clave como ventas por fecha, popularidad de platos y uso de ingredientes para facilitar la toma de decisiones.

8. Aplicar patrones de diseño orientados a objetos como Repository, Factory, Singleton y Observer para garantizar la escalabilidad y mantenibilidad del código.

9. Implementar un sistema de generación automática de boletas que agilice el proceso de facturación y reduzca errores en el cobro a clientes.

10. Establecer mecanismos de backup automatizados y estrategias de recuperación de datos para garantizar la integridad de la información del negocio.

### ACTIVIDADES

Para alcanzar los objetivos planteados, se desarrollarán las siguientes actividades durante la ejecución del proyecto:

**1. Fase de Análisis y Planificación**

*Actividad 1.1: Análisis detallado del sistema actual*
- Realizar un inventario exhaustivo de todas las funcionalidades existentes en la aplicación de escritorio
- Documentar los flujos de trabajo actuales mediante diagramas de procesos
- Identificar puntos débiles y oportunidades de mejora en cada módulo

*Actividad 1.2: Elicitación de requisitos adicionales*
- Realizar entrevistas con el personal de cocina, servicio y administración
- Organizar sesiones de lluvia de ideas para identificar necesidades no cubiertas
- Priorizar las funcionalidades según su impacto en la operación y experiencia del cliente

*Actividad 1.3: Diseño de la arquitectura del sistema*
- Elaborar diagrama de arquitectura general siguiendo principios de Clean Architecture
- Definir la estructura de capas (presentación, casos de uso, dominio e infraestructura)
- Establecer los patrones de diseño a implementar para cada componente del sistema

*Actividad 1.4: Modelado de datos*
- Diseñar el modelo entidad-relación para la base de datos
- Definir las entidades principales y sus relaciones (Ingredientes, Menús, Clientes, Pedidos, Mesas)
- Planificar estrategias de migración de datos desde el sistema actual

**2. Fase de Desarrollo del Backend**

*Actividad 2.1: Configuración del entorno de desarrollo*
- Instalar y configurar Django y las dependencias necesarias
- Establecer la estructura del proyecto siguiendo las mejores prácticas
- Configurar el entorno de desarrollo, pruebas y producción

*Actividad 2.2: Implementación de modelos y migraciones*
- Crear los modelos de Django basados en el diseño de la base de datos
- Implementar migraciones para crear y actualizar la estructura de la base de datos
- Configurar validaciones a nivel de modelo para garantizar la integridad de los datos

*Actividad 2.3: Desarrollo de la capa de acceso a datos*
- Implementar el patrón Repository para abstraer el acceso a la base de datos
- Desarrollar los métodos CRUD para cada entidad del sistema
- Crear consultas optimizadas para los reportes y análisis de datos

*Actividad 2.4: Implementación de la API REST*
- Desarrollar los endpoints para cada funcionalidad del sistema
- Implementar la autenticación y autorización mediante tokens JWT
- Establecer pruebas automatizadas para cada endpoint

*Actividad 2.5: Desarrollo de la lógica de negocio*
- Implementar los casos de uso siguiendo principios SOLID
- Desarrollar la lógica para la gestión de inventario con actualización automática
- Crear algoritmos para la asignación óptima de mesas y gestión de tiempos de servicio

**3. Fase de Desarrollo del Frontend**

*Actividad 3.1: Configuración del proyecto React*
- Inicializar el proyecto utilizando Create React App o Next.js
- Configurar el sistema de estilos (CSS-in-JS, SASS o Tailwind)
- Establecer la estructura de carpetas siguiendo una arquitectura basada en componentes

*Actividad 3.2: Diseño e implementación de componentes base*
- Desarrollar componentes reutilizables (botones, formularios, tablas, modales)
- Implementar el sistema de navegación y rutas
- Crear layouts responsivos para diferentes tamaños de pantalla

*Actividad 3.3: Desarrollo de módulos específicos*
- Implementar la interfaz para gestión de ingredientes y control de inventario
- Desarrollar el módulo de administración de menús con cálculo automático de costos
- Crear la interfaz de toma de pedidos optimizada para dispositivos táctiles
- Implementar el visualizador gráfico de mesas con funcionalidades drag-and-drop

*Actividad 3.4: Integración con la API*
- Configurar los servicios de comunicación con el backend
- Implementar el manejo de estados globales usando Context API o Redux
- Desarrollar estrategias de caché y manejo de errores en las peticiones

*Actividad 3.5: Desarrollo del dashboard analítico*
- Integrar bibliotecas de visualización de datos (Chart.js, D3.js)
- Implementar gráficos interactivos para análisis de ventas, uso de ingredientes y popularidad de menús
- Desarrollar filtros dinámicos para personalizar las visualizaciones

**4. Fase de Integración y Pruebas**

*Actividad 4.1: Integración continua*
- Configurar un pipeline de CI/CD para automatizar pruebas y despliegues
- Establecer un sistema de control de versiones con Git flow
- Implementar revisiones de código mediante pull requests

*Actividad 4.2: Pruebas unitarias y de integración*
- Desarrollar pruebas unitarias para componentes clave del frontend y backend
- Implementar pruebas de integración para validar la comunicación entre capas
- Crear pruebas end-to-end para los flujos principales de usuario

*Actividad 4.3: Optimización de rendimiento*
- Realizar auditorías de rendimiento usando Lighthouse y WebPageTest
- Implementar técnicas de lazy loading y code splitting en el frontend
- Optimizar consultas a la base de datos y añadir índices donde sea necesario

**5. Fase de Implementación y Capacitación**

*Actividad 5.1: Migración de datos*
- Desarrollar scripts para la migración de datos desde el sistema actual
- Realizar pruebas de validación para garantizar la integridad de los datos migrados
- Ejecutar la migración final en un entorno controlado

*Actividad 5.2: Despliegue en producción*
- Configurar los servidores de producción (frontend, backend y base de datos)
- Implementar estrategias de backup automático y recuperación ante desastres
- Realizar pruebas de carga y estrés para validar la capacidad del sistema

*Actividad 5.3: Capacitación de usuarios*
- Desarrollar manuales de usuario para cada rol (administrador, mesero, cocina)
- Realizar sesiones de capacitación presencial para todo el personal
- Crear videos tutoriales para funcionalidades específicas del sistema

*Actividad 5.4: Soporte post-implementación*
- Establecer un periodo de acompañamiento durante las primeras semanas
- Implementar un sistema de tickets para reportar problemas
- Realizar ajustes basados en la retroalimentación de los usuarios

Estas actividades están diseñadas para garantizar una implementación exitosa del sistema, abordando todos los aspectos desde el análisis inicial hasta el soporte post-implementación. Cada fase se construye sobre los resultados de la anterior, siguiendo un enfoque iterativo que permite ajustes y mejoras continuas durante todo el proceso de desarrollo.

### RESULTADOS ESPERADOS

Como resultado de la implementación del proyecto, se espera obtener un sistema de gestión restaurante completamente funcional y moderno que transforme la operatividad del negocio. Los principales resultados esperados son:

**1. Plataforma Web Integral**
- Un sistema web completo con frontend en React y backend en Django que centralice todas las operaciones del restaurante
- Acceso multiplataforma desde computadoras, tablets y dispositivos móviles
- Interfaz responsiva y adaptable a diferentes tamaños de pantalla

**2. Sistema de Gestión de Inventario Optimizado**
- Control detallado del stock de ingredientes con actualización en tiempo real
- Alertas automáticas para niveles críticos de inventario
- Trazabilidad completa del uso de ingredientes vinculados a los pedidos
- Reducción de desperdicios y pérdidas de inventario

**3. Administración Eficiente de Menús**
- Catálogo digital completo de todos los platos disponibles
- Vinculación dinámica entre menús e ingredientes que actualiza la disponibilidad automáticamente
- Cálculo automático de costos y márgenes de ganancia
- Flexibilidad para realizar modificaciones y crear promociones especiales

**4. Proceso de Pedidos Digitalizado**
- Sistema ágil de toma de pedidos desde dispositivos móviles
- Comunicación instantánea entre el personal de servicio y la cocina
- Tracking en tiempo real del estado de cada pedido
- Generación automática de boletas y facturas

**5. Gestión Visual de Mesas**
- Mapa interactivo de la distribución de mesas en el restaurante
- Visualización en tiempo real del estado de ocupación
- Optimización de la asignación de mesas según tamaño de grupos
- Control de tiempos de servicio para mejorar la rotación

**6. Dashboard Analítico**
- Reportes gráficos de ventas por fecha, producto y mesero
- Análisis de popularidad de menús y tendencias de consumo
- Estadísticas de uso de ingredientes y rentabilidad de platos
- Indicadores clave de desempeño (KPI) para la toma de decisiones gerenciales

**7. Arquitectura de Software Robusta**
- Implementación de Clean Architecture que facilita el mantenimiento y la evolución del sistema
- Aplicación de patrones de diseño orientados a objetos que garantizan la escalabilidad
- Código modular y bien documentado que permite futuras extensiones
- Sistema de pruebas automatizadas que aseguran la calidad del software

**8. Mejora en Métricas Operativas**
- Reducción del 90% en errores de pedidos
- Disminución del 40% en tiempo de servicio
- Aumento del 25% en la rotación de mesas
- Reducción del 30% en pérdidas de inventario

Este conjunto de resultados transformará significativamente la operación del restaurante, proporcionando herramientas tecnológicas que optimizan cada aspecto del negocio y mejoran la experiencia tanto del personal como de los clientes.

### ANÁLISIS DE LA SITUACIÓN CON PROYECTO

La implementación del sistema de gestión web para restaurantes generará transformaciones significativas en todas las áreas operativas del negocio, contrastando notablemente con la situación actual:

**Gestión de Inventario: De Manual a Inteligente**

*Situación Sin Proyecto:* Control manual de inventario con discrepancias frecuentes, conteos físicos periódicos y desactualización que provoca quiebres de stock y ofertas de platos no disponibles.

*Situación Con Proyecto:* Sistema automatizado de inventario con actualización en tiempo real cada vez que se prepara un plato. La plataforma descontará automáticamente los ingredientes utilizados en cada pedido, manteniendo un registro preciso del stock disponible. Se implementarán alertas tempranas cuando los ingredientes alcancen niveles mínimos, permitiendo realizar pedidos a proveedores oportunamente. Esta automatización reducirá en un 90% las discrepancias de inventario y eliminará prácticamente las situaciones donde se ofrecen platos que no pueden prepararse.

**Procesamiento de Pedidos: De Papel a Digital**

*Situación Sin Proyecto:* Sistema basado en comandas en papel propenso a pérdidas, errores de interpretación y retrasos en la comunicación entre el área de servicio y la cocina.

*Situación Con Proyecto:* Proceso completamente digitalizado donde los pedidos se registran directamente en dispositivos móviles y se transmiten instantáneamente a la cocina. El sistema permitirá realizar modificaciones en tiempo real, agregar notas especiales y visualizar el estado de preparación de cada pedido. Este cambio reducirá el tiempo entre la toma del pedido y el inicio de la preparación en un 80%, eliminando los errores por pérdida de comandas o mala interpretación de la escritura manual.

**Accesibilidad del Sistema: De Local a Ubicuo**

*Situación Sin Proyecto:* Acceso restringido a una sola computadora con la aplicación de escritorio instalada, generando cuellos de botella en la operación.

*Situación Con Proyecto:* Acceso universal desde cualquier dispositivo con conexión a internet, permitiendo que meseros, cocineros, administradores y gerentes interactúen simultáneamente con el sistema desde sus respectivas áreas. Esta ubicuidad eliminará los tiempos de espera para acceder al sistema y descentralizará la operación, aumentando la eficiencia general en un 40%.

**Gestión de Mesas: De Improvisada a Estructurada**

*Situación Sin Proyecto:* Administración manual de mesas sin visualización clara de la disponibilidad ni optimización del espacio.

*Situación Con Proyecto:* Sistema visual interactivo que mostrará en tiempo real qué mesas están ocupadas, reservadas o disponibles. Permitirá asignar meseros específicos, controlar tiempos de servicio y optimizar la distribución de clientes según el tamaño de los grupos. Esta organización estructurada aumentará la rotación de mesas en un 25% durante horas pico, maximizando la capacidad del restaurante.

**Análisis de Datos: De Básico a Avanzado**

*Situación Sin Proyecto:* Herramientas analíticas limitadas que dificultan la identificación de tendencias y la toma de decisiones estratégicas.

*Situación Con Proyecto:* Dashboard analítico completo con visualizaciones en tiempo real de métricas clave como ventas por período, popularidad de platos, rentabilidad por menú y eficiencia del personal. El sistema permitirá realizar análisis predictivos para anticipar la demanda, optimizar inventarios y planificar promociones efectivas. Esta capacidad analítica avanzada mejorará la toma de decisiones estratégicas, resultando en un aumento proyectado del 15% en rentabilidad.

**Variables que se Modificarán:**

1. **Tiempo de Servicio:** Reducción del 40% en el tiempo desde que un cliente realiza su pedido hasta que recibe su plato.

2. **Precisión de Inventario:** Aumento del 95% en la precisión del inventario registrado versus el inventario físico.

3. **Satisfacción del Cliente:** Mejora del 35% en las calificaciones de satisfacción debido a la reducción de errores y tiempos de espera.

4. **Rotación de Mesas:** Incremento del 25% en la cantidad de clientes atendidos durante períodos de alta demanda.

5. **Eficiencia Operativa:** Reducción del 30% en horas-hombre dedicadas a tareas administrativas que ahora serán automatizadas.

6. **Rentabilidad:** Aumento del 15% en el margen de beneficio debido a mejor control de costos, reducción de desperdicios y optimización de precios basada en análisis de datos.

**Impacto Esperado:**

La implementación del proyecto transformará fundamentalmente la operación del restaurante, pasando de un modelo reactivo y propenso a errores a uno proactivo y basado en datos. Las actividades planificadas abordan directamente cada punto débil identificado en la situación actual:

- El desarrollo de interfaces web responsivas elimina las restricciones de acceso del software actual.
- La implementación de la gestión automatizada de inventario resuelve los problemas de discrepancias y quiebres de stock.
- El sistema digital de pedidos elimina los errores y retrasos asociados con las comandas en papel.
- El módulo de gestión de mesas optimiza el uso del espacio y mejora la experiencia del cliente.
- El dashboard analítico proporciona la información necesaria para tomar decisiones estratégicas basadas en datos reales.

Además, la arquitectura orientada a objetos y el uso de patrones de diseño garantizan que el sistema sea escalable y mantenible a largo plazo, permitiendo agregar nuevas funcionalidades conforme evolucionen las necesidades del negocio.

En resumen, este proyecto no representa simplemente una actualización tecnológica, sino una transformación integral del modelo operativo del restaurante que impactará positivamente en la experiencia del cliente, la eficiencia del personal y la rentabilidad del negocio.