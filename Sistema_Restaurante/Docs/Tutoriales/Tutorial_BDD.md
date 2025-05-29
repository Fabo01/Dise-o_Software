# Tutorial: Ejecución de pruebas BDD en el Sistema de Gestión de Restaurante

Este tutorial explica cómo ejecutar los tests BDD del proyecto utilizando `pytest-bdd`.

## 1. Requisitos previos
- Tener **Python 3.8+** instalado.
- Clonar el repositorio y ubicarse en la carpeta del proyecto.
- Crear y activar un entorno virtual (recomendado):

### En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### En Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

- Instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## 2. Estructura de pruebas
Las pruebas BDD se encuentran en:
- `Backend/tests/features/` → Archivos `.feature` (escenarios escritos en Gherkin)
- `Backend/tests/` → Archivos `test_*.py` (step definitions en Python)

## 3. Ejecución de los tests
Ubícate en la carpeta `Sistema_Restaurante` 

```bash
cd "C:\Users\fabo\Documents\Git Universidad\Dise-o_Software\Sistema_Restaurante"
```
y ejecuta:

```bash
pytest
```

O bien, para ver más detalle:

```powershell
pytest -v
```

Esto ejecutará todos los escenarios BDD definidos en los archivos de la carpeta `Backend/tests/`.

## 4. Ejemplo de salida
```
============================= test session starts =============================
collected 12 items

Backend/tests/test_ingredientes.py ....
Backend/tests/test_usuarios.py ....
Backend/tests/test_clientes.py ....
...
========================== 12 passed in 2.34s ================================
```

## 5. Consejos y buenas prácticas
- Escribe los escenarios en español y claros para todos los roles.
- Cada nueva funcionalidad debe tener su escenario y steps BDD.
- Si un test falla, revisa el step definition y la lógica de negocio.
- Asegúrate de que la base de datos de pruebas esté limpia antes de ejecutar los tests.
- Si usas Docker o un entorno especial, asegúrate de que los servicios estén levantados.

---

**¡Listo! Ahora puedes validar el comportamiento del sistema de forma colaborativa y automatizada.**
