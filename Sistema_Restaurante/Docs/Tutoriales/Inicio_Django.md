# Inicio de un Proyecto Django

## Pasos para Iniciar el Servidor Django

Para iniciar correctamente el servidor Django y comenzar a trabajar con la API, sigue estos pasos en orden:

### 1. Generar Migraciones

```bash
python Sistema_Restaurante/manage.py makemigrations Infraestructura
```

**¿Qué hace?** Detecta los cambios realizados en los modelos de Django y genera archivos de migración que describen cómo transformar la base de datos. No modifica la base de datos todavía.

### 2. Aplicar Migraciones a la Base de Datos

```bash
python Sistema_Restaurante/manage.py migrate Infraestructura
```

Y el comando

```bash
python Sistema_Restaurante/manage.py migrate
```

**¿Qué hace?** Lee los archivos de migración generados y aplica los cambios a la base de datos (creación de tablas, modificación de columnas, etc.). Registra las migraciones aplicadas para no ejecutarlas nuevamente.

### 3. Iniciar el Servidor de Desarrollo

```bash
python Sistema_Restaurante/manage.py runserver
```

**¿Qué hace?** Inicia el servidor de desarrollo de Django en localhost:8000, carga la configuración desde settings.py, configura las URLs y proporciona recarga automática cuando detecta cambios en el código.

### . Acceder a la API y Panel de Administración

Una vez que el servidor esté en ejecución, puedes acceder a:
- API REST: http://localhost:8000/api/
- Panel de administración: http://localhost:8000/admin/ (requiere crear un superusuario)


Este comando te pedirá un nombre de usuario, correo y contraseña para crear una cuenta de administrador que te permitirá acceder al panel de administración.