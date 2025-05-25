# Tutorial: Configuración y Activación de PostgreSQL para el Sistema de Restaurante

Este tutorial te guiará paso a paso para instalar, activar y configurar PostgreSQL en **Arch Linux** y **Windows**, de modo que puedas utilizar la base de datos requerida por el sistema.

---

## 1. Requisitos Previos

- Acceso de administrador en tu sistema operativo.
- Python y Django instalados.
- Acceso a la terminal (Linux) o PowerShell/Command Prompt (Windows).

---

## 2. Instalación de PostgreSQL

### Arch Linux

1. **Instalar PostgreSQL:**
   ```bash
   sudo pacman -Syu postgresql
   ```

2. **Inicializar la base de datos:**
   ```bash
   sudo -iu postgres
   initdb --locale=es_CL.UTF-8 -D /var/lib/postgres/data
   exit
   ```

3. **Habilitar y arrancar el servicio:**
   ```bash
   sudo systemctl enable postgresql
   sudo systemctl start postgresql
   ```

### Windows

1. **Descargar el instalador:**
   - Ve a [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/) y descarga el instalador.

2. **Ejecutar el instalador:**
   - Sigue los pasos del asistente, elige una contraseña para el usuario `postgres` y recuerda el puerto (por defecto: 5432).

3. **Finalizar la instalación:**
   - PostgreSQL se instalará como un servicio de Windows y se iniciará automáticamente.

---

## 3. Crear la Base de Datos y Usuario

### Arch Linux

1. **Entrar al usuario postgres:**
   ```bash
   sudo -iu postgres
   ```

2. **Abrir el intérprete de comandos de PostgreSQL:**
   ```bash
   psql
   ```

3. **Crear la base de datos y el usuario:**
   ```sql
   CREATE DATABASE restaurant_db;
   CREATE USER restaurant_user WITH PASSWORD 'tu_contraseña_segura';
   GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;
   ```

4. **Salir de psql y del usuario postgres:**
   ```sql
   \q
   exit
   ```

### Windows

1. **Abrir "SQL Shell (psql)"** desde el menú de inicio.

2. **Conectarse como usuario `postgres` (usa la contraseña que elegiste):**

3. **Ejecutar los comandos:**
   ```sql
   CREATE DATABASE restaurant_db;
   CREATE USER restaurant_user WITH PASSWORD 'tu_contraseña_segura';
   GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;
   ```

---

## 4. Configuración de Django

1. **Editar el archivo de configuración:**  
   Abre `/home/s1lky/Desktop/s1lky/repos/Dise-o_Software/Sistema_Restaurante/Backend/Config/Settings/settings.py` y asegúrate de que la sección `DATABASES` tenga los siguientes valores:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': 'restaurant_db',
           'USER': 'restaurant_user',
           'PASSWORD': 'tu_contraseña_segura',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **(Opcional) Usar variables de entorno:**  
   Puedes definir la contraseña en un archivo `.env` y cargarla automáticamente.

---

## 5. Aplicar Migraciones y Probar la Conexión

1. **Instalar dependencias si es necesario:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Aplicar migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Crear un superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Levantar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

---

## 6. Solución de Problemas

- Si tienes problemas de conexión, revisa que el servicio de PostgreSQL esté activo:
  - **Arch Linux:** `sudo systemctl status postgresql`
  - **Windows:** Verifica el servicio en el "Administrador de servicios".
- Verifica que el usuario y la contraseña sean correctos.
- Si usas Docker, asegúrate de exponer el puerto 5432.

---

## 7. Recursos Adicionales

- [Documentación oficial de PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación de Django sobre PostgreSQL](https://docs.djangoproject.com/es/4.2/ref/databases/#postgresql-notes)

---

¡Listo! Ahora tu sistema está preparado para trabajar con PostgreSQL en Arch Linux o Windows.
