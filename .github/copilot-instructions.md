# Instrucciones universales para GitHub Copilot en este proyecto

- El proyecto es un sistema web para la gestión de clientes, pedidos, inventario, menús, mesas y reportes en un restaurante.
- Backend: Django (Python), Frontend: React, Base de datos: PostgreSQL.
- Arquitectura: Clean Architecture (Presentación, Casos de Uso, Dominio, Infraestructura), separación estricta de responsabilidades.
- Principios SOLID y patrones de diseño: Repository, Factory, Observer, State, Facade, Dependency Injection.
- Autenticación de usuarios (meseros, cocineros, administradores, gerentes) exclusivamente mediante Google OAuth2 usando google-api-python-client.
- Los usuarios tienen roles diferenciados; la interfaz debe mostrar vistas/componentes específicos según el rol autenticado.
- Seguridad: JWT, cifrado de datos sensibles, protección contra ataques comunes.
- Escalabilidad, mantenibilidad y usabilidad en dispositivos modernos y antiguos.
- Código documentado, siguiendo convenciones de nomenclatura y estructura definidas en la documentación del proyecto.
- Endpoints RESTful; el frontend debe consumir la API de Django.
- Idioma principal para documentación, comentarios y UI: español.
- Multiplataforma: accesible desde navegadores modernos y dispositivos móviles (no requiere app nativa).
- Priorizar mantenibilidad, testabilidad y facilidad de futuras expansiones (integración con delivery, pagos, etc).
- Cada nueva funcionalidad o implementación debe incluir pruebas automatizadas escritas bajo el enfoque BDD (Behavior Driven Development), utilizando un framework BDD para Python/Django (por ejemplo, Behave o pytest-bdd).
- No se permite el uso de TDD puro ni tests unitarios tradicionales fuera del enfoque BDD.
